// Advanced Audio Sync Application
class AudioSyncApp {
    constructor() {
        this.videoFile = null;
        this.audioFile = null;
        this.originalAudioFile = null;
        this.audioOffset = 0;
        this.isPlaying = false;
        this.crossfadeValue = 50; // 0-100 scale
        this.playbackRate = 1.0;
        this.clipVideo = false; // Whether to clip video instead of adding silence
        
        // Web Audio API
        this.audioContext = null;
        this.originalAudioBuffer = null;
        this.cleanAudioBuffer = null;
        this.originalSource = null;
        this.cleanSource = null;
        this.originalGain = null;
        this.cleanGain = null;
        this.masterGain = null;
        
        // Animation
        this.animationFrame = null;
        this.startTime = 0;
        
        this.init();
    }
    
    async init() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.setupAudioNodes();
            this.setupEventListeners();
            console.log('Audio Sync App initialized');
        } catch (error) {
            console.error('Failed to initialize audio context:', error);
        }
    }
    
    setupAudioNodes() {
        // Create gain nodes for crossfading
        this.originalGain = this.audioContext.createGain();
        this.cleanGain = this.audioContext.createGain();
        this.masterGain = this.audioContext.createGain();
        
        // Connect the audio graph
        this.originalGain.connect(this.masterGain);
        this.cleanGain.connect(this.masterGain);
        this.masterGain.connect(this.audioContext.destination);
        
        this.updateCrossfader();
    }
    
    setupEventListeners() {
        // File uploads
        document.getElementById('video-upload')?.addEventListener('change', (e) => this.handleVideoUpload(e.target));
        document.getElementById('audio-upload')?.addEventListener('change', (e) => this.handleAudioUpload(e.target));
        
        // Crossfader
        document.getElementById('crossfader')?.addEventListener('input', (e) => {
            this.crossfadeValue = parseFloat(e.target.value);
            this.updateCrossfader();
        });
        
        // Audio offset
        document.getElementById('audio-offset')?.addEventListener('input', (e) => {
            this.audioOffset = parseFloat(e.target.value);
            this.updateOffsetIndicator();
        });
        
        // Clip video checkbox
        document.getElementById('clip-video-checkbox')?.addEventListener('change', (e) => {
            this.clipVideo = e.target.checked;
            console.log(`🎬 Clip video mode: ${this.clipVideo ? 'enabled' : 'disabled'}`);
        });
        
        // Video player events
        const video = document.getElementById('video-player');
        if (video) {
            video.addEventListener('play', () => this.syncAudioPlay());
            video.addEventListener('pause', () => this.syncAudioPause());
            video.addEventListener('seeked', () => this.syncAudioSeek());
            video.addEventListener('timeupdate', () => this.updatePlayhead());
        }
    }
    
    async handleVideoUpload(input) {
        const file = input.files[0];
        if (!file) return;
        
        console.log('🎬 Video upload started:', file.name, file.type, `${(file.size / 1024 / 1024).toFixed(1)} MB`);
        
        this.videoFile = file;
        const videoPlayer = document.getElementById('video-player');
        const url = URL.createObjectURL(file);
        videoPlayer.src = url;
        
        console.log('🎬 Video player src set, starting audio extraction...');
        
        // Extract audio from video for waveform
        try {
            await this.extractVideoAudio(file);
            console.log('✅ Video audio extraction completed');
        } catch (error) {
            console.error('❌ Video audio extraction failed:', error);
        }
        
        document.getElementById('video-status').textContent = `${file.name.substring(0, 15)}...`;
        this.checkBothFilesLoaded();
    }
    
    async handleAudioUpload(input) {
        const file = input.files[0];
        if (!file) return;
        
        console.log('🎵 Audio upload started:', file.name, file.type, `${(file.size / 1024 / 1024).toFixed(1)} MB`);
        
        this.audioFile = file;
        await this.loadAudioFile(file, 'clean');
        
        document.getElementById('audio-status').textContent = `${file.name.substring(0, 15)}...`;
        this.checkBothFilesLoaded();
    }
    
    async extractVideoAudio(videoFile) {
        console.log('🔊 Starting video audio extraction for:', videoFile.name);
        
        try {
            // Alternative approach: decode the video file directly as audio
            const arrayBuffer = await videoFile.arrayBuffer();
            console.log('🔊 Video file read as ArrayBuffer:', arrayBuffer.byteLength, 'bytes');
            
            try {
                // Try to decode video file directly as audio (works for many video formats)
                const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer.slice());
                console.log('🔊 Successfully decoded video as audio:', {
                    duration: audioBuffer.duration,
                    sampleRate: audioBuffer.sampleRate,
                    channels: audioBuffer.numberOfChannels,
                    length: audioBuffer.length
                });
                
                // Limit to first 20 seconds and draw
                const displayDuration = Math.min(20, audioBuffer.duration);
                const displayFrameCount = displayDuration * audioBuffer.sampleRate;
                
                const displayBuffer = this.audioContext.createBuffer(
                    audioBuffer.numberOfChannels,
                    displayFrameCount,
                    audioBuffer.sampleRate
                );
                
                // Copy first 20 seconds to display buffer
                for (let channel = 0; channel < audioBuffer.numberOfChannels; channel++) {
                    const originalData = audioBuffer.getChannelData(channel);
                    const displayData = displayBuffer.getChannelData(channel);
                    for (let i = 0; i < displayFrameCount; i++) {
                        displayData[i] = originalData[i];
                    }
                }
                
                this.originalAudioBuffer = audioBuffer;
                this.drawWaveform(displayBuffer, 'original-waveform', '#ef4444');
                return audioBuffer;
                
            } catch (decodeError) {
                console.log('🔊 Direct decode failed, trying video element approach:', decodeError.message);
                
                // Fallback to video element approach
                return this.extractVideoAudioViaElement(videoFile);
            }
            
        } catch (error) {
            console.error('❌ Error reading video file:', error);
            this.drawWaveform(null, 'original-waveform', '#ef4444');
        }
    }
    
    async extractVideoAudioViaElement(videoFile) {
        console.log('🔊 Using video element approach for:', videoFile.name);
        
        // Create a temporary video element to extract audio
        const videoElement = document.createElement('video');
        videoElement.src = URL.createObjectURL(videoFile);
        videoElement.muted = false;
        videoElement.volume = 1.0; // Full volume for better signal capture
        
        return new Promise((resolve, reject) => {
            videoElement.addEventListener('loadedmetadata', async () => {
                console.log('🔊 Video metadata loaded:', {
                    duration: videoElement.duration,
                    hasAudioTracks: !!videoElement.audioTracks,
                    audioTracksLength: videoElement.audioTracks?.length || 0,
                    videoWidth: videoElement.videoWidth,
                    videoHeight: videoElement.videoHeight
                });
                
                try {
                    // Ensure audio context is running
                    if (this.audioContext.state === 'suspended') {
                        await this.audioContext.resume();
                    }
                    
                    // Create a fresh media element source (can only be used once)
                    const source = this.audioContext.createMediaElementSource(videoElement);
                    
                    // Create an analyser and script processor for more direct audio capture
                    const analyser = this.audioContext.createAnalyser();
                    analyser.fftSize = 8192; // Larger FFT for better resolution
                    analyser.smoothingTimeConstant = 0;
                    
                    // Create a script processor (deprecated but more reliable for capture)
                    const scriptProcessor = this.audioContext.createScriptProcessor(4096, 1, 1);
                    
                    // Connect the audio graph
                    source.connect(analyser);
                    source.connect(scriptProcessor);
                    scriptProcessor.connect(this.audioContext.destination);
                    
                    console.log('🔊 Audio graph connected with script processor');
                    
                    // Set up capture
                    const duration = Math.min(20, videoElement.duration);
                    const sampleRate = this.audioContext.sampleRate;
                    const audioBuffer = this.audioContext.createBuffer(1, duration * sampleRate, sampleRate);
                    const channelData = audioBuffer.getChannelData(0);
                    let sampleIndex = 0;
                    
                    // Capture audio using script processor
                    scriptProcessor.onaudioprocess = function(audioProcessingEvent) {
                        const inputBuffer = audioProcessingEvent.inputBuffer;
                        const inputData = inputBuffer.getChannelData(0);
                        
                        for (let i = 0; i < inputData.length && sampleIndex < channelData.length; i++) {
                            channelData[sampleIndex++] = inputData[i];
                        }
                        
                        // Check progress
                        if (sampleIndex % 44100 === 0) {
                            const secondsRecorded = sampleIndex / sampleRate;
                            console.log(`🔊 Recorded ${secondsRecorded.toFixed(1)}s of audio`);
                        }
                        
                        // Stop when we have enough data
                        if (videoElement.currentTime >= duration || sampleIndex >= channelData.length) {
                            console.log('🔊 Audio capture completed via script processor');
                            
                            scriptProcessor.disconnect();
                            source.disconnect();
                            videoElement.pause();
                            
                            // Analyze captured data
                            let maxAmplitude = 0;
                            let samplesWithData = 0;
                            for (let i = 0; i < Math.min(10000, channelData.length); i++) {
                                const amplitude = Math.abs(channelData[i]);
                                maxAmplitude = Math.max(maxAmplitude, amplitude);
                                if (amplitude > 0.001) samplesWithData++;
                            }
                            
                            console.log('🔊 Captured audio analysis:', {
                                maxAmplitude: maxAmplitude,
                                samplesWithData: samplesWithData,
                                percentageWithData: (samplesWithData / Math.min(10000, channelData.length) * 100).toFixed(1) + '%'
                            });
                            
                            this.originalAudioBuffer = audioBuffer;
                            this.drawWaveform(audioBuffer, 'original-waveform', '#ef4444');
                            resolve(audioBuffer);
                        }
                    }.bind(this);
                    
                    // Start playback
                    videoElement.currentTime = 0;
                    await videoElement.play();
                    console.log('🔊 Video playback started for audio capture');
                    
                } catch (error) {
                    console.error('❌ Error in video element audio extraction:', error);
                    this.drawWaveform(null, 'original-waveform', '#ef4444');
                    reject(error);
                }
            });
            
            videoElement.addEventListener('error', (error) => {
                console.error('❌ Video element error:', error);
                this.drawWaveform(null, 'original-waveform', '#ef4444');
                reject(error);
            });
        });
    }
    
    async loadAudioFile(file, type) {
        console.log(`🎵 Loading ${type} audio file:`, file.name);
        
        try {
            const arrayBuffer = await file.arrayBuffer();
            console.log(`🎵 File read into ArrayBuffer: ${arrayBuffer.byteLength} bytes`);
            
            const fullAudioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
            console.log(`🎵 Audio decoded:`, {
                duration: fullAudioBuffer.duration,
                sampleRate: fullAudioBuffer.sampleRate,
                channels: fullAudioBuffer.numberOfChannels,
                length: fullAudioBuffer.length
            });
            
            // Check for audio data
            const channelData = fullAudioBuffer.getChannelData(0);
            let maxAmplitude = 0;
            let samplesWithData = 0;
            for (let i = 0; i < Math.min(10000, channelData.length); i++) {
                const amplitude = Math.abs(channelData[i]);
                maxAmplitude = Math.max(maxAmplitude, amplitude);
                if (amplitude > 0.001) samplesWithData++;
            }
            
            console.log(`🎵 Audio analysis:`, {
                maxAmplitude: maxAmplitude,
                samplesWithData: samplesWithData,
                percentageWithData: (samplesWithData / Math.min(10000, channelData.length) * 100).toFixed(1) + '%'
            });
            
            // Limit to first 20 seconds for waveform display
            const displayDuration = Math.min(20, fullAudioBuffer.duration);
            const displayFrameCount = displayDuration * fullAudioBuffer.sampleRate;
            
            // Create a buffer for display (first 20 seconds)
            const displayBuffer = this.audioContext.createBuffer(
                fullAudioBuffer.numberOfChannels,
                displayFrameCount,
                fullAudioBuffer.sampleRate
            );
            
            // Copy first 20 seconds to display buffer
            for (let channel = 0; channel < fullAudioBuffer.numberOfChannels; channel++) {
                const originalData = fullAudioBuffer.getChannelData(channel);
                const displayData = displayBuffer.getChannelData(channel);
                for (let i = 0; i < displayFrameCount; i++) {
                    displayData[i] = originalData[i];
                }
            }
            
            console.log(`🎵 Created display buffer for ${displayDuration}s`);
            
            if (type === 'clean') {
                this.cleanAudioBuffer = fullAudioBuffer; // Keep full buffer for playback
                console.log('🎵 Drawing clean waveform...');
                this.drawWaveform(displayBuffer, 'clean-waveform', '#3b82f6');
            } else {
                this.originalAudioBuffer = fullAudioBuffer; // Keep full buffer for playback
                console.log('🎵 Drawing original waveform...');
                this.drawWaveform(displayBuffer, 'original-waveform', '#ef4444');
            }
            
            console.log(`✅ ${type} audio loaded: ${fullAudioBuffer.duration.toFixed(2)}s (displaying first ${displayDuration.toFixed(1)}s)`);
        } catch (error) {
            console.error(`❌ Error loading ${type} audio:`, error);
            // Draw placeholder on error
            this.drawWaveform(null, type === 'clean' ? 'clean-waveform' : 'original-waveform', type === 'clean' ? '#3b82f6' : '#ef4444');
        }
    }
    
    drawWaveform(audioBuffer, canvasId, color) {
        console.log(`🎨 Drawing waveform for ${canvasId} with color ${color}`);
        
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            console.error(`❌ Canvas not found: ${canvasId}`);
            return;
        }
        
        console.log(`🎨 Canvas found: ${canvas.width}x${canvas.height}`);
        
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        
        ctx.clearRect(0, 0, width, height);
        
        if (!audioBuffer) {
            console.log(`🎨 No audio buffer, drawing placeholder for ${canvasId}`);
            // Draw placeholder with loading message
            ctx.strokeStyle = color + '40';
            ctx.lineWidth = 1;
            ctx.setLineDash([5, 5]);
            ctx.beginPath();
            ctx.moveTo(0, height / 2);
            ctx.lineTo(width, height / 2);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // Add loading text
            ctx.fillStyle = color + '80';
            ctx.font = '12px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('Loading audio...', width / 2, height / 2 - 10);
            return;
        }
        
        console.log(`🎨 Audio buffer provided:`, {
            duration: audioBuffer.duration,
            sampleRate: audioBuffer.sampleRate,
            channels: audioBuffer.numberOfChannels,
            length: audioBuffer.length
        });
        
        const channelData = audioBuffer.getChannelData(0);
        const samples = width * 2; // Higher resolution for smoother curves
        const blockSize = Math.floor(channelData.length / samples);
        
        if (blockSize <= 0) return;
        
        // First pass: find peak amplitude for normalization
        let peakAmplitude = 0;
        for (let i = 0; i < channelData.length; i++) {
            peakAmplitude = Math.max(peakAmplitude, Math.abs(channelData[i]));
        }
        
        // Avoid division by zero and ensure visible waveform
        const normalizeGain = peakAmplitude > 0.001 ? 0.9 / peakAmplitude : 1.0;
        
        // Draw background grid
        ctx.strokeStyle = color + '20';
        ctx.lineWidth = 0.5;
        ctx.setLineDash([2, 2]);
        for (let i = 1; i < 4; i++) {
            const y = (i * height) / 4;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
        ctx.setLineDash([]);
        
        // Calculate waveform points
        const waveformPoints = [];
        
        for (let i = 0; i < samples; i++) {
            let min = 1.0;
            let max = -1.0;
            let rms = 0;
            
            const blockStart = i * blockSize;
            const blockEnd = Math.min(blockStart + blockSize, channelData.length);
            
            for (let j = blockStart; j < blockEnd; j++) {
                const sample = channelData[j] * normalizeGain;
                if (sample < min) min = sample;
                if (sample > max) max = sample;
                rms += sample * sample;
            }
            
            rms = Math.sqrt(rms / blockSize) * normalizeGain;
            
            const x = (i / samples) * width;
            const centerY = height / 2;
            const minY = centerY - (min * centerY * 0.8);
            const maxY = centerY - (max * centerY * 0.8);
            const rmsY = centerY - (rms * centerY * 0.8);
            
            waveformPoints.push({ x, minY, maxY, rmsY });
        }
        
        // Draw filled waveform
        ctx.fillStyle = color + '40';
        ctx.beginPath();
        
        // Top envelope
        waveformPoints.forEach((point, i) => {
            if (i === 0) {
                ctx.moveTo(point.x, point.maxY);
            } else {
                ctx.lineTo(point.x, point.maxY);
            }
        });
        
        // Bottom envelope (reversed)
        for (let i = waveformPoints.length - 1; i >= 0; i--) {
            const point = waveformPoints[i];
            ctx.lineTo(point.x, point.minY);
        }
        
        ctx.closePath();
        ctx.fill();
        
        // Draw RMS envelope for better visibility
        ctx.strokeStyle = color + '80';
        ctx.lineWidth = 1;
        ctx.beginPath();
        
        waveformPoints.forEach((point, i) => {
            const y1 = height / 2 - point.rmsY + height / 2;
            const y2 = height / 2 + point.rmsY - height / 2;
            
            if (i === 0) {
                ctx.moveTo(point.x, y1);
            } else {
                ctx.lineTo(point.x, y1);
            }
        });
        
        for (let i = waveformPoints.length - 1; i >= 0; i--) {
            const point = waveformPoints[i];
            const y2 = height / 2 + point.rmsY - height / 2;
            ctx.lineTo(point.x, y2);
        }
        
        ctx.stroke();
        
        // Add time markers
        ctx.fillStyle = color + '60';
        ctx.font = '10px sans-serif';
        ctx.textAlign = 'center';
        
        const duration = Math.min(20, audioBuffer.duration);
        for (let i = 0; i <= duration; i += 5) {
            const x = (i / duration) * width;
            ctx.fillText(`${i}s`, x, height - 2);
            
            // Draw time tick
            ctx.strokeStyle = color + '40';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(x, height - 10);
            ctx.lineTo(x, height);
            ctx.stroke();
        }
    }
    
    drawWaveformWithOffset(audioBuffer, canvasId, color, offset) {
        // Draw waveform with offset indication
        this.drawWaveform(audioBuffer, canvasId, color);
        
        // Add offset visualization
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        
        // Draw offset indicator showing where audio actually starts
        if (Math.abs(offset) > 0.01) {
            // For positive offset: audio starts LATER (line at +offset position)
            // For negative offset: audio starts EARLIER (line at negative position, may be off-screen)
            const startTimePixels = (offset / 20) * width; // Where audio actually starts in the 20s view
            
            if (startTimePixels >= 0 && startTimePixels <= width) {
                // Draw vertical line showing where audio starts
                ctx.strokeStyle = color + 'AA';
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                ctx.moveTo(startTimePixels, 0);
                ctx.lineTo(startTimePixels, height);
                ctx.stroke();
                ctx.setLineDash([]);
                
                // Add "AUDIO START" label
                ctx.fillStyle = color + 'DD';
                ctx.font = 'bold 10px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('AUDIO START', startTimePixels, 12);
            }
            
            // Always show offset value in corner
            ctx.fillStyle = color + 'DD';
            ctx.font = 'bold 12px sans-serif';
            ctx.textAlign = 'left';
            ctx.fillRect(5, 5, 80, 20);
            ctx.fillStyle = 'white';
            ctx.fillText(`${offset > 0 ? '+' : ''}${offset.toFixed(2)}s`, 8, 19);
            
            // Add delay/advance indicator
            ctx.fillStyle = color + 'BB';
            ctx.font = '10px sans-serif';
            const delayText = offset > 0 ? 'DELAYED' : 'ADVANCED';
            ctx.fillText(delayText, 8, height - 5);
        }
        
        // Add subtle border to indicate this waveform is offset
        if (Math.abs(offset) > 0.01) {
            ctx.strokeStyle = color + '60';
            ctx.lineWidth = 2;
            ctx.strokeRect(1, 1, width - 2, height - 2);
        }
    }
    
    updateCrossfader() {
        if (!this.originalGain || !this.cleanGain) return;
        
        // Convert 0-100 to audio gains (equal power crossfade)
        const cleanLevel = this.crossfadeValue / 100;
        const originalLevel = 1 - cleanLevel;
        
        this.originalGain.gain.value = Math.sqrt(originalLevel);
        this.cleanGain.gain.value = Math.sqrt(cleanLevel);
        
        // Update crossfader visual
        const crossfader = document.getElementById('crossfader');
        if (crossfader) {
            const gradient = `linear-gradient(to right, #ef4444 0%, #ef4444 ${100-this.crossfadeValue}%, #3b82f6 ${100-this.crossfadeValue}%, #3b82f6 100%)`;
            crossfader.style.background = gradient;
        }
    }
    
    updateOffsetIndicator() {
        const indicator = document.getElementById('offset-indicator');
        if (!indicator) return;
        
        // Map offset to visual position (-5s to +5s range)
        const maxOffset = 5;
        const normalizedOffset = Math.max(-1, Math.min(1, this.audioOffset / maxOffset));
        const leftPercent = 50 + (normalizedOffset * 50);
        
        indicator.style.left = `${leftPercent}%`;
        
        // Update sync status
        const status = document.getElementById('sync-status');
        if (status) {
            status.textContent = `${this.audioOffset > 0 ? '+' : ''}${this.audioOffset.toFixed(2)}s`;
        }
        
        // Re-draw waveforms with offset visualization
        this.redrawWaveformsWithOffset();
    }
    
    redrawWaveformsWithOffset() {
        // Re-draw the clean audio waveform with visual offset
        if (this.cleanAudioBuffer) {
            const displayDuration = Math.min(20, this.cleanAudioBuffer.duration);
            const displayFrameCount = displayDuration * this.cleanAudioBuffer.sampleRate;
            
            const displayBuffer = this.audioContext.createBuffer(
                this.cleanAudioBuffer.numberOfChannels,
                displayFrameCount,
                this.cleanAudioBuffer.sampleRate
            );
            
            // Apply offset when copying data - FIXED LOGIC
            const offsetSamples = Math.floor(this.audioOffset * this.cleanAudioBuffer.sampleRate);
            
            console.log(`🎨 Redrawing waveform with offset: ${this.audioOffset.toFixed(2)}s (${offsetSamples} samples)`);
            
            for (let channel = 0; channel < this.cleanAudioBuffer.numberOfChannels; channel++) {
                const originalData = this.cleanAudioBuffer.getChannelData(channel);
                const displayData = displayBuffer.getChannelData(channel);
                
                let silenceSamples = 0;
                let audioSamples = 0;
                
                for (let i = 0; i < displayFrameCount; i++) {
                    // Positive offset = delay audio (add silence at start)
                    // Negative offset = advance audio (start earlier)
                    const sourceIndex = i - offsetSamples;
                    
                    if (sourceIndex >= 0 && sourceIndex < originalData.length) {
                        displayData[i] = originalData[sourceIndex];
                        audioSamples++;
                    } else {
                        displayData[i] = 0; // Silence for out-of-bounds
                        silenceSamples++;
                    }
                }
                
                if (channel === 0) { // Only log once
                    const silenceSeconds = silenceSamples / this.cleanAudioBuffer.sampleRate;
                    const audioSeconds = audioSamples / this.cleanAudioBuffer.sampleRate;
                    console.log(`🎨 Display composition: ${silenceSeconds.toFixed(2)}s silence + ${audioSeconds.toFixed(2)}s audio`);
                }
            }
            
            this.drawWaveformWithOffset(displayBuffer, 'clean-waveform', '#3b82f6', this.audioOffset);
        }
        
        // Re-draw original waveform (no offset, as it's the reference)
        if (this.originalAudioBuffer) {
            const displayDuration = Math.min(20, this.originalAudioBuffer.duration);
            const displayFrameCount = displayDuration * this.originalAudioBuffer.sampleRate;
            
            const displayBuffer = this.audioContext.createBuffer(
                this.originalAudioBuffer.numberOfChannels,
                displayFrameCount,
                this.originalAudioBuffer.sampleRate
            );
            
            for (let channel = 0; channel < this.originalAudioBuffer.numberOfChannels; channel++) {
                const originalData = this.originalAudioBuffer.getChannelData(channel);
                const displayData = displayBuffer.getChannelData(channel);
                for (let i = 0; i < displayFrameCount; i++) {
                    displayData[i] = originalData[i];
                }
            }
            
            this.drawWaveform(displayBuffer, 'original-waveform', '#ef4444');
        }
    }
    
    updatePlayhead() {
        const video = document.getElementById('video-player');
        const playhead = document.getElementById('playhead');
        
        if (!video || !playhead || !video.duration) return;
        
        // Show playhead position relative to 20-second waveform window
        const waveformDuration = 20; // 20 seconds shown in waveform
        const currentTime = video.currentTime;
        
        if (currentTime <= waveformDuration) {
            // Show playhead within the waveform view
            const progress = currentTime / waveformDuration;
            const leftPercent = progress * 100;
            playhead.style.left = `${leftPercent}%`;
            playhead.style.opacity = '0.8';
        } else {
            // Hide playhead when beyond waveform view
            playhead.style.opacity = '0.3';
            playhead.style.left = '100%';
        }
    }
    
    checkBothFilesLoaded() {
        if (this.videoFile && this.audioFile) {
            // Hide upload header and show main layout
            document.getElementById('upload-header').style.display = 'none';
            document.getElementById('main-layout').style.display = 'flex';
        }
    }
    
    // Sync functions
    syncAudioPlay() {
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }
        
        const video = document.getElementById('video-player');
        if (!video) return;
        
        this.startAudioPlayback(video.currentTime);
        this.isPlaying = true;
        
        const btn = document.getElementById('play-pause-btn');
        if (btn) btn.textContent = '⏸ Pause';
    }
    
    syncAudioPause() {
        this.stopAudioPlayback();
        this.isPlaying = false;
        
        const btn = document.getElementById('play-pause-btn');
        if (btn) btn.textContent = '▶ Play';
    }
    
    syncAudioSeek() {
        if (this.isPlaying) {
            const video = document.getElementById('video-player');
            if (video) {
                this.stopAudioPlayback();
                this.startAudioPlayback(video.currentTime);
            }
        }
    }
    
    startAudioPlayback(videoTime) {
        this.stopAudioPlayback();
        
        if (this.cleanAudioBuffer) {
            this.cleanSource = this.audioContext.createBufferSource();
            this.cleanSource.buffer = this.cleanAudioBuffer;
            this.cleanSource.connect(this.cleanGain);
            this.cleanSource.playbackRate.value = this.playbackRate;
            
            // Calculate where in the audio track we should be
            // audioPosition = videoTime - audioOffset
            // Positive offset = delay audio (audio plays later)
            // Negative offset = advance audio (audio plays earlier)
            const audioPosition = videoTime - this.audioOffset;
            
            console.log(`🔊 Starting audio: videoTime=${videoTime.toFixed(2)}s, offset=${this.audioOffset.toFixed(2)}s, audioPosition=${audioPosition.toFixed(2)}s`);
            
            if (audioPosition < 0) {
                // Audio should start in the future (delay)
                const delayTime = -audioPosition;
                console.log(`🔊 Delaying audio start by ${delayTime.toFixed(2)}s`);
                this.cleanSource.start(this.audioContext.currentTime + delayTime, 0);
            } else if (audioPosition >= this.cleanAudioBuffer.duration) {
                // Audio should start beyond the end of the track (silence)
                console.log(`🔊 Audio position ${audioPosition.toFixed(2)}s is beyond track duration ${this.cleanAudioBuffer.duration.toFixed(2)}s`);
                // Don't start audio at all
            } else {
                // Audio should start immediately from audioPosition
                console.log(`🔊 Starting audio immediately from position ${audioPosition.toFixed(2)}s`);
                this.cleanSource.start(0, audioPosition);
            }
        }
    }
    
    stopAudioPlayback() {
        if (this.cleanSource) {
            this.cleanSource.stop();
            this.cleanSource = null;
        }
        if (this.originalSource) {
            this.originalSource.stop();
            this.originalSource = null;
        }
    }
    
    async exportSynchronizedVideo() {
        const exportStatus = document.getElementById('export-status');
        
        // Check for WebCodecs and mp4box support
        if (!window.VideoEncoder || !window.AudioEncoder) {
            throw new Error('WebCodecs API not supported in this browser. Please use Chrome 102+ or Edge 102+.');
        }
        
        if (!window.MP4Box) {
            throw new Error('MP4Box.js not loaded. Please check your internet connection.');
        }
        
        exportStatus.textContent = 'Reading video file...';
        
        // Create video element to extract frames and audio
        const video = document.createElement('video');
        video.src = URL.createObjectURL(this.videoFile);
        video.muted = true;
        
        await new Promise((resolve, reject) => {
            video.onloadedmetadata = resolve;
            video.onerror = reject;
        });
        
        const { videoWidth: originalWidth, videoHeight: originalHeight, duration } = video;
        const fps = 30; // Target frame rate
        
        // Calculate appropriate resolution and AVC level
        const { width: videoWidth, height: videoHeight, avcLevel } = this.calculateVideoSettings(originalWidth, originalHeight);
        
        console.log(`🎬 Video metadata: ${originalWidth}x${originalHeight} -> ${videoWidth}x${videoHeight}, ${duration.toFixed(2)}s, AVC level ${avcLevel}`);
        
        exportStatus.textContent = 'Preparing synchronized audio...';
        
        // Create synchronized audio buffer
        const { outputBuffer: syncedAudioBuffer, finalDuration } = await this.createSynchronizedAudio(duration);
        
        // Determine final video duration
        const finalVideoDuration = this.clipVideo ? finalDuration : duration;
        
        console.log(`🎬 Final video duration: ${finalVideoDuration.toFixed(2)}s (${this.clipVideo ? 'clipped' : 'original'})`);
        
        exportStatus.textContent = 'Initializing video encoder...';
        
        // Set up video encoder
        const videoEncoder = new VideoEncoder({
            output: (chunk, metadata) => {
                videoChunks.push(chunk);
            },
            error: (error) => {
                console.error('Video encoding error:', error);
                throw error;
            }
        });
        
        const videoChunks = [];
        
        videoEncoder.configure({
            codec: `avc1.42E0${avcLevel.toString(16).toUpperCase().padStart(2, '0')}`, // H.264 baseline with appropriate level
            width: videoWidth,
            height: videoHeight,
            bitrate: this.calculateBitrate(videoWidth, videoHeight, fps),
            framerate: fps
        });
        
        exportStatus.textContent = 'Initializing audio encoder...';
        
        // Set up audio encoder
        const audioEncoder = new AudioEncoder({
            output: (chunk, metadata) => {
                audioChunks.push(chunk);
            },
            error: (error) => {
                console.error('Audio encoding error:', error);
                throw error;
            }
        });
        
        const audioChunks = [];
        
        audioEncoder.configure({
            codec: 'mp4a.40.2', // AAC
            sampleRate: syncedAudioBuffer.sampleRate,
            numberOfChannels: syncedAudioBuffer.numberOfChannels,
            bitrate: 128000 // 128 kbps
        });
        
        exportStatus.textContent = 'Processing video frames...';
        
        // Process video frames (with clipping if enabled)
        await this.processVideoFrames(video, videoEncoder, fps, finalVideoDuration, originalWidth, originalHeight, videoWidth, videoHeight);
        
        exportStatus.textContent = 'Processing audio...';
        
        // Process audio
        await this.processAudio(syncedAudioBuffer, audioEncoder);
        
        exportStatus.textContent = 'Finalizing encoders...';
        
        // Finalize encoders
        await videoEncoder.flush();
        await audioEncoder.flush();
        
        videoEncoder.close();
        audioEncoder.close();
        
        exportStatus.textContent = 'Creating MP4 container...';
        
        // Create proper MP4 file using mp4box.js
        const finalBlob = await this.createMP4File(videoChunks, audioChunks, {
            width: videoWidth,
            height: videoHeight,
            fps: fps,
            duration: finalVideoDuration,
            sampleRate: syncedAudioBuffer.sampleRate,
            channels: syncedAudioBuffer.numberOfChannels
        });
        
        exportStatus.textContent = 'Download ready!';
        
        // Download the result
        const url = URL.createObjectURL(finalBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `synced-${this.videoFile.name.replace(/\.[^/.]+$/, '')}.mp4`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        exportStatus.textContent = 'Export complete!';
        
        setTimeout(() => {
            exportStatus.textContent = 'Ready when synced perfectly';
        }, 3000);
    }
    
    async createSynchronizedAudio(videoDuration) {
        console.log(`🎵 Creating synchronized audio track (clip mode: ${this.clipVideo})...`);
        
        const sampleRate = this.cleanAudioBuffer.sampleRate;
        const channels = this.cleanAudioBuffer.numberOfChannels;
        const offsetSamples = Math.floor(this.audioOffset * sampleRate);
        
        let finalDuration, totalSamples;
        
        if (this.clipVideo) {
            // Clip mode: calculate duration based on clean audio + offset
            const cleanDuration = this.cleanAudioBuffer.duration;
            finalDuration = cleanDuration + Math.max(0, this.audioOffset); // Only add positive offset
            totalSamples = Math.floor(finalDuration * sampleRate);
            console.log(`🎵 Clip mode: Clean audio ${cleanDuration.toFixed(2)}s + offset ${this.audioOffset.toFixed(2)}s = ${finalDuration.toFixed(2)}s`);
        } else {
            // Silence mode: use full video duration
            finalDuration = videoDuration;
            totalSamples = Math.floor(videoDuration * sampleRate);
            console.log(`🎵 Silence mode: Full video duration ${videoDuration.toFixed(2)}s, offset ${this.audioOffset.toFixed(2)}s`);
        }
        
        // Create output buffer
        const outputBuffer = this.audioContext.createBuffer(channels, totalSamples, sampleRate);
        
        for (let channel = 0; channel < channels; channel++) {
            const outputData = outputBuffer.getChannelData(channel);
            const cleanData = this.cleanAudioBuffer.getChannelData(channel);
            
            // Mix original and clean audio based on crossfader
            const cleanLevel = this.crossfadeValue / 100;
            const originalLevel = 1 - cleanLevel;
            
            for (let i = 0; i < totalSamples; i++) {
                let sample = 0;
                
                // Add clean audio with offset
                const cleanIndex = i - offsetSamples;
                if (cleanIndex >= 0 && cleanIndex < cleanData.length) {
                    sample += cleanData[cleanIndex] * cleanLevel;
                }
                
                // Add original audio (if we have it extracted)
                if (this.originalAudioBuffer && !this.clipVideo) {
                    // Only mix original audio in silence mode (not clip mode)
                    const originalData = this.originalAudioBuffer.getChannelData(channel);
                    if (i < originalData.length) {
                        sample += originalData[i] * originalLevel;
                    }
                }
                
                outputData[i] = Math.max(-1, Math.min(1, sample)); // Clamp to prevent clipping
            }
        }
        
        return { outputBuffer, finalDuration };
    }
    
    calculateVideoSettings(width, height) {
        const area = width * height;
        
        // AVC level limits (coded area)
        const levels = [
            { level: 0x1E, maxArea: 414720 },   // Level 3.0
            { level: 0x1F, maxArea: 414720 },   // Level 3.1
            { level: 0x20, maxArea: 921600 },   // Level 3.2
            { level: 0x28, maxArea: 1310720 },  // Level 4.0
            { level: 0x29, maxArea: 2097152 },  // Level 4.1
            { level: 0x2A, maxArea: 2097152 },  // Level 4.2
            { level: 0x32, maxArea: 8847360 },  // Level 5.0
            { level: 0x33, maxArea: 8847360 },  // Level 5.1
            { level: 0x34, maxArea: 35389440 }  // Level 5.2
        ];
        
        // Find appropriate level
        let avcLevel = 0x34; // Default to highest
        for (const levelInfo of levels) {
            if (area <= levelInfo.maxArea) {
                avcLevel = levelInfo.level;
                break;
            }
        }
        
        // If still too large, downscale
        const maxArea = levels.find(l => l.level === avcLevel).maxArea;
        if (area > maxArea) {
            const scale = Math.sqrt(maxArea / area);
            width = Math.floor(width * scale / 2) * 2; // Ensure even numbers
            height = Math.floor(height * scale / 2) * 2;
            console.log(`🎬 Downscaling video by ${(scale * 100).toFixed(1)}% to fit AVC level`);
        }
        
        return { width, height, avcLevel };
    }
    
    calculateBitrate(width, height, fps) {
        // Calculate bitrate based on resolution and fps
        const pixels = width * height;
        const baseRate = 0.1; // bits per pixel per frame
        const bitrate = Math.max(500000, Math.min(8000000, pixels * fps * baseRate));
        console.log(`🎬 Calculated bitrate: ${(bitrate / 1000000).toFixed(1)} Mbps`);
        return bitrate;
    }
    
    async processVideoFrames(video, encoder, fps, duration, originalWidth, originalHeight, targetWidth, targetHeight) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas to target resolution
        canvas.width = targetWidth;
        canvas.height = targetHeight;
        
        const frameInterval = 1 / fps;
        const totalFrames = Math.floor(duration * fps);
        
        console.log(`🎬 Processing ${totalFrames} frames at ${fps} fps (${originalWidth}x${originalHeight} -> ${targetWidth}x${targetHeight})...`);
        
        // Calculate scaling to fit target resolution while maintaining aspect ratio
        const scaleX = targetWidth / originalWidth;
        const scaleY = targetHeight / originalHeight;
        const scale = Math.min(scaleX, scaleY);
        
        const scaledWidth = originalWidth * scale;
        const scaledHeight = originalHeight * scale;
        const offsetX = (targetWidth - scaledWidth) / 2;
        const offsetY = (targetHeight - scaledHeight) / 2;
        
        console.log(`🎬 Scaling: ${scale.toFixed(3)}x, offset: ${offsetX.toFixed(1)}, ${offsetY.toFixed(1)}`);
        
        for (let frameNum = 0; frameNum < totalFrames; frameNum++) {
            const timestamp = frameNum * frameInterval;
            
            // Update progress
            if (frameNum % 30 === 0) {
                const progress = (frameNum / totalFrames * 100).toFixed(1);
                document.getElementById('export-status').textContent = `Processing frames: ${progress}%`;
            }
            
            try {
                // Seek to timestamp
                video.currentTime = timestamp;
                await new Promise((resolve, reject) => {
                    const timeout = setTimeout(() => reject(new Error('Seek timeout')), 1000);
                    video.onseeked = () => {
                        clearTimeout(timeout);
                        resolve();
                    };
                });
                
                // Clear canvas with black background
                ctx.fillStyle = '#000000';
                ctx.fillRect(0, 0, targetWidth, targetHeight);
                
                // Draw scaled and centered video frame
                ctx.drawImage(video, offsetX, offsetY, scaledWidth, scaledHeight);
                
                // Create VideoFrame from canvas
                const frame = new VideoFrame(canvas, {
                    timestamp: timestamp * 1000000, // microseconds
                    duration: frameInterval * 1000000
                });
                
                // Encode frame
                encoder.encode(frame);
                
                // Important: Close frame to prevent memory leaks
                frame.close();
                
            } catch (error) {
                console.error(`❌ Error processing frame ${frameNum}:`, error);
                // Continue with next frame
            }
        }
        
        console.log(`✅ Completed processing ${totalFrames} video frames`);
    }
    
    async processAudio(audioBuffer, encoder) {
        const sampleRate = audioBuffer.sampleRate;
        const channels = audioBuffer.numberOfChannels;
        const frameSize = 1024; // AAC frame size
        const totalFrames = Math.floor(audioBuffer.length / frameSize);
        
        console.log(`🎵 Processing ${totalFrames} audio frames...`);
        
        for (let frameNum = 0; frameNum < totalFrames; frameNum++) {
            const start = frameNum * frameSize;
            const end = Math.min(start + frameSize, audioBuffer.length);
            const frameLength = end - start;
            
            // Update progress
            if (frameNum % 100 === 0) {
                const progress = (frameNum / totalFrames * 100).toFixed(1);
                document.getElementById('export-status').textContent = `Processing audio: ${progress}%`;
            }
            
            // Create AudioData
            const audioData = new AudioData({
                format: 'f32-planar',
                sampleRate: sampleRate,
                numberOfChannels: channels,
                numberOfFrames: frameLength,
                timestamp: (start / sampleRate) * 1000000, // microseconds
                data: this.getAudioFrameData(audioBuffer, start, frameLength)
            });
            
            encoder.encode(audioData);
            audioData.close();
        }
    }
    
    getAudioFrameData(audioBuffer, start, length) {
        const channels = audioBuffer.numberOfChannels;
        const bytesPerSample = 4; // f32
        const totalBytes = channels * length * bytesPerSample;
        const arrayBuffer = new ArrayBuffer(totalBytes);
        const view = new Float32Array(arrayBuffer);
        
        // Interleave channels
        for (let i = 0; i < length; i++) {
            for (let channel = 0; channel < channels; channel++) {
                const channelData = audioBuffer.getChannelData(channel);
                view[i * channels + channel] = channelData[start + i];
            }
        }
        
        return arrayBuffer;
    }
    
    async createMP4File(videoChunks, audioChunks, metadata) {
        console.log(`🎬 Creating MP4 with mp4box.js: ${videoChunks.length} video + ${audioChunks.length} audio chunks`);
        
        return new Promise((resolve, reject) => {
            try {
                // Create new MP4Box file
                const file = MP4Box.createFile();
                
                // Add video track
                const videoTrackId = file.addTrack({
                    type: 'video',
                    width: metadata.width,
                    height: metadata.height,
                    duration: metadata.duration * 1000, // milliseconds
                    timescale: 1000,
                    avcDecoderConfigRecord: this.createAVCDecoderConfigRecord()
                });
                
                console.log(`🎬 Added video track ${videoTrackId}: ${metadata.width}x${metadata.height}`);
                
                // Add audio track
                const audioTrackId = file.addTrack({
                    type: 'audio',
                    samplerate: metadata.sampleRate,
                    channel_count: metadata.channels,
                    duration: metadata.duration * 1000, // milliseconds
                    timescale: 1000,
                    audioDecoderConfigRecord: this.createAACDecoderConfigRecord(metadata.sampleRate, metadata.channels)
                });
                
                console.log(`🎬 Added audio track ${audioTrackId}: ${metadata.sampleRate}Hz, ${metadata.channels}ch`);
                
                // Add video samples
                const frameDuration = 1000 / metadata.fps; // milliseconds per frame
                videoChunks.forEach((chunk, index) => {
                    const sample = {
                        track_id: videoTrackId,
                        timescale: 1000,
                        duration: frameDuration,
                        dts: index * frameDuration,
                        cts: index * frameDuration,
                        is_sync: index % 30 === 0, // Keyframe every 30 frames
                        data: chunk
                    };
                    file.addSample(sample);
                });
                
                console.log(`🎬 Added ${videoChunks.length} video samples`);
                
                // Add audio samples
                const audioFrameDuration = (1024 / metadata.sampleRate) * 1000; // AAC frame duration in ms
                audioChunks.forEach((chunk, index) => {
                    const sample = {
                        track_id: audioTrackId,
                        timescale: 1000,
                        duration: audioFrameDuration,
                        dts: index * audioFrameDuration,
                        cts: index * audioFrameDuration,
                        is_sync: true, // Audio frames are always sync points
                        data: chunk
                    };
                    file.addSample(sample);
                });
                
                console.log(`🎬 Added ${audioChunks.length} audio samples`);
                
                // Collect output chunks
                const outputChunks = [];
                
                file.onReady = (info) => {
                    console.log('🎬 MP4 file ready:', info);
                    file.setExtractionOptions(videoTrackId, 'video', { nbSamples: 100 });
                    file.setExtractionOptions(audioTrackId, 'audio', { nbSamples: 100 });
                    file.start();
                };
                
                file.onError = (error) => {
                    console.error('❌ MP4Box error:', error);
                    reject(new Error(`MP4 creation failed: ${error}`));
                };
                
                file.onSegment = (id, user, buffer, sampleNum, is_last) => {
                    outputChunks.push(new Uint8Array(buffer));
                    
                    if (is_last) {
                        // Combine all chunks into final blob
                        const totalSize = outputChunks.reduce((sum, chunk) => sum + chunk.byteLength, 0);
                        const finalBuffer = new Uint8Array(totalSize);
                        let offset = 0;
                        
                        for (const chunk of outputChunks) {
                            finalBuffer.set(chunk, offset);
                            offset += chunk.byteLength;
                        }
                        
                        console.log(`✅ MP4 creation complete: ${totalSize} bytes`);
                        resolve(new Blob([finalBuffer], { type: 'video/mp4' }));
                    }
                };
                
                // Start the process
                file.flush();
                
            } catch (error) {
                console.error('❌ MP4 creation error:', error);
                reject(error);
            }
        });
    }
    
    createAVCDecoderConfigRecord() {
        // Basic H.264 decoder config for baseline profile
        // In practice, you'd extract this from the encoder or video file
        return new Uint8Array([
            0x01, // configurationVersion
            0x42, // AVCProfileIndication (baseline)
            0x00, // profile_compatibility
            0x1E, // AVCLevelIndication (level 3.0)
            0xFF, // lengthSizeMinusOne (4 bytes)
            0xE1, // numOfSequenceParameterSets
            // SPS would go here - simplified for now
            0x00, 0x08, 0x67, 0x42, 0x00, 0x1E, 0x88, 0x84, 0x20,
            0x01, // numOfPictureParameterSets
            // PPS would go here - simplified for now
            0x00, 0x04, 0x68, 0xCE, 0x06, 0xE2
        ]);
    }
    
    createAACDecoderConfigRecord(sampleRate, channels) {
        // AAC AudioSpecificConfig
        const sampleRateIndex = this.getAACFrequencyIndex(sampleRate);
        const channelConfig = channels;
        
        // AudioObjectType = 2 (AAC LC), FrequencyIndex, ChannelConfiguration
        const byte1 = (2 << 3) | (sampleRateIndex >> 1);
        const byte2 = ((sampleRateIndex & 1) << 7) | (channelConfig << 3);
        
        return new Uint8Array([byte1, byte2]);
    }
    
    getAACFrequencyIndex(sampleRate) {
        const frequencies = [
            96000, 88200, 64000, 48000, 44100, 32000,
            24000, 22050, 16000, 12000, 11025, 8000, 7350
        ];
        
        const index = frequencies.indexOf(sampleRate);
        return index !== -1 ? index : 4; // Default to 44100 Hz
    }
}

// Global instance and utility functions
let audioSyncApp;

document.addEventListener('DOMContentLoaded', function() {
    audioSyncApp = new AudioSyncApp();
});

// Global functions for UI controls
function adjustOffset(delta) {
    if (!audioSyncApp) return;
    audioSyncApp.audioOffset += delta;
    document.getElementById('audio-offset').value = audioSyncApp.audioOffset.toFixed(2);
    audioSyncApp.updateOffsetIndicator(); // This now triggers waveform redraw
}

function togglePlayback() {
    const video = document.getElementById('video-player');
    if (!video) return;
    
    if (video.paused) {
        video.play();
    } else {
        video.pause();
    }
}

function seekToPosition(time) {
    const video = document.getElementById('video-player');
    if (video) {
        video.currentTime = time;
    }
}

function setPlaybackRate(rate) {
    if (!audioSyncApp) return;
    
    audioSyncApp.playbackRate = rate;
    const video = document.getElementById('video-player');
    if (video) {
        video.playbackRate = rate;
    }
    
    // Restart audio if playing
    if (audioSyncApp.isPlaying) {
        audioSyncApp.syncAudioSeek();
    }
}

function jumpToMarker(marker) {
    if (marker === 'start') {
        seekToPosition(0);
    }
}

function autoDetectSync() {
    alert('Auto-detection would analyze both audio tracks to find the best sync point. This requires advanced audio processing.');
}

async function exportVideo() {
    if (!audioSyncApp || !audioSyncApp.videoFile || !audioSyncApp.cleanAudioBuffer) {
        alert('Please load both video and audio files first.');
        return;
    }
    
    const exportBtn = document.getElementById('export-btn');
    const exportStatus = document.getElementById('export-status');
    
    try {
        exportBtn.disabled = true;
        exportStatus.textContent = 'Initializing export...';
        
        await audioSyncApp.exportSynchronizedVideo();
        
    } catch (error) {
        console.error('Export failed:', error);
        exportStatus.textContent = `Export failed: ${error.message}`;
        alert(`Export failed: ${error.message}`);
    } finally {
        exportBtn.disabled = false;
    }
}

async function exportVideoServer() {
    if (!audioSyncApp || !audioSyncApp.videoFile || !audioSyncApp.audioFile) {
        alert('Please load both video and audio files first.');
        return;
    }
    
    const exportBtn = document.getElementById('export-server-btn');
    const exportStatus = document.getElementById('export-status');
    
    try {
        exportBtn.disabled = true;
        exportStatus.textContent = 'Uploading files to server...';
        
        // Create FormData with files and settings
        const formData = new FormData();
        formData.append('video_file', audioSyncApp.videoFile);
        formData.append('audio_file', audioSyncApp.audioFile);
        formData.append('offset', audioSyncApp.audioOffset.toString());
        formData.append('crossfade', audioSyncApp.crossfadeValue.toString());
        formData.append('clip_video', audioSyncApp.clipVideo.toString());
        
        // Start export job
        const response = await fetch('/export-video-server', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `Server error: ${response.status}`);
        }
        
        const { job_id } = await response.json();
        console.log(`🎬 Server export started with job ID: ${job_id}`);
        
        // Monitor progress with Server-Sent Events
        await monitorExportProgress(job_id, exportStatus);
        
    } catch (error) {
        console.error('Server export failed:', error);
        exportStatus.textContent = `Server export failed: ${error.message}`;
        alert(`Server export failed: ${error.message}`);
    } finally {
        exportBtn.disabled = false;
    }
}

async function monitorExportProgress(jobId, statusElement) {
    return new Promise((resolve, reject) => {
        const eventSource = new EventSource(`/export-progress/${jobId}`);
        
        eventSource.onmessage = function(event) {
            try {
                const data = JSON.parse(event.data);
                
                if (data.error) {
                    eventSource.close();
                    reject(new Error(data.error));
                    return;
                }
                
                // Update status display
                const progressBar = updateProgressDisplay(data, statusElement);
                
                console.log(`🎬 Export progress: ${data.progress}% - ${data.message}`);
                
                if (data.status === 'complete') {
                    eventSource.close();
                    
                    // Trigger download
                    statusElement.textContent = 'Downloading file...';
                    downloadExportedFile(jobId).then(() => {
                        statusElement.textContent = 'Server export complete!';
                        setTimeout(() => {
                            statusElement.textContent = 'Ready when synced perfectly';
                            // Remove progress bar if it exists
                            const progressContainer = document.getElementById('export-progress-container');
                            if (progressContainer) {
                                progressContainer.remove();
                            }
                        }, 3000);
                        resolve();
                    }).catch(reject);
                    
                } else if (data.status === 'error') {
                    eventSource.close();
                    reject(new Error(data.error || 'Export failed'));
                }
                
            } catch (err) {
                console.error('Error parsing progress data:', err);
            }
        };
        
        eventSource.onerror = function(event) {
            console.error('EventSource error:', event);
            eventSource.close();
            reject(new Error('Connection to server lost'));
        };
    });
}

function updateProgressDisplay(data, statusElement) {
    // Update text status
    statusElement.textContent = data.message;
    
    // Create or update progress bar
    let progressContainer = document.getElementById('export-progress-container');
    if (!progressContainer) {
        progressContainer = document.createElement('div');
        progressContainer.id = 'export-progress-container';
        progressContainer.className = 'mt-2';
        
        const progressBar = document.createElement('div');
        progressBar.className = 'w-full bg-neutral-700 rounded-full h-2';
        
        const progressFill = document.createElement('div');
        progressFill.id = 'export-progress-fill';
        progressFill.className = 'bg-blue-600 h-2 rounded-full transition-all duration-300';
        progressFill.style.width = '0%';
        
        const progressText = document.createElement('div');
        progressText.id = 'export-progress-text';
        progressText.className = 'text-xs text-neutral-400 text-center mt-1';
        progressText.textContent = '0%';
        
        progressBar.appendChild(progressFill);
        progressContainer.appendChild(progressBar);
        progressContainer.appendChild(progressText);
        
        // Insert after status element
        statusElement.parentNode.insertBefore(progressContainer, statusElement.nextSibling);
    }
    
    // Update progress bar
    const progressFill = document.getElementById('export-progress-fill');
    const progressText = document.getElementById('export-progress-text');
    
    if (progressFill && progressText) {
        progressFill.style.width = `${data.progress}%`;
        progressText.textContent = `${data.progress}%`;
        
        // Change color based on status
        progressFill.className = progressFill.className.replace(/bg-\w+-\d+/, 
            data.status === 'error' ? 'bg-red-600' : 
            data.status === 'complete' ? 'bg-green-600' : 'bg-blue-600'
        );
    }
    
    return progressContainer;
}

async function downloadExportedFile(jobId) {
    try {
        const response = await fetch(`/export-download/${jobId}`);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `Download failed: ${response.status}`);
        }
        
        // Get filename from response headers
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'synced_video.mp4';
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }
        
        // Download the file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        console.log(`✅ Downloaded: ${filename}`);
        
    } catch (error) {
        console.error('Download failed:', error);
        throw error;
    }
}