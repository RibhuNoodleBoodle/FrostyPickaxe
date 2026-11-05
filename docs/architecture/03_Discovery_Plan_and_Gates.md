# Evidence-driven implementation gates

Revision 2. Architect-selected work can begin now. This document replaces the initial blanket architecture blocker. Flash uses the statuses PASS, FAIL, BLOCKED and NOT TESTED honestly; an architecture choice is not a test result.

## Dependency graph

`Step_01 audit/privacy -> Step_02 base-source discovery` and independently `Step_01 -> Step_03 SDK baseline`.

`Step_02 G1-base + Step_03 -> Step_04 strict generation -> Step_05 runtime`.

From Step_05, implement/diagnose graphics (Step_06), input (Step_07) and media/streaming (Step_08) in bounded increments. These branches may be worked sequentially by one Flash session; parallel agents are not required. Their preparation does not depend on another branch's full visual acceptance. Real full-path tests require the relevant functioning branches. All required branch results feed `Step_09 fresh game build -> Step_10 early play -> Step_11/Gemini_90 ten minutes -> Step_12 clean HD 620 repeat -> Gemini_99`.

Incremental builds and bounded real launch attempts are permitted during Steps 04-08 after codegen prerequisites; Step_09 is an independently recorded clean-build milestone, not the first permission to compile. A change returns to its owning branch and invalidates dependent proofs. Keep interface-only/fixture results separate from integrated milestone PASS.

TU discovery is an independent branch from Step_02. Its unresolved result does not block the explicitly selected base variant. If base execution later proves an update necessary, mark that execution path BLOCKED and resolve G1-update before switching input. Do not silently relabel the build.

## Experiments and stop scope

| ID / owner step | Procedure / evidence | Pass | Failure / precise stop scope |
| --- | --- | --- | --- |
| E0 / 01 | Recheck repo/dirty files, instructions, tool/host inventory; create safe output exclusions before writers; record status ledger | Safe project identity and scoped work locations established | Wrong repo, overlapping unsafe edits or output exposure stops affected mutation; missing display is recorded for graphics |
| E1-base / 02 | Lawful local read-only source inspection and authorized provisioning; preserve originals; recheck exact base image and content manifest | Known base identity with usable local inputs and bounded destinations | Input corruption/unknown identity/unavailable lawful tooling blocks game-dependent work; SDK setup continues |
| E1-update / 02 | Validate TU container/internal delta source/target metadata, integrity and source compatibility | Exact compatibility proved, result identity recorded if later authorized to apply | Media mismatch stays unresolved until internal proof; blocks only update-dependent work; never force patch |
| E2-sdk / 03 | Acquire chosen SHA/gitlinks, inspect actual CLI/templates/libraries and licenses; compile/test/install SDK | Frozen reproducible SDK plus complete executed test inventory | Missing compiler/network/dependencies or test failure blocks baseline; no floating upgrade to hide it |
| E2-cpu / 04 | Strict discovery/codegen for chosen input; inspect code boundaries, indirect transfers, exceptions, VMX128/ABI and imports; repeat generation | Critical entry/dispatch paths validated and residual unknowns explained; no critical gaps | Unknown critical branch/opcode/dynamic behavior stops game implementation downstream; forced output not PASS |
| E3-runtime / 05 | Real startup traces, import semantics, memory/TLS/waits/timers, VFS/error paths and orderly shutdown | Required exercised behavior works; no hidden stubs/errors | Diagnose first fault; block dependent run, keep unrelated fixes separate |
| E4-device / 06 early probe | Query actual HD 620 driver/features/formats/limits and establish graphical access | Explicit selected device can support required backend path | XCB failure is display/access issue until diagnosed; unavailable required feature without faithful path blocks target rendering |
| E4-frames / 06 | Title-generated frames, same-build references, validation/captures; isolate shader/fetch/resolve/sync issue | Genuine real scene frames with reviewed faults/tolerances | Static/fake/movie-only output fails; severe correctness issues block playability |
| E3-input / 07 | Pinned SDL bridge; real host events -> guest state -> observed response, plus hotplug/focus | Controls operate correctly end to end | Device unavailable blocks physical test; unit mapping tests can continue but not claim M5 PASS |
| E3-media / 08 | Actual codec/import discovery, audio/video timing, streams, scene loads and saves as exercised | Required early-progression content works without hidden faults | Missing required media/API blocks progression; do not globally mute/disable it |
| E5-build / 09 | Fresh source snapshot plus exact candidate diff, private prerequisites and pinned SDK; strict regenerate/build/tests/launch | Authentic game-specific binary/hash with verified launch | Empty template/configure-only output fails; no gameplay inference |
| E5-play / 10 | New Game, substantive controls, scene transitions and expected geometry/HUD/audio | Advancing authentic early session | First hang/incorrect state blocks acceptance; no fabricated checkpoint scene names |
| E6-time / 11 + 90 | Continuous observed interactive run, monotonic eligible >=600 seconds, checkpoints and cross-checked proof | All eight required matrix rows PASS | Idle/movie-only/frozen/harness substitutes fail; absent observation/capture blocks verification |
| E6-repro / 12 | Fresh final candidate reproduction and repeat on HD 620, measured frame/memory behavior and content/license/secret audit | Functional acceptance reproducible; measured limitations explicit; safe original publication set | Severe unresponsiveness or unsafe/unknown rights blocks relevant final gate |
| E7-push / 99 | All applicable core rows passed, scoped candidate matches tested source, authorized remote and actual acknowledgement/ref | Real destination SHA verified | Missing access, rights, technical evidence or wrong remote means BLOCKED PUSH |

## Evidence storage and schemas

Future `docs/implementation/status.md` holds M0-M11 status, experiment/subgate status, dependency links and precise blocker scope. `environment.md` records actual host/tool/device/driver/configuration; `dependencies.md` records SDK, recursive gitlinks, compiler/stdlib and license provenance; `commands.md` records exact commands/cwd/environment/exit codes; `changes.md` records one issue/change/test; `blockers.md` records reproducible fault/owner/next action; `validation.md` maps claims to evidence; `readme-claims.md` records evidence for public claims. These are selected audit destinations, not pre-existing results.

Private `.local/rise360/proof/` holds raw logs/captures by run ID and hashes. Run identity includes UTC and monotonic mapping, source revision plus exact candidate diff/snapshot, SDK/patch/dependency identities, binary/plugin hashes, selected input variant/hash, OS/device/driver, settings, commands and exit status. Redact secrets/proprietary dumps from public summaries. Keep failed evidence as well as passed.

For per-step reports use the mandatory template in Gemini_00. No PASS without actual observations; missing evidence is not a reason to substitute narrative. Source/build/configuration changes invalidate affected results. Tool output showing zero discovered tests is not an executed test pass.

## Functional and performance acceptance

Follow ADR-08 and Gemini_90. Build, boot and time alone are insufficient. Test actual movement/camera/interactions and meaningful advancing state when control is available; inspect geometry/lighting/HUD, required audio/streaming, collisions/timing and transitions against available same-build references. Record visual defects precisely; if required reference evidence cannot be obtained, mark that correctness comparison unverified rather than assert fidelity.

Measure p50/p95/p99 frame times where instrumentation supports it, loading stalls separately, memory growth, cold/warm caches and thermal/power conditions. Synthetic/static scenes are not gameplay benchmarks. The earlier research's numeric aspirations are not promised or prerequisites for starting work. Severe persistent unresponsiveness blocks functional PASS. Wider combat/streaming scenes not reached in the tested session remain NOT TESTED; do not call ten minutes whole-game validation.

## Blocker handling

Continue only tasks whose dependencies are satisfied. Missing display does not halt SDK/source work; missing inputs does not halt SDK-only tests; an unproven TU does not block the chosen base input; unpassed game gates do block final publication. If core static translation or required faithful rendering is infeasible, document the exact constraint and stop that branch. No miracle workarounds, silent feature deletion or unsupported success claims.
