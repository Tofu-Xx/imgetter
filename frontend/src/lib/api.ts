import type { ParseRequest, ParseResponse, DownloadResponse } from "./types";

const BASE = import.meta.env.DEV
  ? "/api"
  : "https://imgetter-api-uffonnnwfp.cn-hangzhou.fcapp.run/api";

export async function parseUrl(req: ParseRequest): Promise<ParseResponse> {
  const res = await fetch(`${BASE}/parse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error(`解析失败: ${res.statusText}`);
  return res.json();
}

export async function downloadToServer(
  urls: string[],
  folder = "downloads",
): Promise<DownloadResponse> {
  const res = await fetch(`${BASE}/download`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ urls, folder }),
  });
  if (!res.ok) throw new Error(`下载失败: ${res.statusText}`);
  return res.json();
}

export async function downloadZip(urls: string[]): Promise<void> {
  const res = await fetch(`${BASE}/download-zip`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ urls }),
  });
  if (!res.ok) throw new Error(`下载失败: ${res.statusText}`);
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "images.zip";
  a.click();
  URL.revokeObjectURL(url);
}

export function getProxyUrl(src: string): string {
  // 线上环境使用 base64 代理
  if (!import.meta.env.DEV) {
    return `${BASE}/proxy?url=${encodeURIComponent(src)}`;
  }
  // 开发环境直接用 proxy
  return `/api/proxy?url=${encodeURIComponent(src)}`;
}

export async function fetchProxyImage(src: string): Promise<string> {
  if (import.meta.env.DEV) {
    return `/api/proxy?url=${encodeURIComponent(src)}`;
  }
  try {
    const res = await fetch(`${BASE}/proxy?url=${encodeURIComponent(src)}`);
    if (!res.ok) return src;
    const data = await res.json();
    if (data.error) return src;
    return `data:${data.content_type};base64,${data.data}`;
  } catch {
    return src;
  }
}
