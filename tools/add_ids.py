#!/usr/bin/env python3
"""Add ID numbers to existing-ids.json as fingerprints.  Usage: python3 tools/add_ids.py 29001010123456 30101011234567"""
import hashlib, json, pathlib, sys
path = pathlib.Path(__file__).resolve().parent.parent / "existing-ids.json"
data = json.loads(path.read_text())
trans = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
for raw in sys.argv[1:]:
    digits = "".join(c for c in raw.translate(trans) if c.isdigit())
    if len(digits) != 14:
        sys.exit(f"Not a 14-digit ID number: {raw}")
    h = hashlib.pbkdf2_hmac("sha256", digits.encode(), data["salt"].encode(), data["iterations"]).hex()
    if h not in data["hashes"]:
        data["hashes"].append(h)
path.write_text(json.dumps(data, indent=2) + "\n")
print(f"{len(data['hashes'])} ID numbers on the list")
