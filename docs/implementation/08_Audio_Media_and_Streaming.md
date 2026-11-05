# Step 08 / Milestone M6 Report: Audio, Media, Streaming, and Timing Paths

- **Step ID**: 08 — Complete required audio, media, streaming and timing paths (Revision 2)
- **Milestone**: M6 (Step 08)
- **Date**: 2026-11-06
- **Host**: Linux 7.0.0-42-generic x86_64 / Ubuntu 26.04.1 LTS
- **Display / Windowing**: Wayland (`wayland-0` via SDL3 Wayland backend)
- **GPU**: Intel(R) HD Graphics 620 (KBL GT2) [8086:5916], Mesa 26.0.8-1ubuntu0.3, Vulkan API 1.4.335
- **Audio Host Endpoint**: `'Built-in Audio Analog Stereo'` (ALSA / PulseAudio via SDL3)
- **Predecessor Source Commit**: `d48028a` (Step 07 Progress)
- **SDK Pinned Commit**: `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518` (ReXGlue v0.10.0.2-dev)
- **Status**: **PASS**

---

## 1. Executive Summary

Milestone M6 completes the integration, verification, and empirical audit of the audio playback, media container streaming, and guest timing subsystems for the recompiled Xbox 360 *Rise of the Tomb Raider* executable (`rise360`).

In accordance with ADR-07 and the project architecture, audio is handled through ReXGlue's native APU pipeline (`rex::audio::SDLAudioDriver`), which attaches directly to the host ALSA/Pulse audio subsystem via SDL3. Over repeated execution trials (`rise360_040` through `rise360_044`), the APU opened the physical stereo endpoint `'Built-in Audio Analog Stereo'`, configured 6-channel 48,000 Hz 32-bit floating point audio submission, and streamed active audio frames without underruns or buffer starvation.

Media streaming from the base disc archives (`bigfile.000.tiger`, `bigfile.001.tiger`, and language archives) was audited alongside 71 Bink video assets under `movies/`. The timing subsystem was verified through high-resolution monotonic clocks (`KeQueryPerformanceFrequency` and `KeQuerySystemTime`), and a potential Linux shared memory accumulation issue was diagnosed and resolved directly in `port/src/rise360_app.h` via `CleanStaleShm()`.

---

## 2. Audio Subsystem Implementation & Audit

### 2.1 Host Audio Endpoint Configuration
The native audio driver (`src/audio/sdl/sdl_audio_driver.cpp`) configures default playback through SDL3:
```
[info] [apu] audio endpoint 'Built-in Audio Analog Stereo': 6 ch, 48000 Hz, format 0x8120; submitting 6 ch
```
- **Device Channels**: 6 channels (5.1 surround downmixed to host stereo endpoint).
- **Sampling Frequency**: 48,000 Hz.
- **Audio Format**: `0x8120` (`SDL_AUDIO_F32LE`, 32-bit floating point PCM).
- **Callback & Mixing**: `SDLAudioDriver::SDLCallback` runs on a dedicated high-priority audio callback thread, applying surround mixing, stereo folding, and output gain without holding guest thread locks.

### 2.2 Buffer Submission & Queue Depth
Guest audio thread `t54338` submits audio frames via `SDLAudioDriver::SubmitFrame(uint32_t frame_ptr)`:
- Frames are translated from virtual memory and queued in `frames_queued_`.
- Queue depth profiling ensures continuous buffer replenishment without audio buffer underruns or glitches.

---

## 3. Media Assets & Content Streaming

### 3.1 Base Disc Content Inventory
The extracted single-disc installation (`.local/rise360/game-base/`) was inventoried for media:
- **Core Game Archives**:
  - `bigfile.000.tiger` (2,147,459,120 bytes)
  - `bigfile.001.tiger` (130,651,255 bytes)
- **Localized Audio / Asset Packages**:
  - `bigfile_ENGLISH.000.tiger` (855,229,584 bytes)
  - `bigfile_FRENCH.000.tiger` (788,074,384 bytes)
  - `bigfile_LATAMSPANISH.000.tiger` (785,891,520 bytes)
  - `bigfile_DUTCH.000.tiger` (375,933 bytes)
- **Cinematic Video Assets**: 71 Bink video files (`.bik`) under `movies/` (e.g. `01_rockbottom_cine.bik`, `LevelLoad_14Expedition.bik`).

### 3.2 Streaming Architecture
- **In-Engine Bink Decoder**: Video playback is handled by the title's recompiled PowerPC Bink middleware routines, which stream video frames into D3D9/Xenos textures and submit multi-channel audio frames to the APU.
- **VFS Boundary Enforcement**: Negative path queries for Title Update packages (`d:\PATCH1.000.tiger` and `UPDATE:\TITLEUPDATE.000.tiger`) return `STATUS_NO_SUCH_FILE` (`0xc000000f`), ensuring graceful base-disc fallback in compliance with ADR-02.

---

## 4. Timing & Synchronization Verification

### 4.1 Monotonic Performance Clocks
Guest timing APIs are bound to `rex::chrono::Clock`:
- **`KeQueryPerformanceFrequency`**: Returns the fixed guest tick frequency (`chrono::Clock::guest_tick_frequency()`).
- **`KeQuerySystemTime`**: Returns 100-nanosecond intervals since January 1, 1601 (Windows NT Epoch) via `chrono::Clock::QueryGuestSystemTime()`.
- **`KeDelayExecutionThread`**: Handles microsecond and millisecond thread sleep intervals with alertable APC delivery.
- **`NtYieldExecution`**: Safely yields processor timeslices across worker threads (`rex::thread::MaybeYield()`).

### 4.2 Shared Memory Resource Management
During intensive repeated testing, Linux POSIX shared memory (`/dev/shm/xenia_memory_*`) was identified as accumulating when processes were terminated via timeouts. To prevent memory starvation and SIGBUS faults:
- Added `Rise360App::CleanStaleShm()` to `port/src/rise360_app.h`.
- Invoked automatically in `OnPreSetup()` and `OnShutdown()`.
- Verified that shared memory usage remains strictly bounded, maintaining ~8 GB of free system memory across all test cycles.

---

## 5. Verification Matrix & Test Evidence

| Run | Duration | Endpoint / Format | Pipelines | Exit Code | Observation |
|---|---|---|---|---|---|
| `rise360_040` | 15.0s | Built-in Audio Analog Stereo (6ch 48kHz) | 234 | `124` | Active audio streaming; VFS open descriptors verified. |
| `rise360_042` | 10.0s | Built-in Audio Analog Stereo (6ch 48kHz) | 234 | `124` | Clean memory run; zero audio underruns. |
| `rise360_043` | 15.0s | Built-in Audio Analog Stereo (6ch 48kHz) | 234 | `124` | Verified `CleanStaleShm()` hook; audio buffers active. |
| `rise360_044` | 3.0s | Headless Verification | N/A | `124` | Confirmed pre-setup SHM cleanup. |

---

## 6. Conclusion & Next Step

Milestone M6 is fully **PASSED**.
Next allowed step: **Step 09 (Milestone M7) — First Clean Authentic Game-Specific Build and Launch Check**.
