# Step 05 / Milestone M3 Report: Guest Services, VFS, and Runtime Initialization

- **Step ID**: 05 — Integrate SDK launcher, guest services and single-disc content (Revision 2)
- **Milestone**: M3 (Step 05)
- **Date**: 2026-11-06
- **Host**: Linux 7.0.0-42-generic x86_64 / Ubuntu 26.04.1 LTS
- **GPU**: Intel(R) HD Graphics 620 (KBL GT2) [8086:5916], Mesa 26.0.8-1ubuntu0.3, Vulkan API 1.4.335
- **Predecessor Source Commit**: `1670763` (Milestone M2)
- **SDK Pinned Commit**: `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518` (ReXGlue v0.10.0.2-dev)
- **Status**: **PASS**

---

## 1. Executive Summary

Milestone M3 establishes the complete native host runtime environment for the recompiled Xbox 360 *Rise of the Tomb Raider* (`Title ID 53510823`, `Media ID 0A657B25`, Version 3). Building upon the 45,104 recompiled PowerPC functions and 207 translation units produced in Milestone M2, this milestone implements the ReXApp custom application glue (`Rise360App`), mounts the single-disc virtual filesystem (VFS), attaches guest memory arenas and multi-core threading schedulers, initialises host audio (ALSA/Pulse 6-channel 48kHz), links the dynamic Xenos GPU plugin via Vulkan on the native Intel HD 620 device, and systematically resolves all indirect PowerPC call dispatch targets.

In bounded runtime tests (`rise360_035.log` and `rise360_036.log`), the recompiled title launched, initialized all guest kernel/XAM services, spawned and synchronized guest worker threads, created and cached over 350 graphics pipeline states, streamed audio buffers, and ran continuously without crashing, unhandled exceptions, or unresolved function aborts, terminating cleanly with exit code 124 upon timeout.

---

## 2. Implemented Subsystems & Configuration

### 2.1 ReXApp Customization (`port/src/rise360_app.h`)
The application class `Rise360App` inherits from `rex::ReXApp` and overrides lifecycle hooks:
- **`OnPreSetup(rex::RuntimeConfig& config)`**:
  Enables the dynamic Xenos GPU plugin (`config.gpu_plugin = "xenos"`) to route Xbox 360 Direct3D 9 / Xenos draw calls directly through ReXGlue's Vulkan translation backend.
- **`OnConfigurePaths(rex::PathConfig& paths)`**:
  - Automatically locates and configures `paths.game_data_root` pointing to `.local/rise360/game-base`.
  - Configures `paths.user_data_root` to `.local/rise360/user` and `paths.cache_root` to `.local/rise360/cache`.
  - **ADR-02 Base-Disc Compliance**: Explicitly clears `paths.update_data_root`, strictly isolating the base disc installation and ensuring no quarantined Title Update assets are accessed.

### 2.2 Target Build Configuration (`port/CMakeLists.txt`)
Configured the build system via:
```cmake
rexglue_setup_target(rise360 GPU_PLUGINS xenos)
```
This links the required host runtime libraries, bundles the Xenos plugin dependency, and establishes clean include directories and definitions across all 207 recompilation compilation units.

### 2.3 Virtual Filesystem (VFS) Mapping & Title Update Handling
The runtime successfully mounts:
- `game:\` and `d:\` -> `/mnt/6421-8598/building/FrostyPickaxe/.local/rise360/game-base/`
- `UPDATE:\` -> unmounted (`[no device]`), as required by ADR-02.
During startup, the engine queries `d:\PATCH1.000.tiger` and `UPDATE:\TITLEUPDATE.000.tiger`. In accordance with base-disc operation, the VFS returns `STATUS_NO_SUCH_FILE` (`0xc000000f`), and the game engine gracefully falls back to disc archives without errors.

### 2.4 Multi-threaded Guest Runtime Topology
The guest threading architecture initializes a 512 MB virtual memory arena mapped at virtual base `0x0000000100000000` and physical base `0x0000000200000000`. The scheduler registers and runs concurrent guest threads:
- Core scheduler thread (`t51232`)
- GPU command processor thread (`t51231`)
- Main engine / game loop thread (`t51237`)
- Audio processing thread (`t51238`)
- Network / HTTP worker thread (`t51273`) executing `NetDll_XHttpDoWork`
- Engine multicore workers (`cdcMulticore 0-5`, `cdcMulticore WUD`, `XenonPostCollect`, `XenonFlush`, `MSFileSource Read Helper`).

### 2.5 APU & Audio Subsystem
The APU driver initializes the native host Linux audio subsystem via SDL3/PulseAudio/ALSA:
```
[info] [apu] audio endpoint 'Built-in Audio Analog Stereo': 6 ch, 48000 Hz, format 0x8120; submitting 6 ch
```
Audio streaming buffers are actively submitted by guest thread `t51237`.

### 2.6 Vulkan Backend on Intel HD Graphics 620
The Xenos plugin initializes Vulkan instance API version 1.4.341 and selects physical device `[0] Intel(R) HD Graphics 620 (KBL GT2)` using `/usr/lib/x86_64-linux-gnu/libvulkan_intel.so` (Mesa 26.0.8-1ubuntu0.3, Vulkan 1.4.335):
- Presenter initializes swapchain with format 44 (`VK_FORMAT_B8G8R8A8_UNORM`), color space 0.
- GPU shader storage initialized for Title `53510823`.
- Dynamically translated over 350 vertex shader (VS) and pixel shader (PS) pipelines from guest microcode into native Vulkan SPIR-V pipelines (e.g. VS `363689C3AA6A2802`, PS `E6FEBCCB1A98F2CA`).

---

## 3. PowerPC Indirect Dispatch Resolution

In static AOT recompilation, indirect branch instructions (`bctr`, `blr`, `b`) targeting function pointers computed at runtime require all valid entrypoint targets to be declared in the function dispatch table. During iterative test runs 001 through 034, whenever an unregistered target was called, runtime execution aborted with:
`[FATAL] Call to invalid or unregistered function at guest address 0x...`

Through inspection probes on loaded PowerPC instructions in memory, each missing entrypoint was analyzed and classified:
1. **Multiple Inheritance `this`-Adjuster Thunks**:
   Pattern: `addi r3, r3, -offset; b target`
   Identified and declared cluster `0x82502160` - `0x825021D0` (10 adjuster thunks adjusting `r3` by -528 and branching).
2. **Interface Dispatch Thunks**:
   Pattern: `lwz r12, 0(r3); lwz r12, offset(r12); mtctr r12; bctr`
   Identified and declared thunk clusters `0x82B13EE8` - `0x82B13FE8`, `0x82BA56E0` - `0x82BA5788`, and `0x829A28E8` - `0x829A2918`.
3. **Leaf Utility Functions**:
   Pattern: standard register operations ending in `blr`.
   Identified and declared `0x82C21240`, `0x823E7730`, `0x82286388`, `0x82286360`, `0x821718D8`, `0x82B0EDD0`, `0x82B0EE28`, `0x823E7758`, `0x823E6018`, `0x823E60E0`, `0x824DFB98`, `0x824DFBA8`, `0x82BE5FF8`, `0x82BE6010`, `0x82BE5F38`, `0x82C77688`, `0x82BC9408`, `0x8299D2E0`, and `0x824EC610`.

All entrypoints were added to `port/rise360_manifest.toml`, bringing the recompiled function count to 45,152 functions.

---

## 4. Test Verification & Evidence

| Run | Configuration | Duration | Result / Exit Code | Observation |
|---|---|---|---|---|
| `rise360_035` | `--headless` Release | 20.0s | `124` (Timeout PASS) | Ran full 20s without errors; 350 Vulkan pipelines built; APU 6ch 48kHz audio streaming; zero invalid calls. |
| `rise360_036` | `--headless` Release | 5.0s | `124` (Timeout PASS) | Fresh reproducible verification run; clean shutdown. |

---

## 5. Artifacts and Protected Files Audit

- **Tracked Files Added / Modified**:
  - `port/CMakeLists.txt`
  - `port/src/rise360_app.h`
  - `docs/implementation/05_Runtime_Guest_Services_and_VFS.md`
  - `docs/implementation/status.md`
  - `docs/implementation/changes.md`
  - `docs/implementation/commands.md`
  - `docs/implementation/validation.md`
- **Protected Files Verified Untouched**:
  - `README.md` (unmodified)
  - `docs/research/00_Repository_State.md` (unmodified)
  - `docs/research/02_Risks_Unknowns_and_Gates.md` (unmodified)
  - `docs/research/03_Sources_and_Evidence.md` (unmodified)
  - `gemini_argon/Gemini_Argon_02_Scope.txt` (unmodified)
  - `gemini_argon/Gemini_Argon_04_Architecture_Handoff.txt` (unmodified)
- **Private Files Confirmed Ignored**:
  - `.local/`
  - `port/generated/`
  - `port/rise360_manifest.toml`
  - `port/out/`

---

## 6. Conclusion & Next Step

Milestone M3 is fully **PASSED**.
Next allowed step: **Step 06 (Milestone M4) — Validate HD 620 Vulkan Device and Real Xenos Frame Path**.
