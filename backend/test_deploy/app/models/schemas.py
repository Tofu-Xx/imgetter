from pydantic import BaseModel


class ParseRequest(BaseModel):
    url: str
    min_width: int = 0
    min_height: int = 0


class ImageInfo(BaseModel):
    src: str
    alt: str
    width: int | None = None
    height: int | None = None
    format: str | None = None
    size_bytes: int | None = None
    thumbnail_url: str


class ParseResponse(BaseModel):
    page_url: str
    page_title: str
    images: list[ImageInfo]
    total_count: int


class DownloadRequest(BaseModel):
    urls: list[str]
    folder: str = "downloads"


class DownloadResult(BaseModel):
    filename: str
    url: str
    success: bool
    error: str | None = None
    size_bytes: int = 0


class DownloadResponse(BaseModel):
    results: list[DownloadResult]
    total_size: int
    output_dir: str
