"""
ImGetter 全链路诊断脚本
用法: python diagnose.py
"""
import httpx
import sys

BASE = "http://localhost:5173"
API = "http://localhost:8002"
OK = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"


def test(name: str, fn):
    try:
        fn()
        print(f"  {OK} {name}")
        return True
    except Exception as e:
        print(f"  {FAIL} {name}: {e}")
        return False


def main():
    print("\n=== ImGetter 诊断 ===\n")
    passed = 0
    total = 0

    # 1. 后端直接测试
    print("[后端直连]")
    with httpx.Client(trust_env=False, timeout=10) as c:
        def t_parse():
            r = c.post(f"{API}/api/parse", json={"url": "https://www.baidu.com/"})
            assert r.status_code in (200, 201), f"status={r.status_code}"
            data = r.json()
            assert data["total_count"] > 0, "no images found"

        total += 1
        if test("POST /api/parse (baidu)", t_parse):
            passed += 1

        def t_proxy():
            img_url = "https://www.baidu.com/img/bdlogo.png"
            r = c.get(f"{API}/api/proxy", params={"url": img_url})
            assert r.status_code == 200, f"status={r.status_code}"
            assert len(r.content) > 100, "image too small"

        total += 1
        if test("GET /api/proxy (baidu logo)", t_proxy):
            passed += 1

        def t_download_zip():
            r = c.post(
                f"{API}/api/download-zip",
                json={"urls": ["https://www.baidu.com/img/bdlogo.png"]},
            )
            assert r.status_code == 200, f"status={r.status_code}"
            assert r.headers.get("content-type", "").startswith(
                "application/zip"
            ), f"not zip: {r.headers.get('content-type')}"
            assert len(r.content) > 100, "zip too small"

        total += 1
        if test("POST /api/download-zip", t_download_zip):
            passed += 1

    # 2. 前端代理测试
    print("\n[前端代理]")
    with httpx.Client(trust_env=False, timeout=10) as c:
        def t_front_parse():
            r = c.post(f"{BASE}/api/parse", json={"url": "https://www.baidu.com/"})
            assert r.status_code in (200, 201), f"status={r.status_code}"

        total += 1
        if test("前端 /api/parse 代理", t_front_parse):
            passed += 1

        def t_front_proxy():
            r = c.get(f"{BASE}/api/proxy", params={"url": "https://www.baidu.com/img/bdlogo.png"})
            assert r.status_code == 200, f"status={r.status_code}"

        total += 1
        if test("前端 /api/proxy 代理", t_front_proxy):
            passed += 1

    # 3. HTML 渲染测试
    print("\n[前端页面]")
    with httpx.Client(trust_env=False, timeout=10) as c:
        def t_html():
            r = c.get(BASE)
            assert r.status_code == 200
            assert "ImGetter" in r.text

        total += 1
        if test("首页可访问", t_html):
            passed += 1

    print(f"\n=== 结果: {passed}/{total} 通过 ===\n")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
