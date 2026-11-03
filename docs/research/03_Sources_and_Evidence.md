# Source Register and Evidence Provenance

**Project:** `FrostyPickaxe` — *Rise of the Tomb Raider* (Xbox 360, Title ID `53510823`)  
**Audit Date:** 2026-11-02  
**Author:** Gemini Argon (Medium Reasoning) — Phase 0 Researcher and Feasibility Analyst  

Each source and claim is classified into one of five strict provenance categories:
- **`LOCAL_OBSERVATION`**: Direct read-only observation of files/git state in `/mnt/6421-8598/building/FrostyPickaxe`.
- **`VERIFIED_UPSTREAM_SOURCE`**: Direct inspection of official upstream repository code, commits, or hardware vendor documentation.
- **`THIRD_PARTY_REPORT`**: Community compatibility reports, technical analyses (e.g., Digital Foundry, Xenia Canary issue tracker), or community ReXGlue port repositories.
- **`INFERENCE`**: Reasoned technical deduction combining verified SDK source behavior with documented game characteristics.
- **`UNKNOWN`**: Unverified fact requiring future inspection of user-supplied Xbox 360 binaries or hardware execution.

---

## 1. Local Workspace Evidence (`LOCAL_OBSERVATION`)

| ID | Local Path / Git Reference | Access Date | Classification | Verified Finding |
| :--- | :--- | :--- | :--- | :--- |
| **LOC-01** | `/mnt/6421-8598/building/FrostyPickaxe/.git` (`HEAD` at `fcee9855881d`, initial commit `aa6ccdfb0558`) | 2026-11-02 | `LOCAL_OBSERVATION` | Standalone game-port repository (`origin`: `https://github.com/RibhuNoodleBoodle/FrostyPickaxe`). Contains only `.gitignore` (`/*.txt`), a 2-line initial `README.md`, and the Phase 0 prompt text file. Zero game binaries, assets, submodules, or SDK files exist locally. |
| **LOC-02** | `/mnt/6421-8598/building/FrostyPickaxe/README.md` (pre-rewrite) | 2026-11-02 | `LOCAL_OBSERVATION` | Contained 2 lines: `# FrostyPickaxe` / `An attempt on Xbox 360 Recompilation port of Rise of the Tomb Raider for Xbox 360`. |

---

## 2. Official ReXGlue SDK Sources (`VERIFIED_UPSTREAM_SOURCE`)

| ID | URL / File Path & Pinned Revision | Access Date | Classification | Verified Finding & Conflict Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **REX-01** | `https://github.com/rexglue/rexglue-sdk` (`main` branch commit `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518`, tag `v0.10.0` at `f5337cdc947f`, 2026-08-21; `development` branch commit `bd833a2ab69d`, 2026-10-02) | 2026-11-02 | `VERIFIED_UPSTREAM_SOURCE` | Official Xbox 360 static recompilation toolkit and runtime (BSD 3-Clause License). Release `v0.10.0` is current stable; `development` (`bd833a2ab69d`, `nightly-20261002-bd833a2a`) is 24 commits ahead with critical codegen (`stwcx.` atomic CAS, `sync`/`lwsync`/`eieio` fences, `vpkuwus` aliasing) and SDL3 (`3.4.14`) updates. |
| **REX-02** | `https://github.com/rexglue/rexglue-sdk/blob/main/CMakeLists.txt` (lines 10–11, 35–46, 88–104) at commit `c94f5ebdcb3c` | 2026-11-02 | `VERIFIED_UPSTREAM_SOURCE` | Project version `0.10.0`. Requires Clang >= 18.0 (or AppleClang >= 16.0), 64-bit host (`x86_64` or `ARM64`), and C++23 (`CMAKE_CXX_STANDARD 23`). **Critical OS Difference:** On `WIN32`, `REXGLUE_USE_D3D12` defaults to `ON` and `REXGLUE_USE_VULKAN` defaults to `OFF`. On non-Windows (`else()`), `REXGLUE_USE_D3D12` is `OFF` and `REXGLUE_USE_VULKAN` defaults to `ON`. |
| **REX-03** | `https://github.com/rexglue/rexglue-sdk/blob/main/.gitmodules` & `thirdparty/sdl3` at commit `c94f5ebdcb3c` and `bd833a2ab69d` | 2026-11-02 | `VERIFIED_UPSTREAM_SOURCE` | Upstream integrates **SDL3** (`https://github.com/libsdl-org/SDL`, branch `release-3.4.x`, submodule commit `8bf3b7215ad9` in `v0.10.0`, bumped to `3.4.14` in `4c1350847`). Uses SDL3 for windowing (`window_sdl.cpp`), audio (`src/audio/sdl/`), and gamepad input (`src/input/sdl/sdl_input_driver.cpp`). |
| **REX-04** | `https://github.com/rexglue/rexglue-sdk/blob/main/src/ui/vulkan/vulkan_device.cpp` (lines 26–42, 96–138, 175–260) at commit `c94f5ebdcb3c` | 2026-11-02 | `VERIFIED_UPSTREAM_SOURCE` | `VulkanDevice::CreateIfSupported` hard-requires `independentBlend`, `fragmentStoresAndAtomics`, and `vertexPipelineStoresAndAtomics` ( plus `geometryShader` and `fillModeNonSolid` by default CVar). Requests `VK_EXT_fragment_shader_interlock`, `VK_KHR_dynamic_rendering`, `VK_EXT_shader_stencil_export`, `VK_EXT_custom_border_color`, `VK_EXT_robustness2`, `VK_KHR_sampler_ycbcr_conversion`, and `VK_KHR_spirv_1_4` when supported. |
| **REX-05** | `https://github.com/rexglue/rexglue-sdk/blob/main/src/graphics/vulkan/render_target_cache.cpp` (lines 40–62, 203–240, 296–330) & `command_processor.cpp` (lines 50–70) at commit `c94f5ebdcb3c` | 2026-11-02 | `VERIFIED_UPSTREAM_SOURCE` | Defines `render_target_path_vulkan` (`"fbo"` / `Path::kHostRenderTargets` by default, or `"fsi"` / `Path::kPixelShaderInterlock`). If `fragmentShaderSampleInterlock` / `PixelInterlock` is unsupported, forces `Path::kHostRenderTargets`. If 16-bit host RT formats (`R16G16`, `R16G16B16A16`, `R16G16B16A16_UNORM`) fail in `fbo` mode and `fsi` is unavailable, initialization fails with `REXGPU_ERROR`. |
| **REX-06** | `https://github.com/rexglue/rexglue-sdk/wiki` (`Home.md`, `Getting-Started.md`, `Runtime-Architecture-Overview.md`, `Codegen-Pipeline-Overview.md`, `rexglue-CLI-Configuration-File.md`) at wiki commit `ebc5cc8534cd` (2026-06-04) | 2026-11-02 | `VERIFIED_UPSTREAM_SOURCE` *(With Documented Version Conflict)* | **Conflict Identified & Resolved:** Wiki `Home.md` claims `"Status: v0.3.x (active development)... Graphics, audio, and input backends are in flux."` This is an outdated wiki text artifact from early 2026; the actual SDK repository is at **`v0.10.0` (2026-08-21) / `0.10.0.24-dev` (2026-10-02)** with 38,305 lines of Vulkan/D3D12 graphics implementation. Wiki pipeline descriptions (`Codegen-Pipeline-Overview.md`, `Runtime-Architecture-Overview.md`) remain structurally valid. |

---

## 3. Hardware & Driver Documentation (`VERIFIED_UPSTREAM_SOURCE`)

| ID | URL / Document Reference | Access Date | Classification | Verified Finding |
| :--- | :--- | :--- | :--- | :--- |
| **HW-01** | Intel Official Support Article `000005524`: *Supported APIs for Intel® Graphics* (`https://www.intel.com/content/www/us/en/support/articles/000005524/graphics.html`) | 2026-11-02 | `VERIFIED_UPSTREAM_SOURCE` | Confirms **Intel® HD Graphics 620** (7th Gen Intel Core / Kaby Lake) officially supports **DirectX 12, OpenGL 4.6, OpenCL 2.0, and Vulkan 1.3** on up-to-date drivers (Windows Intel DCH 7th–10th Gen branch and Linux Mesa ANV). |
| **HW-02** | Khronos / Vulkan Hardware Capability Database (`https://vulkan.gpuinfo.org`) & Mesa ANV Gen9.5 Feature Matrix for Intel HD Graphics 620 (Kaby Lake GT2) | 2026-11-02 | `VERIFIED_UPSTREAM_SOURCE` | Confirms Intel HD Graphics 620 exposes `independentBlend`, `fragmentStoresAndAtomics`, `vertexPipelineStoresAndAtomics`, `geometryShader`, and `fillModeNonSolid`, **but does NOT expose `VK_EXT_fragment_shader_interlock`** (`fragmentShaderSampleInterlock` / `fragmentShaderPixelInterlock`). |

---

## 4. Target Game & Community Precedent Sources (`THIRD_PARTY_REPORT`)

| ID | URL / Source Reference | Access Date | Classification | Verified Finding & Caveats |
| :--- | :--- | :--- | :--- | :--- |
| **GAME-01** | Digital Foundry Technical Analysis: *Rise of the Tomb Raider Xbox 360 Face-Off / Analysis* (Nov 2015) | 2026-11-02 | `THIRD_PARTY_REPORT` | Confirms Xbox 360 version was developed by **Nixxes Software** on Crystal Dynamics' **Foundation Engine**. Renders natively at **1280x720 (720p)** with FXAA targeting **30 FPS** inside 512 MB RAM (~6.23 GB total size across 2 discs). Major real-time cutscenes from Xbox One were replaced with **pre-recorded video files** on Xbox 360. |
| **GAME-02** | Xenia Canary Game Compatibility Tracker Issue #174: `53510823 - Rise of the Tomb Raider` (`https://github.com/xenia-canary/game-compatibility/issues/174`) & Xenia Project Issue #247 (`https://github.com/xenia-project/game-compatibility/issues/247`) | 2026-11-02 | `THIRD_PARTY_REPORT` | Confirms Title ID is **`53510823`**. Labels on #174 (updated 2026-06-23): `state-gameplay`, `gpu-drawing-corrupt`, `gpu-readback`, `tech-middleware-scaleform`, `backwards-compatibility-unsupported`. Unpatched base game hangs on infinite loading after pressing Start and exhibits purple/magenta color corruption on the title screen. Comment by `has207` (2026-05-08): *"Needs TU to get in game, but there are severe rendering issues but I managed to get through the prologue at least."* |
| **GAME-03** | Xbox 360 Retail Multi-Disc Structure Reports for *Rise of the Tomb Raider* (`53510823`) | 2026-11-02 | `THIRD_PARTY_REPORT` | Confirms 2-disc retail distribution: **Disc 1 (Install Disc)** installs mandatory content into `Content\0000000000000000\53510823\00000002\`; **Disc 2 (Play Disc)** contains `default.xex` and main game archives. |
| **PREC-01** | `https://github.com/CrownParkComputing/Xbox360-Native-Ports` (`README.md` and `docs/REXGLUE_FORK_CHANGES.md`, commit `2675c16edd4b`, 2026-09-23) | 2026-11-02 | `THIRD_PARTY_REPORT` | Methodological precedent (~25 retail/XBLA titles built on a fork 97 commits ahead of ReXGlue `v0.10.0`). Documents critical upstream `v0.10.0` bugs (`KeInsertQueueDpc` no-op, `WaitMultiple` polling, `db16cyc` spin-loops, `bctr` fall-through traps, 3D-as-2D LUT texture bug, `exp_adjust` word 3 fix, shared-memory write-watch storms causing 2.5 FPS on MCLA until hot-page batching, and Android Bionic `ucontext` fiber refusal). **Caveat:** Precedent only; does not include *Rise of the Tomb Raider*. |
| **PREC-02** | `https://github.com/deivid22srk/hells-gate-recomp-android` (`README.md` and `patches/`, commit `0a79f938ab83`, 2026-09-08) | 2026-11-02 | `THIRD_PARTY_REPORT` | Methodological precedent for *Dante's Inferno* on Android (`arm64-v8a`) using ReXGlue `v0.10.0` + SDL3 + Vulkan. Required 228 KB of custom SDK patches (`patches/sdk/rexglue-sdk-v0.10.0*.patch`) and abandoned the experimental `rexgpu-native` renderer in commit `0a79f938ab83`. Confirms Android is not supported turnkey upstream. |

---

## 5. Register of Inferences and Unknowns (`INFERENCE` / `UNKNOWN`)

| ID | Topic | Classification | Statement |
| :--- | :--- | :--- | :--- |
| **INF-01** | Purple/Magenta Title Screen Corruption in `53510823` | `INFERENCE` | Highly likely caused by Xenos 3D color-grading LUT volume textures sampled via 2D fetch instructions or `exp_adjust` fetch-constant exponent bias miscalculation (both documented in `PREC-01` as breaking color grading in other 360 titles on ReXGlue `v0.10.0`), combined with `k_8_8_8_8_GAMMA` piecewise linear ramp handling. Requires verification via `EXP-05`. |
| **UNK-01** | Binary-Specific XEX2 & `.xexp` Metrics for `53510823` | `UNKNOWN` | Exact function count, `.pdata` coverage, import ordinal list, section encryption/compression flags, and `.xexp` delta-patch layout of *Rise of the Tomb Raider* (`53510823`) are **UNKNOWN** until a user-owned copy of Disc 1, Disc 2, and the Title Update is inspected locally in a future phase. |
| **UNK-02** | Measured Frame Rate & Memory Usage on Intel HD 620 | `UNKNOWN` | Zero runtime benchmarks exist for `53510823` on ReXGlue or Intel HD Graphics 620. All frame-time numbers in `01_Feasibility_Report.md` and `02_Risks_Unknowns_and_Gates.md` are **target engineering budgets**, not measured results. |
| **UNK-03** | Guest Fiber Usage (`CreateFiber`) in `53510823` | `UNKNOWN` | Whether Nixxes's Xbox 360 build of Foundation Engine imports and executes `CreateFiber` / `SwitchToFiber` is **UNKNOWN** until XEX symbol/import analysis (`EXP-01`), directly impacting future Android Bionic portability. |
