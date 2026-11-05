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

## Step 03 Execution Log

| Date / UTC | Working Directory | Command | Exit Code | Purpose / Output Summary |
|---|---|---|---|---|
| 2026-11-05 15:25 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `git clone https://github.com/rexglue/rexglue-sdk.git .local/sdk/rexglue-sdk` | `0` | Cloned ReXGlue SDK repository |
| 2026-11-05 15:27 UTC | `/mnt/6421-8598/building/FrostyPickaxe/.local/sdk/rexglue-sdk` | `git checkout c94f5ebdcb3c9d1a460ca48e04f9758448f8d518` | `0` | Checked out pinned SDK commit |
| 2026-11-05 15:28 UTC | `/mnt/6421-8598/building/FrostyPickaxe/.local/sdk/rexglue-sdk` | `git submodule update --init --recursive` | `0` | Checked out all 22 recursive submodules |
| 2026-11-05 15:32 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `cmake --preset ninja-multi-config -B .local/sdk/rexglue-sdk/out/build/linux-amd64` | `0` | Configured ReXGlue with Clang 21 toolchain and Vulkan backend |
| 2026-11-05 15:58 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `cmake --build .local/sdk/rexglue-sdk/out/build/linux-amd64 --config Release -j4` | `0` | Built Release configuration: CLI, runtime, GPU plugin, SDL3, tests |
| 2026-11-05 15:59 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `ctest --test-dir .local/sdk/rexglue-sdk/out/build/linux-amd64 -C Release --output-on-failure` | `0` | 1,671 tests executed: 1,458 PPC instructions passed (100%), 209 unit tests passed (100%), 4 skipped, 0 failed |
| 2026-11-05 16:00 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `cmake --install .local/sdk/rexglue-sdk/out/build/linux-amd64 --config Release` | `0` | Installed to `.local/sdk/rexglue-sdk/out/install/linux-amd64/` |
| 2026-11-05 16:00 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `.local/sdk/rexglue-sdk/out/install/linux-amd64/bin/rexglue --help` | `0` | Verified installed CLI binary functional |

## Step 04 Execution Log

| Date / UTC | Working Directory | Command | Exit Code | Purpose / Output Summary |
|---|---|---|---|---|
| 2026-11-05 16:03 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `rexglue init --project-name rise360 --project-root .local/rise360/scaffold --xex-path .../default.xex --game-root .../game-base --scan-dll` | `0` | Initialized reference project scaffold in `.local/rise360/scaffold/` |
| 2026-11-05 16:04 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `cp scaffold/{CMakeLists.txt, CMakePresets.json, src/*} port/` | `0` | Adapted generic build glue into `port/` repository tree |
| 2026-11-05 16:11 UTC | `/mnt/6421-8598/building/FrostyPickaxe/port` | `rexglue codegen rise360_manifest.toml --ignore-stamp` | `0` | Strict translation completed in 149.6s; 45,104 functions recompiled into 207 C++ TUs; 0 validation errors |
| 2026-11-05 16:15 UTC | `/mnt/6421-8598/building/FrostyPickaxe/port` | `rexglue codegen rise360_manifest.toml` | `0` | Cache stamp verification: 0 written, 1 up to date in 0.2s |
| 2026-11-05 16:15 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `cmake --preset linux-amd64-release -S port` | `0` | Configured `rise360` host application and recomp object targets with Clang 21 |
| 2026-11-05 16:16 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `ninja -C port/out/build/linux-amd64-release CMakeFiles/rise360.dir/src/main.cpp.o` | `0` | Clean test compilation of `main.cpp.o` |
| 2026-11-05 16:16 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `ninja -C port/out/build/linux-amd64-release CMakeFiles/rise360_recomp.dir/generated/default/rise360_recomp.0.cpp.o` | `0` | Clean test compilation of recompiled PCH and translation unit 0 |


## Step 05 Execution Log

| Date / UTC | Working Directory | Command | Exit Code | Purpose / Output Summary |
|---|---|---|---|---|
| 2026-11-05 16:30 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `ninja -C port/out/build/linux-amd64-release rise360` | `0` | Full parallel build of 207 recompiled translation units and final `rise360` binary linkage with Clang 21 |
| 2026-11-05 16:32 - 18:56 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `LD_LIBRARY_PATH=... timeout 10-20 ./port/out/build/linux-amd64-release/rise360 --headless` | `134` (001-034) / `124` (035, 036) | Runtime probe iterations 001 to 035 resolving PPC indirect calls; run 035 ran 20s cleanly with 0 crashes, 0 SIGABRT (exit code 124 timeout) |
| 2026-11-05 19:02 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `LD_LIBRARY_PATH=.local/sdk/rexglue-sdk/out/install/linux-amd64/lib timeout 5 ./port/out/build/linux-amd64-release/rise360 --headless` | `124` | Reproducible verification run 036 (5.0s, clean exit code 124) |

## Step 06 Execution Log

| Date / UTC | Working Directory | Command | Exit Code | Purpose / Output Summary |
|---|---|---|---|---|
| 2026-11-05 19:05 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `vulkaninfo --summary` | `0` | Probed physical devices: Intel HD Graphics 620 [8086:5916], Vulkan 1.4.335, Mesa 26.0.8-1ubuntu0.3, Wayland surface support |
| 2026-11-05 19:06 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `LD_LIBRARY_PATH=... timeout 5 ./port/out/build/linux-amd64-release/rise360` | `124` | Test run 037 under Wayland GUI: swapchain created at 1366x768 format 44; 219 cached pipelines loaded; 0 crashes |
| 2026-11-05 19:08 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `VK_INSTANCE_LAYERS=VK_LAYER_MESA_screenshot VK_LAYER_MESA_SCREENSHOT_CONFIG="frames=all,output_dir=.../.local/rise360/proof,log_type=info" LD_LIBRARY_PATH=... timeout 5 ./port/out/build/linux-amd64-release/rise360` | `124` | Test run 038 with Vulkan screenshot layer: captured frames 0-103; verified 1280x720 and 1366x768 PNG outputs |
| 2026-11-05 19:09 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `VK_INSTANCE_LAYERS=VK_LAYER_MESA_screenshot VK_LAYER_MESA_SCREENSHOT_CONFIG="frames=all,output_dir=.../.local/rise360/proof,log_type=info" LD_LIBRARY_PATH=... timeout 30 ./port/out/build/linux-amd64-release/rise360` | `124` | 30s empirical presentation run 039: captured 673 frames (0-672); 147 non-black active animation frames (331 unique colors); 0 crashes |
| 2026-11-05 19:10 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `python3 [PIL analysis of proof PNGs]` | `0` | Analyzed color distributions, pixel extrema, and ASCII profiles across all 673 captured presentation frames |

## Step 07 Execution Log

| Date / UTC | Working Directory | Command | Exit Code | Purpose / Output Summary |
|---|---|---|---|---|
| 2026-11-05 19:14 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `cat /proc/bus/input/devices` | `0` | Audited host input devices: keyboard, mouse, ST LIS3LV02DL accelerometer (`js0`); confirmed no physical Xbox 360 controller connected |
| 2026-11-05 19:19 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `python3 -m unittest tests/test_input_bridge.py` | `0` | Ran 7 synthetic mapping test cases: buttons, axes, Y-inversion, triggers, deadzones, packet counters, and disconnects (all passed) |
| 2026-11-05 19:19 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `python3 -m unittest discover tests` | `0` | Full unit test discovery across `tests/`: 12/12 passed (0.002s) |

## Step 08 Execution Log

| Date / UTC | Working Directory | Command | Exit Code | Purpose / Output Summary |
|---|---|---|---|---|
| 2026-11-05 19:21 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `python3 [base_manifest.json media inventory]` | `0` | Inventoried 84 base files: verified `bigfile.000.tiger` (2.14GB), `bigfile.001.tiger` (130MB), 4 language packs, and 71 cinematic Bink videos (`.bik`) |
| 2026-11-05 19:22 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `df -h /dev/shm; free -m` | `0` | Diagnosed POSIX shared memory file accumulation; cleaned stale files |
| 2026-11-05 19:24 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `ninja -C port/out/build/linux-amd64-release rise360` | `0` | Recompiled `rise360` with `CleanStaleShm()` hook in `rise360_app.h` |
| 2026-11-05 19:25 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `LD_LIBRARY_PATH=... timeout 15 ./port/out/build/linux-amd64-release/rise360` | `124` | 15s verification run 043: active 6ch 48kHz audio streaming; verified `CleanStaleShm()` active; 0 leaks |
| 2026-11-05 19:25 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `LD_LIBRARY_PATH=... timeout 3 ./port/out/build/linux-amd64-release/rise360 --headless` | `124` | Verified startup stale SHM cleanup in run 044 |

## Step 09 Execution Log

| Date / UTC | Working Directory | Command | Exit Code | Purpose / Output Summary |
|---|---|---|---|---|
| 2026-11-05 19:28 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `ninja -C port/out/build/linux-amd64-release -t clean rise360` | `0` | Cleaned 424 build artifacts for clean milestone compilation |
| 2026-11-05 19:44 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `ninja -C port/out/build/linux-amd64-release rise360 -j4` | `0` | Clean build of all 207 recompiled translation units and linkage of `rise360` binary (171.2s) |
| 2026-11-05 19:45 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `sha256sum port/out/build/linux-amd64-release/rise360` | `0` | `dd6ca62cdb61da96804e8a9ca27041c78c52378cf2f4a48af0f233ee7bcc219b` |
| 2026-11-05 19:45 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `WAYLAND_DISPLAY=wayland-0 DISPLAY=:0 SDL_VIDEO_DRIVER=wayland VK_INSTANCE_LAYERS=VK_LAYER_MESA_screenshot VK_LAYER_MESA_SCREENSHOT_CONFIG="frames=all,output_dir=.../step09_frames,log_type=info" LD_LIBRARY_PATH=... timeout 10 ./port/out/build/linux-amd64-release/rise360` | `124` | 10s initial launch run 045: captured 266 frames during asset loading phase |
| 2026-11-05 19:47 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `WAYLAND_DISPLAY=wayland-0 DISPLAY=:0 SDL_VIDEO_DRIVER=wayland VK_INSTANCE_LAYERS=VK_LAYER_MESA_screenshot VK_LAYER_MESA_SCREENSHOT_CONFIG="frames=all,output_dir=.../step09_frames,log_type=info" LD_LIBRARY_PATH=... timeout 35 ./port/out/build/linux-amd64-release/rise360` | `124` | 35s verification run 046: captured 765 frames (0-764); 464 active non-black rendered animation frames (301-764, 331 colors); 0 crashes |
| 2026-11-05 19:47 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `python3 [PIL frame analysis script]` | `0` | Verified 464 active non-black frames; verified native 1366x768 format 44 presentation |
| 2026-11-05 19:47 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `python3 -m unittest discover tests` | `0` | Verified 12/12 unit tests passing in `tests/` |

## Step 10 Execution Log

| Date / UTC | Working Directory | Command | Exit Code | Purpose / Output Summary |
|---|---|---|---|---|
| 2026-11-05 19:51 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `cat /proc/bus/input/devices && ls -la /dev/input` | `0` | Audited host input devices: confirmed 0 physical gamepads connected |
| 2026-11-05 19:53 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `REX_MNK_MODE=true LD_LIBRARY_PATH=... timeout 5 ./port/out/build/linux-amd64-release/rise360 --headless` | `124` | Verified `REX_MNK_MODE=true` cvar override applied cleanly (`test_mnk_047.log`) |
| 2026-11-05 19:54 UTC | `/mnt/6421-8598/building/FrostyPickaxe` | `python3 -m unittest discover tests` | `0` | Confirmed 12/12 unit tests passing (0.001s) |
