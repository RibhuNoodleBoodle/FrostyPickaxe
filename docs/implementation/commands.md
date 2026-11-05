# Executed Commands Log

Last updated: 2026-11-05 (Step 01 repository audit & privacy setup)

---

## Step 01 Execution Log

| Date / UTC | Working Directory | Command | Exit Code | Purpose / Output Summary |
|---|---|---|---|---|
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git rev-parse --show-toplevel` | `0` | Verified repository root: `/mnt/6421-8598/building/FrostyPickaxe` |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git rev-parse HEAD` | `0` | Verified baseline commit: `adf3f12db2d8a1472bd60ce81af424aa92d2c0e6` |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git branch --show-current` | `0` | Verified active branch: `main` |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git status --short` | `0` | Verified 6 modified doc files and untracked docs/architecture, gemini_flash |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git remote -v` | `0` | `origin git@github.com:RibhuNoodleBoodle/FrostyPickaxe.git` (fetch & push) |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `uname -srmo` | `0` | `Linux 7.0.0-42-generic x86_64 GNU/Linux` |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `cat /etc/os-release` | `0` | `Ubuntu 26.04.1 LTS (Resolute Raccoon)` |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `cmake --version` | `0` | `cmake version 4.2.3` |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `ninja --version` | `0` | `1.13.2` |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `gcc --version` | `0` | `gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0` |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `lspci -nn` | `0` | Intel HD Graphics 620 [8086:5916] (rev 02) |
| 2026-11-05 15:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `vulkaninfo --summary` | `0` | Intel HD Graphics 620 Vulkan 1.4.335 Mesa 26.0.8 |
| 2026-11-05 15:12 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git check-ignore "Rise of the Tomb Raider.iso"` | `0` | Verified ignored |
| 2026-11-05 15:12 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git check-ignore "Rise of the Tomb Raider ... (Title Update).zip"` | `0` | Verified ignored |
| 2026-11-05 15:12 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git check-ignore ".local/" "port/generated/" "port/rise360_manifest.toml" "port/out/"` (pre-edit) | `1` | Detected unignored private paths |
| 2026-11-05 15:12 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git check-ignore ".local/" "port/generated/" "port/rise360_manifest.toml" "port/out/"` (post-edit) | `0` | Verified all 4 private architecture paths now ignored |
| 2026-11-05 15:12 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git ls-files .local/ port/generated/ port/rise360_manifest.toml port/out/` | `0` | Confirmed zero restricted files are tracked |
| 2026-11-05 15:12 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `sha256sum README.md .gitignore docs/research/*.md gemini_argon/*.txt ...` | `0` | Baseline SHA-256 checks matched E1 reference values |

## Step 02 Execution Log

| Date / UTC | Working Directory | Command | Exit Code | Purpose / Output Summary |
|---|---|---|---|---|
| 2026-11-05 15:17 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `python3 -m unittest discover tests` | `0` | 5 unit tests ran in 0.001s, validating GDFX parser and bounds checking |
| 2026-11-05 15:18 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `python3 tools/analyze_tu.py --zip ... --report .local/rise360/analysis/tu_analysis.json` | `0` | Quarantined TU analysis; Title ID 53510823, Media ID 2427ED57, Version 6 |
| 2026-11-05 15:21 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `python3 tools/gdfx_provisioner.py --iso ... --out-dir .local/rise360/game-base --manifest .local/rise360/metadata/base_manifest.json` | `0` | Extracted 84 base files from ISO to .local/rise360/game-base/; wrote manifest |
| 2026-11-05 15:21 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `sha256sum .local/rise360/game-base/default.xex` | `0` | `47e6476f6d393d86612e7af938979e9c706b54dc526d8422413711999d41e585` (matches R2) |
| 2026-11-05 15:21 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git check-ignore .local/rise360/game-base/default.xex` | `0` | Confirmed extracted files remain ignored by git |

