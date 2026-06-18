import asyncio
import hashlib
import os
from urllib.parse import urlparse

import httpx

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "downloads")


async def download_images(urls: list[str], folder: str = "downloads") -> list[dict]:
    os.makedirs(os.path.join(DOWNLOAD_DIR, folder), exist_ok=True)
    sem = asyncio.Semaphore(5)

    async def _download(client: httpx.AsyncClient, url: str) -> dict:
        async with sem:
            try:
                resp = await client.get(url, timeout=15)
                resp.raise_for_status()

                path = urlparse(url).path
                filename = os.path.basename(path) or hashlib.md5(url.encode()).hexdigest()
                if "." not in filename:
                    ct = resp.headers.get("content-type", "")
                    ext = ct.split("/")[-1].split(";")[0] if "/" in ct else "jpg"
                    filename = f"{filename}.{ext}"

                filepath = os.path.join(DOWNLOAD_DIR, folder, filename)
                with open(filepath, "wb") as f:
                    f.write(resp.content)

                return {
                    "filename": filename,
                    "url": url,
                    "success": True,
                    "error": None,
                    "size_bytes": len(resp.content),
                }
            except Exception as e:
                return {
                    "filename": "",
                    "url": url,
                    "success": False,
                    "error": str(e),
                    "size_bytes": 0,
                }

    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, trust_env=False) as client:
        tasks = [_download(client, url) for url in urls]
        results = await asyncio.gather(*tasks)

    return list(results)
