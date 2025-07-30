"""Generic inverter API module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, IntEnum
import logging
from typing import Any

from .exceptions import MaxRetriesException, RequestFailedException
from .protocol import (
    InverterProtocol,
    ProtocolCommand,
    ProtocolResponse,
    UDPInverterProtocol,
)
from .util import (
    encode_current,
    encode_datetime,
    encode_voltage,
    read_bytes2,
    read_bytes4,
    read_current,
    read_datetime,
    read_freq,
    read_temp,
    read_voltage,
)

logger = logging.getLogger(__name__)


class Category(IntEnum):
    """Enumeration of inverter categories."""

    ON_GRID = 0
    HYBRID = 1
    UNKNOWN = 99


class SensorKind(Enum):
    """Enumeration of sensor kinds.

    Possible values are:
    PV - inverter photo-voltaic (e.g. dc voltage of pv panels)
    AC - inverter grid output (e.g. ac voltage of grid connected output)
    UPS - inverter ups/eps/backup output (e.g. ac voltage of backup/off-grid connected output)
    BAT - battery (e.g. dc voltage of connected battery pack)
    GRID - power grid/smart meter (e.g. active power exported to grid)
    BMS - BMS direct data (e.g. dc voltage of)
    """

    PV = 1
    AC = 2
    UPS = 3
    BAT = 4
    GRID = 5
    BMS = 6
    TEMP = 7
    TIME = 8
    RSS = 9

@dataclass
class Sensor:
    """Definition of inverter sensor and its attributes."""

    id_: str
    offset: int
    name: str
    size_: int
    unit: str
    kind: SensorKind | int | None

    def read_value(self, data) -> Any:
        """Read the sensor value from data at current position."""
        raise NotImplementedError

    def read(self, data) -> Any:
        """Read the sensor value from data (at sensor offset)."""
        data.seek(self.offset)
        return self.read_value(data)

    def encode_value(self, value: Any, register_value: bytes | None = None) -> bytes:
        """Encode the (setting mostly) value to (usually) 2 bytes raw register value."""
        raise NotImplementedError


class Calculated(Sensor):
    """Sensor representing calculated value."""

    def __init__(
        self,
        id_: str,
        getter: Callable[[ProtocolResponse], Any],
        name: str,
        unit: str,
        kind: SensorKind | int | None = None,
    ) -> None:
        """Initialize Calculated sensor."""
        super().__init__(id_, 0, name, 0, unit, kind)
        self._getter: Callable[[ProtocolResponse], Any] = getter

    def read_value(self, data: ProtocolResponse) -> Any:
        """Read the sensor value from data at current position."""
        raise NotImplementedError

    def read(self, data: ProtocolResponse):
        """Read the sensor value from data (at sensor offset)."""
        return self._getter(data)


class Timestamp(Sensor):
    """Sensor representing datetime value encoded in 6 bytes."""

    def __init__(
        self, id_: str, offset: int, name: str, kind: SensorKind | int | None = None
    ) -> None:
        """Initialize Timestamp sensor."""
        super().__init__(id_, offset, name, 6, "", kind)

    def read_value(self, data: ProtocolResponse):
        """Read the datetime value from data at current position."""
        return read_datetime(data)

    def encode_value(self, value: Any, register_value: bytes | None = None) -> bytes:
        """Encode the datetime value to 6 bytes raw register value."""
        return encode_datetime(value)


class Integer(Sensor):
    """Sensor representing unsigned int value encoded in 2 bytes."""

    def __init__(
        self,
        id_: str,
        offset: int,
        name: str,
        unit: str = "",
        kind: SensorKind | int | None = None,
    ) -> None:
        """Initialize Integer sensor."""
        super().__init__(id_, offset, name, 2, unit, kind)

    def read_value(self, data: ProtocolResponse):
        """Read the integer value from data at current position."""
        return read_bytes2(data, None, 0)

    def encode_value(self, value: Any, register_value: bytes | None = None) -> bytes:
        """Encode the integer value to 2 bytes raw register value."""
        return int.to_bytes(int(value), length=2, byteorder="big", signed=False)


class Enum(Sensor):
    """Sensor representing label from enumeration encoded in 1 bytes."""

    def __init__(
        self,
        id_: str,
        offset: int,
        labels: dict[int, str],
        name: str,
        kind: SensorKind | int | None = None,
    ) -> None:
        """Initialize Enum sensor."""
        super().__init__(id_, offset, name, 1, "", kind)
        self._labels: dict[int, str] = labels


class Voltage(Sensor):
    """Sensor representing voltage [V] value encoded in 2 (unsigned) bytes."""

    def __init__(
        self, id_: str, offset: int, name: str, kind: SensorKind | int | None
    ) -> None:
        """Initialize Voltage sensor."""
        super().__init__(id_, offset, name, 2, "V", kind)

    def read_value(self, data: ProtocolResponse):
        """Read the voltage value from data at current position."""
        return read_voltage(data)

    def encode_value(self, value: Any, register_value: bytes | None = None) -> bytes:
        """Encode the voltage value to 2 bytes raw register value."""
        return encode_voltage(value)


class Current(Sensor):
    """Sensor representing current [A] value encoded in 2 (unsigned) bytes."""

    def __init__(
        self, id_: str, offset: int, name: str, kind: SensorKind | int | None
    ) -> None:
        """Initialize Current sensor."""
        super().__init__(id_, offset, name, 2, "A", kind)

    def read_value(self, data: ProtocolResponse):
        """Read the current value from data at current position."""
        return read_current(data)

    def encode_value(self, value: Any, register_value: bytes | None = None) -> bytes:
        """Encode the current value to 2 bytes raw register value."""
        return encode_current(value)


class Power(Sensor):
    """Sensor representing power [W] value encoded in 4 (unsigned) bytes."""

    def __init__(
        self, id_: str, offset: int, name: str, kind: SensorKind | int | None
    ) -> None:
        """Initialize Power sensor."""
        super().__init__(id_, offset, name, 4, "W", kind)

    def read_value(self, data: ProtocolResponse):
        """Read the power value from data at current position."""
        return read_bytes4(data, None, 0)


class Temp(Sensor):
    """Sensor representing temperature [C] value encoded in 2 bytes."""

    def __init__(
        self, id_: str, offset: int, name: str, kind: SensorKind | int | None = None
    ) -> None:
        """Initialize Temperature sensor."""
        super().__init__(id_, offset, name, 2, "C", kind)

    def read_value(self, data: ProtocolResponse):
        """Read the temperature value from data at current position."""
        return read_temp(data)


class Enum2(Sensor):
    """Sensor representing label from enumeration encoded in 2 bytes."""

    def __init__(
        self,
        id_: str,
        offset: int,
        name: str,
        labels: dict[int, str],
        kind: SensorKind | int | None = None,
    ) -> None:
        """Initialize Enum2 sensor."""
        super().__init__(id_, offset, name, 2, "", kind)
        self._labels: dict[int, str] = labels

    def read_value(self, data: ProtocolResponse):
        """Read the label value from data at current position."""
        return self._labels.get(read_bytes2(data, None, 0))


class Frequency(Sensor):
    """Sensor representing frequency [Hz] value encoded in 2 bytes."""

    def __init__(
        self, id_: str, offset: int, name: str, kind: SensorKind | int | None
    ) -> None:
        """Initialize Frequency sensor."""
        super().__init__(id_, offset, name, 2, "Hz", kind)

    def read_value(self, data: ProtocolResponse):
        """Read the frequency value from data at current position."""
        return read_freq(data)


class Energy(Sensor):
    """Sensor representing energy [kWh] value encoded in 4 bytes."""

    def __init__(
        self, id_: str, offset: int, name: str, kind: SensorKind | int | None
    ) -> None:
        """Initialize Energy sensor."""
        super().__init__(id_, offset, name, 4, "kWh", kind)

    def read_value(self, data: ProtocolResponse):
        """Read the energy value from data at current position."""
        value = read_bytes4(data)
        return float(value) / 10 if value is not None else None


class Long(Sensor):
    """Sensor representing unsigned int value encoded in 4 bytes."""

    def __init__(
        self,
        id_: str,
        offset: int,
        name: str,
        unit: str = "",
        kind: SensorKind | int | None = None,
    ) -> None:
        """Initialize Long sensor."""
        super().__init__(id_, offset, name, 4, unit, kind)

    def read_value(self, data: ProtocolResponse):
        """Read the long value from data at current position."""
        return read_bytes4(data, None, 0)

    def encode_value(self, value: Any, register_value: bytes | None = None) -> bytes:
        """Encode the long value to 4 bytes raw register value."""
        return int.to_bytes(int(value), length=4, byteorder="big", signed=False)


class Inverter(ABC):
    """Common superclass for various inverter models implementations.

    Represents the inverter state and its basic behavior.
    """

    def __init__(
        self,
        host: str,
        port: int,
        comm_addr: int = 0,
        timeout: int = 1,
        retries: int = 3,
    ) -> None:
        """Initialize the inverter instance."""

        # create protocol
        self._protocol: InverterProtocol = self._create_protocol(
            host, port, comm_addr, timeout, retries
        )
        self._consecutive_failures_count: int = 0

        self.serial_number: str | None = None
        self.model: str | None = None
        self.check_code: str | None = None
        self.category: Category | None = None
        self.master_firmware_version: str | None = None
        self.slave_firmware_version: str | None = None

    def _read_command(self, offset: int, count: int) -> ProtocolCommand:
        """Create read protocol command."""
        return self._protocol.read_command(offset, count)

    def _write_command(self, register: int, value: int) -> ProtocolCommand:
        """Create write protocol command."""
        return self._protocol.write_command(register, value)

    def _write_multi_command(self, offset: int, values: bytes) -> ProtocolCommand:
        """Create write multiple protocol command."""
        return self._protocol.write_multi_command(offset, values)

    async def _read_from_socket(self, command: ProtocolCommand) -> ProtocolResponse:
        try:
            result = await command.execute(self._protocol)
            self._consecutive_failures_count = 0
        except MaxRetriesException:
            self._consecutive_failures_count += 1
            raise RequestFailedException(
                f"No valid response received even after {self._protocol.retries} retries",
                self._consecutive_failures_count,
            ) from None
        except RequestFailedException as ex:
            self._consecutive_failures_count += 1
            raise RequestFailedException(
                ex.message, self._consecutive_failures_count
            ) from None
        else:
            return result

    async def do_discover(self) -> Inverter:
        """Discover inverters on the network."""
        raise NotImplementedError

    async def get_work_mode_options(self) -> list[int]:
        """Get supported work modes."""
        raise NotImplementedError

    async def get_grid_export_limit(self) -> int:
        """Get grid export limit."""
        raise NotImplementedError

    async def set_grid_export_limit(self, value: int):
        """Set grid export limit."""
        raise NotImplementedError

    @abstractmethod
    async def read_setting(self, setting_id: str) -> Any:
        """Read the value of specific inverter setting/configuration parameter.

        Setting must be in list provided by settings() method, otherwise ValueError is raised.
        """
        raise NotImplementedError

    @abstractmethod
    async def write_setting(self, setting_id: str, value: Any):
        """Set the value of specific inverter settings/configuration parameter.

        Setting must be in list provided by settings() method, otherwise ValueError is raised.

        BEWARE !!!
        This method modifies inverter operational parameter (usually accessible to installers only).
        Use with caution and at your own risk !
        """
        raise NotImplementedError

    @abstractmethod
    async def read_device_info(self):
        """Request the device information from the inverter.

        The inverter instance variables will be loaded with relevant data.
        """
        raise NotImplementedError

    @abstractmethod
    async def read_runtime_data(self) -> dict[str, Any]:
        """Request the runtime data from the inverter.

        Answer dictionary of individual sensors and their values.
        List of supported sensors (and their definitions) is provided by sensors() method.
        """
        raise NotImplementedError

    @abstractmethod
    def sensors(self) -> tuple[Sensor, ...]:
        """Return tuple of sensor definitions."""
        raise NotImplementedError

    @abstractmethod
    def settings(self) -> tuple[Sensor, ...]:
        """Return dictionary of settings definitions."""
        raise NotImplementedError

    @staticmethod
    def _create_protocol(
        host: str, port: int, comm_addr: int, timeout: int, retries: int
    ) -> InverterProtocol:
        """Create protocol."""
        return UDPInverterProtocol(host, port, comm_addr, timeout, retries)

    @staticmethod
    def _map_response(
        response: ProtocolResponse, sensors: tuple[Sensor, ...]
    ) -> dict[str, Any]:
        """Process the response data and return dictionary with runtime values."""
        result = {}
        for sensor in sensors:
            try:
                result[sensor.id_] = sensor.read(response)
            except ValueError:
                logger.exception("Error reading sensor %s.", sensor.id_)
                result[sensor.id_] = None
        return result
