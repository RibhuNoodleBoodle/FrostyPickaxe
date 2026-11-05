# Repository and local evidence

Audit: 2026-11-05. Supersedes the earlier 2026-11-02/03 inventory and all conflicting handoff statements. Classification: LOCAL_OBSERVATION unless stated otherwise.

## Workspace

Standalone documentation repository, origin previously recorded as `https://github.com/RibhuNoodleBoodle/FrostyPickaxe`. Observed HEAD `5ead9cc` (Phase 0 documentation). No SDK checkout, submodule declaration, source tree, build configuration, extracted game directory or generated output was observed. The original researcher mandate remains unchanged as historical task instructions.

Both user-supplied inputs now exist. Nothing was extracted to disk, decrypted, patched or executed. Python standard-library inspection read the ISO filesystem/XEX outer headers and streamed the ZIP member's outer metadata in memory. Full ISO hashing and full ZIP CRC/signature verification were not performed. A computed SHA-256 identifies bytes; it does not establish authenticity or legal provenance.

## ISO observations

| Field | Observation |
| --- | --- |
| Filename | `Rise of the Tomb Raider.iso` |
| File length | 7,838,695,424 bytes |
| XDVDFS partition base | `0xFD90000` |
| Volume header | `MICROSOFT*XBOX*MEDIA` at base + 32 × 2048 |
| Root directory | sector 257381, length 2048 |
| Executable | `default.xex`, sector 663503, 16,531,456 bytes |
| Executable SHA-256 | `47e6476f6d393d86612e7af938979e9c706b54dc526d8422413711999d41e585` |
| Execution info optional key | `0x00040006`, offset `0x2454` within XEX |
| Title / Media ID | `53510823` / `0A657B25` |
| Version / base version | raw `0x00000003` / `0x00000003` |
| Disc number / count | `1 / 1` |
| Entry / image base | `0x82B00790` / `0x82000000` |
| File-format info | offset `0x22B8`; encryption 1, compression 1 |

Root files also include `bigfile.000.nfo`, `bigfile.000.tiger` (2,147,459,120 bytes), `bigfile.001.tiger` (130,651,255 bytes), English/French/Latin-American-Spanish/Dutch `.tiger` archives, `NxeArt`, `tr2.arg`, and directories `movies` and `$SystemUpdate`. Archive contents and runtime usage were not inspected. `$SystemUpdate` is not evidence that the separately supplied game TU has been applied.

This supports a single-disc layout for **this supplied build**. It does not establish the packaging of every regional release or prove no optional content is needed. Prior import counts, TLS interpretations and library-dependent middleware conclusions were not revalidated and are not architecture prerequisites.

## Title-update observations

| Field | Observation |
| --- | --- |
| ZIP | `Rise of the Tomb Raider (Europe, USA) (En) (v6) (2427ED57) (Title Update).zip` |
| ZIP length | 472,244,308 bytes |
| ZIP SHA-256 | `66846d4d898de78000664c11bda069102d1099dca4d05a020110b6afb8c7261d` |
| Sole directory entry | `53510823/000B0000/tu00000006_00000000` |
| Member length / compressed length | 688,193,536 / 472,244,114 bytes |
| ZIP recorded CRC32 | `E887A596` (recorded, not recomputed) |
| Package magic | `LIVE` |
| Header size at `0x340` | `0xAD0E` |
| Content type at `0x344` | `0x000B0000` (title update) |
| Metadata version at `0x348` | 0 |
| Declared content size at `0x34C` | 688,148,480 bytes |
| Media ID at `0x354` | `2427ED57` |
| Version / base version at `0x358` / `0x35C` | raw `0x00000006` / `0x00000006` |
| Title ID at `0x360` | `53510823` |
| Display name | `Rise of Tomb Raider Title Update` |

Offsets were cross-checked against Xenia's XContent metadata structures (S-STFS). These are outer package fields, **not an internal XEXP applicability verdict**. No internal update file table, delta source/target versions, resulting executable hash or package signature/hash tree was validated. Do not interpret raw package base version 6 as proof of a required executable source version, or assume filename v6 identifies an applicable patch.

## Consequence and handling

The update's Media ID differs from the disc executable. This is a critical applicability warning, not proof that every enclosed payload is incompatible. G1 must inspect internal update metadata using suitable lawful local tooling and establish the exact accepted source image. Do not rewrite IDs or force application.

`.gitignore` contains `/*.txt` and `*.iso`. The ISO is ignored; the TU ZIP appears untracked. The four nested prompts are tracked. No assets were staged, committed or uploaded, and no ignore rules changed. Future asset handling must cover update packages, extracted content, generated code and caches before any staging.
