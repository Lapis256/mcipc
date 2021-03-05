"""Query client library."""

from typing import Union
import asyncio 
import io

import asyncio_dgram

from mcipc.query.proto import BasicStats
from mcipc.query.proto import BasicStatsRequest
from mcipc.query.proto import BigEndianSignedInt32
from mcipc.query.proto import FullStats
from mcipc.query.proto import FullStatsRequest
from mcipc.query.proto import HandshakeRequest
from mcipc.query.proto import Response


__all__ = ['Client']


Request = Union[BasicStatsRequest, FullStatsRequest]
_Response = Union[BasicStats, FullStats]


def get_message_types(full: bool) -> tuple[Request, _Response]:
    """Returns request and response types."""

    if full:
        return (FullStatsRequest, FullStats)

    return (BasicStatsRequest, BasicStats)


class IsNotConnected(Exception):
    pass


class Client:
    """A basic client, common to Query and RCON."""

    def __init__(self, host: str, port: int, *, timeout: float = None):
        """Sets host an port."""
        self.stream = None
        self.addr = (host, port)
        self.timeout = timeout
        self.challenge_token = None

    async def connect(self):
        """Contects the socket."""
        self.stream = await asyncio_dgram.connect(self.addr)
        print(self.stream)

        if self.challenge_token is None:
            self.challenge_token = await self.handshake()

    async def disconnect(self):
        return self.stream.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return await self.disconnect()
    
    async def send(self, message):
        if self.stream is None:
            raise IsNotConnected("is not connected.")

        async def predicate():
            await self.stream.send(bytes(message))
            return await self.stream.recv()

        return await asyncio.wait_for(predicate(), timeout=self.timeout)

    async def handshake(self) -> BigEndianSignedInt32:
        """Performs a handshake."""
        request = HandshakeRequest.create()
        data, _ = await self.send(request)
        file = io.BytesIO(data)
        response = Response.read(file)

        return response.challenge_token

    async def stats(self, full: bool = False) -> Union[BasicStats, FullStats]:
        """Returns basic or full stats."""
        request_type, return_type = get_message_types(full)
        request = request_type.create(self.challenge_token)
     
        data, _ = await self.send(request)
        file = io.BytesIO(data)
        return return_type.read(file)
