#!/usr/bin/env python3
"""
Title Update (STFS Package) Safe Analysis Tool
Part of FrostyPickaxe project (Step 02 / Milestone M0).

This tool safely inspects the quarantined Title Update ZIP and inner STFS package
to record package metadata, media identity, and internal file descriptors
without modifying the package or applying deltas to base game files.
"""

import os
import sys
import argparse
import zipfile
import struct
import hashlib
import json
from pathlib import Path


def analyze_tu_zip(zip_path, report_out=None):
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"TU ZIP not found: {zip_path}")

    zip_size = os.path.getsize(zip_path)
    report = {
        "zip_path": os.path.abspath(zip_path),
        "zip_size": zip_size,
        "members": []
    }

    with zipfile.ZipFile(zip_path, "r") as z:
        for info in z.infolist():
            member_report = {
                "filename": info.filename,
                "file_size": info.file_size,
                "compress_size": info.compress_size,
                "crc": f"{info.CRC:08X}"
            }

            with z.open(info.filename) as f:
                header = f.read(0x1000)
                if len(header) >= 0x400:
                    magic = header[:4]
                    member_report["magic"] = magic.decode("latin1", errors="replace")
                    if magic in (b"LIVE", b"PIRS", b"CON "):
                        header_size, content_type, meta_ver, content_size = struct.unpack(">IIII", header[0x340:0x350])
                        media_id, version, base_ver, title_id = struct.unpack(">IIII", header[0x354:0x364])
                        member_report["stfs_header"] = {
                            "header_size": f"0x{header_size:X}",
                            "content_type": f"0x{content_type:08X}",
                            "metadata_version": meta_ver,
                            "declared_content_size": content_size,
                            "media_id": f"{media_id:08X}",
                            "version": version,
                            "base_version": base_ver,
                            "title_id": f"{title_id:08X}"
                        }
            report["members"].append(member_report)

    output_str = json.dumps(report, indent=2)
    print("Title Update Analysis Summary:")
    print(output_str)

    if report_out:
        Path(report_out).parent.mkdir(parents=True, exist_ok=True)
        with open(report_out, "w") as out_f:
            out_f.write(output_str)
        print(f"Report saved to {report_out}")

    return report


def main():
    parser = argparse.ArgumentParser(description="Title Update Analysis Tool")
    parser.add_argument("--zip", required=True, help="Path to Title Update ZIP")
    parser.add_argument("--report", help="Path to write JSON analysis report")
    args = parser.parse_args()

    try:
        analyze_tu_zip(args.zip, report_out=args.report)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
