"""TODO document"""
import asyncio
import json
import logging
import sys
import time
from typing import Any
from aiortc import RTCSessionDescription

from custom_types.message import MessageDict
from custom_types.connection import ConnectionOfferDict

from modules.config import Config
from modules.connection_state import ConnectionState
from modules.connection import Connection, connection_factory
from modules.subprocess_logging import SubprocessLoggingHandler


class ConnectionRunner:
    """TODO document"""

    _connection: Connection | None
    _lock: asyncio.Lock
    _running: bool
    _stopped_event: asyncio.Event
    _tasks: list[asyncio.Task]
    _logger: logging.Logger

    def __init__(self) -> None:
        """TODO document"""
        self._connection = None
        self._lock = asyncio.Lock()
        self._running = False
        self._tasks = []
        self._stopped_event = asyncio.Event()
        config = Config()

        # Setup logging for subprocess
        handler = SubprocessLoggingHandler(self._send_command)
        logging.basicConfig(level=logging.getLevelName(config.log), handlers=[handler])

        # Set logging level for libraries
        dependencies_log_level = logging.getLevelName(config.log_dependencies)
        logging.getLogger("aiohttp").setLevel(dependencies_log_level)
        logging.getLogger("aioice").setLevel(dependencies_log_level)
        logging.getLogger("aiortc").setLevel(dependencies_log_level)
        logging.getLogger("PIL").setLevel(dependencies_log_level)

        self._logger = logging.getLogger("ConnectionRunner")

    async def run(
        self,
        offer: RTCSessionDescription,
        log_name_suffix: str,
    ) -> None:
        """TODO document"""
        self._running = True
        answer, self._connection = await connection_factory(
            offer, self._relay_api_message, log_name_suffix
        )
        self._connection.add_listener("state_change", self._handle_state_change)
        self._send_command(
            "SET_LOCAL_DESCRIPTION", {"sdp": answer.sdp, "type": answer.type}
        )

        await self._listen_for_messages()
        self._logger.debug("ConnectionRunner exiting")

    async def stop(self) -> None:
        """TODO document"""
        self._logger.debug("ConnectionRunner Stopping")
        async with self._lock:
            self._running = False
        await asyncio.gather(*self._tasks)
        self._stopped_event.set()
        self._logger.debug("Stop complete")

    async def _listen_for_messages(self) -> None:
        """TODO document"""
        self._logger.debug("Listening for messages from main process")
        msg = ""
        while msg != "q":
            async with self._lock:
                if not self._running:
                    return

            msg = await self._read()

            try:
                parsed = json.loads(msg)
            except (json.JSONDecodeError, TypeError) as e:
                self._logger.error(f"Failed to parse message from main process: {e}")
                continue

            await self._handle_message(parsed)

    async def _handle_message(self, msg: dict):
        """TODO document"""
        data = msg["data"]
        command = msg["command"]
        # self._logger.debug(f"Received {command} command from main process")

        if self._connection is None:
            self._logger.warning(
                f"Failed to handle {command}, connection is None. Data: {data}"
            )
            return

        match command:
            case "PING":
                self._send_command(
                    "PONG", {"original": msg["data"], "subprocess_time": time.time()}
                )
            case "SEND":
                await self._connection.send(data)
            case "CREATE_OFFER":
                offer = await self._connection.create_subscriber_offer(data)
                self._send_command("SUBSCRIBER_OFFER", offer)
            case "HANDLE_ANSWER":
                await self._connection.handle_subscriber_answer(data)
            case "STOP_SUBCONNECTION":
                await self._connection.stop_subconnection(data)
            case "SET_MUTED":
                video, audio = data
                await self._connection.set_muted(video, audio)
            case _:
                self._logger.error(f"Unrecognized command from main process: {command}")

    async def _read(self):
        """TODO document"""
        return await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)

    async def _handle_state_change(self, state: ConnectionState) -> None:
        """TODO document"""
        self._send_command("STATE_CHANGE", state.value)
        if state in [ConnectionState.CLOSED, ConnectionState.FAILED]:
            self._logger.debug(f"Stopping, because state is {state}")
            await self.stop()

    async def _relay_api_message(self, message: MessageDict | Any) -> None:
        """TODO document"""
        self._send_command("API", message)
        pass

    def _send_command(
        self,
        command: str,
        data: str | int | float | dict | MessageDict | ConnectionOfferDict,
    ) -> None:
        """Send to main process"""
        data = json.dumps({"command": command, "data": data})
        print(data, flush=True)
