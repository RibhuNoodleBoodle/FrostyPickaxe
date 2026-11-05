# Blocker & Issue Register

Last updated: 2026-11-05 (Step 01 audit)

---

| Issue ID | Subsystem | Description & Reproduction | Severity | Affected Dependencies | Smallest Actionable Next Step |
|---|---|---|---|---|---|
| **BLK-01** | Toolchain | Clang / Clang++ standalone frontend binary not found in PATH (`exit: 1`). GCC 15.2.0 is available. ReXGlue preset specifies Clang. | Medium | Step 03 SDK build | Test compiling ReXGlue with GCC 15.2.0 (which supports C++23) via `-DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++` or locate/download standalone Clang user binary if required. |
| **BLK-02** | Input | Physical Xbox 360 controller not currently attached to host. | Low (for early phases) | Step 07 (interactive visual validation) & Step 11 | Prepare synthetic input tests and programmatic event injection; attach physical controller prior to Step 11 gameplay acceptance. |
| **BLK-03** | Source / Update | Title Update Media ID `2427ED57` differs from Base Disc Media ID `0A657B25`. | Low (for base target) | G1-update branch only; base target (ADR-02) proceeds independently | Quarantine TU package; investigate inner STFS headers in Step 02 without applying to base build. |
