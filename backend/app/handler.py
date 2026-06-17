"""
阿里云函数计算入口
将 Litestar ASGI 应用转换为 FC 兼容的 handler
"""
import json
import base64
import traceback
from app.main import app


async def handler(event, context):
    """
    阿里云 FC 3.0 HTTP 触发器处理函数
    """
    try:
        http_method = event.get("httpMethod", "GET")
        path = event.get("path", "/")
        headers = event.get("headers", {}) or {}
        query_string = event.get("queryStringParameters", {}) or {}

        body = event.get("body", "")
        if body and event.get("isBase64Encoded"):
            body = base64.b64decode(body).decode("utf-8")

        # 构建 query string
        qs = "&".join(f"{k}={v}" for k, v in query_string.items()).encode()

        # 构建 ASGI scope
        scope = {
            "type": "http",
            "method": http_method,
            "path": path,
            "query_string": qs,
            "headers": [
                (k.lower().encode(), str(v).encode())
                for k, v in headers.items()
            ],
        }

        # 构建 receive
        receive_messages = []
        if body:
            receive_messages.append({
                "type": "http.request",
                "body": body.encode("utf-8"),
                "more_body": False,
            })
        else:
            receive_messages.append({
                "type": "http.request",
                "body": b"",
                "more_body": False,
            })

        message_index = 0

        async def receive():
            nonlocal message_index
            msg = receive_messages[message_index]
            message_index += 1
            return msg

        # 收集响应
        response_body = b""
        response_status = 200
        response_headers = {}

        async def send(message):
            nonlocal response_body, response_status, response_headers
            if message["type"] == "http.response.start":
                response_status = message.get("status", 200)
                raw_headers = message.get("headers", [])
                if isinstance(raw_headers, dict):
                    response_headers = raw_headers
                else:
                    for k, v in raw_headers:
                        if isinstance(k, bytes):
                            k = k.decode()
                        if isinstance(v, bytes):
                            v = v.decode()
                        response_headers[k] = v
            elif message["type"] == "http.response.body":
                response_body += message.get("body", b"")

        await app(scope, receive, send)

        # 处理响应
        resp_headers = {}
        for k, v in response_headers.items():
            resp_headers[str(k)] = str(v)

        return {
            "statusCode": response_status,
            "headers": resp_headers,
            "body": response_body.decode("utf-8", errors="replace"),
            "isBase64Encoded": False,
        }

    except Exception as e:
        tb = traceback.format_exc()
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": str(e),
                "traceback": tb,
            }),
            "isBase64Encoded": False,
        }
