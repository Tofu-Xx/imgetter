import type { ImageInfo } from "../types";
import { parseUrl as apiParseUrl, downloadZip, getProxyUrl } from "../api";

class CollectorStore {
  url = $state("");
  isLoading = $state(false);
  loadingMessage = $state("");
  images = $state<ImageInfo[]>([]);
  pageTitle = $state("");
  pageUrl = $state("");
  error = $state("");
  selectedImages = $state<string[]>([]);
  minWidth = $state(0);
  minHeight = $state(0);

  selectedCount = $derived(this.selectedImages.length);

  filteredImages = $derived.by(() => {
    return this.images.filter((img) => {
      if (this.minWidth && img.width && img.width < this.minWidth) return false;
      if (this.minHeight && img.height && img.height < this.minHeight) return false;
      return true;
    });
  });

  async parse(inputUrl: string) {
    this.isLoading = true;
    this.loadingMessage = "正在解析页面...";
    this.error = "";
    this.images = [];
    this.selectedImages = [];

    try {
      const res = await apiParseUrl({
        url: inputUrl,
        min_width: this.minWidth,
        min_height: this.minHeight,
      });
      this.images = res.images.map((img) => ({
        ...img,
        thumbnail_url: getProxyUrl(img.src),
      }));
      this.pageTitle = res.page_title;
      this.pageUrl = res.page_url;
      this.loadingMessage = "";
    } catch (e) {
      this.error = e instanceof Error ? e.message : "解析失败";
    } finally {
      this.isLoading = false;
    }
  }

  toggleSelection(src: string) {
    if (this.selectedImages.includes(src)) {
      this.selectedImages = this.selectedImages.filter((s) => s !== src);
    } else {
      this.selectedImages = [...this.selectedImages, src];
    }
  }

  selectAll() {
    this.selectedImages = this.filteredImages.map((img) => img.src);
  }

  deselectAll() {
    this.selectedImages = [];
  }

  async downloadSelected() {
    if (this.selectedImages.length === 0) return;
    await downloadZip(this.selectedImages);
  }
}

export const store = new CollectorStore();
