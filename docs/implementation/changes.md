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

## Change Entry: CHG-003 (Step 03 - ReXGlue SDK xxHash Public Dependency Patch)
- **Date**: 2026-11-05
- **Author**: Gemini Flash (Implementer)
- **Files Created**:
  - `patches/rexglue/0001-fix-rexcore-public-xxhash.patch`: Narrow upstream patch for `src/core/CMakeLists.txt`.
- **Rationale**: `include/rex/hash.h` is a public SDK header that directly includes `<xxhash.h>`. In the upstream SDK, `xxHash::xxhash` was linked `PRIVATE` to `rexcore`, causing consumers (including the SDK's own unit test suite) to fail compilation with `'xxhash.h' file not found`. Moving `xxHash::xxhash` to `PUBLIC` dependencies of `rexcore` correctly propagates the include directory.
- **Verification / Test**: Applied to `.local/sdk/rexglue-sdk/` and re-triggered CMake build.


