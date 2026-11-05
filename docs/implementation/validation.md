# Validation Matrix & Evidence Mapping

Last updated: 2026-11-05 (Step 01 audit)

---

| Claim / Requirement | ADR / Spec | Status | Observed Evidence & Exit Codes | Location / Artifact |
|---|---|---|---|---|
| Repository baseline established | ADR-04 / Step_01 | **VERIFIED** | HEAD `adf3f12db2d8a1472bd60ce81af424aa92d2c0e6`, branch `main`, remote `origin git@github.com:RibhuNoodleBoodle/FrostyPickaxe.git` | `docs/implementation/commands.md` |
| Six dirty documentation files preserved | ADR-04 / Step_01 | **VERIFIED** | `git status --short` shows 6 modified docs; SHA-256 match E1 reference values | `docs/implementation/commands.md` |
| Base disc ISO ignored | ADR-02 / ADR-04 | **VERIFIED** | `git check-ignore "Rise of the Tomb Raider.iso"` returned 0 | `docs/implementation/commands.md` |
| Title Update ZIP ignored | ADR-02 / ADR-04 | **VERIFIED** | `git check-ignore "Rise of the Tomb Raider ... .zip"` returned 0 | `docs/implementation/commands.md` |
| Private directories excluded from git | ADR-04 | **VERIFIED** | `.local/`, `port/generated/`, `port/rise360_manifest.toml`, `port/out/` all return 0 with `git check-ignore` | `.gitignore`, `docs/implementation/commands.md` |
| Zero private files tracked | ADR-04 | **VERIFIED** | `git ls-files .local/ port/generated/ port/rise360_manifest.toml port/out/` returned 0 lines, exit 0 | `docs/implementation/commands.md` |
| Host OS & Architecture verified | ADR-01 | **VERIFIED** | Ubuntu 26.04.1 LTS x86_64, Linux 7.0.0-42-generic | `docs/implementation/environment.md` |
| Intel HD Graphics 620 Vulkan Support | ADR-01 / ADR-06 | **VERIFIED** | `vulkaninfo --summary` exit 0, Intel HD Graphics 620 [8086:5916], Vulkan 1.4.335, Mesa 26.0.8-1ubuntu0.3 | `docs/implementation/environment.md` |
| Base disc extraction & default.xex SHA-256 | ADR-02 | **VERIFIED** | 84 files provisioned to `.local/rise360/game-base/`; `default.xex` SHA-256 `47e6476f6d393d86612e7af938979e9c706b54dc526d8422413711999d41e585` | `docs/implementation/commands.md` |
| Title Update quarantined | ADR-02 | **VERIFIED** | Outer STFS metadata audited: Media ID `2427ED57` vs Base `0A657B25`; quarantined in `.local/rise360/analysis/` | `docs/implementation/commands.md` |
| ReXGlue SDK Baseline & Test Suite (M1) | ADR-01 / ADR-03 | **VERIFIED** | Pinned commit `c94f5eb`; 1,671 CTest tests executed (1,458 PPC 100%, 209 unit tests 100%, 0 failed); installed to `.local/sdk/rexglue-sdk/out/install/linux-amd64/` | `docs/implementation/commands.md`, `status.md` |
| Strict Codegen & Scaffold (M2) | ADR-04 / ADR-05 | **VERIFIED** | Strict codegen: 45,104 functions recompiled, 207 TUs, 0 validation errors, fingerprint `a726442c842406c1d2bd3305b16bb0b7`; Clang 21 test compile passed | `docs/implementation/commands.md`, `changes.md` |
| Runtime, Guest Services & VFS (M3) | ADR-05 / ADR-06 | **VERIFIED** | Bounded runtime execution: VFS mounted; ALSA/Pulse audio active (6ch 48kHz); 350+ Vulkan pipelines compiled on Intel HD 620; 48 indirect PPC calls resolved; 0 crashes in 20s run 035 (exit code 124) | `docs/implementation/05_Runtime_Guest_Services_and_VFS.md`, `status.md` |
| Vulkan HD 620 Frame Presentation (M4) | ADR-06 | **VERIFIED** | Wayland frame presentation: 673 captured presentation frames (`.local/rise360/proof/`); 147 active animation frames (526-672); 331 unique colors; 1366x768 swapchain on Intel HD 620 | `docs/implementation/06_Vulkan_Frame_Presentation.md`, `status.md` |
| Authentic 10-Minute Gameplay Acceptance | ADR-08 / Gemini_90 | **NOT TESTED** | Blocked on Steps 07-10 | Dependent on future milestones |
