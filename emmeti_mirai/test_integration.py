"""
Standalone smoke-test for emmeti_mirai – runs WITHOUT Home Assistant.

Usage:
    python test_integration.py --host 192.168.1.100 [--port 502] [--slave 1]

The test:
    1. Imports all modules and verifies no syntax errors
    2. Checks that MODBUS_REGISTERS is consistent (keys unique, required fields present)
    3. Tests encode/decode round-trip for every data_type
    4. Optionally connects to a real device (if --host is provided)
"""
import argparse
import sys
import struct

# ── 1. Import check ──────────────────────────────────────────────────────────
try:
    from emmeti_mirai.const import MODBUS_REGISTERS, REGISTERS_BY_ENTITY_TYPE, DOMAIN
    from emmeti_mirai.modbus_client import _decode_value, _encode_value, _word_count
    print("[OK] All modules imported successfully")
except ImportError as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)

# ── 2. Register consistency check ────────────────────────────────────────────
REQUIRED_FIELDS = {"key", "name", "register", "register_type", "data_type",
                   "scale", "offset", "unit", "entity_type", "writable"}

errors = []
seen_keys = set()

for reg in MODBUS_REGISTERS:
    k = reg.get("key", "<missing>")
    missing = REQUIRED_FIELDS - reg.keys()
    if missing:
        errors.append(f"Register '{k}' missing fields: {missing}")
    if k in seen_keys:
        errors.append(f"Duplicate key: '{k}'")
    seen_keys.add(k)
    if reg.get("writable") and reg.get("register_type") not in ("holding", "coil"):
        errors.append(f"Register '{k}' is writable but type={reg['register_type']}")

if errors:
    print("[FAIL] Register consistency errors:")
    for e in errors:
        print(f"       {e}")
    sys.exit(1)

print(f"[OK] {len(MODBUS_REGISTERS)} registers validated – no consistency errors")
print(f"[OK] Entity types found: {list(REGISTERS_BY_ENTITY_TYPE.keys())}")

# ── 3. Encode / decode round-trip ────────────────────────────────────────────
TEST_CASES = [
    ("bool",    True,    1,   0),
    ("bool",    False,   1,   0),
    ("int16",   -153,    0.1, 0),
    ("uint16",  400,     0.1, 0),
    ("int32",   -80000,  1,   0),
    ("uint32",  80000,   1,   0),
    ("float32", 3.14159, 1,   0),
]

rt_errors = []
for dtype, original, scale, offset in TEST_CASES:
    words = _encode_value(original, dtype, scale)
    decoded = _decode_value(words, dtype, scale, offset)
    if dtype == "bool":
        ok = bool(decoded) == bool(original)
    elif dtype == "float32":
        ok = abs(decoded - original) < 0.001
    else:
        ok = abs(decoded - original) < abs(original * 0.001) + 0.001
    if not ok:
        rt_errors.append(f"{dtype}: encoded {original} -> words {words} -> decoded {decoded}")

if rt_errors:
    print("[FAIL] Round-trip errors:")
    for e in rt_errors:
        print(f"       {e}")
    sys.exit(1)

print("[OK] Encode/decode round-trip passed for all data types")

# ── 4. Live device test (optional) ───────────────────────────────────────────
parser = argparse.ArgumentParser(description="Emmeti Mirai smoke test")
parser.add_argument("--host", default=None)
parser.add_argument("--port", type=int, default=502)
parser.add_argument("--slave", type=int, default=1)
args = parser.parse_args()

if args.host:
    try:
        from emmeti_mirai.modbus_client import EmmetiModbusClient
        client = EmmetiModbusClient(args.host, args.port, args.slave)
        ok = client.test_connection()
        if ok:
            print(f"[OK] Connected to {args.host}:{args.port} slave={args.slave}")
            data = client.read_all()
            print(f"[OK] Read {len(data)} register(s):")
            for key, val in sorted(data.items()):
                print(f"       {key:35s} = {val}")
        else:
            print(f"[WARN] Could not connect to {args.host}:{args.port} – check device")
        client.close()
    except Exception as exc:
        print(f"[FAIL] Live test exception: {exc}")
        sys.exit(1)
else:
    print("[SKIP] No --host provided, skipping live device test")

print("\n✓ All tests passed")
