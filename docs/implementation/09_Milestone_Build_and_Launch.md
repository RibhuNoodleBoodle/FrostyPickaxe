# Step 09 / Milestone M7: First Clean Authentic Game-Specific Build and Launch Check

**Date:** 2026-11-05 UTC / 2026-11-06 Local  
**Machine:** Linux 7.0.0-42-generic x86_64 Ubuntu 26.04.1 LTS  
**GPU / Display:** Intel HD Graphics 620 (`[8086:5916]` rev 02), Mesa 26.0.8-1ubuntu0.3, Vulkan 1.4.335, Wayland (`wayland-0`)  
**Source Commit:** `debf2c8` (`Milestone M6 (Step 08): Audio streaming, media assets, timing paths, and shared memory stability`)  
**Pinned SDK Commit:** `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518` (ReXGlue v0.10.0.2-dev.gc94f5eb)  
**Compiler:** Clang 21.1.8 / C++23 / Ninja 1.13.2 / CMake 4.2.3  

---

## 1. Executive Summary and Status

Milestone M7 (Experiment E5-build) independently verifies a clean, from-scratch compilation, linkage, and native launch of the game-specific executable `rise360` from the authentic PowerPC source translation of *Rise of the Tomb Raider* (Xbox 360 Base Disc, Title ID `53510823`, Media ID `0A657B25`).

All 424 build artifacts were cleaned (`ninja -C port/out/build/linux-amd64-release -t clean rise360`), followed by a full recompilation and link of all 207 C++ translation units (`rise360_recomp.0.cpp` through `rise360_recomp.206.cpp`, `rise360_init.cpp`, `rise360_register.cpp`) plus application glue (`src/main.cpp`, `src/rise360_app.h`).

The resulting binary was launched under Wayland with Vulkan on the Intel HD 620 GPU. Over a 35.0-second execution run, 765 presentation frames were captured; 464 active non-black rendered frames (frames 301–764) displaying the animated title emblem with 331 unique colors at native 1366x768 resolution were independently verified.

| Subgate | Status | Description |
|---|---|---|
| **Compile Subgate** | **PASS** | Clean build of all 207 recompiled translation units and application glue into `rise360` (exit code 0). |
| **Link Subgate** | **PASS** | `rise360` executable linked dynamically against `librexruntime.so` (115 MB, SHA-256 `dd6ca62cdb61da96804e8a9ca27041c78c52378cf2f4a48af0f233ee7bcc219b`). |
| **Launch Subgate** | **PASS** | Process spawned cleanly under Wayland, initialized Vulkan swapchain at 1366x768, and ran for 35.0s with 0 crashes (exit code 124 timeout). |
| **Visual Frame Subgate** | **PASS** | 765 presentation frames captured; 464 active non-black rendered animation frames verified (331 unique colors). |
| **Gameplay Subgate** | **NOT TESTED** | Bounded to build & launch verification. Handed off to Step 10 (blocked on physical gamepad attachment per BLK-02). |
| **Overall M7 Milestone** | **PASS** | All required build, launch, and live frame criteria satisfied. |

---

## 2. Binary and Build Provenance

### Executable Identity
- **Binary Path:** `port/out/build/linux-amd64-release/rise360`
- **File Size:** 120,442,168 bytes (~115 MB)
- **SHA-256:** `dd6ca62cdb61da96804e8a9ca27041c78c52378cf2f4a48af0f233ee7bcc219b`
- **Build ID:** `5590be20cbefa9eb001e9f376991d96322afadf3` (SHA-1)
- **ELF Type:** 64-bit LSB PIE executable, x86-64, dynamically linked, interpreter `/lib64/ld-linux-x86-64.so.2`
- **Dynamic Linkages (`ldd`):**
  - `librexruntime.so` -> `.local/sdk/rexglue-sdk/out/install/linux-amd64/lib/librexruntime.so`
  - `libwayland-client.so.0` -> system Wayland client
  - `libX11.so.6`, `libxcb.so.1` -> system X11/XCB libraries
  - `libstdc++.so.6`, `libc.so.6`, `libm.so.6` -> GNU C/C++ runtime

### Build Procedure
1. Cleaned target: `ninja -C port/out/build/linux-amd64-release -t clean rise360` (424 files cleaned).
2. Code generation stamp check: verified 209 files written, 212 unchanged, 0 deleted across 45,104 functions.
3. Translation unit compilation: 207 C++ files compiled in parallel with Clang 21.1.8 using precompiled header (`cmake_pch.hxx.pch`).
4. Application compilation: `port/src/main.cpp`, `port/src/rise360_app.h` compiled with POSIX SHM auto-purging hooks.
5. Final link: `rise360` binary linked in 171.2s total build time.

---

## 3. Empirical Launch and Frame Presentation Evidence

### Launch Command
```bash
WAYLAND_DISPLAY=wayland-0 DISPLAY=:0 SDL_VIDEO_DRIVER=wayland \
VK_INSTANCE_LAYERS=VK_LAYER_MESA_screenshot \
VK_LAYER_MESA_SCREENSHOT_CONFIG="frames=all,output_dir=/mnt/6421-8598/building/FrostyPickaxe/.local/rise360/proof/step09_frames,log_type=info" \
LD_LIBRARY_PATH=.local/sdk/rexglue-sdk/out/install/linux-amd64/lib \
timeout 35 ./port/out/build/linux-amd64-release/rise360
```

### Presentation & Frame Metrics
- **Duration:** 35.0 seconds (clean SIGTERM exit 124 via `timeout`).
- **Total Captured Frames:** 765 frames (`0.png` through `764.png`).
- **Initial Swapchain:** 1280x720 RGB.
- **Engine Swapchain:** Native 1366x768 RGB, Format 44 (`VK_FORMAT_B8G8R8A8_UNORM`).
- **Black Clear Phase:** Frames 0–300 (engine asset loading from `bigfile.000.tiger`).
- **Active Rendered Phase:** Frames 301–764 (464 frames).
  - Frame 301: size=(1366, 768), RGB extrema `((64, 94), (66, 98), (0, 7))`, 77 unique colors.
  - Frame 500: size=(1366, 768), 331 unique colors (animated emblem title render).
  - Frame 764: size=(1366, 768), RGB extrema `((34, 150), (42, 188), (0, 3))`, 331 unique colors.
- **Shared Memory Stability:**
  - Startup stale SHM cleanup: active via `CleanStaleShm()`.
  - `/dev/shm` usage post-run: 246 MB / 7.7 GB total (7.5 GB free).
  - Available host RAM: 8.89 GB. Zero leaks or SIGBUS events.

---

## 4. Test Verification

Unit tests discovery (`python3 -m unittest discover tests`):
- `test_gdfx_parser.py`: 5 tests passed (header magic, sector calculations, boundary guards).
- `test_input_bridge.py`: 7 tests passed (buttons, thumbstick axes, Y-inversion, triggers, deadzones, packet counters, disconnect handling).
- Total: 12/12 unit tests passed in 0.001s.

---

## 5. Requirement -> Evidence -> Result Mapping

| Requirement | Evidence / Artifact | Result |
|---|---|---|
| Fresh isolated source/build environment without discarding user edits | 6 modified user docs preserved; build executed in isolated `.local/` / `port/out/` | **PASS** |
| Genuine generated game logic compiled & linked | 207 recompiled TUs (45,104 functions) compiled with Clang 21; `rise360` linked (115 MB) | **PASS** |
| Record binary identity & SHA-256 | SHA-256 `dd6ca62cdb61da96804e8a9ca27041c78c52378cf2f4a48af0f233ee7bcc219b` | **PASS** |
| Launch binary with Vulkan & retain logs | Run 046 (35s, exit code 124); `.local/rise360/proof/step09_launch_046.log` | **PASS** |
| Cross-check live frame evidence | 765 frames captured; 464 active rendered frames (frames 301-764, 331 colors) | **PASS** |
| Separate compile, launch, and gameplay statuses | Explicitly distinguished in report and ledgers | **PASS** |

---

## 6. Regressions and Blockers

- **Regressions:** None observed. Build is 100% clean and reproducible.
- **Blockers:**
  - **Issue BLK-02:** Full interactive player progression (New Game, menu selection) requires a physical Xbox 360 controller or verified input event source. Host currently has no physical controller attached (`/proc/bus/input/devices`). M5 and M8 remain gated on this physical requirement per the Gemini_00 anti-cheating policy.

---

## 7. Next Allowed Step

- **Step 10 (Milestone M8):** New Game sequence and early player progression audit.
