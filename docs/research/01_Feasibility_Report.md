# Feasibility Report: *Rise of the Tomb Raider* (Xbox 360) Native Port via ReXGlue SDK

**Project:** `FrostyPickaxe`  
**Target Title:** *Rise of the Tomb Raider* — Xbox 360 Release (Title ID `53510823`, Media ID `0A657B25`, developed by Nixxes Software / Crystal Dynamics, Nov 2015)  
**Primary Target:** Native PC (`x86-64`, Windows & Linux) with Vulkan Graphics + SDL3 Gamepad Input; Minimum GPU Gate: **Intel HD Graphics 620**  
**Deferred Target:** Android (`arm64-v8a`, Vulkan + SDL3) — strictly post-PC viability  
**Date:** 2026-11-03 (Revised with Read-Only Inspection of `Rise of the Tomb Raider.iso`)  
**Author:** Gemini Argon (Medium Reasoning) — Phase 0 Researcher and Feasibility Analyst  

---

## 1. Executive Feasibility Verdicts (Falsifiable)

Per Section 3 of the Phase 0 Mandate, each required dimension is evaluated using the strict classification scale:
`SUPPORTED BY EVIDENCE` | `POSSIBLE WITH MATERIAL GAPS` | `UNKNOWN UNTIL BINARY ANALYSIS` | `CURRENTLY BLOCKED` | `NOT FEASIBLE WITH IDENTIFIED CONSTRAINTS`

| # | Dimension | Verdict | Confidence | Primary Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **(1)** | **Static Recompilation / Guest Runtime Viability for THIS Xbox 360 Title** | **POSSIBLE WITH MATERIAL GAPS** *(Outer XEX2 Header Verified; Inner Encrypted Payload & Title Update `.xexp` Still Require Decryption/Merge)* | **High** | Read-only inspection of `Rise of the Tomb Raider.iso` confirms single-disc (`Disc=1/1`) XEX2 (`IntermediateTR2.exe`, `0x82000000`–`0x835B0000`, `enc_type=1`, `comp_type=1`, 541 import records across `xboxkrnl.exe` and `xam.xex`, linked with `D3D9LTCG` and `XAUDIO2`). However, a **Title Update (TU)** for Media ID `0A657B25` is still missing locally and required to pass the Start screen (Xenia Canary #174). |
| **(2)** | **Vulkan Graphics Viability for THIS Xbox 360 Title** | **POSSIBLE WITH MATERIAL GAPS** | **High** | Upstream ReXGlue Vulkan (`src/graphics/vulkan/`) is a 38.3k-LOC Xenos-derived backend, and `default.xex` embeds `D3D9LTCG` (`v2.0.21256.16384`). However, Title `53510823` exhibits known `gpu-drawing-corrupt` (purple/magenta LUT tint) and `gpu-readback` hazards in Xenia Canary (#174) that must be isolated and fixed. |
| **(3)** | **PC Portability Viability under Current ReXGlue SDK (`v0.10.0` / `bd833a2ab69d`)** | **SUPPORTED BY EVIDENCE** *(Single-Disc VFS Confirmed)* / **POSSIBLE WITH MATERIAL GAPS** *(Requires TU Overlay & Windows Vulkan Override)* | **High** | Local ISO audit disproves third-party 2-disc rumors: the entire game (`bigfile.000.tiger`, `bigfile.001.tiger`, language `.tiger` files, and 62 `.bik` movies) resides on a **single XGD2 DVD (`Disc 1/1`)**, vastly simplifying VFS mounting! Still requires a writable `cache:` mount, Title Update VFS/XEX merge, and `-DREXGLUE_USE_VULKAN=ON` on Windows. |
| **(4)** | **Acceptable Performance Plausibility Specifically on Intel HD Graphics 620** | **POSSIBLE WITH MATERIAL GAPS** *(High Risk on Windows; Medium-High Risk on Linux Mesa ANV)* | **Medium** | HD 620 (Gen9.5 Kaby Lake GT2, 24 EUs, shared DDR3/DDR4) supports Vulkan 1.3 and passes ReXGlue's hard feature checks (`fragmentStoresAndAtomics`, `vertexPipelineStoresAndAtomics`, `independentBlend`), **but lacks `VK_EXT_fragment_shader_interlock` (FSI)**. Must run on the Host Render Target (`fbo`) path (`render_target_path_vulkan="fbo"`) and requires shared-memory hot-page batching to survive `.tiger` streaming. |
| **(5)** | **Android Portability (`arm64-v8a`) ONLY AFTER PC Success** | **CURRENTLY BLOCKED** *(Upstream SDK)* / **POSSIBLE WITH MATERIAL GAPS** *(With Community Fork Patches)* | **High** | Upstream `rexglue-sdk` (`v0.10.0` / `bd833a2ab69d`) has no Android CMake preset, no Bionic fiber implementation (`ucontext` absent on Android), and no APK/SAF packaging. Strictly deferred until PC is proven. |

### Overall Phase 0 Gate Recommendation:
> **`PROCEED TO ARCHITECTURAL DISCOVERY` (WITH MANDATORY TITLE UPDATE & DECRYPTION GATES)**  
> The presence of `Rise of the Tomb Raider.iso` in the workspace resolves major structural unknowns (confirming Title ID `0x53510823`, Media ID `0x0A657B25`, single-disc layout, XDK `21256` static libraries, `D3D9LTCG`, `XAUDIO2`, and exact XEX2 memory bounds). Transition to the separate **Gemini Argon Principal Software Architect** session to design the XEX decryption + Title Update (`.xexp`) merge pipeline, single-disc + `cache:` VFS architecture, Xenos Vulkan `fbo`-path fixes, and Intel HD 620 instrumentation harness.

---

## 2. Detailed Verdict Breakdown (Claim – Evidence – Uncertainty)

### Verdict (1): Static Recompilation / Guest Runtime Viability for *Rise of the Tomb Raider* (Xbox 360)
- **Verdict:** **`POSSIBLE WITH MATERIAL GAPS`** *(Outer XEX2 Verified; Inner PE Decryption & Title Update `.xexp` Required for Codegen)*
- **Confidence:** **High**
- **Evidence:**
  1. **Direct Read-Only Audit of `default.xex` in `Rise of the Tomb Raider.iso` (`00_Repository_State.md`):**
     - **File & Hashes:** Located at XDVDFS sector `663503`, size `16,531,456` bytes (`0xFC4000`), SHA-256 `47e6476f6d393d86612e7af938979e9c706b54dc526d8422413711999d41e585`.
     - **Execution Identity:** Title ID `0x53510823`, Media ID `0x0A657B25`, Version `0.0.0.3` (`BaseVer 0.0.0.3`), `Disc = 1/1`, original PE name `IntermediateTR2.exe` (build stamp `491.10_2015-09-22_08-45@UTR-BUILD08` in `tr2.arg`).
     - **Address Space & Resources:** Loads at `0x82000000` with unpacked `image_size = 0x15B0000` (`22,740,992` bytes, spanning `0x82000000`–`0x835B0000`), entry point `0x82B00790`, default stack size `256 KiB` (`0x40000`), and `64` TLS slots (`raw_data_addr = 0x834B0C00`, `2,120` bytes).
     - **Encryption & Compression (`FileFormatInfo` at `0x22B8`):** `encryption_type = 1` (standard retail AES encrypted payload) and `compression_type = 1` (**Basic compression** — 4 simple `[data_size, zero_size]` blocks unpacking directly to `22,708,224` bytes, rather than LZX `compression_type = 2`).
     - **Self-Contained Executable (No External Game DLLs):** `ImportLibraries` (`0x3718`) imports **only** two system modules: `xboxkrnl.exe` (`311` records / ~155 symbols) and `xam.xex` (`230` records / ~115 symbols). All middleware and XDK subsystems (`D3D9LTCG`, `XGRAPHC`, `XAUDIO2`, `XAPOBA`, `XMCORE`, `XMP`, `XMIC`, `XHV2`, `XNET`, `XONLINE`, `XHTTP`, `XAUTH`, `XSOCPST`, `XPARTY`, `XAPILIB`, `LIBCPMT`, `C1`/`C2`) are statically linked into `default.xex` using **XDK `2.0.21256.16384`**.
  2. **Mandatory Title Update (TU) Requirement (`xenia-canary/game-compatibility#174`):**
     - Public compatibility testing on Xenia Canary (#174) proves that unpatched base `default.xex` (`v0.0.0.3`) boots to the start screen and enters an infinite loading spin upon pressing Start. Comment by `has207` (2026-05-08) confirms: *"Needs TU to get in game, but there are severe rendering issues but I managed to get through the prologue at least."*
     - Because `Rise of the Tomb Raider.iso` contains the base `v0.0.0.3` executable (`Media ID 0A657B25`), the user will also need the corresponding Xbox 360 **Title Update (TU)** package for `53510823` / Media ID `0A657B25`, and the Architect must design an offline `.xexp` patch merge before running `rexglue codegen`.
  3. **ReXGlue Codegen & Runtime Capabilities vs. Gaps (`v0.10.0` vs `bd833a2ab69d` vs Community Forks):**
     - Upstream `development` (`bd833a2ab69d`, 2026-10-02) fixed critical codegen bugs present in `v0.10.0` (`c94f5ebdcb3c`), including `vpkuwus`/`vpkuhus` aliasing (`6319e236d`), unsigned register types (`ea222e983`), `stwcx.` `std::atomic` CAS (`7f7c92ef6`), and `sync`/`lwsync`/`eieio` fences (`bd833a2ab`).
     - However, the `CrownParkComputing/Xbox360-Native-Ports` audit (`docs/REXGLUE_FORK_CHANGES.md`, 2026-09-23) proves that upstream `v0.10.0` still lacked:
       - **`KeInsertQueueDpc` execution:** Upstream appended DPCs to `dpc_list` and never drained them in Release builds, dropping all DPC-driven completion signals.
       - **`db16cyc` spin-wait hint lowering:** Upstream dropped `db16cyc`, causing guest streaming/sync spin-loops to burn 100% of a host core.
       - **`bctr` switch fall-through trap:** Upstream emitted `__builtin_trap()` when a switch index fell outside the statically recovered jump table.
       - **Out-of-line basic block branches & `GapFill` over-splitting:** Especially relevant here because `default.xex` is compiled with **`D3D9LTCG` (Link-Time Code Generation)** (`C1`/`C2` `v16.0.11886.17408`), which aggressively inlines and splits cold basic blocks out-of-line past mid-function `blr` instructions!
       - **Host thread FP exception masking & Blocking `WaitMultiple` / FIFO auto-reset events.**
- **Critical Assumptions & Unknowns:**
  - `UNKNOWN` (Until Decryption & TU Acquisition in Phase 2): Exact decrypted `.pdata` function count, exact list of the ~155 `xboxkrnl.exe` and ~115 `xam.xex` import ordinals (as the import table records reside inside the AES-encrypted PE payload), and the `.xexp` Title Update delta layout for Media ID `0A657B25`.
- **Primary Technical Blockers:**
  1. **[Critical]** Acquisition and offline pre-application of the Title Update (`.xexp` -> `default.xex` for Media ID `0A657B25`); base `v0.0.0.3` `default.xex` on the ISO hangs after pressing Start.
  2. **[High]** `D3D9LTCG` Link-Time Code Generation out-of-line basic blocks and `bctr` jump tables in `IntermediateTR2.exe` triggering ReXGlue scanner over-splitting or `__builtin_trap()` fall-throughs without the `CrownParkComputing` codegen fixes.
  3. **[High]** Upstream ReXGlue kernel/threading defects (`KeInsertQueueDpc` no-op, `WaitMultiple` polling/starvation, `db16cyc` spin-loops, FP exception unmasking) in `v0.10.0`.
- **Next Verification Step for Gemini Argon Architect (Pass/Fail Criterion):**
  - *Verification:* Design the offline ISO extraction (`rexiso`), retail XEX decryption/decompression, `.xexp` (Title Update) merge, and static analysis pipeline (`rexglue codegen` audit).
  - *Observable Pass/Fail:* **PASS** if decrypted + TU-patched `default.xex` parses cleanly through `rexglue` function discovery (with LTCG out-of-line block handling) and 100% of its `311` `xboxkrnl` and `230` `xam` import records resolve; **FAIL** if `.xexp` delta patching cannot produce a valid static PE/XEX2 image or if Scaleform executes JIT code from heap pages.

---

### Verdict (2): Vulkan Graphics Viability for *Rise of the Tomb Raider* (Xbox 360)
- **Verdict:** **`POSSIBLE WITH MATERIAL GAPS`**
- **Confidence:** **High**
- **Evidence:**
  1. **Static Library Verification (`D3D9LTCG` & `XGRAPHC` v2.0.21256.16384):**
     - Read-only inspection of `default.xex` confirms it links `D3D9LTCG` (`v2.0.21256.16384`). Because `D3D9LTCG` compiles D3D9 command-buffer construction directly into the game's PowerPC code, ReXGlue cannot intercept high-level D3D9 API calls; it **must** translate low-level Xenos PM4 ring-buffer packets and shared-memory writes via `src/graphics/vulkan/`.
     - Note on `rexgpu-native`: Community forks (`CrownParkComputing` and `deivid22srk`) both proved `rexgpu-native` (bypassing EDRAM emulation) fails on complex 3D games (`VK_ERROR_DEVICE_LOST`). Therefore, ReXGlue's standard Xenos EDRAM-emulating Vulkan backend (`src/graphics/vulkan/`) is mandatory.
  2. **Title-Specific Xenos Rendering Bugs (`xenia-canary/game-compatibility#174`):**
     - Title `53510823` is tagged in Xenia Canary with **`gpu-drawing-corrupt`**, **`gpu-readback`**, and **`tech-middleware-scaleform`**, exhibiting purple/magenta color corruption on the title screen and severe rendering corruption in the prologue.
  3. **Documented Upstream ReXGlue Vulkan Gaps (`CrownParkComputing/Xbox360-Native-Ports` audit):**
     - Upstream ReXGlue `v0.10.0` lacked `xenia-canary` SPIR-V texture-fetch fixes: `exp_adjust` read from fetch-constant word 4 instead of word 3, and 3D volume textures sampled via 2D fetches lost all slices except `Z=0` (breaking 3D color-grading LUTs — a prime suspect for *Rise of the Tomb Raider*'s purple/magenta color corruption!).
- **Critical Assumptions & Unknowns:**
  - `UNKNOWN`: Whether *Rise of the Tomb Raider* (Xbox 360) requires GPU-to-CPU EDRAM resolve readbacks (`vulkan_readback_resolve=true`) or shader `memexport` readbacks (`vulkan_readback_memexport=true`) for visibility culling or exposure adaptation (`gpu-readback` tag on Xenia Canary #174).
- **Primary Technical Blockers:**
  1. **[High]** `gpu-drawing-corrupt` (magenta/purple tint and prologue corruption) in Xenos shader/texture translation.
  2. **[High]** `gpu-readback` dependency stalling the Vulkan pipeline if synchronous CPU readbacks are required every frame.
- **Next Verification Step for Gemini Argon Architect (Pass/Fail Criterion):**
  - *Verification:* Architect a shader/texture diagnostic plan using ReXGlue's GPU CVars (`dump_shaders`, 3D-as-2D LUT image view wrapping, `exp_adjust` word-3 fix, and `vulkan_readback_resolve` toggle testing).
  - *Observable Pass/Fail:* **PASS** if title screen and prologue render in Vulkan `fbo` mode without magenta LUT corruption or `VK_ERROR_DEVICE_LOST`; **FAIL** if rendering requires per-pixel EDRAM format aliasing impossible in `Path::kHostRenderTargets` (`fbo`).

---

### Verdict (3): PC Portability Viability under Current ReXGlue SDK
- **Verdict:** **`SUPPORTED BY EVIDENCE`** *(Single-Disc Layout Verified)* / **`POSSIBLE WITH MATERIAL GAPS`** *(Requires TU Overlay, `cache:` Mount, & Windows Vulkan Override)*
- **Confidence:** **High**
- **Evidence:**
  1. **Single-Disc XDVDFS Archive Layout Verified directly from `Rise of the Tomb Raider.iso`:**
     - Earlier third-party forum claims suggested a 2-disc install/play split. Direct read-only XDVDFS inspection of `Rise of the Tomb Raider.iso` (`7,838,695,424` bytes) and `default.xex` (`ExecutionInfo: Disc = 1/1`) **conclusively disproves the 2-disc rumor**:
       - `default.xex` (`16,531,456` bytes)
       - `bigfile.000.tiger` (`2,147,459,120` bytes / `2.00 GiB` — split at the 2 GiB boundary)
       - `bigfile.001.tiger` (`130,651,255` bytes / `124.6 MiB`)
       - `bigfile.000.nfo` (`191` bytes: `game bap 1563257619 package 1 chunk 2 version 1 required 1 bigfile 1 dlcindex 1 mount 0 unmount 1` / `feature launchchunk` / `feature nonlaunchchunk0`)
       - Language archives: `bigfile_ENGLISH.000.tiger` (`855.2 MB`), `bigfile_FRENCH.000.tiger` (`788.1 MB`), `bigfile_LATAMSPANISH.000.tiger` (`785.9 MB`), `bigfile_DUTCH.000.tiger` (`375.9 KB`)
       - `movies/*.bik`: **62 pre-rendered Bink video files** totaling `1,813,864,636` bytes (`1.69 GiB`), including both narrative cutscenes (`01_rockbottom_cine.bik`..`60_aftermath_cine.bik`, `igc_*.bik`) and loading-screen videos (`LevelLoad_14Expedition.bik`, `LevelLoad_SH3.bik`, `LevelLoad_VH4.bik`).
       - `tr2.arg` (`197` bytes): Engine command-line arguments (`test_leveleditor1 -ARCHIVE -noassert -mainmenu -addLevelSelect=true -nosound=false -"GameMetrics/Record Game Metrics"=true -MetricsFPS=true -Online/MetricsID="491.10_2015-09-22_08-45@UTR-BUILD08"`).
     - This means the entire base game mounts cleanly as a single `game:\` (`d:\`) root directory (or directly via `DiscImageDevice` / `rexiso`), requiring only a writable `cache:\` partition and Title Update (TU) overlay!
  2. **Build System & Toolchain (`CMakeLists.txt`, `CMakePresets.json` at `v0.10.0` / `bd833a2ab69d`):**
     - Supports `win-amd64` and `linux-amd64` with Clang 18+ and C++23 (`-mcmodel=large` on Linux x86-64 for 35MB+ recompiled executables, which is directly needed for `default.xex`'s 22.7 MB unpacked image).
     - **Critical Build Default Difference (`CMakeLists.txt` lines 37–43):** Windows defaults to `REXGLUE_USE_D3D12=ON` and **`REXGLUE_USE_VULKAN=OFF`**; Linux defaults to `REXGLUE_USE_VULKAN=ON`. Windows builds must explicitly pass `-DREXGLUE_USE_VULKAN=ON`.
  3. **SDL3 Integration (`thirdparty/sdl3` & `src/input/sdl/sdl_input_driver.cpp`):**
     - Upstream ReXGlue integrates **SDL3 (`3.4.14` in `bd833a2ab69d`)** for windowing, audio, and controller input (`XamInputGetState` / `XamInputSetState`), requiring only the recursive mutex fix in `InputSystem` to prevent thread races during device refresh.
- **Primary Technical Blockers:**
  1. **[High]** Title Update (TU) acquisition and VFS overlay mounting alongside `game:\` and writable `cache:\`.
  2. **[Medium]** Windows CMake preset defaults `REXGLUE_USE_VULKAN=OFF` and `InputSystem` device refresh race condition.
- **Next Verification Step for Gemini Argon Architect (Pass/Fail Criterion):**
  - *Verification:* Design the `FrostyPickaxeApp` (`ReXApp` subclass) VFS mount topology for `game:` + TU overlay + writable `cache:`, and unified Windows/Linux CMake presets forcing `REXGLUE_USE_VULKAN=ON`.
  - *Observable Pass/Fail:* **PASS** if the runtime resolves `tr2.arg`, `bigfile.000.nfo`, `bigfile.000.tiger`, `bigfile.001.tiger`, `bigfile_ENGLISH.000.tiger`, and `movies/*.bik` with zero file-not-found errors.

---

### Verdict (4): Acceptable Performance Plausibility on Intel HD Graphics 620 (PC Gate)
- **Verdict:** **`POSSIBLE WITH MATERIAL GAPS`** *(High Risk on Windows Intel DCH Driver; Medium-High Risk on Linux Mesa ANV)*
- **Confidence:** **Medium** (Hardware capabilities and game archive sizes are verified; actual frame-time under Foundation Engine's `D3D9LTCG` draw/streaming load is unmeasured)
- **Evidence:**
  1. **Hardware & API Baseline (Intel Official Article `000005524` & Mesa ANV):**
     - **GPU:** Intel HD Graphics 620 (Kaby Lake U-series GT2, Gen9.5, 24 EUs, shared host DDR3L/DDR4 RAM at ~17–34 GB/s), officially supporting **Vulkan 1.3** on Windows DCH and Linux Mesa ANV drivers.
  2. **Audit of ReXGlue Vulkan Device Requirements (`src/ui/vulkan/vulkan_device.cpp`) vs. Intel HD 620:**
     - Passes hard requirements (`independentBlend`, `fragmentStoresAndAtomics`, `vertexPipelineStoresAndAtomics`, `geometryShader`, `fillModeNonSolid`).
     - **Lacks `VK_EXT_fragment_shader_interlock` (`fsi`)**, forcing `Path::kHostRenderTargets` (`render_target_path_vulkan = "fbo"` in `render_target_cache.cpp`).
  3. **CPU & Shared-Memory Bottlenecks Specific to `IntermediateTR2.exe` (`default.xex`):**
     - `default.xex` declares **`64` TLS slots** and links `D3D9LTCG` while streaming from `2.13 GiB` of core `.tiger` archives (`bigfile.000.tiger` + `bigfile.001.tiger`) plus `855 MB` of localized `.tiger` audio/assets.
     - On stock ReXGlue `v0.10.0`, continuous `.tiger` streaming into the 512 MB unified memory arena triggers OS write-watch faults (`mprotect`/`VirtualProtect`), breaking the Vulkan render pass hundreds of times per frame unless `gpu_hot_page_frames`, `clear_memory_page_state = false`, `vulkan_dynamic_constant_buffers`, and `db16cyc -> yield()` are enabled.
- **Primary Technical Blockers:**
  1. **[Critical]** Lack of `VK_EXT_fragment_shader_interlock` on Intel HD 620 — Title `53510823` MUST render accurately on `Path::kHostRenderTargets` (`fbo` mode).
  2. **[High]** Shared-memory page fault / render-pass break storm from continuous `bigfile.*.tiger` streaming on stock ReXGlue `v0.10.0`.
  3. **[High]** Severe CPU contention on 2-core/4-thread Kaby Lake-U laptops.
- **Next Verification Step for Gemini Argon Architect (Pass/Fail Criterion):**
  - *Verification:* Design the HD 620 Performance Validation Plan (Section 4 below) and incorporate hot-page residency batching, descriptor caching, and `fbo` render-target validation into the architecture.
  - *Observable Pass/Fail:* **PASS** if a representative in-game scene sustains **>= 30.0 FPS (<= 33.3 ms P95 frame time)** at 1280x720 (or 960x540 scaled) on Intel HD 620 with <= 2.2 GB host RSS and zero `VK_ERROR_DEVICE_LOST`.

---

### Verdict (5): Android Portability (`arm64-v8a`) ONLY AFTER PC Success
- **Verdict:** **`CURRENTLY BLOCKED`** *(on Upstream ReXGlue SDK)* / **`POSSIBLE WITH MATERIAL GAPS`** *(with Community Android Patches, strictly deferred after PC gates)*
- **Confidence:** **High**
- **Evidence:**
  1. Upstream `rexglue-sdk` (`v0.10.0` / `bd833a2ab69d`) supports `linux-arm64` (`simde`), but lacks Android CMake/APK tooling, SAF storage provisioning (needed for the 7.30 GiB ISO / ~4.67 GiB active English+core asset footprint), and Android Bionic `<ucontext.h>` guest fiber switching (`fiber_posix.cpp`).
- **Next Verification Step for Gemini Argon Architect (Pass/Fail Criterion):**
  - *Verification:* Enforce Architecture-Preservation Rules `AP-1` through `AP-5` on the PC codebase while keeping Android implementation strictly frozen until PC Milestones M1–M6 pass.

---

## 3. Subsystem-by-Subsystem Technical Analysis (Updated with ISO Findings)

### 3.1 Target Title Profile: *Rise of the Tomb Raider* (Xbox 360 — Title ID `53510823`, Media ID `0A657B25`)
- **Provenance & Build Stamp:** Built by **Nixxes Software** on Crystal Dynamics' **Foundation Engine**. Per `tr2.arg` on the ISO, the internal executable is `IntermediateTR2.exe` (`v0.0.0.3`), build ID `491.10_2015-09-22_08-45@UTR-BUILD08`.
- **Single-Disc Asset Footprint (Verified from `Rise of the Tomb Raider.iso`):**
  - **Executable:** `default.xex` (`16.53 MB` on disc; `22.74 MB` unpacked in guest RAM at `0x82000000`–`0x835B0000`).
  - **Core Archives:** `bigfile.000.tiger` (`2,147,459,120` bytes) + `bigfile.001.tiger` (`130,651,255` bytes) + `bigfile.000.nfo` (`191` bytes).
  - **Localization Archives:** `bigfile_ENGLISH.000.tiger` (`855.2 MB`), `bigfile_FRENCH.000.tiger` (`788.1 MB`), `bigfile_LATAMSPANISH.000.tiger` (`785.9 MB`), `bigfile_DUTCH.000.tiger` (`375.9 KB`). *(Note: For an English-only install, stripping unused French/Spanish `.tiger` archives reduces disk footprint by ~1.57 GB!)*
  - **Pre-Rendered Cutscenes (`movies/*.bik`):** **62 Bink Video files** totaling `1.81 GB` (`1.69 GiB`), confirming Digital Foundry's observation that major cutscenes and level-load sequences (`LevelLoad_14Expedition.bik`, `LevelLoad_SH3.bik`, `LevelLoad_VH4.bik`) are pre-recorded videos.
  - **Built-in Engine Telemetry Flags (`tr2.arg`):** Notice that `tr2.arg` contains `-ARCHIVE -noassert -mainmenu -addLevelSelect=true -nosound=false -"GameMetrics/Record Game Metrics"=true -MetricsFPS=true`. The Architect should evaluate whether guest command-line arguments passed via `tr2.arg` or XAM launch data can expose the built-in level selector (`-addLevelSelect=true`) or FPS metrics (`-MetricsFPS=true`) for diagnostic testing!

### 3.2 CPU Recompilation Pipeline & Guest Kernel/XAM (`src/codegen/`, `src/kernel/`)
- **Impact of `D3D9LTCG` and MSVC `v16.0.11886.17408`:**
  - `default.xex` was compiled with Link-Time Code Generation (`D3D9LTCG`, `C1`/`C2` `v16.0.11886.17408`). LTCG performs whole-program cross-module inlining and frequently places cold error-handling blocks out-of-line past mid-function `blr` instructions.
  - Consequently, ReXGlue's `function_scanner.cpp` and `phase_gapfill.cpp` **must** include the `CrownParkComputing` out-of-line block lookup fix (`getFunctionContaining` falling back to the block list) and the `bctr` CTR-dispatch fallback so LTCG functions do not emit `REX_FATAL` or `__builtin_trap()`.
- **Self-Contained Import Surface:**
  - `default.xex` contains **zero** external game DLL imports — only `xboxkrnl.exe` (`311` records) and `xam.xex` (`230` records). Once decrypted, 100% of the game's PowerPC code (including statically linked `D3D9LTCG`, `XAUDIO2`, `XMP`, `XHV2`, `XONLINE`, Scaleform GFx, and Bink Video) lives inside this single `22.74 MB` image (`0x82000000`–`0x835B0000`).

### 3.3 GPU Translation: Xenos to Vulkan (`src/graphics/vulkan/`)
- Because `D3D9LTCG` is statically compiled into `default.xex`, all rendering flows through the Xenos PM4 ring buffer and EDRAM translation in `src/graphics/vulkan/`.
- On Intel HD Graphics 620, `render_target_path_vulkan` is forced to `"fbo"` (`Path::kHostRenderTargets`). Resolving `gpu-drawing-corrupt` and `gpu-readback` (Xenia Canary #174) requires auditing 3D LUT volume texture views (`VK_IMAGE_CREATE_2D_ARRAY_COMPATIBLE_BIT`), `exp_adjust` word-3 fetch bias, `k_8_8_8_8_GAMMA` RT storage, and EDRAM resolve readbacks.

### 3.4 Input Subsystem: SDL3 Host to XAM Guest (`src/input/`)
- ReXGlue `v0.10.0` / `bd833a2ab69d` uses **SDL3 (`3.4.14`)** (`src/input/sdl/sdl_input_driver.cpp`), bridging physical gamepads to guest `XamInputGetState` / `XamInputSetState` calls imported by `XAPILIB` (`v2.0.21256.16384`) inside `default.xex`.

### 3.5 Audio (`XAUDIO2` + `XMP`) and Video (`movies/*.bik`) Subsystems
- **Audio Verified via XEX2 Static Libraries (`XAUDIO2`, `XAPOBA`, `XMCORE`, `XMP`, `XMIC` v2.0.21256.16384):**
  - `default.xex` statically links **`XAUDIO2` (`v2.0.21256.16384`)**, `XAPOBA`, and **`XMP`** (Xbox Music Player).
  - Guest `XAUDIO2` decodes compressed voices via the Xbox 360 hardware XMA context registers (`src/audio/xma_register_file.cpp`, `xma_decoder.cpp`) and submits final mixed PCM frames to the audio driver (`src/audio/sdl/`).
  - As proven in `CrownParkComputing`, `audio_native_xma` must remain **OFF**, while `audio_pace_callback` (187.5 Hz paced schedule) and `xenia-canary` XMA ring-buffer starvation fixes must be active.
- **Video Verified via `movies/*.bik` (62 Files, 1.69 GiB):**
  - With 62 `.bik` movies on disc (including `LevelLoad_*.bik` videos played during level streaming), Bink Video decoding on guest PowerPC/VMX128 threads + XMA audio + Vulkan YCbCr texture presentation will run concurrently with background `.tiger` archive streaming! This reinforces why `WaitMultiple` blocking, `KeInsertQueueDpc` draining, and `db16cyc -> yield()` are critical so background level loads do not starve the Bink video decoder or deadlock during level transitions.

---

## 4. Intel HD Graphics 620 Assessment & Future Validation Plan

### 4.1 Driver & Hardware Constraint Matrix (Intel HD Graphics 620 — Kaby Lake GT2 / Gen9.5)

| Feature / Resource | Windows (Intel DCH Driver 31.0.101.21xx) | Linux (Mesa ANV 23.x–26.x) | Impact on ReXGlue Vulkan (`v0.10.0` / `bd833a2ab69d`) |
| :--- | :--- | :--- | :--- |
| **Max Vulkan API** | Vulkan 1.3 | Vulkan 1.3 | Meets `vulkan_device.cpp` >= 1.1/1.2/1.3 checks. |
| **Execution Units / Clock** | 24 EUs @ 300–1050 MHz (~384–403 GFLOPS FP32) | Same hardware | Modest ALU; heavy SPIR-V shaders (SSBO `vfetch` + format unpack) risk fillrate bottlenecks at 720p. |
| **Memory Bandwidth** | Shared System RAM (17 GB/s single-ch / 34 GB/s dual-ch) | Same hardware | **Primary bottleneck.** EDRAM resolve copies in `fbo` mode and CPU->GPU shared memory re-uploads compete directly for system RAM bandwidth. |
| **`fragmentStoresAndAtomics` & `vertexPipelineStoresAndAtomics`** | Supported (`true`) | Supported (`true`) | Passes ReXGlue hard parity check (`vulkan_device.cpp:112-125`). |
| **`VK_EXT_fragment_shader_interlock`** | **NOT SUPPORTED (`false`)** | **NOT SUPPORTED (`false`)** | **Forces `Path::kHostRenderTargets` (`fbo` path).** `fsi` path cannot be used on HD 620. |
| **Shader Compiler Stack** | Intel IGC (slower pipeline creation, stricter register pressure) | Mesa NIR + Intel BRW (faster compilation, superior barrier coalescing) | Seeded `.vk.xpso` pipeline cache (`shader_storage_seed_root`) is essential on both OSes. |

### 4.2 Practical Performance Validation Plan (Milestones M1–M6)
- **M1 — Compiles:** Decrypts `default.xex`, merges `.xexp` Title Update (Media ID `0A657B25`), runs `rexglue codegen`, and compiles `22.74 MB` guest image into native `x86-64` C++23 with Clang 18+.
- **M2 — Launches:** Initializes `ReXApp`, mounts single-disc VFS (`game:`, `cache:`, TU overlay), initializes Vulkan on HD 620 (`fbo` path), and enters `0x82B00790` (`EntryPoint`).
- **M3 — Renders Menu:** Plays/skips intro `.bik` movies, renders Scaleform main menu legibly (no magenta LUT corruption), responds to SDL3 gamepad input, and passes the Start screen.
- **M4 — Renders First Scene:** Plays `LevelLoad_*.bik` / `01_rockbottom_cine.bik` and renders the opening mountain/Syria prologue in 3D with `XAUDIO2` sound and camera control.
- **M5 — Playable:** Completes a 30-minute continuous playthrough across prologue + Siberian Wilderness hub with working saves, cutscenes, combat, and zero crashes.
- **M6 — Acceptable on Intel HD Graphics 620:** Sustains **<= 33.3 ms median frame time (30 FPS)** and **<= 40.0 ms P95** at 720p (or documented scale), **<= 120 render passes/frame**, and **<= 2.2 GB host RSS** across 15-minute thermal soak.

---

## 5. Deferred Android (`arm64-v8a`) Portability Assessment

**Status:** **STRICTLY BLOCKED / DEFERRED** until PC Milestones M1–M6 pass.  
All five Architecture-Preservation Rules (`AP-1` through `AP-5`: no raw x86 intrinsics outside `simde`, explicit `std::atomic` memory ordering, configurable VFS roots for future SAF provisioning, isolated fiber interface for Android Bionic, and Vulkan+SDL3-only stack) remain mandatory for the Phase 1 Architect. *(Note: The ISO's modular language `.tiger` files mean an Android user could provision only `bigfile.000.tiger`, `bigfile.001.tiger`, `bigfile_ENGLISH.000.tiger`, and `movies/`, saving ~1.57 GB of mobile storage).*

---

## 6. Project Legality, Provenance, and Distribution Constraints

1. **Local ISO Protection:** `Rise of the Tomb Raider.iso` is gitignored via `*.iso` in `.gitignore` and must never be committed or uploaded.
2. **Clean-Room Repository Boundary:** Only original research documentation, CMake build scripts, TOML manifests, and original C++ hook wrappers may reside in Git; `game/` and `generated/` (machine-translated C++ from `default.xex`) must remain local and gitignored.
