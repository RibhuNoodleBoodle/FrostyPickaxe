# Dependencies & Provenance Record

Last updated: 2026-11-05 (Step 01 baseline)
Architect: ChatGPT Astra
Implementer: Gemini Flash

---

## 1. Selected SDK Baseline (ADR-03)
- **Repository**: `https://github.com/rexglue/rexglue-sdk.git`
- **Target Checkout Path**: `.local/sdk/rexglue-sdk/` (excluded by `.gitignore`)
- **Pinned Commit**: `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518`
- **Installation Prefix**: `.local/sdk/rexglue-sdk/out/install/linux-amd64/`
- **CLI Executable**: `.local/sdk/rexglue-sdk/out/install/linux-amd64/bin/rexglue`
- **Submodules Policy**: Strict recursive gitlink checkouts via `git submodule update --init --recursive`. All 22 submodules locked:
  - `thirdparty/FFmpeg`: `0604b464c7cb4ebc94940cf1f324a3b26b87717c`
  - `thirdparty/catch2`: `88abf9bf325c798c33f54f6b9220ef885b267f4f` (v3.12.0)
  - `thirdparty/cli11`: `bfffd37e1f804ca4fae1caae106935791696b6a9` (v1.7.1)
  - `thirdparty/fmt`: `407c905e45ad75fc29bf0f9bb7c5c2fd3475976f` (12.1.0)
  - `thirdparty/glslang`: `f4f1d8a352ca1908943aea2ad8c54b39b4879080`
  - `thirdparty/imgui`: `6d910d5487d11ca567b61c7824b0c78c569d62f0`
  - `thirdparty/inja`: `7d1b4600b68595085a949743331c2e5673f511ea` (v3.5.0)
  - `thirdparty/libmspack`: `305907723a4e7ab2018e58040059ffb5e77db837` (v1.11)
  - `thirdparty/moltenvk`: `db445ff2042d9ce348c439ad8451112f354b8d2a`
  - `thirdparty/o1heap`: `388a73fd9007300e5130c5fe352d9ce3288b6dde` (3.0.0)
  - `thirdparty/sdl3`: `8bf3b7215ad9fc3deb583c6a3a37c6c67f2e24e4` (release-3.4.0-preview)
  - `thirdparty/simde`: `71fd833d9666141edcd1d3c109a80e228303d8d7` (v0.8.2)
  - `thirdparty/spdlog`: `79524ddd08a4ec981b7fea76afd08ee05f83755d`
  - `thirdparty/spirv-headers`: `29981f65241605e08b0ede4cfeb999fe3b723c6a`
  - `thirdparty/spirv-tools`: `9a49b0883b9b635689a85b5647dbfcb223268151`
  - `thirdparty/tomlplusplus`: `30172438cee64926dc41fdd9c11fb3ba5b2ba9de` (v3.4.0)
  - `thirdparty/tracy`: `05cceee0df3b8d7c6fa87e9638af311dbabc63cb` (v0.13.1)
  - `thirdparty/utfcpp`: `63d64de49fd6b829f7c8694df5ab2ee625cb7134`
  - `thirdparty/vulkan-headers`: `e3b1eec08173d6b825cd3ac88c885a63b621504a` (v1.4.357)
  - `thirdparty/vulkan-loader`: `5f157b62e333c63260d05d81bf66faa216ab0fb8`
  - `thirdparty/vulkan-memory-allocator`: `1d8f600fd424278486eade7ed3e877c99f0846b1`
  - `thirdparty/xxHash`: `e626a72bc2321cd320e953a0ccf1584cad60f363` (v0.8.3)
- **Acquisition State**: PASSED (Milestone M1).
- **License**: ReXGlue BSD 3-Clause / MIT / Apache 2.0.

## 2. Host Build System & Compiler Dependencies
- **CMake**: `4.2.3` (Installed, system)
- **Ninja**: `1.13.2` (Installed, system)
- **Compiler**: Clang / Clang++ `21.1.8` configured in `.local/toolchain/bin/clang++` (supporting C++23, x86-64-v3, AVX2, FMA).
- **C++ Standard**: C++23 standard.
- **Python**: `3.14.4` for local build/discovery scripts.

## 3. Graphics & Presentation Dependencies
- **Vulkan Loader**: `1.4.341` (System libvulkan.so.1)
- **Mesa Driver**: `26.0.8-1ubuntu0.3` (ANV / Intel Mesa driver)
- **Wayland / X11**: Wayland compositor `kwin_wayland` (`wayland-0`), Xwayland display `:0`.
- **Target Backend**: Vulkan via ReXGlue `rexgpu-xenos` shared runtime plugin (`out/install/linux-amd64/lib/librexgpu-xenos.so`). Direct3D 12 disabled (`-DREXGLUE_USE_D3D12=OFF`).

## 4. Input & Audio Middleware
- **SDL3**: Pinned commit `8bf3b7215ad9fc3deb583c6a3a37c6c67f2e24e4` (built static into `out/install/linux-amd64/lib/libSDL3.a`).
- **Audio Codec**: FFmpeg AC3/AAC/XMA decoders compiled statically into `out/install/linux-amd64/lib/librexruntime.so`.

## 5. Proprietary Input Sources (ADR-02, Private)
- **Base Disc Image**: `Rise of the Tomb Raider.iso` (7,838,695,424 bytes, local root, ignored). Title ID `53510823`, Media ID `0A657B25`, Version 3.
- **Title Update Package**: `Rise of the Tomb Raider (Europe, USA) (En) (v6) (2427ED57) (Title Update).zip` (472,244,308 bytes, local root, ignored). Title ID `53510823`, Media ID `2427ED57`, Version 6.
- Both inputs are kept immutable, excluded from version control, and processed strictly locally within `.local/rise360/`.
