import json
import os
import re
import subprocess
import tempfile
import uuid

import anyio
from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    Form,
    Request,
    UploadFile,
)
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from tagflow import TagResponse, tag, text

from slopbox.ui import render_base_layout

# Create the router for video sync functionality
router = APIRouter(default_response_class=TagResponse)

# Global progress tracking
export_progress = {}


async def track_ffmpeg_progress(process, job_id, total_duration_seconds):
    """Track FFmpeg progress in real-time by parsing stderr output."""
    print(
        f"📊 Starting progress tracking for job {job_id}, duration: {total_duration_seconds}s"
    )

    stderr_buffer = b""

    async for chunk in process.stderr:
        stderr_buffer += chunk

        # Process complete lines from stderr
        while b"\n" in stderr_buffer:
            line, stderr_buffer = stderr_buffer.split(b"\n", 1)
            line_str = line.decode("utf-8", errors="ignore").strip()

            # Parse time progress from FFmpeg output
            # FFmpeg outputs lines like: "time=00:01:23.45 bitrate=1234.5kbits/s speed=1.2x"
            time_match = re.search(
                r"time=(\d{2}):(\d{2}):(\d{2})\.(\d+)", line_str
            )
            if time_match:
                hours = int(time_match.group(1))
                minutes = int(time_match.group(2))
                seconds = int(time_match.group(3))
                fraction_str = time_match.group(4)

                # Handle different decimal precision (centiseconds vs milliseconds)
                if len(fraction_str) == 2:
                    fraction = int(fraction_str) / 100  # centiseconds
                elif len(fraction_str) == 3:
                    fraction = int(fraction_str) / 1000  # milliseconds
                else:
                    fraction = int(fraction_str) / (10 ** len(fraction_str))

                current_seconds = (
                    hours * 3600 + minutes * 60 + seconds + fraction
                )

                if total_duration_seconds > 0:
                    # Calculate progress percentage (50% to 95% of total progress)
                    # Reserve 50-95% for FFmpeg processing, 95-100% for file handling
                    ffmpeg_progress = min(
                        95,
                        50 + (current_seconds / total_duration_seconds) * 45,
                    )

                    # Extract additional info if available
                    speed_match = re.search(r"speed=([0-9.]+)x", line_str)
                    bitrate_match = re.search(
                        r"bitrate=([0-9.]+)kbits/s", line_str
                    )

                    speed_text = (
                        f" at {speed_match.group(1)}x speed"
                        if speed_match
                        else ""
                    )
                    bitrate_text = (
                        f" ({bitrate_match.group(1)} kbps)"
                        if bitrate_match
                        else ""
                    )

                    progress_message = f"Processing video: {current_seconds:.1f}s / {total_duration_seconds:.1f}s{speed_text}{bitrate_text}"

                    print(
                        f"📈 Progress: {ffmpeg_progress:.1f}% - {progress_message}"
                    )

                    export_progress[job_id].update(
                        {
                            "progress": int(ffmpeg_progress),
                            "message": progress_message,
                            "current_time": current_seconds,
                            "total_time": total_duration_seconds,
                        }
                    )

                    # Small delay to prevent overwhelming the client
                    await anyio.sleep(0.1)

    print(f"✅ FFmpeg progress tracking completed for job {job_id}")


# Root route removed - conflicts with main slopbox app
# Use /video-sync route instead


@router.get("/video-sync")
async def video_sync(request: Request):
    """Serve the video-audio synchronization page."""
    if request.headers.get("HX-Request"):
        render_video_sync_content()
    else:
        with render_base_layout():
            render_video_sync_content()


@router.post("/export-video-server")
async def export_video_server(
    background_tasks: BackgroundTasks,
    video_file: UploadFile = File(...),
    audio_file: UploadFile = File(...),
    offset: float = Form(0.0),
    crossfade: float = Form(50.0),
    clip_video: bool = Form(False),
):
    """Start export and return job ID for progress tracking."""

    # Generate unique job ID
    job_id = str(uuid.uuid4())

    try:
        # Read file contents immediately before they get closed
        await video_file.seek(0)
        video_content = await video_file.read()

        await audio_file.seek(0)
        audio_content = await audio_file.read()

    except Exception as e:
        print(f"❌ Error reading uploaded files: {e}")
        return JSONResponse(
            {"error": f"Failed to read uploaded files: {str(e)}"},
            status_code=400,
        )

    # Initialize progress
    export_progress[job_id] = {
        "status": "initializing",
        "progress": 0,
        "message": "Starting export...",
        "error": None,
        "output_path": None,
        "filename": video_file.filename,
    }

    # Start background task with file contents
    background_tasks.add_task(
        process_video_export_with_content,
        job_id,
        video_content,
        audio_content,
        video_file.filename,
        audio_file.filename,
        offset,
        crossfade,
        clip_video,
    )

    return JSONResponse({"job_id": job_id})


@router.get("/export-progress/{job_id}")
async def get_export_progress(job_id: str):
    """Get export progress via Server-Sent Events."""

    async def event_stream():
        while True:
            if job_id not in export_progress:
                yield f"data: {json.dumps({'error': 'Job not found'})}\n\n"
                break

            progress_data = export_progress[job_id]
            yield f"data: {json.dumps(progress_data)}\n\n"

            # If complete or error, stop streaming
            if progress_data["status"] in ["complete", "error"]:
                break

            await anyio.sleep(1)  # Update every second

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.get("/export-download/{job_id}")
async def download_export(job_id: str):
    """Download completed export."""

    if job_id not in export_progress:
        return JSONResponse({"error": "Job not found"}, status_code=404)

    progress_data = export_progress[job_id]

    if progress_data["status"] != "complete":
        return JSONResponse({"error": "Export not complete"}, status_code=400)

    output_path = progress_data["output_path"]
    if not output_path or not os.path.exists(output_path):
        return JSONResponse(
            {"error": "Output file not found"}, status_code=404
        )

    filename = f"synced_{progress_data['filename']}"

    # Custom FileResponse that cleans up after download
    class CleanupFileResponse(FileResponse):
        def __init__(
            self, *args, cleanup_path=None, cleanup_dir=None, **kwargs
        ):
            super().__init__(*args, **kwargs)
            self.cleanup_path = cleanup_path
            self.cleanup_dir = cleanup_dir

        async def __call__(self, scope, receive, send):
            try:
                await super().__call__(scope, receive, send)
            finally:
                # Clean up after file is sent
                try:
                    if self.cleanup_path and os.path.exists(
                        self.cleanup_path
                    ):
                        os.remove(self.cleanup_path)
                    if self.cleanup_dir and os.path.exists(self.cleanup_dir):
                        import shutil

                        shutil.rmtree(self.cleanup_dir, ignore_errors=True)
                except Exception as e:
                    print(f"Warning: Could not clean up export files: {e}")

    # Clean up progress tracking
    del export_progress[job_id]

    # Get the directory to clean up
    output_dir = os.path.dirname(output_path)

    return CleanupFileResponse(
        output_path,
        media_type="video/mp4",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
        cleanup_path=output_path,
        cleanup_dir=output_dir,
    )


async def process_video_export_with_content(
    job_id: str,
    video_content: bytes,
    audio_content: bytes,
    video_filename: str,
    audio_filename: str,
    offset: float,
    crossfade: float,
    clip_video: bool,
):
    """Background task to process video export with progress tracking."""

    temp_dir = tempfile.mkdtemp()
    output_path = None

    try:
        # Update progress
        export_progress[job_id].update(
            {
                "status": "uploading",
                "progress": 10,
                "message": "Saving uploaded files...",
            }
        )

        # Save uploaded files
        video_path = os.path.join(
            temp_dir, f"input_video{os.path.splitext(video_filename)[1]}"
        )
        audio_path = os.path.join(
            temp_dir, f"input_audio{os.path.splitext(audio_filename)[1]}"
        )
        output_path = os.path.join(temp_dir, "output.mp4")
        progress_path = os.path.join(temp_dir, "progress.txt")

        # Write uploaded files to disk
        try:
            with open(video_path, "wb") as f:
                f.write(video_content)

            with open(audio_path, "wb") as f:
                f.write(audio_content)

        except Exception as e:
            print(f"❌ Error writing uploaded files: {e}")
            export_progress[job_id].update(
                {
                    "status": "error",
                    "error": f"Failed to save uploaded files: {str(e)}",
                    "message": "File upload error",
                }
            )
            return

        # Update progress
        export_progress[job_id].update(
            {
                "status": "analyzing",
                "progress": 20,
                "message": "Analyzing video metadata...",
            }
        )

        # Get video duration for progress calculation
        duration = await get_video_duration(video_path)

        # Build FFmpeg command
        cmd = await build_ffmpeg_command(
            video_path, audio_path, output_path, offset, crossfade, clip_video
        )

        # Update progress
        export_progress[job_id].update(
            {
                "status": "processing",
                "progress": 50,
                "message": "Processing with FFmpeg...",
            }
        )

        # Run FFmpeg process with real-time progress tracking
        print(f"🎬 Running FFmpeg: {' '.join(cmd)}")
        try:
            async with await anyio.open_process(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as process:
                with anyio.move_on_after(300.0) as cancel_scope:
                    # Track progress in real-time by parsing stderr
                    await track_ffmpeg_progress(process, job_id, duration)
                    await process.wait()
                if cancel_scope.cancelled_caught:
                    raise TimeoutError("FFmpeg processing timeout")

            if process.returncode != 0:
                print(
                    f"❌ FFmpeg failed with return code {process.returncode}"
                )
                export_progress[job_id].update(
                    {
                        "status": "error",
                        "error": "FFmpeg processing failed",
                        "message": "Processing failed",
                    }
                )
                return
        except TimeoutError:
            print("❌ FFmpeg timeout")
            export_progress[job_id].update(
                {
                    "status": "error",
                    "error": "Processing timeout (5 minutes)",
                    "message": "Export timed out",
                }
            )
            return

        if not os.path.exists(output_path):
            print(f"❌ Output file not created at {output_path}")
            export_progress[job_id].update(
                {
                    "status": "error",
                    "error": "Output file was not created",
                    "message": "Export failed",
                }
            )
            return

        # Move output to persistent location before cleanup
        persistent_dir = tempfile.mkdtemp(prefix="export_")
        persistent_output = os.path.join(
            persistent_dir, f"synced_{video_filename}"
        )

        import shutil

        shutil.move(output_path, persistent_output)

        # Success!
        export_progress[job_id].update(
            {
                "status": "complete",
                "progress": 100,
                "message": "Export complete! Ready for download.",
                "output_path": persistent_output,
            }
        )

    except Exception as e:
        print(f"❌ Export error: {e}")
        export_progress[job_id].update(
            {
                "status": "error",
                "error": f"Export failed: {str(e)}",
                "message": "Unexpected error",
            }
        )
    finally:
        # Clean up temporary processing directory (but not the output file)
        try:
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            print(f"Warning: Could not clean up temp directory: {e}")


async def get_video_duration(video_path: str) -> float:
    """Get video duration using ffprobe."""
    try:
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            video_path,
        ]
        async with await anyio.open_process(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) as process:
            with anyio.move_on_after(30.0) as cancel_scope:
                # Read all stdout data
                stdout_chunks = []
                async for chunk in process.stdout:
                    stdout_chunks.append(chunk)
                await process.wait()
            if cancel_scope.cancelled_caught:
                raise TimeoutError("ffprobe timeout")

            if process.returncode == 0:
                stdout_data = b"".join(stdout_chunks)
                data = json.loads(stdout_data.decode())
                return float(data["format"]["duration"])
    except Exception as e:
        print(f"Could not get video duration: {e}")

    return 0.0  # Fallback


async def has_video_audio_stream(video_path: str) -> bool:
    """Check if video file has an audio stream using ffprobe."""
    try:
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            "-select_streams",
            "a",
            video_path,
        ]
        async with await anyio.open_process(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) as process:
            with anyio.move_on_after(30.0) as cancel_scope:
                # Read all stdout data
                stdout_chunks = []
                async for chunk in process.stdout:
                    stdout_chunks.append(chunk)
                await process.wait()
            if cancel_scope.cancelled_caught:
                raise TimeoutError("ffprobe timeout")

            if process.returncode == 0:
                stdout_data = b"".join(stdout_chunks)
                data = json.loads(stdout_data.decode())
                # Check if there are any audio streams
                return len(data.get("streams", [])) > 0
    except Exception as e:
        print(f"Could not check video audio streams: {e}")

    return False  # Fallback - assume no audio


async def build_ffmpeg_command(
    video_path: str,
    audio_path: str,
    output_path: str,
    offset: float,
    crossfade: float,
    clip_video: bool,
) -> list[str]:
    """Build FFmpeg command for video synchronization."""

    cmd = ["ffmpeg", "-y"]  # -y to overwrite output

    # Input files
    cmd.extend(["-i", video_path])
    cmd.extend(["-i", audio_path])

    # Check if video has audio stream
    video_has_audio = await has_video_audio_stream(video_path)

    # If video has no audio and crossfade < 100, adjust crossfade to 100
    if not video_has_audio and crossfade < 100:
        crossfade = 100.0

    # Build filter graph
    filters = []

    if clip_video:
        # Clip mode: trim video to match audio timing
        if offset > 0:
            # Positive offset: delay audio, trim video start
            filters.append(f"[0:v]trim=start={offset}[video_trimmed]")
            filters.append(
                f"[1:a]adelay={int(offset * 1000)}|{int(offset * 1000)}[audio_delayed]"
            )
            video_input = "video_trimmed"
            audio_input = "audio_delayed"
        else:
            # Negative offset: advance audio, use original video
            filters.append(f"[1:a]atrim=start={abs(offset)}[audio_trimmed]")
            video_input = "0:v"
            audio_input = "audio_trimmed"
    else:
        # Silence mode: maintain full video duration
        if offset != 0:
            if offset > 0:
                # Positive offset: delay audio
                filters.append(
                    f"[1:a]adelay={int(offset * 1000)}|{int(offset * 1000)}[audio_delayed]"
                )
                audio_input = "audio_delayed"
            else:
                # Negative offset: pad with silence at start
                filters.append(
                    f"[1:a]apad=pad_dur={abs(offset)}[audio_padded]"
                )
                audio_input = "audio_padded"
        else:
            audio_input = "1:a"
        video_input = "0:v"

    # Handle crossfading if not 100% clean audio and video has audio
    if crossfade < 100 and video_has_audio:
        # Extract original video audio
        original_level = (100 - crossfade) / 100
        clean_level = crossfade / 100

        if clip_video and offset > 0:
            # Trim original audio to match
            filters.append(
                f"[0:a]atrim=start={offset},volume={original_level}[orig_audio]"
            )
        else:
            filters.append(f"[0:a]volume={original_level}[orig_audio]")

        filters.append(f"[{audio_input}]volume={clean_level}[clean_audio]")
        filters.append("[orig_audio][clean_audio]amix=inputs=2[final_audio]")
        final_audio = "final_audio"
    else:
        final_audio = audio_input

    # Apply filters if any
    if filters:
        filter_complex = ";".join(filters)
        cmd.extend(["-filter_complex", filter_complex])
        cmd.extend(["-map", f"[{video_input}]", "-map", f"[{final_audio}]"])
    else:
        cmd.extend(["-map", "0:v", "-map", "1:a"])

    # Fast encoding - copy video stream when possible
    if clip_video and offset > 0:
        # If we're trimming video, we need to re-encode
        cmd.extend(
            [
                "-c:v",
                "libx264",  # H.264 video codec
                "-preset",
                "ultrafast",  # Fastest encoding
                "-crf",
                "23",  # Reasonable quality
                "-pix_fmt",
                "yuv420p",  # Compatible pixel format
            ]
        )
    else:
        # Copy video stream without re-encoding (much faster)
        cmd.extend(["-c:v", "copy"])

    # Audio encoding settings
    cmd.extend(
        [
            "-c:a",
            "aac",  # AAC audio codec
            "-b:a",
            "128k",  # Audio bitrate
            "-ar",
            "48000",  # Sample rate
            "-ac",
            "2",  # Stereo audio
            "-movflags",
            "+faststart",  # Web-optimized
            "-f",
            "mp4",  # Force MP4 format
            "-progress",
            "pipe:2",  # Output progress to stderr
            "-stats_period",
            "0.5",  # Update progress every 0.5 seconds
            output_path,
        ]
    )

    return cmd


def render_video_sync_content():
    """Render the video sync page content."""
    with tag.div("w-full h-screen bg-neutral-900 text-white flex flex-col"):
        # Compact upload header (only visible when files not loaded)
        with tag.div(
            "bg-neutral-800 border-b border-neutral-700", id="upload-header"
        ):
            render_file_upload_section()

        # Main layout: optimized horizontal split
        with tag.div(
            "flex-1 flex bg-neutral-900",
            id="main-layout",
            style="display: none;",
        ):
            # Video section - larger
            with tag.div(
                "flex-1 flex items-center justify-center bg-black border-r border-neutral-600"
            ):
                render_video_player_section()

            # Inspector panel - wider for better waveforms
            with tag.div("w-96 bg-neutral-900 flex flex-col"):
                render_inspector_panel()


def render_file_upload_section():
    """Render the compact file upload area."""
    with tag.div("p-4"):
        with tag.form(
            "flex gap-4 items-center", enctype="multipart/form-data"
        ):
            # App title
            with tag.div("flex items-center gap-2"):
                with tag.div("text-xl font-bold text-white"):
                    text("🎬 Video Sync")

            # Video upload - compact
            with tag.div(
                "flex items-center gap-3 bg-neutral-700 rounded-lg p-3"
            ):
                with tag.input(
                    "hidden", type="file", id="video-upload", accept="video/*"
                ):
                    pass
                with tag.label(
                    "px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded cursor-pointer transition-colors",
                    **{"for": "video-upload"},
                ):
                    text("📹 Video")
                with tag.div(
                    "text-xs text-neutral-300 min-w-0", id="video-status"
                ):
                    text("No video")

            # Audio upload - compact
            with tag.div(
                "flex items-center gap-3 bg-neutral-700 rounded-lg p-3"
            ):
                with tag.input(
                    "hidden",
                    type="file",
                    id="audio-upload",
                    accept="audio/*,.mpeg,.mp3,.wav,.m4a",
                ):
                    pass
                with tag.label(
                    "px-3 py-1 bg-green-600 hover:bg-green-700 text-white text-sm rounded cursor-pointer transition-colors",
                    **{"for": "audio-upload"},
                ):
                    text("🎵 Audio")
                with tag.div(
                    "text-xs text-neutral-300 min-w-0", id="audio-status"
                ):
                    text("No audio")


def render_video_player_section():
    """Render the video player optimized for space."""
    with tag.div("p-6"):
        with tag.video(
            "max-w-full max-h-full object-contain shadow-lg",
            id="video-player",
            controls=True,
            preload="metadata",
            style="max-height: 85vh;",
        ):
            text("Your browser does not support the video tag.")

    # Hidden audio players
    with tag.audio("hidden", id="original-audio-player", preload="metadata"):
        text("Your browser does not support the audio tag.")
    with tag.audio("hidden", id="clean-audio-player", preload="metadata"):
        text("Your browser does not support the audio tag.")


def render_inspector_panel():
    """Render optimized inspector panel with better waveforms."""
    with tag.div("flex flex-col h-full"):
        # Header
        with tag.div("px-4 py-3 bg-neutral-800 border-b border-neutral-600"):
            with tag.div("text-sm font-semibold text-white"):
                text("🎬 Audio Sync")

        # Large waveforms section - takes most space
        with tag.div("p-4 border-b border-neutral-700 flex-1"):
            with tag.div("space-y-4"):
                # Video audio waveform
                with tag.div():
                    with tag.div("flex items-center justify-between mb-2"):
                        with tag.div("text-sm font-medium text-neutral-300"):
                            text("Video Audio")
                        with tag.div("text-xs text-red-400 font-mono"):
                            text("Original")
                    with tag.div("relative"):
                        with tag.canvas(
                            "w-full h-20 border border-neutral-600 rounded bg-neutral-800",
                            id="original-waveform",
                            width="320",
                            height="80",
                        ):
                            pass

                # Clean audio waveform
                with tag.div():
                    with tag.div("flex items-center justify-between mb-2"):
                        with tag.div("text-sm font-medium text-neutral-300"):
                            text("Clean Audio")
                        with tag.div("text-xs text-blue-400 font-mono"):
                            text("Replacement")
                    with tag.div("relative"):
                        with tag.canvas(
                            "w-full h-20 border border-neutral-600 rounded bg-neutral-800",
                            id="clean-waveform",
                            width="320",
                            height="80",
                        ):
                            pass

                        # Playhead indicator spans both waveforms
                        with tag.div(
                            "absolute w-0.5 bg-yellow-400 opacity-90 pointer-events-none z-10",
                            id="playhead",
                            style="top: -88px; height: 168px; left: 0px; transition: left 0.1s ease-out;",
                        ):
                            pass

                # Audio mix slider
                with tag.div("mt-4"):
                    with tag.div("flex justify-between items-center mb-2"):
                        with tag.span("text-xs text-red-400"):
                            text("Original")
                        with tag.span("text-xs text-neutral-400"):
                            text("Audio Mix")
                        with tag.span("text-xs text-blue-400"):
                            text("Clean")
                    with tag.input(
                        "w-full h-3 bg-neutral-700 rounded-lg appearance-none cursor-pointer",
                        type="range",
                        id="crossfader",
                        min="0",
                        max="100",
                        value="50",
                        style="background: linear-gradient(to right, #ef4444 0%, #ef4444 50%, #3b82f6 50%, #3b82f6 100%)",
                    ):
                        pass

                # Clip video option
                with tag.div("mt-3 flex items-center gap-2"):
                    with tag.input(
                        "w-4 h-4 text-blue-600 bg-neutral-700 border-neutral-600 rounded focus:ring-blue-500 focus:ring-2",
                        type="checkbox",
                        id="clip-video-checkbox",
                    ):
                        pass
                    with tag.label(
                        "text-xs text-neutral-300",
                        **{"for": "clip-video-checkbox"},
                    ):
                        text("Clip video instead of adding silence")
                    with tag.div(
                        "ml-auto text-xs text-neutral-500 cursor-help",
                        title="When checked: trims video length to match audio timing. When unchecked: adds silence to maintain full video duration.",
                    ):
                        text("?")

        # Compact controls section
        with tag.div("p-4 space-y-3 bg-neutral-850"):
            # Sync controls - horizontal layout
            with tag.div():
                with tag.div("flex items-center justify-between mb-2"):
                    with tag.label("text-sm font-medium text-white"):
                        text("Sync Offset")
                    with tag.div(
                        "text-sm text-blue-400 font-mono", id="sync-status"
                    ):
                        text("0.00s")

                # Visual offset indicator
                with tag.div("relative mb-2"):
                    # Background track
                    with tag.div(
                        "w-full h-2 bg-neutral-700 rounded-full relative"
                    ):
                        # Center mark
                        with tag.div(
                            "absolute top-0 left-1/2 transform -translate-x-1/2 w-0.5 h-2 bg-neutral-500"
                        ):
                            pass
                        # Offset indicator
                        with tag.div(
                            "absolute top-0 w-3 h-2 bg-blue-500 rounded-full transform -translate-x-1/2 transition-all duration-200",
                            id="offset-indicator",
                            style="left: 50%",
                        ):
                            pass
                    # Range labels
                    with tag.div(
                        "flex justify-between text-xs text-neutral-400 mt-1"
                    ):
                        with tag.span():
                            text("-5s")
                        with tag.span():
                            text("0s")
                        with tag.span():
                            text("+5s")

                # Offset input and fine tune in one row
                with tag.div("flex items-center gap-2 mb-2"):
                    with tag.input(
                        "w-20 px-2 py-1 bg-neutral-700 border border-neutral-600 rounded text-white text-sm",
                        type="number",
                        id="audio-offset",
                        step="0.01",
                        value="0",
                    ):
                        pass
                    with tag.span("text-xs text-neutral-400 mr-2"):
                        text("sec")

                    # Fine tune buttons
                    with tag.button(
                        "px-2 py-1 bg-neutral-700 hover:bg-neutral-600 text-white text-xs rounded transition-colors",
                        onclick="adjustOffset(-0.1)",
                    ):
                        text("-0.1")
                    with tag.button(
                        [
                            "px-2 py-1 bg-neutral-700 hover:bg-neutral-600",
                            "text-white text-xs rounded transition-colors",
                        ],
                        onclick="adjustOffset(-0.01)",
                    ):
                        text("-0.01")
                    with tag.button(
                        [
                            "px-2 py-1 bg-neutral-700 hover:bg-neutral-600",
                            "text-white text-xs rounded transition-colors",
                        ],
                        onclick="adjustOffset(0.01)",
                    ):
                        text("+0.01")
                    with tag.button(
                        [
                            "px-2 py-1 bg-neutral-700 hover:bg-neutral-600",
                            "text-white text-xs rounded transition-colors",
                        ],
                        onclick="adjustOffset(0.1)",
                    ):
                        text("+0.1")

            # Playback controls
            with tag.div():
                with tag.div("text-sm font-medium text-white mb-2"):
                    text("Playback")

                with tag.div("flex gap-2 mb-2"):
                    with tag.button(
                        [
                            "flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700",
                            "text-white text-sm rounded font-medium transition-colors",
                        ],
                        id="play-pause-btn",
                        onclick="togglePlayback()",
                    ):
                        text("▶ Play")

                    with tag.button(
                        [
                            "px-3 py-2 bg-neutral-700 hover:bg-neutral-600",
                            "text-white text-sm rounded transition-colors",
                        ],
                        onclick="resetPlayback()",
                    ):
                        text("⏹ Reset")

                    with tag.div("flex items-center gap-1"):
                        with tag.label(
                            "text-xs text-neutral-400",
                            **{"for": "auto-checkbox"},
                        ):
                            text("Auto")
                        with tag.input(
                            [
                                "w-4 h-4 text-blue-600 bg-neutral-700",
                                "border-neutral-600 rounded focus:ring-blue-500 focus:ring-2",
                            ],
                            type="checkbox",
                            id="auto-checkbox",
                            checked=True,
                        ):
                            pass

                # Speed controls
                with tag.div("flex gap-1"):
                    with tag.button(
                        [
                            "px-2 py-1 bg-neutral-700 hover:bg-neutral-600",
                            "text-white text-xs rounded transition-colors",
                        ],
                        onclick="setPlaybackRate(0.25)",
                    ):
                        text("0.25x")
                    with tag.button(
                        [
                            "px-2 py-1 bg-neutral-700 hover:bg-neutral-600",
                            "text-white text-xs rounded transition-colors",
                        ],
                        onclick="setPlaybackRate(0.5)",
                    ):
                        text("0.5x")
                    with tag.button(
                        "px-2 py-1 bg-blue-600 text-white text-xs rounded",
                        onclick="setPlaybackRate(1.0)",
                    ):
                        text("1.0x")

            # Export section
            with tag.div():
                with tag.div("text-sm font-medium text-white mb-2"):
                    text("Export")

                with tag.div(
                    "text-xs text-green-400 mb-2", id="export-status"
                ):
                    text("Ready when synced.")

                with tag.div("flex gap-2"):
                    with tag.button(
                        [
                            "flex-1 px-3 py-2 bg-green-600 hover:bg-green-700",
                            "text-white text-sm rounded font-medium transition-colors",
                        ],
                        id="export-browser-btn",
                        onclick="exportVideo()",
                    ):
                        text("🌐 Export (Browser)")

                    with tag.button(
                        [
                            "flex-1 px-3 py-2 bg-green-600 hover:bg-green-700",
                            "text-white text-sm rounded font-medium transition-colors",
                        ],
                        id="export-server-btn",
                        onclick="exportVideoServer()",
                    ):
                        text("🖥️ Export (Server)")

                # Progress bar (hidden by default)
                with tag.div("mt-2 hidden", id="export-progress-container"):
                    with tag.div("w-full bg-neutral-700 rounded-full h-2"):
                        with tag.div(
                            [
                                "bg-green-600 h-2 rounded-full",
                                "transition-all duration-300",
                            ],
                            id="export-progress-bar",
                            style="width: 0%",
                        ):
                            pass
                    with tag.div(
                        "text-xs text-neutral-400 mt-1",
                        id="export-progress-text",
                    ):
                        text("Starting export...")

        # JavaScript
        with tag.script(src="/static/video-sync.js"):
            pass
