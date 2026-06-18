"""
阿里云函数计算入口
"""
import json
import sys
import os
import re
from urllib.parse import urljoin, urlparse

pkg = os.path.join(os.path.dirname(__file__), '..', 'package')
if os.path.exists(pkg):
    sys.path.insert(0, pkg)


def handler(event, context):
    try:
        import httpx

        if isinstance(event, bytes):
            event = json.loads(event.decode("utf-8"))
        elif isinstance(event, str):
            event = json.loads(event)

        path = event.get("rawPath", event.get("path", "/"))
        method = event.get("httpMethod", event.get("requestContext", {}).get("http", {}).get("method", "GET"))
        query = event.get("queryParameters", event.get("queryStringParameters", {})) or {}
        body = event.get("body", "")

        if body and event.get("isBase64Encoded"):
            import base64
            body = base64.b64decode(body).decode("utf-8")

        UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

        # CORS 预检
        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Max-Age": "86400",
                },
                "body": "",
            }

        with httpx.Client(headers={"User-Agent": UA}, timeout=15, follow_redirects=True, trust_env=False) as c:
            if path == "/api/parse" and method == "POST":
                data = json.loads(body) if body else {}
                url = data.get("url", "")
                if not url:
                    return _r(400, {"error": "no url"})

                resp = c.get(url)
                resp.raise_for_status()
                html = resp.text

                title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
                title = title_match.group(1).strip() if title_match else ""

                exts = {"jpg", "jpeg", "png", "gif", "webp", "bmp", "svg", "avif"}
                imgs = []
                seen = set()

                for match in re.finditer(r'<img\s+[^>]*?src=["\']([^"\']+)["\']', html, re.IGNORECASE):
                    src = match.group(1)
                    if src.startswith("data:"):
                        continue
                    abs_url = urljoin(url, src.split(",")[0].strip().split(" ")[0])
                    if abs_url in seen:
                        continue
                    p = urlparse(abs_url).path.lower()
                    ext = p.rsplit(".", 1)[-1].split("?")[0] if "." in p else ""
                    if ext not in exts:
                        continue
                    seen.add(abs_url)

                    alt_match = re.search(r'alt=["\']([^"\']*)["\']', match.group(0), re.IGNORECASE)
                    alt = alt_match.group(1) if alt_match else ""

                    imgs.append({
                        "src": abs_url,
                        "alt": alt,
                        "width": None,
                        "height": None,
                        "format": ext,
                        "size_bytes": None,
                        "thumbnail_url": f"/api/proxy?url={abs_url}",
                    })

                return _r(200, {
                    "page_url": url,
                    "page_title": title,
                    "images": imgs,
                    "total_count": len(imgs),
                })

            elif path == "/api/proxy":
                u = query.get("url", "")
                if not u:
                    return _r(400, {"error": "no url"})
                try:
                    resp = c.get(u, headers={
                        "User-Agent": UA,
                        "Referer": "https://www.google.com",
                    })
                    ct = resp.headers.get("content-type", "image/jpeg")
                    import base64
                    body_b64 = base64.b64encode(resp.content).decode("ascii")
                    return {
                        "statusCode": 200,
                        "headers": {
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*",
                        },
                        "body": json.dumps({"content_type": ct, "data": body_b64}),
                        "isBase64Encoded": False,
                    }
                except Exception as e:
                    return _r(502, {"error": f"proxy failed: {str(e)}"})

            return _r(404, {"error": "not found"})

    except Exception as e:
        import traceback
        return _r(500, {"error": str(e), "tb": traceback.format_exc()[-500:]})


def _r(s, d):
    return {
        "statusCode": s,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(d, ensure_ascii=False),
    }
