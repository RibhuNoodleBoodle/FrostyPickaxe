# Risks, unknowns and gates

Revised 2026-11-05. All experiments below are future protocols, not executed results.

| Risk | Severity | Current evidence / uncertainty | Resolution |
| --- | --- | --- | --- |
| BLK-01 Update applicability | Critical | ISO Media `0A657B25` versus TU package `2427ED57`; internal delta unknown | EXP-01 / G1 |
| BLK-02 XEX discovery/codegen | Critical | Encrypted inner code not analyzed | EXP-02 / G2 |
| BLK-03 Runtime completeness | High | Actual imports and exercised synchronization unknown | EXP-03 / G2 |
| BLK-04 Xenos correctness | Critical | No title-specific backend captures | EXP-04 / G3 |
| BLK-05 HD 620 features/performance | Critical | No user's driver capabilities or timings | EXP-05 / G3 and EXP-06 / G4 |
| BLK-06 Content/media/save coverage | High | Single-disc root observed; archive/update semantics unknown | EXP-01 and EXP-03 |
| BLK-07 Provenance/distribution | High | No redistribution license established; ZIP untracked | G0 and packaging review |
| BLK-08 Android platform gaps | High, deferred | PC not proven; Android runtime not audited | G5 |

## Discovery experiments

- **EXP-01 — Input compatibility:** recheck immutable input fingerprints and outer headers, validate container integrity, then inventory internal TU entries and delta source/target metadata locally with suitable read-only tools. Identify whether this exact base image is accepted. Pass only with documented applicability; if mismatch persists, hold updated-code analysis pending a lawfully available matching input. Never force acceptance or edit identifiers. A base-only investigation must remain separately labeled.
- **EXP-02 — Static translation audit:** in a later authorized phase, record selected SDK/dependency SHAs, source executable identity, executable ranges, function/switch discovery, unsupported instructions, exception handling and dynamic-code assumptions. Pass only with explained coverage and no silent unknown branch fallback. A generated file count alone is insufficient.
- **EXP-03 — Runtime/content:** map import ordinals to implementations, identify executed gaps, diagnose guest waits, and test startup, streaming, localization, video/audio, input hotplug, save/load and offline operation. Capture missing paths, thread state and errors before proposing runtime patches. A menu is not a gameplay pass.
- **EXP-04 — Rendering correctness:** compare fixed menu, prologue and representative gameplay views against the same Xbox 360 build; isolate shader, fetch, render-target, EDRAM resolve/readback and gamma errors individually. Pass with explicit reference captures and documented tolerances; no speculative LUT fix may count as proof.
- **EXP-05 — Device compatibility:** record HD 620 OS/driver/API/features/extensions/formats/limits and selected backend path separately on Windows and Linux. Pass only when all required checks and fallback correctness succeed on the tested combination. Missing required features with no faithful fallback stop that configuration.
- **EXP-06 — Performance:** on actual HD 620, record CPU/RAM/driver/power state, content/SDK hashes, resolution, fidelity settings and cold versus warm caches. Measure CPU/GPU frame times, p50/p95/p99, stalls, pipeline compilation, readbacks, memory and audio underruns. Use prologue traversal, a streaming-heavy area, combat, UI and video over repeatable runs including sustained thermal load. Proposed acceptance: 720p/30 FPS target, p95 at most 33.3 ms and p99 at most 50 ms over declared gameplay windows, no sustained memory growth or severe visual/audio faults. These are provisional design criteria, not measurements. Report loading transitions separately. If they fail, attribute the bottleneck before proposing a fidelity compromise; record any revised acceptance explicitly.

## Sequential decision gates

| Gate | Pass evidence | Current state / stop condition |
| --- | --- | --- |
| G0 Evidence and private handling | Local inventory, exclusions before staging, source provenance and SDK selection plan | Metadata recorded; TU ZIP untracked/unignored; SDK unselected |
| G1 Exact input applicability | Verified exact base/update source relationship, complete content inventory, repeatable identity record | OPEN: differing Media IDs; do not assume patched image |
| G2 CPU and runtime | Audited translation/import coverage and reproducible startup/scene transition | NOT RUN; stop on unresolved code/runtime gaps |
| G3 Graphics/device | Correct reference scenes and actual driver/format/path evidence | NOT RUN; stop on unsupported required behavior |
| G4 Playability/performance | EXP-06 acceptance plus controls, audio, saves and sustained stability | NOT RUN; no HD 620 claim before measured pass |
| G5 Android eligibility | Accepted PC gates plus separately authorized Android feasibility audit | DEFERRED |

Milestones remain M1 compiles, M2 launches, M3 menu, M4 scene, M5 playable, M6 acceptable on HD 620. Each needs its own evidence; gates can require several milestones.

Architecture documents may be produced with unresolved gates, provided decisions remain conditional. Do not execute codegen/builds or create worker execution prompts during the initial architecture session. Completion of research does not itself pass G1 or authorize implementation.
