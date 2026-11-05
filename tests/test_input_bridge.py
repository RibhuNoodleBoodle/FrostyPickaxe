#!/usr/bin/env python3
"""
Synthetic Unit Test Suite for SDL3 to Guest XInput Mapping Bridge (tests/test_input_bridge.py)

Per Step 07 and ADR-07:
Tests semantic contracts of SDL3 Gamepad events, XInput state translation,
axes/trigger normalization, deadzones, packet numbering, and hotplug disconnect semantics.

NOTE: NOT GAME-SPECIFIC ACCEPTANCE. This verifies input mapping semantics on synthetic
fixtures prior to physical controller attachment.
"""

import unittest
import struct

# XInput Constants (matches rex/input/xinput.h)
XINPUT_GAMEPAD_DPAD_UP        = 0x0001
XINPUT_GAMEPAD_DPAD_DOWN      = 0x0002
XINPUT_GAMEPAD_DPAD_LEFT      = 0x0004
XINPUT_GAMEPAD_DPAD_RIGHT     = 0x0008
XINPUT_GAMEPAD_START          = 0x0010
XINPUT_GAMEPAD_BACK           = 0x0020
XINPUT_GAMEPAD_LEFT_THUMB     = 0x0040
XINPUT_GAMEPAD_RIGHT_THUMB    = 0x0080
XINPUT_GAMEPAD_LEFT_SHOULDER  = 0x0100
XINPUT_GAMEPAD_RIGHT_SHOULDER = 0x0200
XINPUT_GAMEPAD_A              = 0x1000
XINPUT_GAMEPAD_B              = 0x2000
XINPUT_GAMEPAD_X              = 0x4000
XINPUT_GAMEPAD_Y              = 0x8000
XINPUT_GAMEPAD_GUIDE          = 0x0400

# Deadzones
XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE  = 7849
XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE = 8689
XINPUT_GAMEPAD_TRIGGER_THRESHOLD    = 30

# SDL3 Gamepad Button Enum Values
SDL_GAMEPAD_BUTTON_SOUTH         = 0  # A
SDL_GAMEPAD_BUTTON_EAST          = 1  # B
SDL_GAMEPAD_BUTTON_WEST          = 2  # X
SDL_GAMEPAD_BUTTON_NORTH         = 3  # Y
SDL_GAMEPAD_BUTTON_BACK          = 4
SDL_GAMEPAD_BUTTON_GUIDE         = 5
SDL_GAMEPAD_BUTTON_START         = 6
SDL_GAMEPAD_BUTTON_LEFT_STICK    = 7
SDL_GAMEPAD_BUTTON_RIGHT_STICK   = 8
SDL_GAMEPAD_BUTTON_LEFT_SHOULDER = 9
SDL_GAMEPAD_BUTTON_RIGHT_SHOULDER= 10
SDL_GAMEPAD_BUTTON_DPAD_UP       = 11
SDL_GAMEPAD_BUTTON_DPAD_DOWN     = 12
SDL_GAMEPAD_BUTTON_DPAD_LEFT     = 13
SDL_GAMEPAD_BUTTON_DPAD_RIGHT    = 14

# Error codes
X_ERROR_SUCCESS              = 0
X_ERROR_DEVICE_NOT_CONNECTED = 1167
X_ERROR_BAD_ARGUMENTS        = 160


def map_sdl_button_to_xinput(sdl_button: int) -> int:
    """Simulates SDLInputDriver::OnControllerDeviceButtonChangedLocked lookup."""
    lookup = [
        XINPUT_GAMEPAD_A,
        XINPUT_GAMEPAD_B,
        XINPUT_GAMEPAD_X,
        XINPUT_GAMEPAD_Y,
        XINPUT_GAMEPAD_BACK,
        XINPUT_GAMEPAD_GUIDE,
        XINPUT_GAMEPAD_START,
        XINPUT_GAMEPAD_LEFT_THUMB,
        XINPUT_GAMEPAD_RIGHT_THUMB,
        XINPUT_GAMEPAD_LEFT_SHOULDER,
        XINPUT_GAMEPAD_RIGHT_SHOULDER,
        XINPUT_GAMEPAD_DPAD_UP,
        XINPUT_GAMEPAD_DPAD_DOWN,
        XINPUT_GAMEPAD_DPAD_LEFT,
        XINPUT_GAMEPAD_DPAD_RIGHT,
    ]
    if 0 <= sdl_button < len(lookup):
        return lookup[sdl_button]
    return 0


def map_sdl_axis_to_xinput(axis_type: str, sdl_value: int) -> int:
    """
    Simulates SDLInputDriver::OnControllerDeviceAxisMotionLocked.
    SDL left/right sticks: Sint16 [-32768, 32767].
    XInput stick Y is inverted relative to SDL (~value).
    Triggers: Sint16 [0, 32767] -> Uint8 [0, 255] via value >> 7.
    """
    if axis_type in ("thumb_lx", "thumb_rx"):
        return sdl_value
    elif axis_type in ("thumb_ly", "thumb_ry"):
        # PowerPC / XInput Y-inversion
        # Note: in C++ ~event.gaxis.value with Sint16 sign-extended
        val16 = struct.unpack("=h", struct.pack("=H", (~sdl_value) & 0xFFFF))[0]
        return val16
    elif axis_type in ("left_trigger", "right_trigger"):
        if sdl_value <= 0:
            return 0
        return (sdl_value >> 7) & 0xFF
    raise ValueError(f"Unknown axis: {axis_type}")


def apply_deadzone(value: int, deadzone: int) -> int:
    """Applies radial or axial deadzone threshold."""
    if abs(value) < deadzone:
        return 0
    return value


class TestSDLInputBridge(unittest.TestCase):

    def test_all_gamepad_buttons_mapped(self):
        """Verifies 1:1 mapping of all 15 SDL3 gamepad buttons to XInput bitmasks."""
        expected = [
            (SDL_GAMEPAD_BUTTON_SOUTH, XINPUT_GAMEPAD_A),
            (SDL_GAMEPAD_BUTTON_EAST, XINPUT_GAMEPAD_B),
            (SDL_GAMEPAD_BUTTON_WEST, XINPUT_GAMEPAD_X),
            (SDL_GAMEPAD_BUTTON_NORTH, XINPUT_GAMEPAD_Y),
            (SDL_GAMEPAD_BUTTON_BACK, XINPUT_GAMEPAD_BACK),
            (SDL_GAMEPAD_BUTTON_GUIDE, XINPUT_GAMEPAD_GUIDE),
            (SDL_GAMEPAD_BUTTON_START, XINPUT_GAMEPAD_START),
            (SDL_GAMEPAD_BUTTON_LEFT_STICK, XINPUT_GAMEPAD_LEFT_THUMB),
            (SDL_GAMEPAD_BUTTON_RIGHT_STICK, XINPUT_GAMEPAD_RIGHT_THUMB),
            (SDL_GAMEPAD_BUTTON_LEFT_SHOULDER, XINPUT_GAMEPAD_LEFT_SHOULDER),
            (SDL_GAMEPAD_BUTTON_RIGHT_SHOULDER, XINPUT_GAMEPAD_RIGHT_SHOULDER),
            (SDL_GAMEPAD_BUTTON_DPAD_UP, XINPUT_GAMEPAD_DPAD_UP),
            (SDL_GAMEPAD_BUTTON_DPAD_DOWN, XINPUT_GAMEPAD_DPAD_DOWN),
            (SDL_GAMEPAD_BUTTON_DPAD_LEFT, XINPUT_GAMEPAD_DPAD_LEFT),
            (SDL_GAMEPAD_BUTTON_DPAD_RIGHT, XINPUT_GAMEPAD_DPAD_RIGHT),
        ]
        for sdl_btn, xinput_mask in expected:
            with self.subTest(btn=sdl_btn):
                self.assertEqual(map_sdl_button_to_xinput(sdl_btn), xinput_mask)

    def test_composite_button_state(self):
        """Tests bitwise OR combination of multiple simultaneously pressed buttons."""
        buttons = [
            SDL_GAMEPAD_BUTTON_SOUTH,         # A
            SDL_GAMEPAD_BUTTON_RIGHT_SHOULDER,# RB
            SDL_GAMEPAD_BUTTON_START          # Start
        ]
        bitmask = 0
        for b in buttons:
            bitmask |= map_sdl_button_to_xinput(b)

        expected_mask = XINPUT_GAMEPAD_A | XINPUT_GAMEPAD_RIGHT_SHOULDER | XINPUT_GAMEPAD_START
        self.assertEqual(bitmask, expected_mask)

    def test_axis_conversion_and_y_inversion(self):
        """Verifies analog thumbstick axis conversion and vertical axis inversion."""
        # Horizontal axis: no inversion
        self.assertEqual(map_sdl_axis_to_xinput("thumb_lx", 16384), 16384)
        self.assertEqual(map_sdl_axis_to_xinput("thumb_lx", -16384), -16384)
        self.assertEqual(map_sdl_axis_to_xinput("thumb_lx", 0), 0)

        # Vertical axis: bitwise NOT (~value)
        # 0 -> -1
        self.assertEqual(map_sdl_axis_to_xinput("thumb_ly", 0), -1)
        # SDL positive Y is down (+32767); XInput positive Y is up. Inverted: ~32767 = -32768
        self.assertEqual(map_sdl_axis_to_xinput("thumb_ly", 32767), -32768)

    def test_trigger_normalization(self):
        """Verifies trigger 16-bit to 8-bit unsigned conversion (value >> 7)."""
        self.assertEqual(map_sdl_axis_to_xinput("left_trigger", 0), 0)
        self.assertEqual(map_sdl_axis_to_xinput("left_trigger", -100), 0)
        # Half press: 16384 >> 7 = 128
        self.assertEqual(map_sdl_axis_to_xinput("left_trigger", 16384), 128)
        # Full press: 32767 >> 7 = 255
        self.assertEqual(map_sdl_axis_to_xinput("left_trigger", 32767), 255)
        self.assertEqual(map_sdl_axis_to_xinput("right_trigger", 32767), 255)

    def test_deadzone_filtering(self):
        """Verifies deadzone filtering on thumbsticks and triggers."""
        # Below left stick deadzone
        self.assertEqual(apply_deadzone(5000, XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE), 0)
        self.assertEqual(apply_deadzone(-7000, XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE), 0)
        # Above left stick deadzone
        self.assertEqual(apply_deadzone(8000, XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE), 8000)
        self.assertEqual(apply_deadzone(-10000, XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE), -10000)

        # Trigger threshold (30 out of 255)
        raw_trigger = map_sdl_axis_to_xinput("left_trigger", 2000)  # 2000 >> 7 = 15
        self.assertEqual(apply_deadzone(raw_trigger, XINPUT_GAMEPAD_TRIGGER_THRESHOLD), 0)

        pressed_trigger = map_sdl_axis_to_xinput("left_trigger", 10000)  # 10000 >> 7 = 78
        self.assertEqual(apply_deadzone(pressed_trigger, XINPUT_GAMEPAD_TRIGGER_THRESHOLD), 78)

    def test_packet_counter_increments(self):
        """Verifies that state changes increment the XInput packet counter."""
        packet_number = 0
        prev_state = {"buttons": 0, "lx": 0, "ly": 0}

        def update(new_state):
            nonlocal packet_number, prev_state
            if new_state != prev_state:
                packet_number += 1
                prev_state = new_state.copy()
            return packet_number

        self.assertEqual(update({"buttons": 0, "lx": 0, "ly": 0}), 0)
        # State change: button pressed
        self.assertEqual(update({"buttons": XINPUT_GAMEPAD_A, "lx": 0, "ly": 0}), 1)
        # Redundant poll without change: packet number unchanged
        self.assertEqual(update({"buttons": XINPUT_GAMEPAD_A, "lx": 0, "ly": 0}), 1)
        # State change: stick moved
        self.assertEqual(update({"buttons": XINPUT_GAMEPAD_A, "lx": 5000, "ly": 0}), 2)

    def test_disconnect_semantics(self):
        """Verifies X_ERROR_DEVICE_NOT_CONNECTED when pad slot is unoccupied."""
        connected_slots = {0: True}

        def query_user(user_index: int):
            if user_index not in connected_slots or not connected_slots[user_index]:
                return X_ERROR_DEVICE_NOT_CONNECTED
            return X_ERROR_SUCCESS

        self.assertEqual(query_user(0), X_ERROR_SUCCESS)
        self.assertEqual(query_user(1), X_ERROR_DEVICE_NOT_CONNECTED)
        self.assertEqual(query_user(2), X_ERROR_DEVICE_NOT_CONNECTED)
        self.assertEqual(query_user(3), X_ERROR_DEVICE_NOT_CONNECTED)

        # Disconnect slot 0
        connected_slots[0] = False
        self.assertEqual(query_user(0), X_ERROR_DEVICE_NOT_CONNECTED)


if __name__ == "__main__":
    unittest.main()
