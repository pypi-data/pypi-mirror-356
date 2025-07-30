"""Sunways Product."""

import logging
from typing import Any

from .const import (
    BATTERY_SOC,
    BATTERY_SOH,
    GRID_ENABLE,
    GRID_EXPORT_LIMIT,
    GRID_EXPORT_LIMIT_ENABLE,
    ILLEGAL_DATA_ADDRESS,
    PAC,
    PLOAD,
    PMETER,
    PPV,
    WORK_MODES,
    WORK_STATUS,
)
from .exceptions import InverterError, RequestRejectedException
from .inverter import (
    Calculated,
    Category,
    Current,
    Energy,
    Enum2,
    Frequency,
    Integer,
    Inverter,
    Long,
    Power,
    Sensor,
    SensorKind,
    Temp,
    Timestamp,
    Voltage,
)
from .protocol import ProtocolCommand
from .util import (
    decode_string,
    read_current,
    read_unsigned_int16,
    read_unsigned_int32,
    read_voltage,
)

logger = logging.getLogger(__name__)


class OnGridInv(Inverter):
    """并网逆变器."""

    __sensors: tuple[Sensor, ...] = (
        Timestamp("timestamp", 10100, "Timestamp"),
        Integer("rssi", 10103, "RSSI"),
        Integer("safety_country", 10104, "Safety Country code"),
        Enum2("work_status", 10105, "Work Status", WORK_STATUS),
    )

    __sensors2: tuple[Sensor, ...] = (
        Power(PMETER, 11000, "Meter Power", SensorKind.AC),
        Voltage("v_grid1", 11009, "On-grid L1 Voltage", SensorKind.AC),
        Current("i_grid1", 11010, "On-grid L1 Current", SensorKind.AC),
        Calculated(
            "p_grid1",
            lambda data: round(read_voltage(data, 11009) * read_current(data, 11010)),
            "On-grid L1 Power",
            "W",
            SensorKind.AC,
        ),
        Voltage("v_grid2", 11011, "On-grid L2 Voltage", SensorKind.AC),
        Current("i_grid2", 11012, "On-grid L2 Current", SensorKind.AC),
        Calculated(
            "p_grid2",
            lambda data: round(read_voltage(data, 11011) * read_current(data, 11012)),
            "On-grid L2 Power",
            "W",
            SensorKind.AC,
        ),
        Voltage("v_grid3", 11013, "On-grid L3 Voltage", SensorKind.AC),
        Current("i_grid3", 11014, "On-grid L3 Current", SensorKind.AC),
        Frequency("f_grid", 11015, "On-grid Frequency", SensorKind.AC),
        Power(PAC, 11016, "Active Power", SensorKind.AC),
        Calculated(
            "p_grid3",
            lambda data: round(read_voltage(data, 11013) * read_current(data, 11014)),
            "On-grid L3 Power",
            "W",
            SensorKind.AC,
        ),
        Power("ppvInput", 11028, "PV Power", SensorKind.PV),
        Temp("temperature", 11032, "Inverter Temperature", SensorKind.TEMP),
        Voltage("vpv1", 11038, "PV1 Voltage", SensorKind.PV),
        Current("ipv1", 11039, "PV1 Current", SensorKind.PV),
        Voltage("vpv2", 11040, "PV2 Voltage", SensorKind.PV),
        Current("ipv2", 11041, "PV2 Current", SensorKind.PV),
        Voltage("vpv3", 11042, "PV3 Voltage", SensorKind.PV),
        Current("ipv3", 11043, "PV3 Current", SensorKind.PV),
        Calculated(
            "ppv1",
            lambda data: round(read_voltage(data, 11038) * read_current(data, 11039)),
            "PV1 Power",
            "W",
            SensorKind.PV,
        ),
        Calculated(
            "ppv2",
            lambda data: round(read_voltage(data, 11040) * read_current(data, 11041)),
            "PV2 Power",
            "W",
            SensorKind.PV,
        ),
        Calculated(
            "ppv3",
            lambda data: round(read_voltage(data, 11042) * read_current(data, 11043)),
            "PV3 Power",
            "W",
            SensorKind.PV,
        ),
        Calculated(
            PPV,
            lambda data: (round(read_voltage(data, 11038) * read_current(data, 11039)))
            + (round(read_voltage(data, 11040) * read_current(data, 11041)))
            + (round(read_voltage(data, 11042) * read_current(data, 11043))),
            "PV Power",
            "W",
            SensorKind.PV,
        ),
        Calculated(
            PLOAD,
            lambda data: 0,
            "Load Power",
            "W",
            SensorKind.AC,
        ),
        Energy("e_day", 11018, "Today's PV Generation", SensorKind.PV),
        Energy("e_total", 11020, "Total PV Generation", SensorKind.PV),
        Long("time_total", 11022, "Hours Total", "h", SensorKind.PV),
    )

    __settings_on_grid: tuple[Sensor, ...] = (
        Timestamp("time", 20000, "Inverter time"),
        Integer(GRID_ENABLE, 25008, "Grid Enabled", "", SensorKind.GRID),
        Integer(
            GRID_EXPORT_LIMIT_ENABLE,
            25100,
            "Grid Export Limit Enabled",
            "",
            SensorKind.GRID,
        ),
        Integer(GRID_EXPORT_LIMIT, 25103, "Grid Export Limit", "%", SensorKind.GRID),
    )

    def __init__(
        self, host: str, port: int, timeout: int = 1, retries: int = 3
    ) -> None:
        """Init On-grid inverter."""
        super().__init__(host, port, 0xFE, timeout, retries)
        self._READ_DEVICE_INFO: ProtocolCommand = self._read_command(0x2710, 57)
        self._READ_RUNTIME_DATA: ProtocolCommand = self._read_command(0x2774, 24)
        self._READ_RUNTIME_DATA2: ProtocolCommand = self._read_command(0x2AF8, 98)
        self._sensors = self.__sensors
        self._sensors2 = self.__sensors2
        self._settings: dict[str, Sensor] = {s.id_: s for s in self.__settings_on_grid}
        self.category = Category.ON_GRID

    async def _read_sensor(self, sensor: Sensor) -> Any:
        try:
            count = (sensor.size_ + (sensor.size_ % 2)) // 2
            response = await self._read_from_socket(
                self._read_command(sensor.offset, count)
            )
            return sensor.read_value(response)
        except RequestRejectedException as ex:
            if ex.message == ILLEGAL_DATA_ADDRESS:
                logger.debug("Unsupported sensor/setting %s", sensor.id_)
                self._settings.pop(sensor.id_, None)
                raise ValueError(f'Unknown sensor/setting "{sensor.id_}"') from None
            return None

    async def _write_setting(self, setting: Sensor, value: Any):
        if setting.size_ == 1:
            # modbus can address/store only 16 bit values, read the other 8 bytes
            response = await self._read_from_socket(
                self._read_command(setting.offset, 1)
            )
            raw_value = setting.encode_value(value, response.data()[0:2])
        else:
            raw_value = setting.encode_value(value)
        if len(raw_value) <= 2:
            value = int.from_bytes(raw_value, byteorder="big", signed=True)
            await self._read_from_socket(self._write_command(setting.offset, value))
        else:
            await self._read_from_socket(
                self._write_multi_command(setting.offset, raw_value)
            )

    async def read_device_info(self):
        """读取设备信息."""
        device_response = await self._read_from_socket(self._READ_DEVICE_INFO)
        device_data = device_response.data()
        self.serial_number = decode_string(device_data[0:16])
        self.model = read_unsigned_int16(device_data, 16)
        self.master_firmware_version = read_unsigned_int32(device_data, 26)
        self.slave_firmware_version = read_unsigned_int32(device_data, 30)
        self.check_code = decode_string(device_data[46:49])

    async def read_runtime_data(self) -> dict[str, Any]:
        """读取运行时数据."""
        response = await self._read_from_socket(self._READ_RUNTIME_DATA)
        runtime_data = self._map_response(response, self._sensors)
        response = await self._read_from_socket(self._READ_RUNTIME_DATA2)
        runtime_data.update(self._map_response(response, self._sensors2))
        ppv = runtime_data.get(PPV, 0)
        pmeter = runtime_data.get(PMETER, 0) or 0
        # 计算pload
        if await self.read_setting(GRID_EXPORT_LIMIT_ENABLE):
            runtime_data[PLOAD] = ppv - pmeter
        else:
            runtime_data[PPV] = runtime_data[PAC]
        return runtime_data

    async def read_setting(self, setting_id: str) -> Any:
        """Read setting."""
        setting: Sensor = self._settings.get(setting_id)
        if setting:
            return await self._read_sensor(setting)
        raise ValueError(f'Unknown setting "{setting_id}"')

    async def write_setting(self, setting_id: str, value: Any):
        """Write setting."""
        setting = self._settings.get(setting_id)
        if setting:
            await self._write_setting(setting, value)
        else:
            raise ValueError(f'Unknown setting "{setting_id}"')

    async def get_grid_export_limit(self) -> int:
        """获取电网出口限制."""
        return (await self.read_setting(GRID_EXPORT_LIMIT) or 0) // 10

    async def set_grid_export_limit(self, value: int):
        """设置电网出口限制."""
        if 0 <= value <= 100:
            await self.write_setting(GRID_EXPORT_LIMIT, value * 10)

    def sensors(self) -> tuple[Sensor, ...]:
        """返回传感器列表."""
        return self._sensors + self._sensors2

    def settings(self) -> tuple[Sensor, ...]:
        """返回设置列表."""
        return tuple(self._settings.values()) # type: ignore[]


class HybridInv(OnGridInv):
    """混合逆变器."""

    __sensors_battery: tuple[Sensor, ...] = (
        Power("p_battery", 40258, "Battery Power", SensorKind.BAT),
        Power(BATTERY_SOC, 43000, "SOC", SensorKind.BAT),
        Integer(BATTERY_SOH, 43001, "SOH", "%", SensorKind.BAT),
        Temp("battery_temperature", 43003, "Battery Temperature", SensorKind.TEMP),
    )

    __settings_hybrid: tuple[Sensor, ...] = (
        Integer("work_mode", 50000, "Work Mode", "", SensorKind.AC),
    )

    def __init__(
        self, host: str, port: int, timeout: int = 1, retries: int = 3
    ) -> None:
        """Init Hybrid inverter."""
        super().__init__(host, port, timeout, retries)
        self._READ_BATTERY_INFO: ProtocolCommand = self._read_command(0xA410, 7)
        self._READ_BATTERY_RUNTIME_DATA1: ProtocolCommand = self._read_command(
            0x9D42, 2
        )
        self._READ_BATTERY_RUNTIME_DATA2: ProtocolCommand = self._read_command(
            0xA7F8, 4
        )
        self._settings: dict[str, Sensor] = {
            s.id_: s for s in self.__settings_hybrid + self.__settings_on_grid
        }
        self._sensors_battery = self.__sensors_battery
        self.battery_version: str | None = None
        self.category = Category.HYBRID

    async def read_device_info(self):
        """读取储能设备信息."""
        await super().read_device_info()
        battery_response = await self._read_from_socket(self._READ_BATTERY_INFO)
        battery_data = battery_response.data()
        self.battery_version = read_unsigned_int16(battery_data, 6)

    async def read_runtime_data(self) -> dict[str, Any]:
        """读取储能运行时数据."""
        response = await self._read_from_socket(self._READ_RUNTIME_DATA)
        runtime_data = self._map_response(response, self._sensors)
        response = await self._read_from_socket(self._READ_RUNTIME_DATA2)
        runtime_data.update(self._map_response(response, self._sensors2))
        response = await self._read_from_socket(self._READ_BATTERY_RUNTIME_DATA1)
        runtime_data.update(self._map_response(response, self._sensors_battery))
        response = await self._read_from_socket(self._READ_BATTERY_RUNTIME_DATA2)
        runtime_data.update(self._map_response(response, self._sensors_battery))
        ppv = runtime_data.get(PPV, 0)
        pmeter = runtime_data.get(PMETER, 0) or 0
        runtime_data[PLOAD] = ppv - pmeter
        return runtime_data

    async def get_work_mode_options(self) -> list[int]:
        """Get work mode options."""
        return list(WORK_MODES)

    def sensors(self) -> tuple[Sensor, ...]:
        """返回储能机传感器列表."""
        return self._sensors + self._sensors2 + self._sensors_battery


class InvHelper(OnGridInv):
    """Inverter helper class."""

    def __init__(
        self, host: str, port: int, timeout: int = 1, retries: int = 3
    ) -> None:
        """Init Discovery helper."""
        super().__init__(host, port, timeout, retries)
        self.category = None
        self._host, self._port, self._timeout, self._retries = (
            host,
            port,
            timeout,
            retries,
        )
        self._READ_SN: ProtocolCommand = self._read_command(0x2710, 8)

    async def do_discover(self) -> Inverter:
        """Discover inverter."""
        device_response = await self._read_from_socket(self._READ_SN)
        device_data = device_response.data()
        self.serial_number = decode_string(device_data[0:16])
        if self.serial_number and self.serial_number[2] == "0":
            return OnGridInv(self._host, self._port, self._timeout, self._retries)
        if self.serial_number and self.serial_number[2] == "1":
            return HybridInv(self._host, self._port, self._timeout, self._retries)
        raise InverterError("Unknown inverter type")
