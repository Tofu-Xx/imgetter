import type { ParseRequest, ParseResponse, DownloadResponse } from "./types";

const BASE = "/api";

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
  return `${BASE}/proxy?url=${encodeURIComponent(src)}`;
}
