"""连接."""

from .exceptions import InverterError
from .inverter import Category, Inverter
from .product import HybridInv, InvHelper, OnGridInv


async def connect(
    host: str,
    port: int = 5488,
    timeout: int = 3,
    retries: int = 3,
    discover: bool = True,
    category: int | None = None,
) -> Inverter:
    """不同的设备不同的处理."""

    if category == Category.ON_GRID:
        inv = OnGridInv(host, port, timeout, retries)
    elif category == Category.HYBRID:
        inv = HybridInv(host, port, timeout, retries)
    elif category is None and discover:
        helper = InvHelper(host, port, timeout, retries)
        inv = await helper.do_discover()
    else:
        raise InverterError(f"Unknown category: {category}")
    await inv.read_device_info()
    return inv
