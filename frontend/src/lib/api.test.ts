import { describe, it, expect, vi, beforeEach } from "vitest";
import { parseUrl, downloadZip, getProxyUrl } from "./api";
import type { ParseResponse } from "./types";

describe("api", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  describe("getProxyUrl", () => {
    it("应该正确编码 URL 参数", () => {
      const result = getProxyUrl("https://example.com/image.jpg");
      expect(result).toBe(
        "/api/proxy?url=https%3A%2F%2Fexample.com%2Fimage.jpg",
      );
    });

    it("应该处理特殊字符", () => {
      const result = getProxyUrl(
        "https://example.com/path?q=1&name=测试",
      );
      expect(result).toContain("/api/proxy?url=");
      expect(result).toContain("q%3D1");
    });
  });

  describe("parseUrl", () => {
    it("应该发送正确的请求并返回结果", async () => {
      const mockResponse: ParseResponse = {
        page_url: "https://example.com",
        page_title: "Test Page",
        images: [
          {
            src: "https://example.com/img.jpg",
            alt: "test",
            width: 800,
            height: 600,
            format: "jpg",
            size_bytes: 102400,
            thumbnail_url: "/api/proxy?url=encoded",
          },
        ],
        total_count: 1,
      };

      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response(JSON.stringify(mockResponse), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      );

      const result = await parseUrl({ url: "https://example.com" });

      expect(fetch).toHaveBeenCalledWith("/api/parse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: "https://example.com" }),
      });
      expect(result.total_count).toBe(1);
      expect(result.images[0].src).toBe("https://example.com/img.jpg");
    });

    it("应该在请求失败时抛出错误", async () => {
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response(null, {
          status: 500,
          statusText: "Internal Server Error",
        }),
      );

      await expect(parseUrl({ url: "https://example.com" })).rejects.toThrow(
        "解析失败",
      );
    });
  });

  describe("downloadZip", () => {
    it("应该发送正确的下载请求并触发浏览器下载", async () => {
      const mockArrayBuffer = new ArrayBuffer(8);
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response(mockArrayBuffer, { status: 200 }),
      );

      const clickSpy = vi.fn();
      const mockElement = { href: "", download: "", click: clickSpy };
      vi.spyOn(document, "createElement").mockReturnValue(
        mockElement as unknown as HTMLAnchorElement,
      );
      vi.spyOn(URL, "createObjectURL").mockReturnValue(
        "blob:http://localhost/test",
      );
      vi.spyOn(URL, "revokeObjectURL").mockImplementation(() => {});

      await downloadZip([
        "https://example.com/img1.jpg",
        "https://example.com/img2.jpg",
      ]);

      expect(fetch).toHaveBeenCalledWith("/api/download-zip", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          urls: [
            "https://example.com/img1.jpg",
            "https://example.com/img2.jpg",
          ],
        }),
      });
      expect(clickSpy).toHaveBeenCalled();
    });
  });
});
