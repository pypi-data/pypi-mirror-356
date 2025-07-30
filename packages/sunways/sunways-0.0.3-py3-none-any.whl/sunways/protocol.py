"""protocol class."""

from __future__ import annotations

import asyncio
from asyncio.futures import Future
from collections.abc import Callable
import io
import logging

from .exceptions import (
    MaxRetriesException,
    PartialResponseException,
    RequestFailedException,
    RequestRejectedException,
)
from .modbus import (
    MODBUS_READ_CMD,
    MODBUS_WRITE_CMD,
    MODBUS_WRITE_MULTI_CMD,
    create_modbus_rtu_multi_request,
    create_modbus_rtu_request,
    validate_modbus_rtu_response,
)

logger = logging.getLogger(__name__)


class InverterProtocol:
    """Inverter protocol class."""

    def __init__(
        self, host: str, port: int, comm_addr: int, timeout: int, retries: int
    ) -> None:
        """Initialize the inverter protocol."""

        self._host: str = host
        self._port: int = port
        self._comm_addr: int = comm_addr
        self._running_loop: asyncio.AbstractEventLoop | None = None
        self._lock: asyncio.Lock | None = None
        self._partial_data: bytes | None = None
        self._partial_missing: int = 0
        self._timer: asyncio.TimerHandle | None = None
        self._transport: asyncio.transports.Transport | None = None
        self.keep_alive: bool = False
        self.timeout: int = timeout
        self.retries: int = retries
        self.protocol: asyncio.Protocol | None = None
        self.command: ProtocolCommand | None = None
        self.response_future: Future | None = None

    def _close_transport(self) -> None:
        if self._transport:
            try:
                self._transport.close()
            except RuntimeError:
                logger.debug("Failed to close transport.")
            self._transport = None
        # Cancel Future on connection lost
        if self.response_future and not self.response_future.done():
            self.response_future.cancel()

    def _ensure_lock(self) -> asyncio.Lock:
        """Validate (or create) asyncio Lock.

        The asyncio.Lock must always be created from within's asyncio loop,
           so it cannot be eagerly created in constructor.
           Additionally, since asyncio.run() creates and closes its own loop,
           the lock's scope (its creating loop) mus be verified to support proper
           behavior in subsequent asyncio.run() invocations.

        """
        if self._lock and self._running_loop == asyncio.get_event_loop():
            return self._lock
        logger.debug("Creating lock instance for current event loop.")
        self._lock = asyncio.Lock()
        self._running_loop = asyncio.get_event_loop()
        self._close_transport()
        return self._lock

    def _max_retries_reached(self) -> Future:
        logger.debug(
            "Max number of retries (%d) reached, request %s failed.",
            self.retries,
            self.command,
        )
        self._close_transport()
        self.response_future = asyncio.get_running_loop().create_future()
        self.response_future.set_exception(MaxRetriesException)
        return self.response_future

    def read_command(self, offset: int, count: int) -> ProtocolCommand:
        """Create read protocol command."""
        raise NotImplementedError

    def write_command(self, register: int, value: int) -> ProtocolCommand:
        """Create write protocol command."""
        raise NotImplementedError

    def write_multi_command(self, offset: int, values: bytes) -> ProtocolCommand:
        """Create write multiple protocol command."""
        raise NotImplementedError

    async def close(self):
        """Close transport."""
        raise NotImplementedError

    async def send_request(self, command: ProtocolCommand) -> Future:
        """Convert command to request and send it to inverter."""
        raise NotImplementedError


class ProtocolCommand:
    """Protocol command class."""

    def __init__(self, request: bytes, validator: Callable[[bytes], bool]) -> None:
        """Initialize protocol command."""
        self.request: bytes = request
        self.validator: Callable[[bytes], bool] = validator

    def __eq__(self, other):
        """Judge via cmd."""
        if not isinstance(other, ProtocolCommand):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.request == other.request

    def __repr__(self):
        """Return string representation of the command."""
        return self.request.hex()

    def trim_response(self, raw_response: bytes):
        """Trim raw response from header and checksum data."""
        return raw_response

    def get_offset(self, address: int):
        """Calculate relative offset to start of the response bytes."""
        return address

    async def execute(self, protocol: InverterProtocol) -> ProtocolResponse:
        """Execute the protocol command on the specified connection.

        Return ProtocolResponse with raw response data
        """
        try:
            response_future = await protocol.send_request(self)
            result = response_future.result()
            if result is not None:
                return ProtocolResponse(result, self)
            raise RequestFailedException(
                "No response received to '" + self.request.hex() + "' request."
            )
        except (asyncio.CancelledError, ConnectionRefusedError):
            raise RequestFailedException(
                "No valid response received to '" + self.request.hex() + "' request."
            ) from None
        finally:
            if not protocol.keep_alive:
                await protocol.close()


class ProtocolResponse:
    """Protocol response class."""

    def __init__(self, raw_data: bytes, command: ProtocolCommand | None) -> None:
        """Response init."""
        self.raw_data: bytes = raw_data
        self.command: ProtocolCommand = command
        self._bytes: io.BytesIO = io.BytesIO(self.data())

    def __repr__(self):
        """Return string representation of the response."""
        return self.raw_data.hex()

    def data(self) -> bytes:
        """Raw data."""
        if self.command is not None:
            return self.command.trim_response(self.raw_data)
        return self.raw_data

    def seek(self, address: int) -> None:
        """Seek."""
        if self.command is not None:
            self._bytes.seek(self.command.get_offset(address))
        else:
            self._bytes.seek(address)

    def read(self, size: int) -> bytes:
        """Read."""
        return self._bytes.read(size)


class ModbusRtuProtocolCommand(ProtocolCommand):
    """Inverter communication protocol seen on newer generation of inverters, based on Modbus protocol over UDP transport layer."""

    def __init__(self, request: bytes, cmd: int, offset: int, value: int) -> None:
        """Initialize Modbus RTU protocol command."""
        super().__init__(
            request,
            lambda x: validate_modbus_rtu_response(x, cmd, offset, value),
        )
        self.first_address: int = offset
        self.value = value

    def trim_response(self, raw_response: bytes):
        """Trim raw response from header and checksum data."""
        return raw_response[3:-2]

    def get_offset(self, address: int):
        """Calculate relative offset to start of the response bytes."""
        return (address - self.first_address) * 2


class UDPInverterProtocol(InverterProtocol, asyncio.DatagramProtocol):
    """UDP inverter protocol class."""

    def __init__(
        self, host: str, port: int, comm_addr: int, timeout: int = 1, retries: int = 3
    ) -> None:
        """Initialize the UDP inverter protocol."""

        super().__init__(host, port, comm_addr, timeout, retries)
        self._retry: int = 0

    def _send_request(self, command: ProtocolCommand, response_future: Future) -> None:
        """Send message via transport."""
        self._partial_data = None
        self._partial_missing = 0
        self.command = command
        self.response_future = response_future
        payload = command.request
        if self._retry > 0:
            logger.debug(
                "Sending: %s - retry #%s/%s", self.command, self._retry, self.retries
            )
        else:
            logger.debug("Sending: %s", self.command)
        self._transport.sendto(payload)
        self._timer = asyncio.get_running_loop().call_later(
            self.timeout, self._timeout_mechanism
        ) # type: ignore[arg-type]

    def _timeout_mechanism(self) -> None:
        """Timeout mechanism to prevent hanging transport."""
        if self.response_future and self.response_future.done():
            logger.debug("Response already received.")
            self._retry = 0
        else:
            if self._timer:
                logger.debug(
                    "Failed to receive response to %s in time (%ds).",
                    self.command,
                    self.timeout,
                )
                self._timer = None
            if self.response_future and not self.response_future.done():
                self.response_future.cancel()

    async def _connect(self) -> None:
        """连接并监听."""
        if not self._transport or self._transport.is_closing():
            (
                self._transport,
                self.protocol,
            ) = await asyncio.get_running_loop().create_datagram_endpoint(
                lambda: self,
                remote_addr=(self._host, self._port),
            )

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        """On connection made."""
        self._transport = transport

    def connection_lost(self, exc: Exception | None) -> None:
        """On connection lost."""
        if exc:
            logger.debug("Socket closed with error: %s.", exc)
        else:
            logger.debug("Socket closed.")
        self._close_transport()

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        """On datagram received."""
        if self._timer:
            self._timer.cancel()
            self._timer = None
        try:
            if self._partial_data and self._partial_missing == len(data):
                logger.debug(
                    "Composed fragmented response: %s + %s",
                    self._partial_data.hex(),
                    data.hex(),
                )
                data = self._partial_data + data
                self._partial_data = None
                self._partial_missing = 0
            if self.command.validator(data):
                logger.debug("Received: %s", data.hex())
                self._retry = 0
                self.response_future.set_result(data)
            else:
                logger.debug("Received invalid response: %s", data.hex())
                asyncio.get_running_loop().call_soon(self._timeout_mechanism) # type: ignore[arg-type]
        except PartialResponseException as ex:
            logger.debug(
                "Received response fragment (%d of %d): %s",
                ex.length,
                ex.expected,
                data.hex(),
            )
            self._partial_data = data
            self._partial_missing = ex.expected - ex.length
            self._timer = asyncio.get_running_loop().call_later(
                self.timeout, self._timeout_mechanism
            ) # type: ignore[arg-type]
        except asyncio.InvalidStateError:
            logger.debug("Response already handled: %s", data.hex())
        except RequestRejectedException as ex:
            logger.debug("Received exception response: %s", data.hex())
            if self.response_future and not self.response_future.done():
                self.response_future.set_exception(ex)
            self._close_transport()

    def error_received(self, exc: Exception) -> None:
        """On error received."""
        logger.debug("Received error: %s", exc)
        self.response_future.set_exception(exc)
        self._close_transport()

    def read_command(self, offset: int, count: int) -> ProtocolCommand:
        """Create read protocol command."""
        return ModbusRtuReadCommand(self._comm_addr, offset, count)

    def write_command(self, register: int, value: int) -> ProtocolCommand:
        """Create write protocol command."""
        return ModbusRtuWriteCommand(self._comm_addr, register, value)

    def write_multi_command(self, offset: int, values: bytes) -> ProtocolCommand:
        """Create write multiple protocol command."""
        return ModbusRtuWriteMultiCommand(self._comm_addr, offset, values)

    async def close(self):
        """Close transport."""
        self._close_transport()

    async def send_request(self, command: ProtocolCommand) -> Future:
        """Send message via transport."""
        await self._ensure_lock().acquire()
        try:
            await self._connect()
            response_future = asyncio.get_running_loop().create_future()
            self._send_request(command, response_future)
            await response_future
        except asyncio.CancelledError:
            if self._retry < self.retries:
                self._retry += 1
                if self._lock and self._lock.locked():
                    self._lock.release()
                if not self.keep_alive:
                    self._close_transport()
                return await self.send_request(command)
            return self._max_retries_reached()
        else:
            return response_future
        finally:
            if self._lock and self._lock.locked():
                self._lock.release()
            if not self.keep_alive:
                self._close_transport()


class ModbusRtuReadCommand(ModbusRtuProtocolCommand):
    """Inverter Modbus/RTU READ command for retrieving <count> modbus registers starting at register # <offset>."""

    def __init__(self, comm_addr: int, offset: int, count: int) -> None:
        """Initialize Modbus RTU read command."""
        super().__init__(
            create_modbus_rtu_request(comm_addr, MODBUS_READ_CMD, offset, count),
            MODBUS_READ_CMD,
            offset,
            count,
        )

    def __repr__(self):
        """Return string representation of the command."""
        if self.value > 1:
            return f"READ {self.value} registers from {self.first_address} ({self.request.hex()})"
        return f"READ register {self.first_address} ({self.request.hex()})"


class ModbusRtuWriteCommand(ModbusRtuProtocolCommand):
    """Inverter Modbus/RTU WRITE command setting single modbus register # <register> value <value>."""

    def __init__(self, comm_addr: int, register: int, value: int) -> None:
        """Initialize Modbus RTU write command."""
        super().__init__(
            create_modbus_rtu_request(comm_addr, MODBUS_WRITE_CMD, register, value),
            MODBUS_WRITE_CMD,
            register,
            value,
        )

    def __repr__(self):
        """Return string representation of the command."""
        return f"WRITE {self.value} to register {self.first_address} ({self.request.hex()})"


class ModbusRtuWriteMultiCommand(ModbusRtuProtocolCommand):
    """Inverter Modbus/RTU WRITE command setting multiple modbus register # <register> value <value>."""

    def __init__(self, comm_addr: int, offset: int, values: bytes) -> None:
        """Initialize Modbus RTU write multi command."""
        super().__init__(
            create_modbus_rtu_multi_request(
                comm_addr, MODBUS_WRITE_MULTI_CMD, offset, values
            ),
            MODBUS_WRITE_MULTI_CMD,
            offset,
            len(values) // 2,
        )
