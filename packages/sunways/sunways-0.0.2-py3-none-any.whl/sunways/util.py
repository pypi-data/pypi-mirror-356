"""decode and encode."""

from __future__ import annotations

from datetime import datetime
from struct import unpack
from typing import Any

from .protocol import ProtocolResponse

DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
MONTH_NAMES = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


def read_byte(buffer: ProtocolResponse, offset: int | None = None) -> int:
    """Retrieve single byte (signed int) value from buffer."""
    if offset is not None:
        buffer.seek(offset)
    return int.from_bytes(buffer.read(1), byteorder="big", signed=True)


def read_bytes2(
    buffer: ProtocolResponse, offset: int | None = None, undef: int | None = None
) -> int:
    """Retrieve 2 byte (unsigned int) value from buffer."""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(2), byteorder="big", signed=False)
    return undef if value == 0xFFFF else value


def read_bytes2_signed(buffer: ProtocolResponse, offset: int | None = None) -> int:
    """Retrieve 2 byte (signed int) value from buffer."""
    if offset is not None:
        buffer.seek(offset)
    return int.from_bytes(buffer.read(2), byteorder="big", signed=True)


def read_bytes4(
    buffer: ProtocolResponse, offset: int | None = None, undef: int | None = None
) -> int:
    """Retrieve 4 byte (unsigned int) value from buffer."""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(4), byteorder="big", signed=False)
    return undef if value == 0xFFFFFFFF else value


def read_bytes4_signed(buffer: ProtocolResponse, offset: int | None = None) -> int:
    """Retrieve 4 byte (signed int) value from buffer."""
    if offset is not None:
        buffer.seek(offset)
    return int.from_bytes(buffer.read(4), byteorder="big", signed=True)


def read_bytes8(
    buffer: ProtocolResponse, offset: int | None = None, undef: int | None = None
) -> int:
    """Retrieve 8 byte (unsigned int) value from buffer."""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(8), byteorder="big", signed=False)
    return undef if value == 0xFFFFFFFFFFFFFFFF else value


def read_decimal2(
    buffer: ProtocolResponse, scale: int, offset: int | None = None
) -> float:
    """Retrieve 2 byte (signed float) value from buffer."""
    if offset is not None:
        buffer.seek(offset)
    return float(int.from_bytes(buffer.read(2), byteorder="big", signed=True)) / scale


def read_float4(buffer: ProtocolResponse, offset: int | None = None) -> float:
    """Retrieve 4 byte (signed float) value from buffer."""
    if offset is not None:
        buffer.seek(offset)
    data = buffer.read(4)
    if len(data) == 4:
        return unpack(">f", data)[0]
    return float(0)


def read_voltage(buffer: ProtocolResponse, offset: int | None = None) -> float:
    """Retrieve voltage [V] value (2 unsigned bytes) from buffer."""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(2), byteorder="big", signed=False)
    return float(value) / 10 if value != 0xFFFF else 0


def encode_voltage(value: Any) -> bytes:
    """Encode voltage value to raw (2 unsigned bytes) payload."""
    return int.to_bytes(int(float(value) * 10), length=2, byteorder="big", signed=False)


def read_current(buffer: ProtocolResponse, offset: int | None = None) -> float:
    """Retrieve current [A] value (2 unsigned bytes) from buffer."""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(2), byteorder="big", signed=False)
    return float(value) / 10 if value != 0xFFFF else 0


def read_current_signed(buffer: ProtocolResponse, offset: int | None = None) -> float:
    """Retrieve current [A] value (2 signed bytes) from buffer."""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(2), byteorder="big", signed=True)
    return float(value) / 10


def encode_current(value: Any) -> bytes:
    """Encode current value to raw (2 unsigned bytes) payload."""
    return int.to_bytes(int(float(value) * 10), length=2, byteorder="big", signed=False)


def encode_current_signed(value: Any) -> bytes:
    """Encode current value to raw (2 signed bytes) payload."""
    return int.to_bytes(int(float(value) * 10), length=2, byteorder="big", signed=True)


def read_freq(buffer: ProtocolResponse, offset: int | None = None) -> float:
    """Retrieve frequency [Hz] value (2 bytes) from buffer."""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(2), byteorder="big", signed=True)
    return float(value) / 100


def read_temp(buffer: ProtocolResponse, offset: int | None = None) -> float | None:
    """Retrieve temperature [C] value (2 bytes) from buffer."""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(2), byteorder="big", signed=True)
    if value in (-1, 32767):
        return None
    return float(value) / 10


def read_datetime(buffer: ProtocolResponse, offset: int | None = None) -> datetime:
    """Retrieve datetime value (6 bytes) from buffer."""
    if offset is not None:
        buffer.seek(offset)
    year = 2000 + int.from_bytes(buffer.read(1), byteorder="big")
    month = int.from_bytes(buffer.read(1), byteorder="big")
    day = int.from_bytes(buffer.read(1), byteorder="big")
    hour = int.from_bytes(buffer.read(1), byteorder="big")
    minute = int.from_bytes(buffer.read(1), byteorder="big")
    second = int.from_bytes(buffer.read(1), byteorder="big")
    return datetime(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )


def encode_datetime(value: Any) -> bytes:
    """Encode datetime value to raw (6 bytes) payload."""
    timestamp = value
    if isinstance(value, str):
        timestamp = datetime.fromisoformat(value)

    return bytes(
        [
            timestamp.year - 2000,
            timestamp.month,
            timestamp.day,
            timestamp.hour,
            timestamp.minute,
            timestamp.second,
        ]
    )


def read_grid_mode(buffer: ProtocolResponse, offset: int | None = None) -> int:
    """Retrieve 'grid mode' sign value from buffer."""
    value = read_bytes2_signed(buffer, offset)
    if value < -90:
        return 2
    if value >= 90:
        return 1
    return 0


def read_unsigned_int16(data: bytes, offset: int) -> int:
    """Retrieve 2 byte (unsigned int) value from bytes at specified offset."""
    return int.from_bytes(data[offset : offset + 2], byteorder="big", signed=False)


def read_unsigned_int32(data: bytes, offset: int) -> int:
    """Retrieve 4 byte (unsigned int) value from bytes at specified offset."""
    return int.from_bytes(data[offset : offset + 4], byteorder="big", signed=False)


def decode_bitmap(value: int, bitmap: dict[int, str]) -> str:
    """Decode bitmap."""
    bits = value
    result = []
    for i in range(32):
        if bits & 0x1 == 1:
            if bitmap.get(i, f"err{i}"):
                result.append(bitmap.get(i, f"err{i}"))
        bits = bits >> 1
    return ", ".join(result)


def decode_day_of_week(data: int) -> str:
    """Decode_day_of_week."""
    if data == -1:
        return "Mon-Sun"
    if data == 0:
        return ""
    names = list(DAY_NAMES)
    return decode_dm(data, names)


def decode_months(data: int) -> str | None:
    """Decode_months."""
    if data <= 0 or data == 0x0FFF:
        return None
    names = list(MONTH_NAMES)
    return decode_dm(data, names)

def decode_dm(data: int, names: list[str]) -> str | None:
    dm = ""
    bits = bin(data)[2:]
    for each in bits[::-1]:
        if each == "1":
            if len(dm) > 0:
                dm += ","
            dm += names[0]
        names.pop(0)
    return dm

def decode_string(data: bytes) -> str:
    """Decode the bytes to ascii string."""
    try:
        if any(x < 32 for x in data):
            return data.decode("utf-16be").rstrip().replace("\x00", "")
        return data.decode("ascii").rstrip()
    except ValueError:
        return data.hex()
