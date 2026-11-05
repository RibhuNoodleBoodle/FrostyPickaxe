# Changes & Modifications Log

Last updated: 2026-11-05 (Step 01 repository audit & privacy boundaries)

---

## Change Entry: CHG-001 (Step 01 - Private Boundary Protection)
- **Date**: 2026-11-05
- **Author**: Gemini Flash (Implementer)
- **Files Modified**:
  - `.gitignore`: Appended architecture-prescribed private path exclusions:
    - `.local/`
    - `port/generated/`
    - `port/rise360_manifest.toml`
    - `port/out/`
- **Files Created**:
  - `docs/implementation/status.md`: Audit ledger for milestones M0-M11 and subgates E0-E7.
  - `docs/implementation/environment.md`: Hardware, OS, Vulkan, and compiler inventory.
  - `docs/implementation/dependencies.md`: Pinned SDK, compiler, and proprietary input provenance.
  - `docs/implementation/commands.md`: Exact command log with UTC timestamps and exit codes.
  - `docs/implementation/changes.md`: This change log.
  - `docs/implementation/blockers.md`: Issue/blocker register.
  - `docs/implementation/validation.md`: Evidence mapping matrix.
  - `docs/implementation/readme-claims.md`: Record of evidence for public claims.
- **Rationale**: ADR-04 requires that all private directories and title-derived assets, generated files, manifests, and test outputs remain strictly ignored and uncommitted prior to any generator/build invocation.
- **Verification / Test**: Ran `git check-ignore` on each path; all returned exit code 0. Ran `git ls-files` on each path; confirmed zero tracked files exist.

---

## Change Entry: CHG-002 (Step 02 - Base Disc Provisioning & TU Quarantine)
- **Date**: 2026-11-05
- **Author**: Gemini Flash (Implementer)
- **Files Created**:
  - `tools/gdfx_provisioner.py`: Safe GDFX filesystem reader and extractor with strict path traversal checking.
  - `tools/analyze_tu.py`: STFS metadata reader to safely inspect Title Update packages.
  - `tests/test_provisioner.py`: Synthetic unit tests (5/5 passing) validating path bounds and binary parsing.
  - `.local/rise360/metadata/base_manifest.json` (ignored): Manifest of 84 extracted base disc files.
  - `.local/rise360/analysis/tu_analysis.json` (ignored): Title Update package analysis report.
  - `.local/rise360/game-base/` (ignored): Provisioned base disc files including `default.xex`, `.tiger` archives, movies.
- **Rationale**: ADR-02 requires lawful local provisioning of the unmodified base disc build (Title 53510823, Media 0A657B25) without modifying input images or bypassing DRM, while keeping the Title Update quarantined.
- **Verification / Test**: Synthetic unit tests passed (5/5). Extracted `default.xex` verified with SHA-256 `47e6476f6d393d86612e7af938979e9c706b54dc526d8422413711999d41e585`. All extracted files confirmed ignored by git.

---

## Change Entry: CHG-003 (Step 03 - ReXGlue SDK Linux Compatibility & Milestone M1)
- **Date**: 2026-11-05
- **Author**: Gemini Flash (Implementer)
- **Files Created / Modified**:
  - `patches/rexglue/0001-fix-rexcore-public-xxhash.patch`: Upstream compatibility patch covering:
    1. `src/core/CMakeLists.txt`: Promoted `xxHash::xxhash` from `PRIVATE` to `PUBLIC` on `rexcore` because public header `include/rex/hash.h` includes `<xxhash.h>`.
    2. `tests/unit/CMakeLists.txt`: Added `${PROJECT_SOURCE_DIR}/thirdparty/xxHash` to include directories for `unit_tests` to satisfy include without violating link audit singleton invariants (`rexglue_link_audit.cmake`).
    3. `include/rex/chrono/chrono.h`, `src/kernel/xboxkrnl/xboxkrnl_rtl.cpp`, `tests/unit/core/chrono_test.cpp`: Templated `to_sys()` / `from_sys()` to return `std::chrono::sys_time<Duration>` (defaulting to hundrednanoseconds). On Linux libstdc++, `std::chrono::system_clock::time_point` has nanosecond precision (`int64_t`), whose ±292-year representable range around 1970 overflows for NT epoch 1601 (-1.164 * 10^19 ns vs -9.223 * 10^18 ns `int64_t::min()`). Using `sys_time<hundrednanoseconds>` or `sys_time<milliseconds>` preserves exact 1601 NT epoch representation and eliminates integer overflow.
    4. `tests/unit/codegen/output_stamp_test.cpp`: Corrected backslash escaping in string literals from `"has\ space.toml"` to `R"(has\ space.toml)"`.
- **Rationale**: ADR-01 / ADR-03 requires a clean, reproducible baseline build and complete executed test inventory with zero test failures before advancing to game codegen.
- **Verification / Test**: Executed CTest across all 1,671 tests: 1,458 PPC instruction tests (100%) PASSED; 209 unit tests (100%) PASSED; 4 skipped by upstream; 0 failed. Installed cleanly to `.local/sdk/rexglue-sdk/out/install/linux-amd64/`. CLI executable verified functional.

---

## Change Entry: CHG-004 (Step 04 - Project Scaffold & Strict Codegen Milestone M2)
- **Date**: 2026-11-05
- **Author**: Gemini Flash (Implementer)
- **Files Created**:
  - `port/CMakeLists.txt`: Project CMake definition targeting C++23, defining `rise360` executable and recomp target.
  - `port/CMakePresets.json`: Configure/build presets specifying Clang toolchain and Ninja generator.
  - `port/cmake/rexglue.cmake`: ReXGlue build glue handling SDK discovery, recomp object compilation, and codegen custom targets.
  - `port/src/main.cpp`: Application entrypoint declaring `Rise360App` via `REX_DEFINE_APP`.
  - `port/src/rise360_app.h`: ReXApp subclass header providing lifecycle hook overrides.
  - `port/rise360_manifest.toml` (ignored): Private project manifest configuring entrypoint `default.xex` and declared branch target `0x82C21240`.
  - `port/generated/default/` (ignored): 421 generated source/header files (207 recomp translation units).
- **Rationale**: ADR-04 / ADR-05 requires setting up a clean, non-derivative project scaffold in `port/` and running strict code generation against the provisioned base XEX, ensuring zero critical gaps, while keeping proprietary generated code and manifests completely untracked.
- **Verification / Test**:
  1. Ran `rexglue codegen rise360_manifest.toml --ignore-stamp`: discovered and recompiled 45,104 functions into 207 translation units with 0 validation errors; generated input fingerprint `a726442c842406c1d2bd3305b16bb0b7`.
  2. Verified incremental codegen caching (0 written, 1 up to date in 0.2s).
  3. Ran CMake configure on `port/`: successfully resolved ReXGlue SDK 0.10.0 and generated build targets.
  4. Compiled `main.cpp.o` and recompiled translation unit `rise360_recomp.0.cpp.o` with Clang 21 with zero errors.
  5. Verified `git status`: confirmed `port/generated/` and `port/rise360_manifest.toml` remain completely untracked and ignored.



---

## Change Entry: CHG-005 (Step 05 - Runtime, Guest Services, VFS, and Indirect Dispatch Resolution)
- **Date**: 2026-11-06
- **Author**: Gemini Flash (Implementer)
- **Files Modified / Created**:
  - `port/CMakeLists.txt`: Configured `rexglue_setup_target(rise360 GPU_PLUGINS xenos)`.
  - `port/src/rise360_app.h`: Overrode `OnPreSetup()` to set default `config.gpu_plugin = "xenos"`; overrode `OnConfigurePaths()` to map `.local/rise360/game-base` to `game_data_root`, user/cache roots, and explicitly clear `update_data_root` per ADR-02 base disc isolation.
  - `port/rise360_manifest.toml` (ignored): Added 48 missing indirect PowerPC call dispatch entrypoints (vtable `this`-adjuster thunks, interface dispatch thunks, and leaf blr utility routines).
  - `docs/implementation/05_Runtime_Guest_Services_and_VFS.md`: Milestone M3 technical and verification report.
- **Rationale**: ADR-05 / ADR-06 requires initializing ReXApp lifecycle, mounting the single-disc virtual filesystem, spawning guest multi-core threads, attaching native ALSA/Pulse audio, and resolving all runtime indirect function calls on Intel HD Graphics 620 via Vulkan.
- **Verification / Test**:
  1. Recompiled 207 translation units and linked `rise360` with Clang 21 without errors.
  2. Bounded test execution `rise360_035` ran for 20.0s without crashing or SIGABRT, cleanly exiting with code 124 upon timeout.
  3. Verified ALSA/Pulse audio stream active (`Built-in Audio Analog Stereo: 6 ch, 48000 Hz`).
  4. Verified Vulkan 1.4.335 device initialization on Intel HD Graphics 620 (`/usr/lib/x86_64-linux-gnu/libvulkan_intel.so`) with swapchain creation and 350+ graphics pipelines compiled and cached.

---

## Change Entry: CHG-006 (Step 06 - Vulkan HD 620 Device Validation & Xenos Frame Path)
- **Date**: 2026-11-06
- **Author**: Gemini Flash (Implementer)
- **Files Created / Modified**:
  - `docs/implementation/06_Vulkan_Frame_Presentation.md`: Milestone M4 technical and empirical frame evidence report.
  - `docs/implementation/status.md`: Updated M4, E4-device, and E4-frames to PASS; unlocked Steps 07 and 08.
  - `docs/implementation/commands.md`: Added Step 06 execution commands and empirical evidence entries.
  - `docs/implementation/validation.md`: Added Milestone M4 verification entry.
  - `.local/rise360/proof/` (ignored): 673 captured presentation PNG frames.
- **Rationale**: ADR-06 requires verifying genuine hardware graphics rendering on the Intel HD Graphics 620 device using the Xenos Vulkan backend, capturing real title presentation frames, and confirming shader and swapchain presentation without fallbacks.
- **Verification / Test**:
  1. Ran `vulkaninfo --summary`: confirmed Intel HD Graphics 620 [8086:5916], Vulkan 1.4.335, Mesa 26.0.8-1ubuntu0.3, Wayland/XCB surface extensions.
  2. Executed `rise360` under Wayland graphical session (`rise360_037` to `rise360_039`).
  3. Swapchains created at 1280x720 and native 1366x768 format 44 (`VK_FORMAT_B8G8R8A8_UNORM`).
  4. Captured 673 sequential frames using `VK_LAYER_MESA_screenshot` in `.local/rise360/proof/`.
  5. Verified 147 active rendered animation frames (526-672) with 331 unique colors and animated emblem rendering; zero GPU errors or crashes in 30s session (exit code 124 timeout).
