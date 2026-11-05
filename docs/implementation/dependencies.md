# Dependencies & Provenance Record

Last updated: 2026-11-05 (Step 01 baseline)
Architect: ChatGPT Astra
Implementer: Gemini Flash

---

## 1. Selected SDK Baseline (ADR-03)
- **Repository**: `https://github.com/rexglue/rexglue-sdk.git`
- **Target Checkout Path**: `.local/sdk/rexglue-sdk/` (excluded by `.gitignore`)
- **Pinned Commit**: `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518`
- **Submodules Policy**: Strict recursive gitlink checkouts via `git submodule update --init --recursive`. No floating `--remote` updates allowed.
- **Acquisition State**: Pending acquisition in Step 03.
- **License**: ReXGlue MIT / 3-Clause BSD / Apache 2.0 (to be audited upon checkout from `LICENSE`). ReXGlue SDK license confers no rights to game content or proprietary assets.

## 2. Host Build System & Compiler Dependencies
- **CMake**: `4.2.3` (Installed, system)
- **Ninja**: `1.13.2` (Installed, system)
- **Compiler**: GCC / G++ `15.2.0` (`/usr/bin/gcc`, `/usr/bin/g++`) supporting standard C++23.
- **C++ Standard**: C++23 required by ReXGlue `CMakeLists.txt`.
- **Python**: `3.14.4` for local build/discovery scripts.

## 3. Graphics & Presentation Dependencies
- **Vulkan Loader**: `1.4.341` (System libvulkan.so.1)
- **Mesa Driver**: `26.0.8-1ubuntu0.3` (ANV / Intel Mesa driver)
- **Wayland / X11**: Wayland compositor `kwin_wayland` (`wayland-0`), Xwayland display `:0`.
- **Target Backend**: Vulkan via ReXGlue `rexgpu-xenos` shared runtime plugin. Direct3D 12 disabled (`-DREXGLUE_USE_D3D12=OFF`).

## 4. Input & Audio Middleware
- **SDL3**: Submodule bundled in ReXGlue (`thirdparty/sdl3`). Exact commit and build flags to be locked upon Step 03 checkout.

## 5. Proprietary Input Sources (ADR-02, Private)
- **Base Disc Image**: `Rise of the Tomb Raider.iso` (7,838,695,424 bytes, local root, ignored). Title ID `53510823`, Media ID `0A657B25`, Version 3.
- **Title Update Package**: `Rise of the Tomb Raider (Europe, USA) (En) (v6) (2427ED57) (Title Update).zip` (472,244,308 bytes, local root, ignored). Title ID `53510823`, Media ID `2427ED57`, Version 6.
- Both inputs are kept immutable, excluded from version control, and processed strictly locally within `.local/rise360/`.
