from asyncio.subprocess import Process
import json
import logging

import asyncio
import os
from typing import Optional, TypeVar
import uuid

from reffinder.messages import BaseMessage
from reffinder.enums import LSPMethod

logger = logging.getLogger(__name__)
PYRIGHT_CMD = ["pyright-langserver", "--stdio"]

class LangServer:
    def __init__(self, proc: Process) -> None:
        """Start the Pyright language server as a subprocess."""
        self.proc = proc
        self._writer = proc.stdin
        self._reader = proc.stdout

    @classmethod
    async def start(cls) -> "LangServer":
        logger.info(f"Starting langserver")
        proc = await asyncio.create_subprocess_exec(
            *PYRIGHT_CMD,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        logger.info("Language server started")
        return cls(proc)

    @property
    def writer(self) -> asyncio.StreamWriter:
        if self._writer is None:
            raise RuntimeError("Server hasn't been started yet")
        return self._writer
    @property
    def reader(self)-> asyncio.StreamReader:
        if self._reader is None:
            raise RuntimeError("Server hasn't been started yet")
        return self._reader
    
    async def send_message(self,message:BaseMessage, read_response=False) -> Optional[dict] :
        """Send a JSON-RPC message to the LSP server."""

        logger.debug(f"Sending: {message}")

        self.writer.write(message.encode())
        await self.writer.drain()
        # Wait for initialize response
        while read_response:
            msg = await self.read_lsp_response()
            logger.debug(f"{msg}")
            if msg.get("id") == message.id:
                return msg
        return None



    async def read_lsp_response(self) -> dict:
        # Read headers
        headers = {}
        while True:
            line = await self.reader.readline()
            if line == b"\r\n":
                break
            key, value = line.decode().strip().split(": ", 1)
            headers[key] = value
        content_length = int(headers.get("Content-Length", 0))
        body = await self.reader.readexactly(content_length)
        return json.loads(body.decode())

    async def initialize(self, root_uri: str) -> None:
        """Initialize the language server with the given root URI."""
        logger.debug(f"Initializing langserver with root URI: {root_uri}")
        msg = BaseMessage(
            method=LSPMethod.INITIALIZE,
            params={
                "processId": None,
                "rootUri": f"file://{os.path.abspath(root_uri)}",
                "workspaceFolders": [
                    {
                        "uri": root_uri,
                        "name": os.path.basename(root_uri)
                    }
                ],
                "capabilities": {},
            },
            id=str(uuid.uuid4())
        )
        await self.send_message(
            message=msg,
            read_response=True
        )
        msg= BaseMessage(method=LSPMethod.INITIALIZED)
        # Send initialized notification
        await self.send_message(message=msg)
        return
    
    async def shutdown(self) -> None:
        """Shutdown the language server."""
        if self.proc is not None:
            logger.debug("Shutting down langserver")
            self.proc.terminate()
            await self.proc.wait()
            self._writer = None
            self._reader = None
            logger.info("Langserver shutdown complete")
