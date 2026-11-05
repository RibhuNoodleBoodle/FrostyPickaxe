# Flash implementation work packages

Revision 2. Astra is the architect; Flash is the implementer. Start with `gemini_flash/Gemini_00_Read_First.txt`. Read the four architecture documents and `Gemini_03_Pinned_SDK_and_Commands.txt`, then execute the numbered prompts. Each carries the full required step sections. No separate Argon approval is needed.

| Prompt | Concrete deliverable | Dependencies | Allowed scope / completion |
| --- | --- | --- | --- |
| Step_01 | Repository baseline, output exclusions, audit ledger and ready/blocked branch map | Current repository | `.gitignore`, `docs/implementation/`; preserve prior edits, verify private families before writes |
| Step_02 | Verified/provisioned base input identity and manifest; separately classified TU applicability | 01 privacy | Original `tools/`/synthetic `tests/`, private content/analysis; no original-input modification, no bypass |
| Step_03 | Pinned SDK install with recursive dependency/SDL lock, real test results and exact command record | 01, independent of 02 | `.local/sdk/`, original tooling and sanitized docs; baseline only, no game claim |
| Step_04 | Reviewed `rise360` app scaffold and strict game-specific generation | 02 base + 03 | `port/` original build/app files; private manifest/generated data; no publishing derivative code |
| Step_05 | Working required startup/runtime/VFS semantics and missing-import corrections | 04 | `port/src/guest/`, `content/`, thin app, narrow original SDK patches and relevant tests |
| Step_06 | Verified HD 620 Vulkan path and genuine frame evidence | 05 for title run; 01 sufficient for device preflight | Existing SDK backend integration and reproduced corrections; captured evidence private |
| Step_07 | Real SDL-to-guest controls | 05; 06 required only for integrated visual proof | Input adapter only if needed; synthetic tests plus physical end-to-end correlation |
| Step_08 | Required audio/media/streaming and early-scene stability | 05; appropriate 06/07 results for integrated trial | Only proven missing media/content/timing integration; preserve required functionality |
| Step_09 | Fresh authentic game-specific build and launch proof | 04-08 applicable integration results | Clean candidate/build/proof only; fixes go back to owning step |
| Step_10 | Demonstrated New Game and early interactive progression | 09 | Actual observation and proof, not fake flow |
| Step_11 + 90 | At least 600 eligible seconds of observed real gameplay | 10 | Unchanged qualified executable, controller, HD 620 Vulkan and local proof |
| Step_12 | Final clean reproduction, repeat gameplay, measured behavior, legal-content/secret audit and accurate README | 11 | Review/report/reproduce; no final publication yet |
| Gemini_99 | Scoped reviewed commit/push to actual authorized destination | All applicable core M0-M10 gates | No force/history rewrite; only safe original content and verified remote hash |

Each implementation package follows observe -> small change -> test -> record -> decide. Incremental compile/launch is allowed as needed before Step_09, which is the independent milestone verification. Do not make every branch wait for every other branch: use document 03's actual dependencies. Preparatory input/media tests can proceed while graphics is blocked, but cannot be mislabeled full end-to-end passes.

Exact future paths are chosen architecture, not assertions that code exists. SDK API spelling comes from selected source/CLI; project implementation details are Flash's responsibility. First initialize in ignored staging, review outputs and adapt into `port/` without overwriting existing root files. Preserve case and privacy. If a source template's behavior differs from a moving wiki, the verified chosen tree controls.

Routine engineering decisions, narrow bug fixes and selecting available compatible tools do not need another permission loop. A missing empirical prerequisite is reported with its smallest corrective action; continue independent tasks. Scope changes that substitute another game/version, renderer, target, fidelity acceptance, DRM handling or publication rights must not be silently invented.
