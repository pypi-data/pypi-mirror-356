# Sunways

[![PyPi](https://img.shields.io/pypi/v/sunways.svg)](https://pypi.python.org/pypi/sunways/)
[![Python Versions](https://img.shields.io/pypi/pyversions/sunways.svg)](https://github.com/Chriss-Leo/sunways/)
![License](https://img.shields.io/github/license/Chriss-Leo/sunways.svg)

Library for connecting to Sunways inverter over local network and retrieving runtime sensor values and configuration
parameters.

It has been reported to work with Sunways inverters. It
should work with other inverters as well, as long as they listen on UDP port 8899 and respond to one of supported
communication protocols.
In general, if you can connect to your inverter with the official mobile app (SolarGo/PvMaster) over Wi-Fi (not
bluetooth), this library should work.

(If you can't communicate with the inverter despite your model is listed above, it is possible you have old ARM firmware
version. You should ask manufacturer support to upgrade your ARM firmware (not just inverter firmware) to be able to
communicate with the inverter via UDP.)

White-label (sunways manufactured) inverters may work as well, e.g. General Electric GEP (PSB, PSC) and GEH models are
know to work properly.

Since v0.4.x the library also supports standard Modbus/TCP over port 502.
This protocol is supported by the V2.0 version of LAN+WiFi communication dongle (model WLA0000-01-00P).

## Usage

1. Install this package `pip install sunways`
2. Write down your Sunways inverter's IP address (or invoke `sunways.search_inverters()`)
3. Connect to inverter and read all runtime data, example below

```python
import asyncio
import sunways


async def get_runtime_data():
    ip_address = '192.168.1.14'

    inverter = await sunways.connect(ip_address)
    runtime_data = await inverter.read_runtime_data()

    for sensor in inverter.sensors():
        if sensor.id_ in runtime_data:
            print(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")


asyncio.run(get_runtime_data())
```

## References and useful links

- https://github.com/chris/home-assistant-sunways-inverter

