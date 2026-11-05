#!/usr/bin/env python3
"""
GDFX (Xbox 360 Game Disc) Safe Provisioning & Inventory Tool
Part of FrostyPickaxe project (Step 02 / Milestone M0).

This tool reads Xbox 360 GDFX filesystem structures from a supplied ISO
and extracts files to a target directory with path validation and SHA-256 verification.
No game bytes or decryption keys are hardcoded.
"""

import os
import sys
import argparse
import hashlib
import struct
import json
from pathlib import Path

GDFX_MAGIC = b"MICROSOFT*XBOX*MEDIA"
SECTOR_SIZE = 2048


def find_gdfx_base_offset(f, max_sectors=200000):
    """
    Scans for the sector-aligned GDFX volume header and returns the partition base byte offset.
    In Xbox 360 discs, the volume descriptor is at partition sector 32.
    """
    f.seek(0, 2)
    file_size = f.tell()
    
    # Check common known offsets first
    candidate_sectors = [129856, 19200, 2048, 32]
    for sec in candidate_sectors:
        offset = sec * SECTOR_SIZE
        if offset + 20 <= file_size:
            f.seek(offset)
            if f.read(20) == GDFX_MAGIC:
                base_sector = max(0, sec - 32)
                return base_sector * SECTOR_SIZE

    # Linear scan if not at candidate offsets
    sectors_to_scan = min(max_sectors, file_size // SECTOR_SIZE)
    for sec in range(sectors_to_scan):
        f.seek(sec * SECTOR_SIZE)
        if f.read(20) == GDFX_MAGIC:
            base_sector = max(0, sec - 32)
            return base_sector * SECTOR_SIZE

    return None


def sanitize_filename(name):
    """
    Validates and sanitizes entry name to prevent directory traversal or escapes.
    Raises ValueError if malicious path elements are detected.
    """
    if ".." in name or name.startswith("/") or name.startswith("\\"):
        raise ValueError(f"Path traversal detected: {name}")
    parts = Path(name).parts
    for part in parts:
        if part in ("..", ".", ""):
            raise ValueError(f"Invalid path component: {part}")
    return name


def parse_gdfx_dir(stream, base_offset, dir_sector, dir_size, iso_size):
    """
    Recursively parses a GDFX directory binary structure from the stream.
    Validates bounds to ensure all sectors reside within the file size.
    """
    abs_dir_offset = base_offset + (dir_sector * SECTOR_SIZE)
    if abs_dir_offset + dir_size > iso_size:
        raise ValueError(f"Directory out of bounds: offset={abs_dir_offset}, size={dir_size}")

    stream.seek(abs_dir_offset)
    data = stream.read(dir_size)
    if len(data) < dir_size:
        raise ValueError(f"Truncated directory read: expected {dir_size}, got {len(data)}")

    entries = []
    visited_offsets = set()

    def parse_entry(offset):
        if offset in visited_offsets or offset + 14 > len(data):
            return
        visited_offsets.add(offset)
        left, right, sector, size, attr, name_len = struct.unpack_from("<HHIIBB", data, offset)
        if left != 0:
            parse_entry(left * 4)
        if name_len > 0:
            name_raw = data[offset + 14 : offset + 14 + name_len]
            name = name_raw.decode("latin1", errors="replace")
            clean_name = sanitize_filename(name)
            entries.append({
                "name": clean_name,
                "sector": sector,
                "size": size,
                "is_dir": bool(attr & 0x10),
                "attr": attr
            })
        if right != 0:
            parse_entry(right * 4)

    parse_entry(0)
    return entries


def collect_gdfx_tree(stream, base_offset, dir_sector, dir_size, iso_size, prefix=""):
    """
    Traverses the directory tree and returns a flat list of all files with their relative paths.
    """
    entries = parse_gdfx_dir(stream, base_offset, dir_sector, dir_size, iso_size)
    all_files = []
    for entry in entries:
        rel_path = f"{prefix}{entry['name']}" if not prefix else f"{prefix}/{entry['name']}"
        if entry["is_dir"]:
            sub_files = collect_gdfx_tree(stream, base_offset, entry["sector"], entry["size"], iso_size, prefix=rel_path)
            all_files.extend(sub_files)
        else:
            all_files.append({
                "path": rel_path,
                "sector": entry["sector"],
                "size": entry["size"],
                "abs_offset": base_offset + (entry["sector"] * SECTOR_SIZE)
            })
    return all_files


def parse_xex_execution_info(stream, xex_abs_offset, xex_size):
    """
    Extracts execution info (Title ID, Media ID, version, base version) from an XEX2 executable.
    """
    stream.seek(xex_abs_offset)
    hdr_data = stream.read(min(xex_size, 16384))
    if len(hdr_data) < 24 or hdr_data[:4] != b"XEX2":
        return None

    opt_cnt = struct.unpack(">I", hdr_data[0x14:0x18])[0]
    exec_info = {}
    for i in range(opt_cnt):
        pos = 0x18 + i * 8
        if pos + 8 > len(hdr_data):
            break
        key, val = struct.unpack(">II", hdr_data[pos : pos + 8])
        if key == 0x00010100:
            exec_info["entrypoint"] = f"0x{val:08X}"
        elif key == 0x00010201:
            exec_info["image_base"] = f"0x{val:08X}"
        elif key == 0x00040006:
            if val + 20 <= len(hdr_data):
                media_id, version, base_ver, title_id, platform, exec_table, disc_num, disc_cnt = struct.unpack(">IIIIBBBB", hdr_data[val:val+20])
                exec_info["title_id"] = f"{title_id:08X}"
                exec_info["media_id"] = f"{media_id:08X}"
                exec_info["version"] = version
                exec_info["base_version"] = base_ver
                exec_info["disc_number"] = disc_num
                exec_info["disc_count"] = disc_cnt
    return exec_info


def extract_file(stream, abs_offset, size, out_path, compute_hash=True):
    """
    Safely writes a file from stream to out_path in chunks, computing SHA-256.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    stream.seek(abs_offset)
    hasher = hashlib.sha256() if compute_hash else None
    remaining = size
    chunk_size = 1024 * 1024 # 1 MB chunks

    with open(out_path, "wb") as out_f:
        while remaining > 0:
            to_read = min(remaining, chunk_size)
            chunk = stream.read(to_read)
            if not chunk:
                raise IOError(f"Unexpected EOF reading {size} bytes from offset {abs_offset}")
            out_f.write(chunk)
            if hasher:
                hasher.update(chunk)
            remaining -= len(chunk)

    return hasher.hexdigest() if hasher else None


def provision_iso(iso_path, out_dir=None, manifest_out=None, dry_run=False):
    """
    Main entry point for ISO inventory and provisioning.
    """
    if not os.path.exists(iso_path):
        raise FileNotFoundError(f"ISO file not found: {iso_path}")

    iso_size = os.path.getsize(iso_path)
    with open(iso_path, "rb") as f:
        base_offset = find_gdfx_base_offset(f)
        if base_offset is None:
            raise ValueError(f"Could not locate GDFX filesystem in {iso_path}")

        vol_offset = base_offset + (32 * SECTOR_SIZE)
        f.seek(vol_offset)
        vol_hdr = f.read(SECTOR_SIZE)
        if vol_hdr[:20] != GDFX_MAGIC:
            raise ValueError(f"Invalid GDFX volume header at offset {vol_offset}")

        root_sector, root_size = struct.unpack("<II", vol_hdr[20:28])
        files = collect_gdfx_tree(f, base_offset, root_sector, root_size, iso_size)

        xex_info = None
        for file_entry in files:
            if file_entry["path"].lower() == "default.xex":
                xex_info = parse_xex_execution_info(f, file_entry["abs_offset"], file_entry["size"])
                file_entry["execution_info"] = xex_info

        manifest_data = {
            "iso_path": os.path.abspath(iso_path),
            "iso_size": iso_size,
            "partition_base_offset": base_offset,
            "files_count": len(files),
            "execution_info": xex_info,
            "files": []
        }

        print(f"Discovered {len(files)} files in GDFX filesystem (base offset: 0x{base_offset:X}):")
        if xex_info:
            print(f"  Title ID: {xex_info.get('title_id')} | Media ID: {xex_info.get('media_id')} | Version: {xex_info.get('version')} | Disc: {xex_info.get('disc_number')}/{xex_info.get('disc_count')}")

        for file_entry in files:
            rel_path = file_entry["path"]
            size = file_entry["size"]
            abs_off = file_entry["abs_offset"]
            sha256 = None

            if not dry_run and out_dir:
                dest = Path(out_dir) / rel_path
                sha256 = extract_file(f, abs_off, size, dest)
                print(f"  Extracted: {rel_path} ({size:,} bytes) -> {sha256[:12]}...")
            else:
                print(f"  {rel_path:<40} ({size:>11,} bytes) at offset 0x{abs_off:X}")

            manifest_data["files"].append({
                "path": rel_path,
                "size": size,
                "abs_offset": abs_off,
                "sha256": sha256
            })

        if manifest_out:
            Path(manifest_out).parent.mkdir(parents=True, exist_ok=True)
            with open(manifest_out, "w") as mf:
                json.dump(manifest_data, mf, indent=2)
            print(f"Manifest written to {manifest_out}")

        return manifest_data


def main():
    parser = argparse.ArgumentParser(description="GDFX ISO Provisioning Tool")
    parser.add_argument("--iso", required=True, help="Path to input Xbox 360 ISO")
    parser.add_argument("--out-dir", help="Output directory to extract files")
    parser.add_argument("--manifest", help="Path to write output manifest JSON")
    parser.add_argument("--dry-run", action="store_true", help="List files without extracting")
    args = parser.parse_args()

    try:
        provision_iso(args.iso, out_dir=args.out_dir, manifest_out=args.manifest, dry_run=args.dry_run)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
