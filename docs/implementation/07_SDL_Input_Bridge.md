# Step 07 Report: SDL-to-Guest Controller Semantics & Mapping Bridge

- **Step ID**: 07 — Implement and prove SDL-to-guest controller semantics (Revision 2)
- **Milestone Subgate**: E3-input (Preparatory Verification)
- **Date**: 2026-11-06
- **Host**: Linux 7.0.0-42-generic x86_64 / Ubuntu 26.04.1 LTS
- **Display / Windowing**: Wayland (`wayland-0` via SDL3 Wayland backend)
- **Predecessor Source Commit**: `7641faf` (Milestone M4)
- **SDK Pinned Commit**: `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518` (ReXGlue v0.10.0.2-dev)
- **Status**: **PREPARATORY VERIFIED / BLOCKED ON PHYSICAL CONTROLLER FOR FULL M5 ACCEPTANCE**

---

## 1. Executive Summary

Step 07 inspects, verifies, and tests the SDL3-to-guest XInput controller mapping bridge for the recompiled Xbox 360 *Rise of the Tomb Raider* executable (`rise360`).

In accordance with ADR-07 and the modular architecture, ReXGlue's native input pipeline (`rex::input::InputSystem` and `rex::input::SDLInputDriver`) attaches directly to the host SDL3 window. The driver initialises the SDL gamepad subsystem (`SDL_INIT_GAMEPAD`), maps host joystick events into standard guest Xbox 360 `X_INPUT_STATE` structures, applies hardware deadzones and Y-axis coordinate inversions, and responds to guest `XamInputGetState` and `XamInputSetState` kernel calls.

A dedicated synthetic test suite (`tests/test_input_bridge.py`, 7/7 tests passing) was implemented to verify button bitmask lookups, trigger scaling, deadzone thresholds, packet counter increment semantics, and hotplug disconnect transitions. Full Milestone M5 end-to-end interactive acceptance requires a physical Xbox 360 controller attached to the host, recorded in `docs/implementation/blockers.md` as Issue BLK-02.

---

## 2. Input Subsystem Architecture

### 2.1 Initialization & Event Queue (`rex::input::SDLInputDriver`)
- **Initialization**: Initialized on the UI/display thread via `SDL_InitSubSystem(SDL_INIT_GAMEPAD)`.
- **Event Handling**: Host SDL events (`SDL_EVENT_GAMEPAD_ADDED`, `SDL_EVENT_GAMEPAD_REMOVED`, `SDL_EVENT_GAMEPAD_AXIS_MOTION`, `SDL_EVENT_GAMEPAD_BUTTON_DOWN`, `SDL_EVENT_GAMEPAD_BUTTON_UP`) are queued via `HandleEvent()` and drained synchronously into `ProcessEventLocked()`.
- **Locking & Deadlock Prevention**: Lock ordering separates `event_queue_mutex_` from `controllers_mutex_` to prevent inversion deadlocks with SDL internal joystick locks.

### 2.2 Host to Guest Mapping Contracts
1. **Buttons (15 Gamepad Buttons)**:
   Mapped via `xbutton_lookup` table to exact Xbox 360 bitmasks:
   - `SDL_GAMEPAD_BUTTON_SOUTH` -> `XINPUT_GAMEPAD_A` (`0x1000`)
   - `SDL_GAMEPAD_BUTTON_EAST` -> `XINPUT_GAMEPAD_B` (`0x2000`)
   - `SDL_GAMEPAD_BUTTON_WEST` -> `XINPUT_GAMEPAD_X` (`0x4000`)
   - `SDL_GAMEPAD_BUTTON_NORTH` -> `XINPUT_GAMEPAD_Y` (`0x8000`)
   - D-Pad: `DPAD_UP` (`0x0001`), `DPAD_DOWN` (`0x0002`), `DPAD_LEFT` (`0x0004`), `DPAD_RIGHT` (`0x0008`)
   - Triggers/Shoulders: `LEFT_SHOULDER` (`0x0100`), `RIGHT_SHOULDER` (`0x0200`)
   - System: `START` (`0x0010`), `BACK` (`0x0020`), `GUIDE` (`0x0400`)
   - Stick clicks: `LEFT_THUMB` (`0x0040`), `RIGHT_THUMB` (`0x0080`)
2. **Thumbsticks**:
   - `SDL_GAMEPAD_AXIS_LEFTX` / `RIGHTX`: Sint16 `[-32768, 32767]` directly mapped to `thumb_lx` / `thumb_rx`.
   - `SDL_GAMEPAD_AXIS_LEFTY` / `RIGHTY`: Inverted via bitwise NOT (`~event.gaxis.value`) to match Xbox 360 PowerPC coordinate conventions (positive Y = up).
3. **Triggers**:
   - `SDL_GAMEPAD_AXIS_LEFT_TRIGGER` / `RIGHT_TRIGGER`: Sint16 `[0, 32767]` scaled to 8-bit unsigned integer `[0, 255]` via `value >> 7`.
4. **Deadzone Standards**:
   - Left Thumb Deadzone: `7849`
   - Right Thumb Deadzone: `8689`
   - Trigger Threshold: `30`

### 2.3 Guest Polling (`xam_input.cpp`)
The guest engine calls `XamInputGetState(user_index, flags, &input_state)`:
- Queries are routed to `rex::input::InputSystem::GetState()`.
- Active user is pinned to slot 0 (`XINPUT_FLAG_ANY_USER`).
- If no pad is attached, returns `X_ERROR_DEVICE_NOT_CONNECTED` (`1167`).
- When a pad is attached, copies `X_INPUT_STATE` and updates packet sequence counter.

---

## 3. Synthetic Verification Suite (`tests/test_input_bridge.py`)

To ensure mapping accuracy without modifying upstream ReXGlue code, `tests/test_input_bridge.py` verifies:

| Test Case | Method | Result | Notes |
|---|---|---|---|
| Button Mapping | `test_all_gamepad_buttons_mapped` | **PASS** | Verified 15/15 SDL3 buttons map to XInput bitmasks |
| Composite Buttons | `test_composite_button_state` | **PASS** | Verified multi-button bitwise OR combination |
| Axis & Inversion | `test_axis_conversion_and_y_inversion` | **PASS** | Verified signed range and vertical axis inversion |
| Trigger Scaling | `test_trigger_normalization` | **PASS** | Verified 16-bit to 8-bit unsigned conversion |
| Deadzone Filtering | `test_deadzone_filtering` | **PASS** | Verified left/right thumb and trigger thresholds |
| Packet Counters | `test_packet_counter_increments` | **PASS** | Verified sequence number increment on state transition |
| Disconnect Semantics | `test_disconnect_semantics` | **PASS** | Verified `X_ERROR_DEVICE_NOT_CONNECTED` on unoccupied slots |

Command executed:
```bash
python3 -m unittest discover tests
# Ran 12 tests in 0.002s (5 provisioner + 7 input bridge) -> OK
```

---

## 4. Current Device State & Blocker Audit

- **Host Device Inventory**:
  Inspection of `/dev/input/` and `/proc/bus/input/devices` indicates standard laptop devices (keyboard, touchpad, accelerometer sensor `js0`). No physical Xbox 360 controller is currently plugged in via USB or paired via Bluetooth.
- **Milestone M5 Scope Constraint**:
  Per Gemini_00 Section H and Gemini_Step_07 criteria:
  > "PASS requires genuine controller-to-guest-to-visible-game response and relevant edge behavior; enumerated SDL device alone is insufficient. Preparatory tests are recorded separately; unavailable controller/graphics blocks full M5."
  Full Milestone M5 is therefore marked as **PREPARATION PASS / BLOCKED ON PHYSICAL CONTROLLER FOR END-TO-END ACCEPTANCE** (recorded as Issue BLK-02).
- **Independent Ready Work**:
  In accordance with the project DAG (`docs/architecture/03_Discovery_Plan_and_Gates.md`), Step 08 (Milestone M6 — Audio, Media, Streaming, and Timing) is an independent ready branch and proceeds immediately.

---

## 5. Conclusion & Next Steps

1. Preparatory synthetic input verification for Step 07 is **PASSED**.
2. Milestone M5 status: **BLOCKED on physical controller for interactive acceptance**.
3. Immediate next step: **Step 08 (Milestone M6) — Complete required audio, media, streaming and timing paths**.
