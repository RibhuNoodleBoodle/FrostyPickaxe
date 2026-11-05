#!/usr/bin/env python3
"""
Unit tests for GDFX Provisioning Tool (tests/test_provisioner.py)
Validates bounds, path safety, and binary parsing on SYNTHETIC fixtures only.
NO commercial game bytes or keys are used in these tests.
"""

import unittest
import io
import struct
from pathlib import Path
import sys

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from gdfx_provisioner import (
    sanitize_filename,
    parse_gdfx_dir,
    parse_xex_execution_info,
    extract_file,
    GDFX_MAGIC,
    SECTOR_SIZE
)


class TestGDFXProvisioner(unittest.TestCase):

    def test_sanitize_filename_safe(self):
        self.assertEqual(sanitize_filename("default.xex"), "default.xex")
        self.assertEqual(sanitize_filename("movies/intro.bik"), "movies/intro.bik")
        self.assertEqual(sanitize_filename("sub/dir/file.txt"), "sub/dir/file.txt")

    def test_sanitize_filename_traversal_rejected(self):
        with self.assertRaises(ValueError):
            sanitize_filename("../secret.txt")
        with self.assertRaises(ValueError):
            sanitize_filename("movies/../../etc/passwd")
        with self.assertRaises(ValueError):
            sanitize_filename("/absolute/path")
        with self.assertRaises(ValueError):
            sanitize_filename("\\windows\\path")

    def test_parse_gdfx_dir_synthetic(self):
        """
        Creates a synthetic in-memory GDFX directory table with two files and one directory.
        """
        dir_buf = bytearray(SECTOR_SIZE)

        # File 1: "test1.bin", sector 10, size 100, attr 0x00
        # Entry layout: <HHIIBB name pad
        # Left child points to File 2 at entry index 10 (offset 40)
        # Right child is 0
        name1 = b"test1.bin"
        left1 = 10  # 10 * 4 = 40
        right1 = 0
        sec1 = 10
        size1 = 100
        attr1 = 0x00
        nlen1 = len(name1)
        entry1 = struct.pack("<HHIIBB", left1, right1, sec1, size1, attr1, nlen1) + name1
        # Pad entry1 to 4-byte boundary
        pad1 = (4 - (len(entry1) % 4)) % 4
        entry1 += b"\x00" * pad1
        dir_buf[0 : len(entry1)] = entry1

        # File 2: "dirA", sector 20, size 2048, attr 0x10 (directory)
        name2 = b"dirA"
        left2 = 0
        right2 = 0
        sec2 = 20
        size2 = 2048
        attr2 = 0x10
        nlen2 = len(name2)
        entry2 = struct.pack("<HHIIBB", left2, right2, sec2, size2, attr2, nlen2) + name2
        pad2 = (4 - (len(entry2) % 4)) % 4
        entry2 += b"\x00" * pad2
        dir_buf[40 : 40 + len(entry2)] = entry2

        stream = io.BytesIO(bytes(dir_buf))
        entries = parse_gdfx_dir(stream, base_offset=0, dir_sector=0, dir_size=SECTOR_SIZE, iso_size=SECTOR_SIZE * 100)

        self.assertEqual(len(entries), 2)
        # Entry 2 parsed first due to left-first traversal
        names = [e["name"] for e in entries]
        self.assertIn("test1.bin", names)
        self.assertIn("dirA", names)

        dir_entry = next(e for e in entries if e["name"] == "dirA")
        self.assertTrue(dir_entry["is_dir"])
        self.assertEqual(dir_entry["sector"], 20)

    def test_parse_gdfx_bounds_check(self):
        stream = io.BytesIO(b"\x00" * 1024)
        # Sector 10 is at offset 20480, beyond the stream size of 1024 -> must raise ValueError
        with self.assertRaises(ValueError):
            parse_gdfx_dir(stream, base_offset=0, dir_sector=10, dir_size=2048, iso_size=1024)

    def test_parse_xex_execution_info_synthetic(self):
        """
        Creates a synthetic XEX header with Execution Info (0x00040006).
        """
        xex_buf = bytearray(4096)
        xex_buf[0:4] = b"XEX2"
        # Optional header count = 2 at 0x14
        struct.pack_into(">I", xex_buf, 0x14, 2)

        # Opt header 0: Entry Point (0x00010100) -> 0x82001000
        struct.pack_into(">II", xex_buf, 0x18, 0x00010100, 0x82001000)
        # Opt header 1: Execution Info (0x00040006) -> offset 0x200
        struct.pack_into(">II", xex_buf, 0x20, 0x00040006, 0x200)

        # At offset 0x200: Execution Info struct
        # media_id=0x11223344, version=1, base_ver=1, title_id=0x55667788, platform=1, table=0, disc=1, count=1
        struct.pack_into(">IIIIBBBB", xex_buf, 0x200, 0x11223344, 1, 1, 0x55667788, 1, 0, 1, 1)

        stream = io.BytesIO(bytes(xex_buf))
        info = parse_xex_execution_info(stream, 0, len(xex_buf))

        self.assertIsNotNone(info)
        self.assertEqual(info["title_id"], "55667788")
        self.assertEqual(info["media_id"], "11223344")
        self.assertEqual(info["version"], 1)
        self.assertEqual(info["entrypoint"], "0x82001000")
        self.assertEqual(info["disc_number"], 1)
        self.assertEqual(info["disc_count"], 1)


if __name__ == "__main__":
    unittest.main()
