from urllib.parse import urljoin, urlparse

import httpx
from selectolax.parser import HTMLParser

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

VALID_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp", "bmp", "svg", "avif"}


def _resolve_url(base: str, src: str) -> str | None:
    if not src or src.startswith("data:"):
        return None
    abs_url = urljoin(base, src.split(",")[0].strip().split(" ")[0])
    return abs_url


def _extract_ext(url_str: str) -> str | None:
    path = urlparse(url_str).path.lower()
    if "." in path:
        ext = path.rsplit(".", 1)[-1].split("?")[0]
        if ext in VALID_EXTENSIONS:
            return ext
    return None


async def parse_page(url: str, min_width: int = 0, min_height: int = 0) -> dict:
    async with httpx.AsyncClient(
        headers=HEADERS, timeout=20, follow_redirects=True, trust_env=False
    ) as client:
        resp = await client.get(url)
        resp.raise_for_status()

    tree = HTMLParser(resp.text)
    title_node = tree.css_first("title")
    title = title_node.text() if title_node else ""

    images = []
    seen = set()

    for img in tree.css("img"):
        raw_src = (
            img.attributes.get("src")
            or img.attributes.get("data-src")
            or img.attributes.get("data-lazy-src")
            or ""
        )

        abs_url = _resolve_url(url, raw_src)
        if not abs_url or abs_url in seen:
            continue

        ext = _extract_ext(abs_url)
        if not ext:
            continue

        seen.add(abs_url)

        alt = img.attributes.get("alt", "") or ""
        width = img.attributes.get("width")
        height = img.attributes.get("height")

        try:
            width = int(width) if width and width.isdigit() else None
        except (ValueError, TypeError):
            width = None
        try:
            height = int(height) if height and height.isdigit() else None
        except (ValueError, TypeError):
            height = None

        if min_width and width and width < min_width:
            continue
        if min_height and height and height < min_height:
            continue

        images.append(
            {
                "src": abs_url,
                "alt": alt,
                "width": width,
                "height": height,
                "format": ext,
                "size_bytes": None,
                "thumbnail_url": f"/api/proxy?url={abs_url}",
            }
        )

    images.sort(key=lambda x: (x["width"] or 0) * (x["height"] or 0), reverse=True)

    return {
        "page_url": url,
        "page_title": title,
        "images": images,
        "total_count": len(images),
    }
