import { describe, it, expect, vi, beforeEach } from "vitest";

// Mock the api module
vi.mock("$lib/api", () => ({
  parseUrl: vi.fn(),
  downloadZip: vi.fn(),
  getProxyUrl: vi.fn((src: string) => `/api/proxy?url=${encodeURIComponent(src)}`),
}));

import { store } from "./collector.svelte";
import * as api from "$lib/api";

describe("CollectorStore", () => {
  beforeEach(() => {
    store.url = "";
    store.isLoading = false;
    store.loadingMessage = "";
    store.images = [];
    store.pageTitle = "";
    store.pageUrl = "";
    store.error = "";
    store.selectedImages = [];
    store.minWidth = 0;
    store.minHeight = 0;
    vi.clearAllMocks();
  });

  it("初始状态正确", () => {
    expect(store.url).toBe("");
    expect(store.isLoading).toBe(false);
    expect(store.images).toEqual([]);
    expect(store.selectedImages).toEqual([]);
    expect(store.selectedCount).toBe(0);
  });

  it("parse 成功时更新 images", async () => {
    const mockResponse = {
      page_url: "https://example.com",
      page_title: "Example",
      images: [
        {
          src: "https://example.com/1.jpg",
          alt: "img1",
          width: 100,
          height: 100,
          format: "jpg",
          size_bytes: 1000,
          thumbnail_url: "",
        },
        {
          src: "https://example.com/2.png",
          alt: "img2",
          width: 200,
          height: 200,
          format: "png",
          size_bytes: 2000,
          thumbnail_url: "",
        },
      ],
      total_count: 2,
    };
    vi.mocked(api.parseUrl).mockResolvedValue(mockResponse);

    await store.parse("https://example.com");

    expect(store.images).toHaveLength(2);
    expect(store.pageTitle).toBe("Example");
    expect(store.isLoading).toBe(false);
    expect(api.parseUrl).toHaveBeenCalledWith({
      url: "https://example.com",
      min_width: 0,
      min_height: 0,
    });
  });

  it("parse 失败时设置 error", async () => {
    vi.mocked(api.parseUrl).mockRejectedValue(new Error("网络错误"));

    await store.parse("https://bad-url.com");

    expect(store.error).toBe("网络错误");
    expect(store.images).toEqual([]);
    expect(store.isLoading).toBe(false);
  });

  it("toggleSelection 添加和移除", () => {
    store.toggleSelection("a.jpg");
    expect(store.selectedImages).toEqual(["a.jpg"]);
    expect(store.selectedCount).toBe(1);

    store.toggleSelection("b.jpg");
    expect(store.selectedImages).toEqual(["a.jpg", "b.jpg"]);
    expect(store.selectedCount).toBe(2);

    store.toggleSelection("a.jpg");
    expect(store.selectedImages).toEqual(["b.jpg"]);
    expect(store.selectedCount).toBe(1);
  });

  it("selectAll 和 deselectAll", () => {
    store.images = [
      {
        src: "1.jpg",
        alt: "",
        width: null,
        height: null,
        format: null,
        size_bytes: null,
        thumbnail_url: "",
      },
      {
        src: "2.jpg",
        alt: "",
        width: null,
        height: null,
        format: null,
        size_bytes: null,
        thumbnail_url: "",
      },
    ];

    store.selectAll();
    expect(store.selectedImages).toEqual(["1.jpg", "2.jpg"]);

    store.deselectAll();
    expect(store.selectedImages).toEqual([]);
  });
});
