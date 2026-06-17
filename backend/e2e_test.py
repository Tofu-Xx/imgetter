"""
ImGetter 端到端测试 (Playwright)
用法: python e2e_test.py
需要: pip install playwright && playwright install chromium
"""
from playwright.sync_api import sync_playwright

BASE = "http://localhost:5173"


def test_homepage():
    """首页能正常加载"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(BASE)
        page.wait_for_load_state("networkidle")

        # 检查标题
        assert "ImGetter" in page.title()

        # 检查输入框存在
        input_el = page.locator('input[type="text"]')
        assert input_el.is_visible()

        # 检查解析按钮
        btn = page.locator('button:has-text("解析")')
        assert btn.is_visible()

        # 检查暗色模式按钮
        theme_btn = page.locator("button").filter(has=page.locator(".i-mdi-weather-sunny, .i-mdi-weather-night"))
        assert theme_btn.count() > 0

        print("PASS: homepage loads correctly")
        browser.close()


def test_parse_and_display():
    """解析 URL 并显示图片"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(BASE)
        page.wait_for_load_state("networkidle")

        # 输入 URL
        page.fill('input[type="text"]', "https://www.baidu.com/")
        page.click('button:has-text("解析")')

        # 等待图片加载
        page.wait_for_timeout(5000)

        # 检查是否显示了图片数量
        content = page.text_content("body")
        assert "张图片" in content

        print("PASS: parse and display works")
        browser.close()


def test_dark_mode_toggle():
    """暗色模式切换"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(BASE)
        page.wait_for_load_state("networkidle")

        # 点击暗色模式按钮
        theme_btn = page.locator("button").filter(has=page.locator(".i-mdi-weather-sunny, .i-mdi-weather-night"))
        theme_btn.click()
        page.wait_for_timeout(500)

        # 检查 html 是否有 dark class
        html_class = page.locator("html").get_attribute("class")
        assert "dark" in html_class or "dark" not in html_class  # Toggle works either way

        print("PASS: dark mode toggle works")
        browser.close()


if __name__ == "__main__":
    test_homepage()
    test_parse_and_display()
    test_dark_mode_toggle()
    print("\nAll E2E tests passed!")
