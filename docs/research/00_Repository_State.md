# Repository and Asset Inventory (Phase 0 Read-Only Audit — Revised with ISO Inspection)

**Project:** `FrostyPickaxe` — *Rise of the Tomb Raider* (Xbox 360) Native Recompilation Research  
**Audit Date:** 2026-11-03 (Updated following local ISO addition)  
**Analyst Role:** Gemini Argon (Medium Reasoning) — Phase 0 Researcher and Feasibility Analyst  
**Methodology:** Strictly read-only inspection of the local repository, in-memory XDVDFS/XEX2 metadata headers from the user-supplied ISO, and external public upstream metadata. Zero source code generation, compilation, SDK installation, file extraction, decryption, or binary execution occurred.

---

## 1. Repository Identification and Classification

- **Workspace Path:** `/mnt/6421-8598/building/FrostyPickaxe`
- **Classification:** Standalone game-port research repository (NOT an upstream `rexglue-sdk` checkout, fork, or mixed workspace).
- **Git Remote (`origin`):** `https://github.com/RibhuNoodleBoodle/FrostyPickaxe`
- **Branch & Commit State:**
  - Branch: `main`
  - Commit `aa6ccdfb055801d54b6552cfdeda02fd56d68315` (2026-11-02): `"Initial commit"` — added initial `README.md`.
  - Commit `fcee9855881da690af68c2af6059f329afe25af8` (2026-11-02): `"added .gitignore"` — added `/*.txt` (subsequently updated to ignore `*.iso`).

Because this workspace is the user's distinct game-port repository (`FrostyPickaxe`) and not an upstream third-party SDK checkout, updating the root `README.md` directly is safe and mandated by Section 6 of the Phase 0 instructions.

---

## 2. Inventory of Existing, Missing, and Planned Artifacts

### 2.1 What Currently EXISTS in the Repository
1. **Git & Documentation Scaffolding:**
   - `.git/` — Git repository metadata.
   - `.gitignore` — Contains `/*.txt` and `*.iso`, properly preventing both prompt files and the 7.30 GiB game ISO from being staged or committed.
   - `README.md` — Project overview and honest Phase 0 status report.
   - `docs/research/00..03.md` & `gemini_argon/Gemini_Argon_01..04.txt` — Phase 0 feasibility research and Phase 1 Architect handoff deliverables.
2. **User-Supplied Retail Game ISO (Local Only, Gitignored, Inspected Read-Only):**
   - **Filename:** `Rise of the Tomb Raider.iso`
   - **Size:** `7,838,695,424` bytes (`7.3004 GiB` / standard Xbox 360 XGD2 Dual-Layer DVD image; XDVDFS partition magic `MICROSOFT*XBOX*MEDIA` located at partition base `0xFD90000`, header offset `0xFDA0000`).
   - **Crucial Single-Disc Discovery:** Read-only inspection of the XDVDFS directory tree and XEX2 `ExecutionInfo` (`Disc=1/1`) proves that *Rise of the Tomb Raider* (Xbox 360) is a **single-disc retail release (`Disc 1 of 1`)** containing `default.xex`, two core data archives (`bigfile.000.tiger` [2.00 GiB] and `bigfile.001.tiger` [124.6 MB]), four language pack archives (`bigfile_ENGLISH.000.tiger` [815.6 MB], `bigfile_FRENCH.000.tiger` [751.6 MB], `bigfile_LATAMSPANISH.000.tiger` [749.5 MB], `bigfile_DUTCH.000.tiger` [367 KB]), 62 Bink video files (`movies/*.bik`, totaling ~1.69 GiB), `bigfile.000.nfo`, `tr2.arg`, `NxeArt`, and `$SystemUpdate/`. This directly falsifies earlier third-party forum claims of a 2-disc install/play split.

### 2.2 Read-Only Metadata Audit of `default.xex` (Inside `Rise of the Tomb Raider.iso`)
Without extracting, decrypting, or modifying the binary, the unencrypted outer XEX2 header of `default.xex` (XDVDFS sector `663503`, file size `16,531,456` bytes / `0xFC4000`) was parsed in-memory:

| XEX2 Header Field | Verified Value | Architectural Significance |
| :--- | :--- | :--- |
| **File Size & SHA-256** | `16,531,456` bytes (`15.77 MiB`)<br>`47e6476f6d393d86612e7af938979e9c706b54dc526d8422413711999d41e585` | Exact baseline fingerprint for clean-room verification. |
| **Title ID & Media ID** | Title ID: **`0x53510823`** (`53510823`)<br>Media ID: **`0x0A657B25`** | Confirms exact match with Xenia Canary Issue #174 (`53510823`). |
| **Executable Version** | `Ver = 0.0.0.3` (`0x00000003`), `BaseVer = 0.0.0.3`, `Disc = 1/1` | Base retail disc build (`UTR-BUILD08`, dated `2015-09-22` per `tr2.arg`). |
| **Original PE Name** | `IntermediateTR2.exe` | Internal Nixxes / Crystal Dynamics executable name (`TR2` = *Tomb Raider 2* in the reboot trilogy). |
| **Memory Layout & Entry Point** | `ImageBaseAddress = 0x82000000`<br>`EntryPoint = 0x82B00790`<br>`image_size = 0x15B0000` (`22,740,992` bytes / `21.69 MiB`) | Unpacked PE image spans `0x82000000`–`0x835B0000`. |
| **File Format (Encryption & Compression)** | `encryption_type = 1` (**Normal retail AES encryption**)<br>`compression_type = 1` (**Basic zero-run compression**, 4 blocks: `0xFC0000` data + `0x5E8000` zeros = `0x15A8000` unpacked) | **CRITICAL FINDING:** Because the inner PE payload is AES-encrypted (`enc_type = 1`), internal `.pdata` function tables and PowerPC instructions cannot be read until decrypted by XEX loader/tooling. However, `comp_type = 1` (Basic) is much simpler than LZX (`comp_type = 2`). |
| **TLS & Stack Configuration** | `TLSInfo`: `64` slots (`raw_data_addr = 0x834B0C00`, `2,120` bytes)<br>`DefaultStackSize`: `0x40000` (`262,144` bytes / `256 KiB`) | High TLS slot count (`64`) typical of multi-threaded Foundation Engine worker threads. |
| **Import Libraries (`0x000103FF`)** | 2 libraries (`541` total import records):<br>• `xboxkrnl.exe` (v2.0.21256.0): `311` records (~155 imports)<br>• `xam.xex` (v2.0.21256.0): `230` records (~115 imports) | Imports **only** `xboxkrnl.exe` and `xam.xex` — no external dynamic XEX DLL modules required! |
| **Embedded Static Libraries (`0x000200FF`)** | `20` libraries (all XDK **`v2.0.21256.16384`**, plus MSVC `C1`/`C2` `v16.0.11886.17408` and `LIBCPMT`):<br>`D3D9LTCG`, `XGRAPHC`, `XAUDIO2`, `XAPOBA`, `XMCORE`, `XMP`, `XMA`/`XMIC`, `XHV2`, `XNET`, `XONLINE`, `XHTTP`, `XAUTH`, `XSOCPST`, `XPARTY`, `XAPILIB`, `XBOXKRNL` | **CRITICAL FINDING:** Uses **`D3D9LTCG`** (Link-Time Code Generation D3D9) and **`XAUDIO2` + `XMP`**. LTCG inlines D3D9 command-buffer functions into game code, increasing the importance of accurate PM4 ring-buffer and shared-memory translation in ReXGlue. |

### 2.3 What is Still MISSING from the Repository
1. **Xbox 360 Title Update (TU) Package (`UNKNOWN` / Absent Locally):**
   - The ISO provides the base `v0.0.0.3` executable (`MediaID 0A657B25`). As documented in Xenia Canary Issue #174 (`53510823`), the unpatched base build hangs on an infinite loading spinner after pressing Start and **requires a Title Update (TU)** (matching Media ID `0A657B25`) to enter gameplay. No TU package (`tu*` / `.xexp` patch) is present in the workspace yet.
2. **Extracted/Decrypted Game Directory (`game/`):**
   - In accordance with Phase 0 rules, `Rise of the Tomb Raider.iso` was not extracted or decrypted.
3. **ReXGlue SDK & Build Scaffolding (Absent Locally):**
   - No `.gitmodules`, `thirdparty/rexglue-sdk`, `CMakeLists.txt`, `CMakePresets.json`, `<project>_manifest.toml`, `src/`, or `generated/` exist yet.

---

## 3. Upstream ReXGlue SDK Revision Pinning

Upstream `rexglue/rexglue-sdk` was inspected read-only on **2026-11-02**:

| Channel / Branch | Revision / Commit SHA | Date | Key Observations |
| :--- | :--- | :--- | :--- |
| **Latest Stable Release (`main` / `v0.10.0`)** | `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518` (tag `v0.10.0` at `f5337cdc947f`) | 2026-08-21 | Project version `0.10.0` in `CMakeLists.txt`. Requires Clang 18+ and C++23. Pre-built release archives for `win-amd64`, `linux-amd64`, and `linux-arm64`. |
| **Upstream Development (`development` / Nightly)** | `bd833a2ab69d` (`nightly-20261002-bd833a2a`, `0.10.0.24-dev`) | 2026-10-02 | 24 commits ahead of `v0.10.0`. Adds `sync`/`lwsync`/`eieio` memory fences (`bd833a2ab`), `stwcx.` `std::atomic` CAS (`7f7c92ef6`), `vpkuwus`/`vpkuhus` aliasing fix (`6319e236d`), `writable_code_segments` (`5e2dae1dd`), SDL3 `3.4.14` (`4c1350847`), and SDL3 input rumble/deadzone/hotplug refinements (`3cd72439f`). |
| **Upstream Wiki (`rexglue-sdk.wiki.git`)** | `ebc5cc8534cdba659e1c005ca984745f975cf0f3` | 2026-06-04 | **Outdated Status Banner:** `Home.md` still states `"Status: v0.3.x"`, conflicting with the `v0.10.0` source tree. |

---

## 4. Legal, Provenance, and Asset-Handling Rules

1. **Game ISO Ignored by Git:** `Rise of the Tomb Raider.iso` is matched by `*.iso` in `.gitignore` and must never be committed or uploaded.
2. **No Extraction or Decryption in Phase 0:** The ISO was inspected strictly read-only in place. Any future extraction (`rexiso`), retail XEX decryption, or `.xexp` Title Update patching must occur locally in a gitignored directory (`game/`) under explicit user authorization.
3. **Non-Affiliation:** Independent technical feasibility study; not affiliated with or endorsed by Microsoft, Square Enix, Crystal Dynamics, Eidos-Montréal, or Nixxes Software.
