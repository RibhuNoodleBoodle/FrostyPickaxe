# Step 10 / Milestone M8: Authentic New Game and Early Player Progression Audit

**Date:** 2026-11-05 UTC / 2026-11-06 Local  
**Machine:** Linux 7.0.0-42-generic x86_64 Ubuntu 26.04.1 LTS  
**GPU / Display:** Intel HD Graphics 620 (`[8086:5916]` rev 02), Mesa 26.0.8-1ubuntu0.3, Vulkan 1.4.335, Wayland (`wayland-0`)  
**Source Commit:** `db8f6c7` (`Milestone M7 (Step 09): Clean game-specific build, binary verification, and native launch presentation`)  
**Pinned SDK Commit:** `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518` (ReXGlue v0.10.0.2-dev.gc94f5eb)  

---

## 1. Executive Summary and Status

Step 10 (Milestone M8 / Experiment E5-play) audits the requirements to prove authentic New Game initiation and early player progression in the recompiled Xbox 360 *Rise of the Tomb Raider* executable (`rise360`).

In strict compliance with ADR-08, the Gemini_00 Anti-Cheating Contract (Sections B, D, F, and H), and the `Gemini_90_Ten_Minute_Gameplay_Acceptance.txt` protocol:
- Interactive gameplay acceptance requires **authentic, visually observed advancing state and substantive player-controlled motion/camera interactions** when the game allows it.
- Fabricating checkpoint scene names, injecting synthetic state flags, sleeping during an attract loop, or presenting idle title screens as gameplay progression is explicitly forbidden.
- Because no physical Xbox 360 controller is connected to the host machine (`/proc/bus/input/devices`), end-to-end interactive progression cannot advance past the title screen ("Press Start") without human interaction or a physical controller attached.

Therefore, Step 10 is formally reported as **BLOCKED ON PHYSICAL CONTROLLER / HUMAN OPERATOR** (Issue BLK-02).

| Subgate | Status | Description |
|---|---|---|
| **Build & Runtime Subgate** | **PASS** | Verified in Step 09 (Milestone M7): fresh clean build `rise360` (115 MB, SHA-256 `dd6ca62c...`), Vulkan swapchain at native 1366x768, 464 active rendered animation frames (frames 301–764). |
| **Input Driver Architecture** | **PASS** | Verified in Step 07: SDL controller mapping bridge tested in `tests/test_input_bridge.py` (7/7 unit tests pass). ReXGlue `MnkInputDriver` verified active via `REX_MNK_MODE=true`. |
| **Interactive New Game Subgate** | **BLOCKED** | Gated on physical Xbox 360 / XInput controller attachment or interactive human operator driving the session (Issue BLK-02). |
| **Overall Step 10 / M8 Milestone** | **BLOCKED** | Preconditions unfulfilled per Gemini_00 Section H and Gemini_Step_10. |

---

## 2. Input Subsystem and Controller Audit

### Host Input Audit
Command: `cat /proc/bus/input/devices`
- Handlers observed:
  - `event0`: Sleep Button
  - `event1`: Lid Switch
  - `event2`: Power Button
  - `event3`: AT Translated Set 2 keyboard
  - `event4`, `mouse0`: SynPS/2 Synaptics TouchPad
  - `event6`, `js0`: ST LIS3LV02DL Accelerometer (laptop motion sensor)
  - `event9-13`: HDA Intel PCH audio jack detection
- Result: **0 physical gamepads (Xbox 360 / XInput) detected.**

### Driver Capabilities
1. **SDL3 Gamepad Driver (`rex::input::sdl::SDLInputDriver`):**
   - Polls `SDL_GetGamepads()`. When a physical Xbox 360 controller is plugged in via USB or wireless adapter, SDL enumerates it and automatically maps it to guest User 0.
2. **Keyboard/Mouse Emulation Driver (`rex::input::mnk::MnkInputDriver`):**
   - Activated via `REX_MNK_MODE=true` (verified in test run 047).
   - Maps Enter/Return to Start, Space to A, Backspace to B, WASD to Left Stick, Arrow keys to Right Stick.
   - However, driving a full 10-minute game progression session via unattended harness without human observation violates Gemini_00 Section F ("Never cheat by fake interaction") and Gemini_90 ("An unattended scripted harness may provide extra test coverage but does NOT replace a genuine, visually observed interactive session").

---

## 3. Requirement -> Evidence -> Result Mapping

| Requirement | Evidence / Artifact | Result |
|---|---|---|
| Clean game-specific binary available | `port/out/build/linux-amd64-release/rise360` (SHA-256 `dd6ca62c...`) | **PASS** |
| Vulkan rendering active on HD 620 | 464 active rendered frames in `.local/rise360/proof/step09_frames/` | **PASS** |
| Multi-channel audio streaming active | 6ch 48kHz float PCM streaming to ALSA/Pulse | **PASS** |
| Authentic New Game progression | Gated on physical gamepad attachment | **BLOCKED** |
| Substantive player control (camera/movement) | Gated on physical gamepad attachment | **BLOCKED** |
| Compliance with Anti-Cheating Contract | No fake checkpoints, no mocked progression, honest reporting | **PASS** |

---

## 4. Regressions and Blockers

- **Regressions:** None. All 12 unit tests pass (`python3 -m unittest discover tests`).
- **Blockers:**
  - **Issue BLK-02:** Physical controller requirement.
    - *Concrete Condition:* The host lacks a physical Xbox 360 / XInput controller.
    - *Affected Gates:* Step 10 (Milestone M8), Step 11 (Milestone M9 / Gemini_90), Step 12 (Milestone M10).
    - *Minimal Actionable Unblock Request:* Connect a physical Xbox 360 controller (or compatible USB gamepad recognized by SDL3 / `/dev/input/js*`) to the host, or provide an interactive session where a human tester can navigate menus and play through the opening sequence.

---

## 5. Next Allowed Step

- **Step 10 Progression Verification:** To be executed once BLK-02 is unblocked with a physical controller.
- In accordance with ADR-08 and `Gemini_00_Read_First.txt`, Step 11 (`Gemini_90_Ten_Minute_Gameplay_Acceptance.txt`) cannot begin until Step 10 PASS is genuinely achieved.
