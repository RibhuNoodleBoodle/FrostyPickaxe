# FrostyPickaxe implementation architecture

Revision 2 — 2026-11-05. Architect: ChatGPT Astra. Implementer: Gemini Flash.

The user's latest direction is: “I am asking you to be the architect and write the implementation for gemini flash”. This appoints Astra to make the architecture and author Flash's implementation instructions. It supersedes the prior requirement to wait for a separate Argon architecture session. These are architect-selected decisions under that delegation, not a claim that the user separately reviewed every technical detail. Flash can implement this plan within its active step and actual permissions. No second architecture approval is required for the decisions below.

**Readiness: READY FOR DISCOVERY AND IMPLEMENTATION.** Hardware, source provisioning and runtime feasibility remain empirical gates on their dependent tasks. No game-specific build or gameplay has been verified. Astra writes design and worker instructions; Flash writes the program. No Android development or final publication before the prescribed gates.

## Evidence and authority

Local evidence: `docs/research/00_Repository_State.md` (R2), `01_Feasibility_Report.md` (R3), `02_Risks_Unknowns_and_Gates.md` (R4), `03_Sources_and_Evidence.md` (R5), all in `docs/research/`; repository/host audit and hashes in `gemini_flash/Astra_Evidence_and_Traceability.txt`. `gemini_argon/Gemini_Argon_04_Architecture_Handoff.txt` describes desired design deliverables but is not an implemented design. The user's master prompt supplies the PC, authentic gameplay, provenance and publication requirements. Its old role/missing-architect provisions yield to the latest direct instruction.

A source register and command recipes are in `gemini_flash/Gemini_03_Pinned_SDK_and_Commands.txt`. Every new design choice below is explicitly a decision, not an observed runtime capability. If the pinned checkout contradicts retrieved sources, Flash must record exact hashes and stop only affected integration until the contradiction is resolved; do not silently change revision.

## ADR-01 — Host and execution architecture

**Decision:** initial host is Linux x86-64, matching the observed Ubuntu 26.04.1 workspace. Use statically recompiled Xbox 360 CPU code with ReXGlue guest services and the SDK Xenos Vulkan path. Use Intel HD 620 as the acceptance device. Windows stays a portability follow-up with no tested-support claim; Android is outside this package.

**Evidence:** R0 target invariants; E1 host/PCI observations; pinned runtime/header/build sources in command register. **Rejected:** native PC executable/assets, Xenia-as-runtime wrapper, dynamic emulator substitution, custom host gameplay reimplementation, parallel Android.

**Consequence/test:** build and process identities must connect real input -> generated CPU code -> native executable -> real guest state -> Vulkan output. SDK fixtures stay explicitly separate. Linux display access is needed for graphics acceptance, not SDK compilation or CPU analysis.

## ADR-02 — Exact initial game build and update policy

**Decision:** initial implementation targets the supplied unmodified base-disc build, identified by R2 as Title `53510823`, Media `0A657B25`, version/base 3, disc 1/1. This is an explicit base-only scope decision by the appointed architect. It is not an assertion that base-only runtime is sufficient or that an update is unnecessary. Runtime failures may prove an update required.

The supplied TU (reported Media `2427ED57`) remains quarantined and unapplied. Audit its identity/internals as an independent discovery branch. An unresolved TU mismatch blocks updated-build work only. G1 is split into G1-base and G1-update; never label the latter passed through this scope choice. If base progression requires a TU, block that progression until a lawfully available applicable update and resulting image identity are validated. Do not force application, rewrite IDs or bypass protection. R2's reported XEX hash must be independently checked during lawful provisioning.

**Storage:** original ISO and ZIP remain immutable. Flash may use authorized, lawful local container inspection/provisioning tools to populate `.local/rise360/game-base/`, retaining disc-relative layout and original filename case. No undocumented decryption, keys, DRM bypass or downloads of commercial content. If available tooling cannot legally supply SDK-compatible inputs, block codegen and continue asset-independent tasks. Record provenance and authorization as user context, not a legal conclusion or distribution grant.

**Rejected:** blindly merging TU, assuming two discs, waiting for update research before any SDK work. **Tests:** stable input fingerprints, bounds/container integrity, exact base XEX identity, content inventory, no input writes; negative test ensures TU cannot be selected silently.

## ADR-03 — SDK baseline and change control

**Decision:** select ReXGlue `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518` as the initial immutable integration pin. Previously this was merely a documentary revision; it becomes a deliberate architect-selected baseline here. Selection is based on accessible pinned build, launcher/runtime, CLI and Xenos plugin sources, not a latest/stable or title-compatibility claim. Keep exact gitlink revisions for all submodules; branch labels in `.gitmodules` do not authorize updates. Do not use `submodule update --remote`.

Use `.local/sdk/rexglue-sdk/` as the ignored source/build/install checkout, with package discovery pointing only to this install. Record all recursive submodule SHAs, compiler/linker/stdlib versions and dependency notices in `docs/implementation/dependencies.md`. Resolve actual SDL version from its pinned gitlink checkout; do not select another SDL based on a moving wiki. Prefer a usable Clang 20+ installation if available; the selected build file's minimum is 18. Select one supported compiler/stdlib pair by a real clean build, record it and freeze it. No automatic compiler install or privilege assumption.

**Rejected:** floating main/latest, preapproved community patch stack, wholesale SDK fork. A reproduced SDK defect may be fixed narrowly in the local checkout with an original permissible patch under `patches/rexglue/`, base SHA, rationale and regression. SDK revision changes require an amended ADR with source evidence and rerun baseline, not fresh permission for ordinary reversible engineering. Fundamental target/fidelity changes go back to the user.

**Test:** exact checkout and submodule identities, baseline test enumeration/execution, reproducible install, explicit Vulkan configuration, license inventory. Missing network/toolchain blocks baseline execution only.

## ADR-04 — Project and private-data layout

**Decision:** project app is named `rise360`; original app/build work lives in `port/`; root README/research remain separate. Initial SDK scaffold is staged in ignored `.local/rise360/scaffold/`, reviewed, then only original/licensable glue is promoted into `port/`. This avoids overwriting existing root documents. Public tooling is in `tools/`, synthetic tests in `tests/`, SDK patch descriptions/artifacts in `patches/rexglue/`, audit summaries in `docs/implementation/`.

Default local-only locations: `port/generated/`, `port/rise360_manifest.toml`, `port/out/`, `.local/` in its entirety. Generated CMake integration is regenerated with SDK tooling too; do not force-add the generated directory. Title-derived function maps/metadata/config with uncertain redistribution rights stay private. A public provisioning recipe can recreate local manifests from supplied input and original configuration, subject to its own provenance review.

Separate `.local/rise360/game-base/` (read-only content), `user/` (writable test saves), `cache/`, `metadata/`, `proof/` (raw logs/captures), and `analysis/`. Original ISO/ZIP remain in their existing ignored root paths. Preserve case and relative paths; do not lowercase actual content to accommodate a tool bug. Resolve filesystem targets and reject escapes/symlinks into unapproved directories in project-owned provisioning tools. Before any generator/provisioner writes, verify exclusions and tracked-file absence for destination families. Existing root ignore patterns are insufficient.

**Tests:** missing input and outside-root paths produce actionable errors; outputs stay local; clean regeneration works without tracked generated code. Never store real game bytes in test fixtures. See module map for exact ownership and contracts.

## ADR-05 — CPU and runtime integration

**Decision:** retain SDK-generated project and native dispatch structure; use a thin ReXApp customization layer and source-verified hooks. Do not construct a parallel guest OS, dispatcher or main loop. Keep generated C++ immutable between codegen invocations; fixes belong in evidenced configuration, original overrides or upstream patch artifacts. Use strict generation with critical indirect transfers, VMX128/ABI, exceptions and imports audited. Forced generation may aid diagnosis but cannot pass M2.

Use existing guest memory, TLS, kernel objects, threads, timing and waits. New import behavior must match actual guest-visible semantics, including failures; no success stubs. Associate traces with guest module/address, thread and subsystem, keeping proprietary dumps private. Track import resolution separately from exercised correctness. Guest online/profile/storage errors must be real supported offline behavior or explicit blockers, not fabricated success.

**VFS:** one base content root, writable test-user root separate from game files, optional update root absent in base mode. Use SDK mount plumbing with read-only enforcement where supported; otherwise protect the content location and block unsafe writes. Verify actual source and traces for path case, overlay and save behavior. No invented second-disc device or eager custom `.tiger` parser: preserve guest-driven access unless a traced missing facility requires original integration.

**Tests:** strict regenerate, dispatch/import audit, startup/error paths, wait/timer behavior, loading and shutdown, repeatable scene transitions. Compile success cannot stand in for these.

## ADR-06 — Graphics and device behavior

**Decision:** use the selected SDK's existing runtime-loaded Xenos plugin and Vulkan backend. Do not link an invented monolithic GPU target into the app or duplicate SDK global state. The source register identifies the plugin/build contract; verify loading/search paths against installed artifacts. Explicitly reject fallback to another graphics API or another device as baseline acceptance.

Query actual HD 620 Vulkan features/formats/limits and driver in the user's accessible graphical session. PCI visibility does not prove Vulkan use. Current XCB failure is an environment blocker to investigate, not a feature failure. Rendering issues are localized through title command/frame captures and same-build Xbox 360 reference evidence: shader/fetch, textures, render targets, depth/stencil/blending, EDRAM/resolve, aliasing and synchronization. Select faithful fallback only if pinned source supports it and actual captures validate it. Otherwise report unsupported target, do not invent a replacement.

**Tests:** device selection plus actual GPU work, validation, genuine scene frames, correctness tolerances grounded in reference captures and explicit flaw reporting. No mandatory LUT/interlock assumptions or speculative backend rewrite.

## ADR-07 — Input, audio and streaming

**Decision:** reuse pinned SDL input/audio integration; original adapters are only for demonstrated title-specific gaps. Guest XInput/XAM polling remains the game-facing contract. Host event ownership and guest reads follow SDK locking/threading; do not introduce a second event pump or lock across blocking guest callbacks. Validate buttons, axes, triggers, dead zones, focus, disconnect/reconnect and game camera/movement.

Inventory media requirements from actual executed imports/content, not guessed middleware. Preserve guest-driven file/decode/audio timing where implemented; bounded host adapters must preserve guest error and completion behavior. No new host decoder or archive parser until a specific unsupported path is demonstrated. Audio starvation, missing codec, streaming deadlock or required movie failure is a progression blocker, not permission to disable functionality.

**Tests:** host event -> guest state -> visible action; real audio/scene progression with underrun/sync diagnostics, saves and offline behavior where exercised. Synthetic tests cover semantics only, never replace authentic gameplay.

## ADR-08 — Acceptance and measurements

**Decision:** first build, boot, rendering, controls, early progression, 600 eligible seconds and HD 620 validation are independent evidence rows. `Gemini_90_Ten_Minute_Gameplay_Acceptance.txt` is binding. Minimum functional target: substantive responsive player control, real state progression/scene transitions and no hard blockers through that session, with required sound/content. Persistent unresponsiveness preventing normal play fails regardless of elapsed clock time.

Measure frame-time distribution, stalls, memory, settings and cache/thermal state. R4's 720p/30 FPS and percentile figures remain experimental performance aspirations, not a new approval prerequisite or invented guarantee. Report whether measured behavior meets them, without conflating that result with functional acceptance. No claim of an optimized performance target or full-game support until separately evidenced. Clear fidelity failures and a slideshow cannot pass as playable. Keep strict correctness/diagnostic runs and production-performance configuration distinct; revalidate actual final configuration and document overhead.

**Tests:** exact binary/SDK/input identity, observed continuous interactive session with exclusions, independent cross-check, fresh-source final repeat and raw local proof. Unavailable tester/capture/device blocks these rows, not all prior coding.

## ADR-09 — Publication and worker autonomy

**Decision:** no commit/push before master-prompt final technical/content gates. Remote observation is not invented publication permission; confirm actual scoped destination when publication becomes concrete. Do not leak proprietary generated code, inputs, saves, keys, captures or dependencies with unresolved rights. Sanitized docs must state exact tested stage and limitations; root README changes only after relevant evidence. Preserve the six existing dirty documentation files and do not sweep them into unrelated commits.

Flash executes within the active work package, chooses routine implementation details, makes small reversible corrections and updates the decision/change log with evidence. No blanket request for another architect or approval of every module. Stop only when a specific missing prerequisite, infeasible feature, restricted operation or materially changed product requirement demands it. In that event continue independent ready tasks and report the exact affected gates.

## Remaining empirical contracts

Not decided by assertion: legal/provenance facts; valid local input provisioning; exact SDK submodule/SDL identities; compiler success; strict CPU coverage; exercised guest imports; real Vulkan features/path; codec requirements; performance; final remote authentication. Flash resolves these using the experiments in document 03. A failed experiment can invalidate a decision; preserve evidence and amend only the affected ADR.
