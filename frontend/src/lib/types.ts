export interface ImageInfo {
  src: string;
  alt: string;
  width: number | null;
  height: number | null;
  format: string | null;
  size_bytes: number | null;
  thumbnail_url: string;
}

export interface ParseRequest {
  url: string;
  min_width?: number;
  min_height?: number;
}

export interface ParseResponse {
  page_url: string;
  page_title: string;
  images: ImageInfo[];
  total_count: number;
}

export interface DownloadResult {
  filename: string;
  url: string;
  success: boolean;
  error: string | null;
  size_bytes: number;
}

export interface DownloadResponse {
  results: DownloadResult[];
  total_size: number;
  output_dir: string;
}
