import asyncio
import socket
import ssl
from urllib.parse import urlparse
from .response import Response
from .exceptions import HTTPException
from .utils import build_headers
from .cache import exiosCache

class ClientSession:
    def __init__(self, default_headers=None, timeout=10):
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.cache = exiosCache()

    async def request(self, method, url, headers=None, body=None):
        cached = self.cache.get(url)
        if cached:
            return Response(cached.encode())

        parsed = urlparse(url)
        host = parsed.hostname
        path = parsed.path or "/"
        port = parsed.port or (443 if parsed.scheme == "https" else 80)

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port, ssl=ssl.create_default_context() if parsed.scheme == "https" else None),
                timeout=self.timeout
            )

            payload = body.encode("utf-8") if body else None
            request = build_headers(method.upper(), host, path, self.default_headers, headers, payload)
            writer.write(request.encode("utf-8"))
            if payload:
                writer.write(payload)

            await writer.drain()

            data = b""
            while not reader.at_eof():
                data += await reader.read(1024)

            writer.close()
            await writer.wait_closed()

        except Exception as e:
            raise HTTPException(f"Request failed: {e}")

        self.cache.set(url, data.decode())
        return Response(data)

    async def get(self, url, headers=None):
        return await self.request("GET", url, headers=headers)

    async def post(self, url, headers=None, body=None):
        return await self.request("POST", url, headers=headers, body=body)

    async def put(self, url, headers=None, body=None):
        return await self.request("PUT", url, headers=headers, body=body)

    async def delete(self, url, headers=None):
        return await self.request("DELETE", url, headers=headers)
