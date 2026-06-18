"""
阿里云函数计算入口 - 极简版
"""
import json
import sys
import os

# 添加依赖路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'package'))
sys.path.insert(0, os.path.dirname(__file__))


async def handler(event, context):
    try:
        import httpx
        from selectolax.parser import HTMLParser
        from urllib.parse import urljoin, urlparse

        method = event.get("httpMethod", "GET")
        path = event.get("path", "/")
        query = event.get("queryStringParameters", {}) or {}
        body = event.get("body", "")

        if body and event.get("isBase64Encoded"):
            import base64
            body = base64.b64decode(body).decode("utf-8")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        async with httpx.AsyncClient(headers=headers, timeout=20, follow_redirects=True, trust_env=False) as client:
            if path == "/api/parse" and method == "POST":
                data = json.loads(body) if body else {}
                url = data.get("url", "")
                if not url:
                    return resp(400, {"error": "missing url"})

                r = await client.get(url)
                r.raise_for_status()
                tree = HTMLParser(r.text)
                title_el = tree.css_first("title")
                page_title = title_el.text() if title_el else ""

                images = []
                seen = set()
                valid_ext = {"jpg", "jpeg", "png", "gif", "webp", "bmp", "svg", "avif"}
                for img in tree.css("img"):
                    src = img.attributes.get("src") or img.attributes.get("data-src") or ""
                    if not src or src.startswith("data:"):
                        continue
                    abs_url = urljoin(url, src.split(",")[0].strip().split(" ")[0])
                    if abs_url in seen:
                        continue
                    p = urlparse(abs_url).path.lower()
                    ext = p.rsplit(".", 1)[-1].split("?")[0] if "." in p else ""
                    if ext not in valid_ext:
                        continue
                    seen.add(abs_url)
                    images.append({
                        "src": abs_url,
                        "alt": img.attributes.get("alt", "") or "",
                        "width": None, "height": None,
                        "format": ext, "size_bytes": None,
                        "thumbnail_url": f"/api/proxy?url={abs_url}",
                    })

                return resp(200, {
                    "page_url": url,
                    "page_title": page_title,
                    "images": images,
                    "total_count": len(images),
                })

            elif path == "/api/proxy":
                img_url = query.get("url", "")
                if not img_url:
                    return resp(400, {"error": "missing url"})
                r = await client.get(img_url)
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": r.headers.get("content-type", "image/jpeg"), "Cache-Control": "public, max-age=86400"},
                    "body": r.content.decode("latin-1"),
                    "isBase64Encoded": False,
                }

            return resp(404, {"error": "not found"})

    except Exception as e:
        import traceback
        return resp(500, {"error": str(e), "trace": traceback.format_exc()})


def resp(status, data):
    return {"statusCode": status, "headers": {"Content-Type": "application/json"}, "body": json.dumps(data, ensure_ascii=False)}
