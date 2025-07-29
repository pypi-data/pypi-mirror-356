# TA-CMI
A Python wrapper to read out sensors from Technische Alternative using the C.M.I.

## How to use package

### Json API

```python
import asyncio

from ta_cmi import CMI, Languages, ApiError, RateLimitError, InvalidCredentialsError, InvalidDeviceError, ChannelType


async def main():
    try:
        cmi = CMI("http://192.168.1.101", "admin", "admin")

        devices = await cmi.get_devices()

        device = devices[0]

        # Set type automatically
        await device.fetch_type()

        # Set type manually
        device.set_device_type("UVR16x2")

        await device.update()

        print(str(device))

        inputChannels = device.get_channels(ChannelType.INPUT)
        outputChannels = device.get_channels(ChannelType.OUTPUT)
        analogLogging = device.get_channels(ChannelType.ANALOG_LOGGING)

        for i in inputChannels:
            ch = inputChannels.get(i)
            print(str(ch))

        for o in outputChannels:
            ch = outputChannels.get(o)
            print(f"{str(ch)} - {ch.get_unit(Languages.DE)}")

        for al in analogLogging:
            ch = analogLogging.get(al)
            print(f"{str(ch)} - {ch.get_unit(Languages.DE)}")

    except (ApiError, RateLimitError, InvalidCredentialsError, InvalidDeviceError) as error:
        print(f"Error: {error}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

## Supported data types

| Device type | Inputs | Outputs | DL-inputs | System-values: General | System-values: Date | System-values: Time | System-values: Sun | System-values: Electrical power | Analog network inputs | Digital network inputs | M-Bus | Modbus | KNX | Analog logging | Digital logging |
|-------------|:------:|:-------:|:---------:|:----------------------:|:-------------------:|:-------------------:|:------------------:|:-------------------------------:|:---------------------:|:----------------------:|:-----:|:------:|:---:|:--------------:|:---------------:|
| UVR1611     |   ✔    |    ✔    |     ❌     |           ❌            |          ❌          |          ❌          |         ❌          |                ❌                |           ✔           |           ✔            |   ❌   |   ❌    |  ❌  |       ❌        |        ❌        |
| UVR16x2     |   ✔    |    ✔    |     ✔     |           ✔            |          ✔          |          ✔          |         ✔          |                ❌                |           ❌           |           ❌            |   ❌   |   ❌    |  ❌  |       ✔        |        ✔        |
| RSM610      |   ✔    |    ✔    |     ✔     |           ❌            |          ❌          |          ❌          |         ❌          |                ❌                |           ❌           |           ❌            |   ✔   |   ❌    |  ❌  |       ❌        |        ❌        |
| CAN-I/O45   |   ✔    |    ✔    |     ✔     |           ❌            |          ❌          |          ❌          |         ❌          |                ❌                |           ❌           |           ❌            |   ❌   |   ❌    |  ❌  |       ❌        |        ❌        |
| CAN-EZ2     |   ✔    |    ✔    |     ❌     |           ❌            |          ❌          |          ❌          |         ❌          |                ✔                |           ❌           |           ❌            |   ❌   |   ❌    |  ❌  |       ❌        |        ❌        |
| CAN-MTx2    |   ✔    |    ✔    |     ❌     |           ❌            |          ❌          |          ❌          |         ❌          |                ❌                |           ❌           |           ❌            |   ❌   |   ❌    |  ❌  |       ❌        |        ❌        |
| CAN-BC2     |   ❌    |    ❌    |     ❌     |           ❌            |          ❌          |          ❌          |         ❌          |                ❌                |           ❌           |           ❌            |   ✔   |   ✔    |  ✔  |       ❌        |        ❌        |
| UVR65       |   ✔    |    ✔    |     ❌     |           ❌            |          ❌          |          ❌          |         ❌          |                ❌                |           ❌           |           ❌            |   ❌   |   ❌    |  ❌  |       ❌        |        ❌        |
| CAN-EZ3     |   ❌    |    ❌    |     ✔     |           ✔            |          ✔          |          ✔          |         ✔          |                ✔                |           ❌           |           ❌            |   ❌   |   ✔    |  ❌  |       ✔        |        ✔        |
| UVR610      |   ✔    |    ✔    |     ✔     |           ❌            |          ❌          |          ❌          |         ❌          |                ❌                |           ❌           |           ❌            |   ✔   |   ❌    |  ❌  |       ✔        |        ✔        |
| UVR67       |   ✔    |    ✔    |     ❌     |           ❌            |          ❌          |          ❌          |         ❌          |                ❌                |           ❌           |           ❌            |   ❌   |   ❌    |  ❌  |       ❌        |        ❌        |

> **Note**
> The supported data types may differ from the official API. If a device type supports other data types than listed here, please create an issue.

### CoE Server

Data can be retrieved using [this](https://gitlab.com/DeerMaximum/ta-coe) CoE to HTTP server

```python
import asyncio

from ta_cmi import (
    ApiError,
    ChannelMode,
    CoE,
    InvalidCredentialsError,
    InvalidDeviceError,
    Languages,
    RateLimitError,
)


async def main():
    try:
        coe = CoE("http://192.168.2.201:9000")
        
        can_id = 42

        await coe.update(can_id)

        analog_channels = coe.get_channels(can_id, ChannelMode.ANALOG)
        digital_channels = coe.get_channels(can_id, ChannelMode.DIGITAL)

        for i in analog_channels:
            ch = analog_channels.get(i)
            print(str(ch))

        for o in digital_channels:
            ch = digital_channels.get(o)
            print(f"{str(ch)} - {ch.get_unit(Languages.DE)}")

    except (ApiError, RateLimitError, InvalidCredentialsError, InvalidDeviceError) as error:
        print(f"Error: {error}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```