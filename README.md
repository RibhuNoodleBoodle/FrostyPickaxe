# FrostyPickaxe

Research into a native PC x86-64 recompilation of **Rise of the Tomb Raider for Xbox 360**, using ReXGlue, Vulkan and SDL3, with Intel HD Graphics 620 as the performance target. Android ARM64 is deferred until PC compatibility and performance are demonstrated.

**Status — 2026-11-05:** research and architecture preparation only. No local SDK, code generation, build, boot, rendering or performance result exists.

The original ISO and a title-update ZIP are now available locally. Read-only metadata inspection confirms Title ID `53510823` in both, but **their Media IDs differ**: ISO executable `0A657B25`, update package `2427ED57`. Update applicability remains unverified. Do not assume that owning both inputs means an updated executable can be produced.

The supplied executable reports **disc 1 of 1**; the observed disc root contains the executable, `.tiger` archives and movies. The earlier two-disc install/play assumption has been withdrawn. No mandatory second-disc mount is justified by this evidence.

Start with [the research report](docs/research/01_Feasibility_Report.md), [local evidence](docs/research/00_Repository_State.md), [risks and gates](docs/research/02_Risks_Unknowns_and_Gates.md), and [sources](docs/research/03_Sources_and_Evidence.md). For a separate design session, use [the architecture handoff](gemini_argon/Gemini_Argon_04_Architecture_Handoff.txt), which reads the other three prompts first.

The next step is **architectural discovery**, beginning with update applicability and an evidence-based SDK selection. It does not authorize implementation. Intel's API support table is not a gameplay benchmark or an extension inventory for the user's driver.

Game files remain private and must not be committed or uploaded. The ISO is ignored; the update ZIP is currently untracked and is **not covered by the existing ignore rules**. No ignore/build configuration was changed during this documentation-only audit. Independently redistributable tooling and game data require separate provenance and licensing review; ownership alone is not a distribution license. This project is unaffiliated with the game's publishers and developers.
