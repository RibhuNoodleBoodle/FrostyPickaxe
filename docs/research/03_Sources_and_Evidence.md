# Sources and evidence register

Audit date: 2026-11-05. This register supersedes prior unsupported pins, patch prescriptions and blanket device claims. LOCAL_OBSERVATION, VERIFIED_UPSTREAM_SOURCE, THIRD_PARTY_REPORT, INFERENCE and UNKNOWN are distinct classifications.

| ID | Source | Classification / scope |
| --- | --- | --- |
| L1 | Local `Rise of the Tomb Raider.iso`; XDVDFS directory and outer XEX headers; offsets/hash in `00_Repository_State.md` | LOCAL_OBSERVATION: exact supplied build, not every retail release |
| L2 | Local title-update ZIP; ZIP directory, streamed outer LIVE metadata and ZIP SHA-256; details in `00` | LOCAL_OBSERVATION: package identity, not internal applicability or authenticity |
| L3 | `git status --short`, `git ls-files`, `git log -3 --oneline`, root listing and `.gitignore` | LOCAL_OBSERVATION: docs repository, absent SDK/build, untracked TU ZIP |
| S-STFS | [Xenia XContent/STFS structures](https://raw.githubusercontent.com/xenia-project/xenia/master/src/xenia/vfs/devices/stfs_xbox.h), `XContentMetadata` and embedded execution info; retrieved 2026-11-05 | VERIFIED_UPSTREAM_SOURCE: field layout interpretation; moving branch, no immutable SHA established |
| S-GPU | [ReXGlue device selection](https://raw.githubusercontent.com/rexglue/rexglue-sdk/c94f5ebdcb3c9d1a460ca48e04f9758448f8d518/src/ui/vulkan/vulkan_device.cpp), `CreateIfSupported`, lines 84–127; retrieved 2026-11-05 | VERIFIED_UPSTREAM_SOURCE at exact documentary revision: feature checks; not a local dependency pin |
| S-BUILD | [ReXGlue CMake](https://raw.githubusercontent.com/rexglue/rexglue-sdk/main/CMakeLists.txt); retrieved 2026-11-05 | VERIFIED_UPSTREAM_SOURCE: host/toolchain/backend configuration; moving reference, not a reproducible build baseline |
| S-INTEL | [Intel supported APIs](https://www.intel.com/content/www/us/en/support/articles/000005524/graphics.html), article 000005524; retrieved 2026-11-05 | VERIFIED_UPSTREAM_SOURCE: HD 620 API table, not extension inventory or performance |
| S-TRACKER | [Xenia Canary title issue 174](https://github.com/xenia-canary/game-compatibility/issues/174); page retrieved 2026-11-05 | THIRD_PARTY_REPORT: title issue exists; available page did not expose enough comment detail to revalidate earlier TU/loading and corruption claims |

## Conflicts and evidence limits

1. **Files absent:** superseded by L1/L2. The ISO and TU exist; an extracted or updated executable does not.
2. **Two-disc install/play topology:** contradicted for this supplied build by L1's disc 1/1 metadata and root inventory. Do not require an invented second disc.
3. **TU guaranteed to work:** unsupported; L1/L2 expose different Media IDs. Internal applicability is UNKNOWN, not proven incompatible solely by outer metadata.
4. **SDK pinned/latest stable:** prior tag/branch hashes were inconsistent between files. No installed baseline exists. Only S-GPU's full hash was revalidated as accessible source. GitHub API lookups failed through web; local network DNS was unavailable. No latest-release claim is retained.
5. **HD 620 definitely lacks interlock / passes all checks:** not verified on the user's driver. The Intel API table cannot resolve either claim. Require EXP-05.
6. **Mandatory LUT, exponent, DPC, wait, input mutex and audio pacing patches:** withdrawn as prescriptions. Prior community reports were not revalidated against a selected SDK or this executable. Reproduce a defect and cite the affected source revision before recommending a patch.
7. **Middleware and precise performance:** Wwise/FMOD, Scaleform usage, callback rates, expected FPS and bottleneck causes remain UNKNOWN unless independently evidenced. No binary or benchmark result supports them in this run.

The audit used in-memory read-only inspection without persisting inspection scripts, extracting game files, decrypting payloads or running binaries. No public source validates this private input pair. The ISO's full integrity and the TU's internal signature/hash tree and patch requirements remain unchecked. Future evidence must record tool/version, offsets or source revision, exact input identity, expected/observed result and uncertainty.
