import httpx

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


async def proxy_image(url: str) -> tuple[bytes, str]:
    async with httpx.AsyncClient(headers=HEADERS, timeout=15, follow_redirects=True, trust_env=False) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        content_type = resp.headers.get("content-type", "image/jpeg")
        return resp.content, content_type
