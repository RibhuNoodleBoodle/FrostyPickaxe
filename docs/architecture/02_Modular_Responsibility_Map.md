# Module boundaries and implementation ownership

Revision 2, authored by Astra under the user's architect delegation. These are selected future paths and contracts; no implementation files exist yet. Read `01_System_Architecture_ADR.md` and the full anti-cheating policy in `gemini_flash/Gemini_00_Read_First.txt`.

| Owner / future paths | Responsibility and inputs | Output / failure contract | Verification |
| --- | --- | --- | --- |
| Flash: `tools/`, `tests/` | Original private-input inventory/provisioning and source identity checks; supplied immutable ISO/ZIP, lawful tools | Reproducible local content manifest, exact base identity, bounded destinations; reject mismatch, truncated container, path escape and unsupported operation | Synthetic malformed-path/container fixtures; real metadata kept private; input hashes unchanged |
| Flash: `.gitignore`, `docs/implementation/` | Extend exclusions before private/generated writes; preserve existing rules | Private path families untracked/ignored; ledger distinguishes base/update and actual evidence | `git check-ignore`, tracked-file checks and manual publication scan |
| SDK checkout: `.local/sdk/rexglue-sdk/` | Immutable baseline and recursive gitlink dependencies | SDK install, tests, CLI, runtime/plugin libraries; no floating updates | Dependency lock record; clean build/test; explicit package resolution |
| Flash: `patches/rexglue/` | Only independently authored, reproduced SDK corrections and their regression notes | Patch plus base SHA/ordering/reproduction; no title-derived bytes or unexplained backports | Apply to fresh pin, test regression, update patch identity in proof |
| Flash: `port/CMakeLists.txt`, `port/CMakePresets.json` | Original app integration adapted from inspected SDK template | Explicit pinned SDK package, native executable, correct plugin deployment; missing SDK/generated input fails clearly | Clean configure/compile/link; inspect linked dependencies and launched path |
| Flash: `port/src/main.cpp`, `port/src/rise360_app.h` | Thin SDK app entry/customization; paths, selected backends and diagnostics | Validated startup/shutdown and native guest dispatch; fail before launch on mismatched inputs | Launcher/error-path tests; runtime trace and shutdown |
| Flash: `port/src/guest/` | Only title-required guest service adapters/overrides proven missing | Correct guest ABI/endian/status/completion behavior, never unconditional success | Specific semantic/regression probes and actual exercised import trace |
| Flash: `port/src/content/` | Path validation and local content/save integration if SDK hooks need it | Read-only base, separate writable user/cache paths; absent TU; true missing-file errors | Single-disc actual file reads, missing path, save/load and overlay-negative test |
| Flash: `port/src/input/` | Only demonstrated SDL-to-guest mapping gaps | Stable controller identity, mapped guest state, focus/hotplug handling without synthetic progression | Host/guest/visible response correlation plus synthetic edge tests |
| Flash: `port/src/diagnostics/` | Low-overhead events and evidence capture coordination | Timestamped lifecycle/import/VFS/GPU/input/audio faults; rate limiting with explicit dropped-event counts | No concealed critical error; measure diagnostic overhead |
| SDK: guest memory/kernel/runtime modules | Native dispatch, memory/TLS/threads/waits/exceptions and timing | Existing source-verified SDK semantics; project adapters do not duplicate global state | CPU/ABI/import tests, deadlock traces, bounded execution experiments |
| SDK: Xenos plugin and Vulkan code | Guest GPU packets/shaders/resources to genuine host frames | Correct selected-device work and resource synchronization; fail unsupported required path | Actual device query, validation, reference scenes and frame captures |
| SDK: SDL input/audio and guest media services | Host event/device output behind guest-facing contracts | Actual input/audio/media completion and timing | Real input/playback, underrun/sync/streaming tests |
| Private generator: `port/generated/`, `port/rise360_manifest.toml` | Validated base XEX, original configuration, pinned CLI | Game-derived translation/configuration kept ignored; regeneration owns outputs | Strict codegen, input/config hashes, explained nondeterministic stamps |
| Private runtime: `.local/rise360/{game-base,user,cache,metadata}/` | Lawfully supplied content and per-run local state | Separate immutable content, disposable test saves and caches | Case/path preservation, no writes to originals, no personal-save overwrite |
| Private QA: `.local/rise360/{analysis,proof}/`, `port/out/` | Binaries, logs, captures and reports | Full local proof; public summaries contain no game bytes or secrets | SHA-256 and cross-correlated process/input/frame/clock evidence |

Braced paths above are notation for separate directories, not shell commands. Only create a source subdirectory when a proven task needs it; avoid empty speculative layers.

## Interfaces Flash must implement or verify

These are semantic contracts, not invented SDK function names. Exact existing API anchors and source links are in `Gemini_03_Pinned_SDK_and_Commands.txt`.

1. **Provisioner -> codegen:** versioned private record of selected variant, input hash, image identity, immutable content root, tool/version and derivation history. Codegen refuses unknown/mismatched variant. It must not choose a TU based on filename alone. Verify full file bounds and safe paths before reading/copying; errors preserve originals.
2. **Codegen -> build:** manifest plus strict generation report, function/import coverage and generated output inventory with SDK/config/input identities. No successful build gate while critical unresolved transfers remain. Regeneration handles generated source, including integration glue; manual generated edits are not durable fixes. Compare two runs accounting only for explained timestamps/stamps; never normalize away substantive differences.
3. **Build -> launch:** actual executable path/hash, source tree plus candidate diff, dependency and plugin hashes, configuration and private input manifest. Launcher checks existence/identity before guest execution and emits a precise error rather than an empty window presented as success.
4. **App -> runtime:** configure paths/backend before initialization, retain SDK lifecycle and ownership, use guest dispatcher and memory, shutdown in supported order. Do not run callbacks against destroyed runtime objects. Host UI and guest threads follow SDK ownership; audit exact source before any custom callbacks.
5. **Guest services -> host content:** translate paths/status/completion semantics, preserve case-sensitive host access with an explicit guest mapping, separate read-only content from writable saves. Input validation does not rewrite game data. Never assume an SDK mount is read-only without testing.
6. **Guest GPU -> Vulkan:** retain existing command processor and translation/resource caches; diagnose defects using packet/shader/resource identities locally. A feature requirement must map to a queried capability or a faithful tested SDK path. Record selected plugin/device, real work, presentation and resource lifetime.
7. **Host controls -> guest API:** event sample/controller identity -> guest-visible state -> observed game response. Distinguish no-device from neutral state, handle hotplug/focus without stale input, no fabricated progress. Keep exact axis conventions and dead zones based on pinned SDL bridge/source and observed behavior.
8. **Media/streaming -> guest scheduler:** preserve ordering, guest error codes, interrupts/completions and clocks; log starvation and missing paths. Do not add arbitrary sleeps to conceal races or report successful decoding without data.
9. **Runtime -> proof:** monotonic timestamps mapped to capture time, run/source/binary/device IDs and subsystem faults; raw events private. Repeated failures are summarized without dropping the first cause. Evidence links and hashes survive later reruns.

## SDK defect boundary

Use existing source first. A defect reproduced with an original synthetic case belongs to SDK patch scope. An actual title-specific configuration/import gap belongs to project glue; proprietary analysis stays private. Record why each fix sits in its chosen layer. No blanket exception suppression or patch imported from an unverified community report. Unit tests cannot establish gameplay acceptance.

## Data and publication boundaries

No source input, title-derived generated code, private manifest, icon/string extraction, raw memory, saves, footage or shader caches is included in public commits by default. Original build/tool/adapters are reviewed separately for provenance. Root README/research and six initial dirty files remain untouched until an authorized evidence-grounded documentation update requires a specific edit. Final staging is explicit and scoped.
