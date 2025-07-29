"""Async client for SVO semantic chunker microservice."""

__version__ = "1.0.1"

import aiohttp
from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class SVOServerError(Exception):
    """Raised when the SVO server returns an error in the chunk response."""
    def __init__(self, code: str, message: str, chunk_error: dict = None):
        self.code = code
        self.message = message
        self.chunk_error = chunk_error or {}
        super().__init__(f"SVO server error [{code}]: {message}")

class ChunkerClient:
    def __init__(self, url: str = "http://localhost", port: int = 8009, timeout: float = 60.0):
        """
        :param url: Base URL of the SVO chunker service
        :param port: Port of the service
        :param timeout: HTTP request timeout in seconds (default: 60.0)
        """
        self.base_url = f"{url.rstrip('/')}: {port}"
        self.base_url = f"{url.rstrip('/')}: {port}".replace(': ', ':')
        self.session: Optional[aiohttp.ClientSession] = None
        self.timeout = timeout

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def get_openapi_schema(self, timeout: Optional[float] = None) -> Any:
        url = f"{self.base_url}/openapi.json"
        req_timeout = aiohttp.ClientTimeout(total=timeout if timeout is not None else self.timeout)
        async with self.session.get(url, timeout=req_timeout) as resp:
            resp.raise_for_status()
            return await resp.json()

    def parse_chunk(self, chunk) -> 'SemanticChunk':
        from chunk_metadata_adapter import SemanticChunk
        if isinstance(chunk, SemanticChunk):
            return chunk
        obj, err = SemanticChunk.validate_and_fill({k: v for k, v in chunk.items() if k in SemanticChunk.model_fields})
        if err:
            error_fields = err.get('fields')
            if error_fields:
                raise ValueError(f"Chunk does not validate against chunk_metadata_adapter.SemanticChunk: {err['error']}\nFields: {error_fields}\nChunk: {chunk}")
            else:
                raise ValueError(f"Chunk does not validate against chunk_metadata_adapter.SemanticChunk: {err}\nChunk: {chunk}")
        return obj

    async def chunk_text(self, text: str, timeout: Optional[float] = None, **params) -> List['SemanticChunk']:
        url = f"{self.base_url}/cmd"
        payload = {
            "jsonrpc": "2.0",
            "method": "chunk",
            "params": {"text": text, **params},
            "id": 1
        }
        req_timeout = aiohttp.ClientTimeout(total=timeout if timeout is not None else self.timeout)
        async with self.session.post(url, json=payload, timeout=req_timeout) as resp:
            resp.raise_for_status()
            data = await resp.json()
            chunks = data.get("result", {}).get("chunks", [])
            parsed_chunks = []
            for chunk in chunks:
                if isinstance(chunk, dict) and "error" in chunk:
                    err = chunk["error"]
                    raise SVOServerError(
                        code=err.get("code", "unknown"),
                        message=err.get("message", str(err)),
                        chunk_error=err
                    )
                parsed_chunks.append(self.parse_chunk(chunk))
            return parsed_chunks

    async def get_help(self, cmdname: Optional[str] = None, timeout: Optional[float] = None) -> Any:
        url = f"{self.base_url}/cmd"
        payload = {
            "jsonrpc": "2.0",
            "method": "help",
            "id": 1
        }
        if cmdname:
            payload["params"] = {"cmdname": cmdname}
        req_timeout = aiohttp.ClientTimeout(total=timeout if timeout is not None else self.timeout)
        async with self.session.post(url, json=payload, timeout=req_timeout) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def health(self, timeout: Optional[float] = None) -> Any:
        url = f"{self.base_url}/cmd"
        payload = {
            "jsonrpc": "2.0",
            "method": "health",
            "id": 1
        }
        req_timeout = aiohttp.ClientTimeout(total=timeout if timeout is not None else self.timeout)
        async with self.session.post(url, json=payload, timeout=req_timeout) as resp:
            resp.raise_for_status()
            return await resp.json()

    def reconstruct_text(self, chunks: List['SemanticChunk']) -> str:
        """
        Reconstruct the original text from a list of SemanticChunk objects.
        Склеивает текст из чанков в исходном порядке.
        """
        sorted_chunks = sorted(
            chunks,
            key=lambda c: c.ordinal if getattr(c, 'ordinal', None) is not None else chunks.index(c)
        )
        return ''.join(chunk.text for chunk in sorted_chunks if getattr(chunk, 'text', None)) 