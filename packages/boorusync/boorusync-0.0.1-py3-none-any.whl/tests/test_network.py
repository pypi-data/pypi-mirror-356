import pytest
from aiohttp import ClientSession
from pathlib import Path
from boorusync.core.network import HttpClient, Response
from boorusync.core.config import Config

@pytest.mark.asyncio
async def test_http_client_get():
    config = Config()
    client = HttpClient(config=config)
    async with client:
        response = await client.get("https://httpbin.org/get")
        assert response.status == 200
        assert "url" in await response.json()

@pytest.mark.asyncio
async def test_http_client_post():
    config = Config()
    client = HttpClient(config=config)
    async with client:
        response = await client.post("https://httpbin.org/post", data={"key": "value"})
        assert response.status == 200
        json_data = await response.json()
        assert json_data["json"]["key"] == "value"

@pytest.mark.asyncio
async def test_http_client_download_file(tmp_path):
    config = Config()
    client = HttpClient(config=config)
    async with client:
        file_path = await client.download_file(
            url="https://httpbin.org/image/png",
            folder_path=str(tmp_path),
            filename="test_image.png"
        )
        assert file_path.exists()
        assert file_path.name == "test_image.png"

@pytest.mark.asyncio
async def test_http_client_bulk_request():
    config = Config()
    client = HttpClient(config=config)
    urls = ["https://httpbin.org/get", "https://httpbin.org/status/200"]
    async with client:
        response = await client.bulk_get(urls)
        assert response.status == 200
