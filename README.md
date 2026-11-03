# FrostyPickaxe: *Rise of the Tomb Raider* (Xbox 360) — Native Recompilation Research

> **CURRENT PROJECT STATUS: `PHASE 0 — RESEARCH & FEASIBILITY ANALYSIS ONLY`**  
> **No working port, compiled binary, bootable build, rendered scene, benchmark, or Android build exists in this repository.**  
> This repository currently contains **only** technical feasibility research, risk/blocker audits, source provenance records, and architectural handoff prompts for the next engineering phase.

---

## 1. Project Overview & Target Distinction

**FrostyPickaxe** is an independent technical research and engineering study investigating whether the **Xbox 360 release of *Rise of the Tomb Raider*** (Title ID `53510823`, released November 2015, developed by Nixxes Software and Crystal Dynamics on the Foundation Engine) can be statically recompiled ahead-of-time (AOT) from PowerPC (`default.xex`) into native `x86-64` C++23 using the [ReXGlue SDK](https://github.com/rexglue/rexglue-sdk), rendered via **Vulkan**, and controlled via **SDL3**.

### Why the Xbox 360 Release (and NOT the Native PC Edition)?
- **Explicit Source Target:** This project exclusively targets the **Xbox 360 version (`53510823`)** and its Xbox 360 executable/assets. It does **not** use, modify, or repackage the existing commercial PC, Xbox One, or PlayStation 4 releases.
- **Core Research Hypothesis:** Whereas the commercial PC release is a high-fidelity DirectX 11/12 build (20–35 GB of assets) designed for stronger GPUs, Nixxes Software engineered the Xbox 360 edition specifically to run at `1280x720` (720p) with FXAA at 30 FPS inside **512 MB of unified RAM** and **10 MB Xenos EDRAM** (~6.23 GB across 2 DVDs, using simplified geometry, pared-back post-processing, and pre-recorded video cutscenes). This project investigates the **hypothesis** that a native static recompilation of the lighter Xbox 360 workload — paired with a well-tuned Vulkan backend — could run playably on modest integrated PC hardware such as the **Intel HD Graphics 620**. This remains an **unproven hypothesis** until benchmarked.

---

## 2. Target Priorities (Mandatory Sequence)

1. **Primary Target (Gate 1 — Active Research Focus):**
   - **Platform:** Native PC `x86-64` (Windows 10/11 and Linux `x86-64` evaluated separately where driver and SDK defaults diverge).
   - **Minimum Target GPU Baseline:** **Intel HD Graphics 620** (Kaby Lake GT2, Gen9.5 architecture, 24 Execution Units, shared host DDR3/DDR4 memory, Vulkan 1.3).
   - **Core Stack:** ReXGlue SDK (`v0.10.0` / `development` commit `bd833a2ab69d`), Vulkan graphics backend (`src/graphics/vulkan/`), and SDL3 (`3.4.14`) controller abstraction (`src/input/sdl/`).
2. **Deferred Target (Strictly Blocked Pending PC Viability):**
   - **Platform:** Android `arm64-v8a` with Vulkan and SDL3 gamepad/touch integration.
   - **Status:** **DEFERRED / CURRENTLY BLOCKED.** Zero Android development will occur unless and until PC runtime compatibility, visual correctness, and Intel HD Graphics 620 performance gates pass. Architectural portability requirements are recorded now solely so PC design choices do not block Android later.

---

## 3. Summary of Phase 0 Findings: Confirmed Facts vs. Hypotheses vs. Unknowns

For full evidence citations, commit SHAs, and falsifiable pass/fail criteria, consult [`docs/research/01_Feasibility_Report.md`](docs/research/01_Feasibility_Report.md).

### Confirmed Facts (Verified from Sources & SDK Code)
- **Target Title Multi-Disc & Title Update Requirement:** Retail Xbox 360 *Rise of the Tomb Raider* (`53510823`) shipped across **two discs** (~6.23 GB total): **Disc 1 (Mandatory Install Disc)** installs STFS content packages into `Content\0000000000000000\53510823\00000002\`, and **Disc 2 (Play Disc)** holds `default.xex` and the primary `.tiger` archives. Compatibility reports from [Xenia Canary Issue #174](https://github.com/xenia-canary/game-compatibility/issues/174) confirm that the unpatched base game hangs in an infinite loading loop after pressing Start and **requires a Title Update (TU)** to enter gameplay.
- **Known Xenos GPU & Middleware Hazards:** In Xenia Canary (#174), Title `53510823` is tagged `gpu-drawing-corrupt`, `gpu-readback`, and `tech-middleware-scaleform`, exhibiting purple/magenta color corruption on the title screen and severe rendering corruption in the prologue.
- **ReXGlue SDK State (`v0.10.0` / `bd833a2ab69d`):**
  - Upstream `rexglue-sdk` is at `v0.10.0` (`c94f5ebdcb3c`, 2026-08-21) with `development` at `bd833a2ab69d` (`0.10.0.24-dev`, 2026-10-02). *(Note: The upstream wiki `Home.md` contains a stale `"v0.3.x"` banner that is outdated relative to the `v0.10.0` source tree).*
  - Integrates **SDL3 (`3.4.14`)** and a 38.3k-LOC Xenia-derived Vulkan/D3D12 Xenos translator (`src/graphics/vulkan/`).
  - On Windows (`WIN32`), `CMakeLists.txt` defaults to `REXGLUE_USE_D3D12=ON` and **`REXGLUE_USE_VULKAN=OFF`**; on Linux, `REXGLUE_USE_VULKAN=ON` is default. Windows builds must explicitly pass `-DREXGLUE_USE_VULKAN=ON`.
- **Intel HD Graphics 620 Hardware Gate:**
  - Supports **Vulkan 1.3** (Intel Support Article `000005524` & Mesa ANV) and passes ReXGlue's hard feature checks (`independentBlend`, `fragmentStoresAndAtomics`, `vertexPipelineStoresAndAtomics`).
  - **Does NOT support `VK_EXT_fragment_shader_interlock` (`fsi`)**, forcing ReXGlue's Vulkan backend onto the host framebuffer path (`Path::kHostRenderTargets` / `render_target_path_vulkan = "fbo"`).

### Core Hypotheses (To Be Tested in Future Phases)
- **H1 (Visual Fix Hypothesis):** That the purple/magenta corruption (`gpu-drawing-corrupt`) in `53510823` is caused by Xenos 3D volume color-grading LUT textures sampled via 2D fetch instructions, `exp_adjust` exponent bias offsets, and `k_8_8_8_8_GAMMA` EDRAM resolve handling — all fixable within the `fbo` render-target path without needing `VK_EXT_fragment_shader_interlock`.
- **H2 (HD 620 Performance Hypothesis):** That applying shared-memory hot-page upload batching (`gpu_hot_page_frames`), dynamic uniform buffers (`vulkan_dynamic_constant_buffers`), descriptor caching, and `db16cyc -> yield()` lowering will prevent CPU/write-watch stalls and allow the 720p Xbox 360 workload to sustain 30 FPS on an Intel HD Graphics 620 laptop.

### Critical Unknowns (`UNKNOWN` Until Local Binary & Hardware Inspection)
- **`UNK-01` (Binary Metrics):** Exact function count, `.pdata` exception coverage, imported kernel/XAM ordinals, `bctr` switch table recovery rate, and offline `.xexp` Title Update merge behavior for `53510823` are **`UNKNOWN`** because no game binaries exist in this repository.
- **`UNK-02` (Measured Performance):** Actual frame times, CPU/GPU bottlenecks, and RAM usage on Intel HD Graphics 620 are **`UNKNOWN`** (zero benchmarks have been run).
- **`UNK-03` (Guest Fibers):** Whether `53510823` calls Xbox 360 guest fibers (`CreateFiber` / `SwitchToFiber`) — which currently fail on Android Bionic due to missing `<ucontext.h>` — is **`UNKNOWN`** until XEX import analysis.

---

## 4. Current Blockers & Next Stage (Gemini Argon Architectural Discovery)

### Top Current Blockers
1. **[Critical] `BLK-01` — Offline Title Update (`.xexp`) Pre-Application:** Base `default.xex` hangs after pressing Start without a Title Update; static AOT recompilation requires merging the `.xexp` patch into `default.xex` prior to `rexglue codegen` (plus local user provisioning of Disc 1, Disc 2, and TU files).
2. **[Critical] `BLK-02` — Forced Vulkan `fbo` Path on Intel HD 620:** Because Intel HD Graphics 620 lacks `VK_EXT_fragment_shader_interlock`, all Xenos EDRAM rendering for `53510823` must work accurately in `Path::kHostRenderTargets` (`fbo`) mode.
3. **[High] `BLK-03` / `BLK-04` / `BLK-05` — Xenos Shader Corruption, Kernel DPC/Wait Bugs, & Shared-Memory Streaming Storms:** Upstream ReXGlue `v0.10.0` requires targeted fixes for `KeInsertQueueDpc` draining, `WaitMultiple` FIFO blocking, `db16cyc` spin yields, 3D-as-2D LUT texture views, `gpu-readback` handling, and shared-memory hot-page batching.

### Next Stage
The next stage of this project is **Phase 1: Architectural Discovery** conducted by a separate **Gemini Argon (Principal Software Architect)** session using the prompts in [`gemini_argon/`](gemini_argon/), beginning with [`gemini_argon/Gemini_Argon_04_Architecture_Handoff.txt`](gemini_argon/Gemini_Argon_04_Architecture_Handoff.txt).

---

## 5. Repository Layout & Research Documentation

What actually exists in this repository right now:

```text
FrostyPickaxe/
├── README.md                                        # Honest project status & navigation (this file)
├── .gitignore                                       # Ignores root-level .txt prompt inputs
├── docs/
│   └── research/
│       ├── 00_Repository_State.md                   # Repo inventory, pinned SDK revisions, provenance rules
│       ├── 01_Feasibility_Report.md                 # Full falsifiable verdicts, CPU/GPU/HD 620/Android analysis
│       ├── 02_Risks_Unknowns_and_Gates.md           # Ranked blockers, EXP-01..06 specs, Gates G0..G5
│       └── 03_Sources_and_Evidence.md               # Verified source register & wiki/source conflict audit
└── gemini_argon/
    ├── Gemini_Argon_01_Personality.txt              # Phase 1 Architect identity & no-coding mandate
    ├── Gemini_Argon_02_Scope.txt                    # Phase 1 Architect scope, targets, and exclusions
    ├── Gemini_Argon_03_Skills.txt                   # Phase 1 Architect required skill domains & checks
    └── Gemini_Argon_04_Architecture_Handoff.txt     # Master entry-point prompt for Phase 1 Architect session
```

---

## 6. Legal, Clean-Room Provenance, and Non-Affiliation Notice

- **Non-Affiliation:** `FrostyPickaxe` is an independent, non-commercial technical research project. It is **not** affiliated with, endorsed by, authorized by, or sponsored by Microsoft Corporation, Square Enix, Crystal Dynamics, Eidos-Montréal, or Nixxes Software. All trademarks and copyrights belong to their respective owners.
- **No Copyrighted Game Assets or Binaries:** This repository contains **zero** Xbox 360 executables (`.xex`, `.xexp`), game archives (`.tiger`), shaders, audio, video, or proprietary assets, and none will ever be committed or distributed here. Any future local testing requires the user to supply their own lawfully obtained retail Xbox 360 copy of *Rise of the Tomb Raider*.
- **No DRM Circumvention:** This project does not provide tools or instructions for bypassing digital rights management (DRM), extracting cryptographic keys, or pirating software.
