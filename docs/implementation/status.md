# FrostyPickaxe Implementation Status Ledger

Last updated: 2026-11-06 (Step 05 / Milestone M3 completed)
Architect: ChatGPT Astra (ADR-01 through ADR-09)
Implementer: Gemini Flash

---

## 1. Milestone Status Ledger

| Milestone | Owning Step | Description | Status | Dependencies / Prerequisites | Evidence / Notes |
|---|---|---|---|---|---|
| **M0** | Step 01 / 02 | Audit baseline, private path exclusions, base-disc provisioning & TU analysis | **PASS** | Clean repository state, user architect delegation | Step 01 passed: `.gitignore` protects private paths; hardware probed. Step 02 passed: GDFX provisioner extracted 84 files to `.local/rise360/game-base/` with SHA-256 match for `default.xex`; TU audited and quarantined. |
| **M1** | Step 03 | SDK-only baseline (pinned ReXGlue `c94f5eb`, recursive submodules, build & test) | **PASS** | Step 01 PASS | Pinned SDK clone `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518` & 22 recursive submodules locked. Clang 21.1.8 toolchain in `.local/toolchain/`. Built Release mode; 1,671 CTest tests executed: 1,458/1,458 PPC instructions passed (100%), 209/209 active unit tests passed (4 skipped by upstream), 0 failures. Installed to `.local/sdk/rexglue-sdk/out/install/linux-amd64/`. CLI verified. |
| **M2** | Step 04 | Strict game-specific codegen (`rise360` scaffold & strict base XEX translation) | **PASS** | Step 02 (G1-base PASS) + Step 03 (M1 PASS) | Scaffold configured in `port/`; `rise360_manifest.toml` configured with entrypoint `default.xex` and entrypoint branch target `0x82C21240`. Strict codegen completed in 149.6s: 45,104 functions discovered and recompiled into 207 translation units (`port/generated/default/`); 0 validation errors; deterministic fingerprint `a726442c842406c1d2bd3305b16bb0b7`. CMake configured `rise360` executable and successfully test-compiled recompiled TU with Clang 21. |
| **M3** | Step 05 | Runtime, guest services, VFS & thin app integration | **PASS** | Step 04 (M2 PASS) | `Rise360App` implemented in `port/src/rise360_app.h`; Xenos GPU plugin enabled; VFS mounted `game:`/`d:` to `game-base`; 48 indirect dispatch targets resolved; 18+ threads spawned; ALSA/Pulse 6ch 48kHz audio active; 350+ Vulkan pipelines compiled on Intel HD 620; ran 20s with 0 crashes (exit code 124 timeout). See `docs/implementation/05_Runtime_Guest_Services_and_VFS.md`. |
| **M4** | Step 06 | Vulkan HD 620 device validation & Xenos frame path | **READY** | Step 05 (M3 PASS) | Hardware Vulkan 1.4.335 on HD 620 confirmed; ready for graphical session frame presentation validation. |
| **M5** | Step 07 | SDL-to-guest controller mapping and semantics | **BLOCKED** | Step 05; Step 06 for visual proof | Synthetic mapping can prepare after M3; full interactive acceptance requires M4. |
| **M6** | Step 08 | Audio, media, streaming and scene loading | **BLOCKED** | Step 05; Step 06/07 for integrated trial | Codec/timing integration. |
| **M7** | Step 09 | First clean authentic game-specific build and launch | **BLOCKED** | M2 through M6 applicable results | Independent milestone build. |
| **M8** | Step 10 | New Game and early player progression | **BLOCKED** | Step 09 (M7 PASS) | Substantive control & state advancing. |
| **M9** | Step 11 | Ten-minute gameplay acceptance (Gemini_90 protocol) | **BLOCKED** | Step 10 (M8 PASS) | Continuous interactive >=600s session. |
| **M10** | Step 12 | Final clean reproduction on HD 620, measurements & publication audit | **BLOCKED** | Step 11 (M9 PASS) | Fresh rebuild, repeat gameplay, performance data. |
| **M11** | Step 99 | Scoped repository push to origin/main | **BLOCKED** | All core gates M0–M10 PASSED | Final push gate. |

---

## 2. Experiments & Subgates (docs/architecture/03_Discovery_Plan_and_Gates.md)

| Experiment | Target | Description | Status | Evidence Pointer |
|---|---|---|---|---|
| **E0** | Step 01 | Repository baseline, private output exclusions, environment audit | **PASS** | `docs/implementation/environment.md`, `.gitignore` |
| **E1-base** | Step 02 | Base-disc container validation & lawful local provisioning to `.local/rise360/game-base/` | **PASS** | `tools/gdfx_provisioner.py`, `.local/rise360/metadata/base_manifest.json`, `default.xex` SHA-256 `47e6476f6d393d86612e7af938979e9c706b54dc526d8422413711999d41e585` |
| **E1-update**| Step 02 | TU container/metadata analysis & delta applicability classification | **AUDITED / QUARANTINED** | `tools/analyze_tu.py`, `.local/rise360/analysis/tu_analysis.json` (Media ID mismatch: `2427ED57` vs `0A657B25`) |
| **E2-sdk** | Step 03 | Pin `c94f5eb`, recursive submodule lock, build, CTest suite, install | **PASS** | Pinned SDK installed to `.local/sdk/rexglue-sdk/out/install/linux-amd64/`; CTest 1,671 tests (1,458 PPC 100%, 209 unit tests 100%, 0 failed). |
| **E2-cpu** | Step 04 | Strict discovery/codegen for base XEX, coverage & entrypoint audit | **PASS** | 45,104 functions, 207 recomp files, 0 validation errors, fingerprint `a726442c842406c1d2bd3305b16bb0b7`. |
| **E3-runtime**| Step 05 | Real startup trace, kernel/XAM services, memory/threads/waits, single-disc VFS | **PASS** | Full runtime initialization, VFS mounts, threading, APU audio 6ch 48kHz, Vulkan pipeline state compilation, 0 crashes in 20s run 035 (`port/out/build/linux-amd64-release/logs/rise360_035.log`). |
| **E4-device** | Step 06 | Query HD 620 driver/features/limits; verify graphical session | **PREFLIGHT PASS** | `vulkaninfo --summary` exit 0, HD 620 Vulkan 1.4.335 |
| **E4-frames** | Step 06 | Title-generated frames, reference comparison, shader/EDRAM diagnosis | **READY** | Ready to proceed with Step 06 graphical presentation validation |
| **E3-input** | Step 07 | SDL controller bridge, guest XInput state, focus/hotplug | **BLOCKED** | Dependent on E3-runtime / E4-frames |
| **E3-media** | Step 08 | Middleware/codec discovery, audio/video streams, loading stability | **BLOCKED** | Dependent on E3-runtime / E4-frames |
| **E5-build** | Step 09 | Fresh clean game-specific compilation, linkage, and launch check | **BLOCKED** | Dependent on E2-cpu through E3-media |
| **E5-play** | Step 10 | New Game sequence, controls, scene transitions | **BLOCKED** | Dependent on E5-build |
| **E6-time** | Step 11 | Gemini_90 continuous 10-minute session on HD 620 | **BLOCKED** | Dependent on E5-play |
| **E6-repro** | Step 12 | Clean final candidate rebuild, measurement, content audit | **BLOCKED** | Dependent on E6-time |
| **E7-push** | Step 99 | Authenticated scoped push to authorized remote | **BLOCKED** | Core gates M0-M10 must pass first |

---

## 3. Dependency DAG and Ready Work

```
Step 01 (PASS)
  ├──> Step 02: Base Input Provisioning (E1-base) [PASS]
  │       └──> Step 02: Title Update Investigation (E1-update) [AUDITED / QUARANTINED]
  │
  └──> Step 03: ReXGlue SDK Baseline (E2-sdk) [PASS]
          │
          └──> (Join Step 02 G1-base + Step 03 M1) ──> Step 04: Strict Codegen (E2-cpu) [PASS]
                                                              │
                                                              └──> Step 05: Runtime & VFS (E3-runtime) [PASS]
                                                                      │
                                                                      └──> Step 06: Vulkan HD 620 Validation (E4-frames) [READY]
```
