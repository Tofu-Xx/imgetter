import asyncio
import io
import zipfile

import httpx
from litestar import Controller, Request, Response, get, post

from ..models.schemas import (
    DownloadRequest,
    DownloadResponse,
    DownloadResult,
    ParseRequest,
    ParseResponse,
)
from ..services.downloader import download_images
from ..services.parser import parse_page
from ..services.proxy import proxy_image

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


class ImagesController(Controller):
    path = "/api"

    @post("/parse")
    async def parse(self, data: ParseRequest, request: Request) -> ParseResponse:
        try:
            result = await parse_page(data.url, data.min_width, data.min_height)
            return ParseResponse(**result)
        except Exception as e:
            from litestar.exceptions import HTTPException

            raise HTTPException(status_code=400, detail=f"解析失败: {str(e)}")

    @get("/proxy")
    async def proxy(self, request: Request) -> Response:
        url = request.query_params.get("url", "")
        if not url:
            return Response(content=b"missing url", status_code=400)

        try:
            content, content_type = await proxy_image(url)
            return Response(
                content=content,
                status_code=200,
                media_type=content_type,
                headers={"Cache-Control": "public, max-age=86400"},
            )
        except Exception as e:
            return Response(
                content=f"proxy error: {str(e)}".encode(),
                status_code=502,
            )

    @post("/download-zip")
    async def download_zip(self, data: DownloadRequest, request: Request) -> Response:
        sem = asyncio.Semaphore(5)

        async def fetch_one(
            client: httpx.AsyncClient, url: str
        ) -> tuple[str, bytes | None]:
            async with sem:
                try:
                    resp = await client.get(url, timeout=15)
                    resp.raise_for_status()
                    from urllib.parse import urlparse

                    path = urlparse(url).path
                    filename = path.split("/")[-1] or "image.jpg"
                    if "." not in filename:
                        filename = f"{filename}.jpg"
                    return filename, resp.content
                except Exception:
                    return "", None

        async with httpx.AsyncClient(
            headers=HEADERS, follow_redirects=True, trust_env=False
        ) as client:
            tasks = [fetch_one(client, url) for url in data.urls]
            results = await asyncio.gather(*tasks)

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            seen = set()
            for filename, content in results:
                if content and filename:
                    if filename in seen:
                        base, ext = filename.rsplit(".", 1)
                        filename = f"{base}_{len(seen)}.{ext}"
                    seen.add(filename)
                    zf.writestr(filename, content)

        return Response(
            content=buf.getvalue(),
            status_code=200,
            media_type="application/zip",
            headers={
                "Content-Disposition": "attachment; filename=images.zip",
            },
        )

    @post("/download")
    async def download(self, data: DownloadRequest) -> DownloadResponse:
        results = await download_images(data.urls, data.folder)
        total_size = sum(r["size_bytes"] for r in results)
        return DownloadResponse(
            results=[DownloadResult(**r) for r in results],
            total_size=total_size,
            output_dir=f"downloads/{data.folder}",
        )
