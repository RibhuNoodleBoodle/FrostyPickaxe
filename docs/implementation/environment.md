# Environment & System Inventory Record

Last updated: 2026-11-05 (Step 01 audit)
Host: Linux x86-64 (Ubuntu 26.04.1 LTS "Resolute Raccoon")

---

## 1. Operating System and Kernel
- **Kernel / Machine**: `Linux 7.0.0-42-generic x86_64 GNU/Linux` (`uname -srmo`, exit 0)
- **OS Release**: `PRETTY_NAME="Ubuntu 26.04.1 LTS"`, `VERSION_ID="26.04"`, `VERSION_CODENAME=resolute` (`cat /etc/os-release`, exit 0)
- **User / Session**: User `ribhu`, UID 1000. Graphical session is KDE Plasma 6 running under KWin Wayland (`WAYLAND_DISPLAY=wayland-0`, `DISPLAY=:0` via Xwayland rootless).

## 2. Hardware Inventory
- **CPU**: Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz (2 cores, 4 threads, x86_64)
- **Memory**: 15 GiB total RAM (5.0 GiB used, 5.9 GiB free, 10 GiB available), 0B Swap (`free -h`, exit 0)
- **Disk**: Filesystem `/dev/sda2` mounted on `/mnt/6421-8598`, 354 GB total, 88 GB used, 267 GB available (25% utilization) (`df -h .`, exit 0)
- **GPU (PCI)**: `00:02.0 VGA compatible controller [0300]: Intel Corporation Kaby Lake-U GT2 [HD Graphics 620] [8086:5916] (rev 02)` (`lspci -nn`, exit 0)

## 3. Graphics & Vulkan Capabilities
- **Vulkan Loader**: Instance Version 1.4.341 (`vulkaninfo --summary`, exit 0)
- **Primary GPU (GPU0)**:
  - Device Name: `Intel(R) HD Graphics 620 (KBL GT2)`
  - Vendor ID / Device ID: `0x8086` / `0x5916`
  - Device Type: `PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU`
  - Driver: `Intel open-source Mesa driver` (`DRIVER_ID_INTEL_OPEN_SOURCE_MESA`), version `26.0.8-1ubuntu0.3`
  - API Version: `1.4.335` (Vulkan 1.4 compliant)
  - Conformance Version: `1.4.0.0`
- **Fallback GPU (GPU1)**:
  - Device Name: `llvmpipe (LLVM 21.1.8, 256 bits)`
  - API Version: `1.4.335`
- **Instance Extensions**: 26 extensions present, including `VK_KHR_surface`, `VK_KHR_wayland_surface`, `VK_KHR_xcb_surface`, `VK_KHR_xlib_surface`.

## 4. Installed Toolchain & Compilers
- **CMake**: `cmake version 4.2.3` (`/usr/bin/cmake`, exit 0)
- **Ninja**: `1.13.2` (`/usr/bin/ninja`, exit 0)
- **GCC / G++**: `gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0` / `g++ 15.2.0` (`/usr/bin/gcc`, `/usr/bin/g++`, exit 0)
  - Full C++23 standard support (`-std=c++23`)
- **Clang / LLVM**:
  - `libclang-cpp21` and `libllvm21` installed in `/usr/lib/llvm-21/`
  - Standalone `clang`/`clang++` frontend binary is not present in system PATH (`exit: 1`).
  - GCC 15.2.0 is the primary available C++23 compiler.
- **Python**: `Python 3.14.4` (`/usr/bin/python3`, exit 0)

## 5. Input Devices & Controllers
- `/dev/input/` contains:
  - Touchpad: `SynPS/2 Synaptics TouchPad` (`mouse0`, `event4`)
  - Keyboard: `AT Translated Set 2 keyboard` (`event3`)
  - Accelerometer: `ST LIS3LV02DL Accelerometer` (`js0`, `event6`)
  - Physical Gamepad/Controller: Not currently plugged in. SDL controller mappings and synthetic mock tests can be verified programmatically; physical gamepad interaction is evaluated when connected.

## 6. Repository Baseline
- Root: `/mnt/6421-8598/building/FrostyPickaxe`
- HEAD Commit: `adf3f12db2d8a1472bd60ce81af424aa92d2c0e6` ("More updated docs")
- Branch: `main`
- Remote: `origin git@github.com:RibhuNoodleBoodle/FrostyPickaxe.git`
