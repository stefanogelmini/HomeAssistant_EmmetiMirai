"""Modbus RTU over TCP client wrapper for Emmeti Mirai heat pump."""
from __future__ import annotations

import logging
import socket
import struct
from typing import Any

from pymodbus.framer import FramerType

from .const import MODBUS_REGISTERS

_LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Block read configuration
# Registers are grouped into contiguous address ranges to minimise Modbus
# round-trips.  Each tuple is (start_address, count) covering all registers
# within that span.  Gaps between real registers are read but discarded.
# Changing MAX_BLOCK_GAP controls how far apart two registers can be and
# still be merged into one block read (tune if the device rejects sparse reads).
# ---------------------------------------------------------------------------
MAX_BLOCK_GAP = 20   # max address gap to still merge into one block
MAX_BLOCK_SIZE = 125  # pymodbus / Modbus spec safe limit per request


def _build_blocks(registers: list[dict]) -> list[tuple[int, int]]:
    """Return a list of (start_address, count) blocks for holding registers.

    Only holding-register type is handled here; other types fall back to
    individual reads in read_all().
    """
    holding = sorted(
        (r for r in registers if r["register_type"] == "holding"),
        key=lambda r: r["register"],
    )
    if not holding:
        return []

    blocks: list[tuple[int, int]] = []
    start = holding[0]["register"]
    end = holding[0]["register"]

    for reg in holding[1:]:
        addr = reg["register"]
        if addr - end <= MAX_BLOCK_GAP and (addr - start + 1) <= MAX_BLOCK_SIZE:
            end = addr
        else:
            blocks.append((start, end - start + 1))
            start = addr
            end = addr
    blocks.append((start, end - start + 1))
    return blocks


# Pre-computed block layout (static – registers don't change at runtime)
_HOLDING_BLOCKS: list[tuple[int, int]] = _build_blocks(MODBUS_REGISTERS)

# Pre-index registers by address for O(1) lookup when mapping block results
_REG_BY_ADDRESS: dict[int, dict] = {r["register"]: r for r in MODBUS_REGISTERS}


# ---------------------------------------------------------------------------
# Value encoding / decoding helpers
# ---------------------------------------------------------------------------

def _decode_value(raw_words: list[int], data_type: str, scale: float, offset: float) -> Any:
    if data_type == "bool":
        return bool(raw_words[0])
    if data_type == "int16":
        v = struct.unpack(">h", struct.pack(">H", raw_words[0]))[0]
        return round(v * scale + offset, 4)
    if data_type == "uint16":
        return round(raw_words[0] * scale + offset, 4)
    if data_type in ("int32", "uint32", "float32"):
        combined = (raw_words[0] << 16) | raw_words[1]
        if data_type == "int32":
            v = struct.unpack(">i", struct.pack(">I", combined))[0]
        elif data_type == "uint32":
            v = combined
        else:
            v = struct.unpack(">f", struct.pack(">I", combined))[0]
        return round(v * scale + offset, 4)
    return raw_words[0]


def _encode_value(value: Any, data_type: str, scale: float) -> list[int]:
    if data_type == "bool":
        return [1 if value else 0]
    raw = value / scale if scale else value
    if data_type == "int16":
        return [struct.unpack(">H", struct.pack(">h", int(raw)))[0]]
    if data_type == "uint16":
        return [int(raw) & 0xFFFF]
    if data_type == "int32":
        return list(struct.unpack(">HH", struct.pack(">i", int(raw))))
    if data_type == "uint32":
        return list(struct.unpack(">HH", struct.pack(">I", int(raw) & 0xFFFFFFFF)))
    if data_type == "float32":
        return list(struct.unpack(">HH", struct.pack(">f", float(raw))))
    return [int(raw) & 0xFFFF]


def _word_count(data_type: str) -> int:
    return 2 if data_type in ("int32", "uint32", "float32") else 1


def _tcp_reachable(host: str, port: int, timeout: float = 5.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _call_modbus(fn, address: int, count: int, slave_id: int):
    """Call a pymodbus read function trying all known keyword variants."""
    for kwargs in [
        {"count": count, "slave": slave_id},
        {"count": count, "device_id": slave_id},
        {"count": count},
    ]:
        try:
            return fn(address, **kwargs)
        except TypeError:
            continue
    return fn(address, count, slave_id)


# ---------------------------------------------------------------------------
# Main client
# ---------------------------------------------------------------------------

class EmmetiModbusClient:
    """RTU-over-TCP Modbus client for the Emmeti Mirai heat pump."""

    def __init__(self, host: str, port: int, slave_id: int) -> None:
        self._host = host
        self._port = port
        self._slave_id = slave_id
        self._client = None

    def _get_client(self):
        if self._client is None:
            from pymodbus.client import ModbusTcpClient
            self._client = ModbusTcpClient(
                self._host,
                port=self._port,
                timeout=5,
                framer=FramerType.RTU,
            )
        return self._client

    def _ensure_connected(self) -> bool:
        c = self._get_client()
        return True if c.connected else c.connect()

    def test_connection(self) -> bool:
        """Quick TCP reachability check (used by config flow)."""
        return _tcp_reachable(self._host, self._port)

    def close(self) -> None:
        if self._client:
            try:
                self._client.close()
            except Exception:  # noqa: BLE001
                pass
            self._client = None

    # ------------------------------------------------------------------
    # Block-read path (holding registers)
    # ------------------------------------------------------------------

    def _read_blocks(self) -> dict[str, Any]:
        """Read all holding registers in bulk blocks and decode each register."""
        data: dict[str, Any] = {}
        c = self._get_client()
        fn = c.read_holding_registers

        for start_addr, count in _HOLDING_BLOCKS:
            try:
                result = _call_modbus(fn, start_addr, count, self._slave_id)
            except Exception as exc:
                _LOGGER.error(
                    "Block read error at addr=%s count=%s: %s", start_addr, count, exc
                )
                continue

            if result is None or result.isError():
                _LOGGER.warning(
                    "Block read returned error at addr=%s count=%s: %s",
                    start_addr, count, result,
                )
                continue

            regs_raw: list[int] = result.registers

            # Map each known register that falls within this block
            for offset in range(count):
                addr = start_addr + offset
                reg = _REG_BY_ADDRESS.get(addr)
                if reg is None:
                    continue  # gap filler word – skip

                words_needed = _word_count(reg["data_type"])
                if offset + words_needed > count:
                    _LOGGER.warning(
                        "Register %s at addr=%s extends beyond block boundary",
                        reg["key"], addr,
                    )
                    continue

                raw_words = regs_raw[offset: offset + words_needed]
                try:
                    data[reg["key"]] = _decode_value(
                        raw_words, reg["data_type"], reg["scale"], reg["offset"]
                    )
                except Exception as exc:
                    _LOGGER.error(
                        "Decode error for %s addr=%s: %s", reg["key"], addr, exc
                    )

        return data

    # ------------------------------------------------------------------
    # Individual read fallback (non-holding register types)
    # ------------------------------------------------------------------

    def _read_individual(self) -> dict[str, Any]:
        """Read registers that are not holding type (coil, discrete, input)."""
        non_holding = [r for r in MODBUS_REGISTERS if r["register_type"] != "holding"]
        if not non_holding:
            return {}

        data: dict[str, Any] = {}
        c = self._get_client()
        fn_map = {
            "input": c.read_input_registers,
            "coil": c.read_coils,
            "discrete_input": c.read_discrete_inputs,
        }

        for reg in non_holding:
            key = reg["key"]
            address = reg["register"]
            reg_type = reg["register_type"]
            count = _word_count(reg["data_type"])
            try:
                result = _call_modbus(fn_map[reg_type], address, count, self._slave_id)
                if result is None or result.isError():
                    _LOGGER.warning(
                        "Read error for %s addr=%s: %s", key, address, result
                    )
                    continue
                raw_words = (
                    result.registers
                    if hasattr(result, "registers")
                    else [int(result.bits[0])]
                )
                data[key] = _decode_value(
                    raw_words, reg["data_type"], reg["scale"], reg["offset"]
                )
            except Exception as exc:
                _LOGGER.error("Read error for %s addr=%s: %s", key, address, exc)

        return data

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def read_all(self) -> dict[str, Any]:
        """Read all registers and return a key→value mapping."""
        if not self._ensure_connected():
            raise ConnectionError(f"Cannot connect to {self._host}:{self._port}")

        data = self._read_blocks()
        data.update(self._read_individual())

        _LOGGER.debug("read_all: %d values read", len(data))
        return data

    def write_register(self, key: str, value: Any) -> bool:
        """Write a value to a writable register."""
        reg = next((r for r in MODBUS_REGISTERS if r["key"] == key), None)
        if reg is None or not reg.get("writable"):
            return False
        if not self._ensure_connected():
            return False

        words = _encode_value(value, reg["data_type"], reg["scale"])
        address = reg["register"]
        try:
            c = self._get_client()
            fn = c.write_register if len(words) == 1 else c.write_registers
            val = words[0] if len(words) == 1 else words
            for kw in [{"slave": self._slave_id}, {"device_id": self._slave_id}, {}]:
                try:
                    result = fn(address, val, **kw)
                    break
                except TypeError:
                    continue
            return not result.isError()
        except Exception as exc:
            _LOGGER.error("Write error for %s addr=%s: %s", key, address, exc)
            return False
