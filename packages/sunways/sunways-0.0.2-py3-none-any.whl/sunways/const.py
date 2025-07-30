"""Constants for the Sunways device."""

from datetime import timedelta

DOMAIN = "sunways"

DEFAULT_NAME = "Sunways"

CATEGORY = "category"

SCAN_INTERVAL = timedelta(seconds=10)

GRID_EXPORT_LIMIT, WORK_MODE, GRID_ENABLE, GRID_EXPORT_LIMIT_ENABLE = (
    "grid_export_limit",
    "work_mode",
    "grid_enable",
    "grid_export_limit_enable",
)
PAC, PPV, PLOAD, PMETER = ("pac", "ppv", "pload", "pmeter")

BATTERY_SOC, BATTERY_SOH = "battery_soc", "battery_soh"

WORK_STATUS: dict[int, str] = {
    0: "Work Wait",
    1: "Work Check",
    2: "Work Normal",
    3: "Work Fault",
    4: "Work Flash",
    5: "Off Grid",
}

WORK_MODES: dict[int, str] = {
    257: "general_mode",
    258: "economic_mode",
    259: "ups_mode",
    260: "auto_ups",
    261: "coupled_mode",
    262: "gen_mode",
    512: "off_grid_mode",
    513: "single_machine_mode",
    514: "piece_together_mode",
    515: "parallel_mode",
    768: "ems_mode",
    769: "ems_ac_ctrl",
    770: "ems_general",
    771: "ems_batt_ctrl",
    772: "ems_off_grid_mode",
    1024: "heavy_charge_mode",
    1025: "strong_mode",
}

ILLEGAL_DATA_ADDRESS: str = "ILLEGAL DATA ADDRESS"
