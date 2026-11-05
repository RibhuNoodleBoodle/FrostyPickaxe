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


