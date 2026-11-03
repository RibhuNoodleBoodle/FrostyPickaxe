# Ranked Blockers, Unknowns, Falsifiable Experiments, and Decision Gates

**Project:** `FrostyPickaxe` — *Rise of the Tomb Raider* (Xbox 360, Title ID `53510823`)  
**Date:** 2026-11-02  
**Author:** Gemini Argon (Medium Reasoning) — Phase 0 Researcher and Feasibility Analyst  
**Scope Note:** This document contains *conceptual experiment specifications and pass/fail gates only*. No runnable commands, scripts, patches, or code are included in this Phase 0 deliverable.

---

## 1. Ranked Technical Blockers and Unknowns

| Rank | ID | Blocker / Unknown | Severity | Subsystem | Current Evidence Status | Confidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **BLK-01** | **Mandatory Title Update (`.xexp`) Pre-Application for Static Codegen** | **Critical** | Codegen / XEX Loader | Xenia Canary Issue #174 confirms base `default.xex` (`53510823`) hangs in an infinite loading loop after pressing Start without a Title Update (TU). Unlike dynamic emulators that patch XEX pages in RAM, static recompilation (`rexglue codegen`) requires a statically merged XEX binary (`default.xex` + `.xexp` delta patch) before C++ generation. | **High** |
| **2** | **BLK-02** | **Intel HD 620 Lacks `VK_EXT_fragment_shader_interlock` (Forced `fbo` Path)** | **Critical** | GPU / Vulkan (`render_target_cache.cpp`) | Verified via `vulkan.gpuinfo.org` and ReXGlue `src/graphics/vulkan/render_target_cache.cpp:203-238`. Intel Gen9.5 (HD 620) does not support fragment shader interlock (`fsi`), forcing `Path::kHostRenderTargets` (`fbo`). If `53510823` relies on incompatible EDRAM tile aliasing or unsupported 16-bit RT formats that cannot be emulated in `fbo` mode, rendering will fail or abort initialization. | **High** |
| **3** | **BLK-03** | **Title-Specific Xenos Rendering Corruption (`gpu-drawing-corrupt` & `gpu-readback`)** | **High** | GPU / Vulkan (`shader.cpp`, `texture_cache.cpp`) | Xenia Canary Issue #174 and Xenia #247 document purple/magenta color corruption on the title screen and severe rendering corruption in the prologue, plus `gpu-readback` dependency. High likelihood of 3D color-grading LUT volume textures sampled via 2D fetch constants, `exp_adjust` exponent bias bug, or EDRAM resolve readbacks. | **High** |
| **4** | **BLK-04** | **Upstream ReXGlue v0.10.0 Kernel & Threading Defects (`KeInsertQueueDpc`, `WaitMultiple`, `db16cyc`, FP Unmasking)** | **High** | Guest Kernel / Threading (`src/kernel/`, `src/core/`) | Verified from `CrownParkComputing/Xbox360-Native-Ports` (`docs/REXGLUE_FORK_CHANGES.md`): upstream `v0.10.0` drops queued DPCs (`KeInsertQueueDpc`), busy-polls `WaitMultiple` with non-FIFO auto-reset event wakes, ignores `db16cyc` spin hints, and unmasks host FP exceptions (`SIGFPE`) on non-`XThread` host threads. | **High** |
| **5** | **BLK-05** | **Shared-Memory Write-Watch & Render-Pass Break Storm on Streaming Engines** | **High** | GPU / Memory (`shared_memory.cpp`) | Foundation Engine continuously streams `.tiger` archives into 512 MB unified memory. On stock ReXGlue `v0.10.0`, page write-watches trigger hundreds of render-pass breaks per frame and >100 MB/s of redundant re-uploads, crippling 2-core Intel HD 620 systems. | **High** |
| **6** | **BLK-06** | **Multi-Disc (Disc 1 Content + Disc 2 Play Disc) & Writable `cache:` VFS Topology** | **High** | Filesystem / XAM (`src/filesystem/`, `src/kernel/xam/`) | Retail Xbox 360 *Rise of the Tomb Raider* splits mandatory assets across Disc 1 (`Content\0000000000000000\53510823\00000002\` STFS package) and Disc 2 (`default.xex` + `.tiger` archives). Both must be mounted simultaneously alongside a writable `cache:` partition. | **High** |
| **7** | **BLK-07** | **Scaleform GFx & Foundation Engine Indirect Jump Tables (`bctr`) & Exceptions** | **Medium-High** | Codegen (`function_scanner.cpp`) | Tagged `tech-middleware-scaleform` in Xenia Canary #174. Unrecovered `bctr` switch tables emit `__builtin_trap()` in stock `v0.10.0`, and C++ exceptions / `setjmp` require exact manifest configuration. | **Medium** |
| **8** | **BLK-08** | **Windows Vulkan CMake Default (`REXGLUE_USE_VULKAN=OFF`) & Input Mutex Race** | **Medium** | Build / Input (`CMakeLists.txt`, `input_system.cpp`) | Upstream `CMakeLists.txt:37-43` disables Vulkan by default on Windows (`D3D12=ON`). Upstream `InputSystem` lacks recursive mutex serialization between guest `XamInput*` calls and UI-thread SDL3 device refreshes. | **High** |
| **9** | **BLK-09** | **Deferred Android Blockers (`ucontext` Fibers, Bionic Gaps, Mobile TBDR Vulkan)** | **High (Deferred)** | Android Platform (`fiber_posix.cpp`) | Android Bionic lacks `<ucontext.h>` (refusing guest fibers), upstream `rexglue-sdk` lacks Android CMake/APK tooling, and mobile TBDR GPUs choke on mid-pass buffer uploads. Strictly blocked until PC succeeds. | **High** |

---

## 2. Prerequisites Before Architectural Execution Can Advance to Codegen

1. **User-Owned Game Media Acquisition (Local, Private, Gitignored):**
   - Legally obtained Xbox 360 Disc 1 (Install Disc) and Disc 2 (Play Disc) of *Rise of the Tomb Raider* (Title ID `53510823`).
   - Legally obtained latest Xbox 360 Title Update (TU) package for Title ID `53510823` (containing the `.xexp` patch and updated `.tiger`/manifest data).
2. **Pinned ReXGlue SDK Baseline:**
   - Upstream `rexglue/rexglue-sdk` pinned at or after `development` commit `bd833a2ab69d` (2026-10-02), audited against the specific runtime/GPU fixes documented in `01_Feasibility_Report.md`.
3. **Host Hardware & Driver Baseline for PC Gate:**
   - x86-64 PC with Clang 18+, CMake 3.25+, Ninja, Vulkan 1.3 SDK, and an **Intel HD Graphics 620** validation target (tested separately on Linux Mesa ANV and Windows Intel DCH 31.0.101.21xx drivers).

---

## 3. Falsifiable Experiments to be Designed by Gemini Argon (Next Phase)

In Phase 1 (Architectural Discovery), the **Gemini Argon Principal Software Architect** must design the following six falsifiable experiments (at design level first, executed only after user authorization):

### Experiment EXP-01: XEX2 + `.xexp` (Title Update) Static Inspection & Merge Audit
- **Objective:** Verify whether `default.xex` (Disc 2) and the Title Update `.xexp` patch for `53510823` can be merged offline into a single valid, unencrypted, uncompressed XEX2/PE image suitable for `rexglue codegen`, and inventory all imported kernel/XAM ordinals, code sections, and `.pdata` records.
- **Required Inputs:** User-supplied `default.xex` and TU package (local read-only inspection).
- **Observable Pass/Fail Criterion:**
  - **PASS:** Merged XEX2 header validates; 100% of executable sections are statically visible (no runtime-decrypted overlays or self-modifying heap code); missing kernel/XAM imports in ReXGlue are <= 15 ordinals and none require undocumented hardware security processors.
  - **FAIL:** Title relies on encrypted runtime overlays, dynamic XEX module loading without static `.pdata`, or Scaleform JIT code generation that cannot be translated ahead of time.

### Experiment EXP-02: Codegen Control-Flow & Jump-Table Completeness Audit
- **Objective:** Determine how many functions in `53510823` fail automatic boundary detection, contain out-of-line blocks past a mid-function `blr`, or contain unresolved `bctr` switch tables.
- **Observable Pass/Fail Criterion:**
  - **PASS:** With `bctr` CTR-dispatch fallback enabled and manifest `[[switch_tables]]` / `[entrypoint.functions]` overrides configured, `rexglue codegen` produces C++23 partitions that compile cleanly under Clang 18+ with zero unresolved symbol references.
  - **FAIL:** Codegen encounters systemic control-flow obfuscation or thousands of unrecoverable indirect branches that prevent deterministic C++ emission.

### Experiment EXP-03: Multi-Disc VFS + Title Update + `cache:` Boot & Start-Screen Gate
- **Objective:** Validate whether mounting Disc 2 (`game:`), Disc 1 mandatory install content (`Content\0000000000000000\53510823\00000002\`), the Title Update content directory, and a writable `cache:` directory allows the recompiled binary (with `KeInsertQueueDpc` and `WaitMultiple` fixes) to pass the Start-screen infinite loading spin reported in Xenia Canary Issue #174.
- **Observable Pass/Fail Criterion:**
  - **PASS:** Title boots to the Scaleform main menu, accepts SDL3 Start button input, loads the initial profile/configuration without hanging, and transitions into the New Game prologue loading sequence.
  - **FAIL:** Title deadlocks on an unimplemented XAM/kernel synchronization primitive or content-enumeration check even with Disc 1 + TU mounted and DPC draining enabled.

### Experiment EXP-04: Intel HD Graphics 620 Vulkan `fbo` Render-Target Initialization Test
- **Objective:** Verify that `VulkanDevice` and `VulkanRenderTargetCache` initialize cleanly on Intel HD Graphics 620 (where `VK_EXT_fragment_shader_interlock` is absent and `Path::kHostRenderTargets` / `fbo` is forced) on both Linux Mesa ANV and Windows Intel DCH drivers.
- **Observable Pass/Fail Criterion:**
  - **PASS:** `VulkanRenderTargetCache` initializes in `fbo` mode without failing the `R16G16` / `R16G16B16A16` / `R16G16B16A16_UNORM` format checks (`render_target_cache.cpp:300-330`), and creates swapchain + render passes without validation errors or `VK_ERROR_INCOMPATIBLE_DRIVER`.
  - **FAIL:** Required Xbox 360 EDRAM render target formats used by `53510823` are rejected by HD 620 in `fbo` mode and have no lossless/acceptable host format substitute.

### Experiment EXP-05: Xenos Shader, 3D LUT (`gpu-drawing-corrupt`), and Readback (`gpu-readback`) Isolation
- **Objective:** Isolate the root cause of the purple/magenta title-screen corruption and prologue rendering artifacts in `53510823`, and test whether the game requires `vulkan_readback_resolve` or `vulkan_readback_memexport`.
- **Observable Pass/Fail Criterion:**
  - **PASS:** Applying the 3D-as-2D volume texture view wrapper (`VK_IMAGE_CREATE_2D_ARRAY_COMPATIBLE_BIT`), `exp_adjust` word-3 fetch fix, and gamma RT tuning eliminates the magenta corruption and renders the Syria/Siberia prologue accurately; any required EDRAM readback is either unnecessary for gameplay or executes asynchronously within frame budget.
  - **FAIL:** Accurate rendering requires per-sample `VK_EXT_fragment_shader_interlock` (`fsi`) EDRAM byte aliasing that is physically impossible on Intel HD 620's `fbo` pipeline.

### Experiment EXP-06: Intel HD 620 Frame-Time, Shared-Memory Residency, and Thermal Gate
- **Objective:** Measure CPU and GPU frame-time distributions across the four representative scenes (Menu, Bink Cutscene, Syria Prologue, Siberian Wilderness Hub) on Intel HD Graphics 620 with hot-page residency batching (`gpu_hot_page_frames`) and dynamic constant buffers enabled.
- **Observable Pass/Fail Criterion:**
  - **PASS:** Sustained median frame time **<= 33.3 ms (>= 30 FPS)** and P95 **<= 40.0 ms** at 720p (or documented resolution scale), with <= 120 render passes/frame and <= 2.2 GB host RSS.
  - **FAIL:** Sustained median frame time **> 50.0 ms (< 20 FPS)** on HD 620 after exhausting CPU/residency/shader cache optimizations.

---

## 4. Sequential Decision and Stop Gates

```
[Phase 0: Research Complete (Current)]
       │
       ▼
[Gate G0: Proceed to Phase 1 Gemini Argon Architecture Session]
  - Condition: Deliverables 00..03, 4 Argon prompts, and honest README verified.
  - Rule: Architect produces System Architecture & Discovery Plan ONLY (no coding).
       │
       ▼
[Gate G1: Binary & Title Update Availability Gate (STOP IF ABSENT)]
  - Condition: User provides lawful local copy of Disc 1 Content + Disc 2 default.xex + TU (Title ID 53510823).
  - STOP CONDITION: If binaries or TU are unavailable, halt at design level; do not fabricate codegen results.
       │
       ▼
[Gate G2: Static Recompilation & Kernel Bring-Up Gate (EXP-01, EXP-02, EXP-03)]
  - Condition: Merged XEX + TU compiles via ReXGlue + Clang 18+ and passes Start screen into prologue load.
  - STOP CONDITION: Unresolvable runtime code encryption/JIT or unfixable kernel deadlock.
       │
       ▼
[Gate G3: Vulkan Visual Correctness Gate on `fbo` Path (EXP-04, EXP-05)]
  - Condition: Renders menu and prologue in `Path::kHostRenderTargets` (`fbo`) without magenta LUT corruption or device loss.
  - STOP CONDITION: Game strictly requires `VK_EXT_fragment_shader_interlock` (`fsi`) unsupported by Intel HD 620.
       │
       ▼
[Gate G4: Intel HD Graphics 620 Performance Gate (EXP-06)]
  - Condition: Meets M6 budget (<= 33.3 ms median / >= 30 FPS, <= 2.2 GB RAM, 15-min thermal stability).
  - STOP CONDITION: Hardware bandwidth/EU ceiling prevents playable frame rates (< 20 FPS) on HD 620.
       │
       ▼
[Gate G5: Deferred Android ARM64 Unfreeze Gate]
  - Condition: Gates G1–G4 PASSED on PC x86-64 AND guest fiber usage (`CreateFiber`) audited for Bionic ARM64 switcher.
```
