# ImGetter

> 网页图片批量采集与分类系统 | Web Image Batch Collector & Organizer

[![Deploy to Cloudflare Pages](https://deploy.workers.cloudflare.com/button)](https://imgetter.pages.dev)

**English** | [中文](#中文)

## Overview

ImGetter is a full-stack web application for scraping, previewing, and downloading images from any given URL. Users can filter discovered images by dimensions, select specific images, and download them individually or as a ZIP archive.

### Key Features

- **URL Parsing** — Extract all `<img>` tags from any webpage
- **Image Preview** — Grid view with lazy loading and thumbnails
- **Smart Filtering** — Filter by image dimensions (min width/height)
- **Batch Download** — Select multiple images and download as ZIP
- **Image Proxy** — Server-side proxy to bypass CORS and hotlink protection
- **Dark Mode** — Toggle between light and dark themes
- **Auto URL Fix** — Automatically adds `https://` if missing

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Svelte 5, UnoCSS (Wind4 + Icons), Vite |
| Backend | Python 3.10+, Litestar, selectolax, httpx |
| Testing | Vitest, oxlint, diagnose.py |
| Deployment | Cloudflare Pages, GitHub Actions |

## Project Structure

```
imgetter/
├── frontend/                  # Svelte 5 SPA
│   ├── src/
│   │   ├── App.svelte         # Root component with dark mode
│   │   └── lib/
│   │       ├── api.ts         # HTTP client
│   │       ├── types.ts       # TypeScript interfaces
│   │       ├── stores/        # Svelte 5 runes store
│   │       └── components/    # UI components
│   ├── uno.config.ts          # UnoCSS configuration
│   └── vite.config.ts         # Vite + API proxy
├── backend/                   # Python Litestar API
│   ├── app/
│   │   ├── main.py            # Litestar app entry
│   │   ├── routers/images.py  # API endpoints
│   │   ├── services/          # parser, proxy, downloader
│   │   └── models/schemas.py  # Pydantic models
│   ├── diagnose.py            # Full-stack diagnostics
│   └── requirements.txt
└── .github/workflows/         # CI/CD
```

## Getting Started

### Prerequisites

- Node.js 22+ (via fnm/nvm)
- Python 3.10+
- pnpm

### Installation

```bash
# Clone the repo
git clone https://github.com/Tofu-Xx/imgetter.git
cd imgetter

# Frontend
cd frontend
pnpm install

# Backend
cd ../backend
pip install -r requirements.txt
```

### Running Locally

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002

# Terminal 2: Frontend
cd frontend
pnpm dev
```

Open http://localhost:5173

### Diagnostics

```bash
# Run full-stack diagnostics
cd backend
python diagnose.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/parse` | Parse URL and extract images |
| GET | `/api/proxy` | Proxy image requests (bypass CORS) |
| POST | `/api/download-zip` | Download images as ZIP archive |
| POST | `/api/download` | Download images to server |

## Testing

```bash
# Frontend unit tests
cd frontend
pnpm vitest run

# Lint
pnpm oxlint src/

# Type check
pnpm svelte-check
```

## Deployment

### Cloudflare Pages (Frontend)

```bash
cd frontend
pnpm build
wrangler pages deploy dist --project-name=imgetter
```

### GitHub Pages (Alternative)

Push to `main` branch — GitHub Actions auto-deploys.

## License

MIT

---

# 中文

## 项目简介

ImGetter 是一个全栈网页图片采集工具，支持从任意 URL 批量提取、预览和下载图片。用户可以按尺寸筛选图片、批量选择并打包下载。

### 功能特性

- **URL 解析** — 自动提取网页中所有 `<img>` 标签的图片链接
- **图片预览** — 网格布局，支持懒加载和缩略图
- **智能筛选** — 按图片尺寸（最小宽度/高度）过滤
- **批量下载** — 选择多张图片，打包为 ZIP 下载
- **图片代理** — 服务端代理，绕过 CORS 和防盗链限制
- **暗色模式** — 支持明暗主题切换
- **自动补全 URL** — 输入 `baidu.com` 自动补全为 `https://baidu.com`

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Svelte 5, UnoCSS (Wind4 + Icons), Vite |
| 后端 | Python 3.10+, Litestar, selectolax, httpx |
| 测试 | Vitest, oxlint, diagnose.py |
| 部署 | Cloudflare Pages, GitHub Actions |

## 项目结构

```
imgetter/
├── frontend/                  # Svelte 5 前端
│   ├── src/
│   │   ├── App.svelte         # 根组件（含暗色模式）
│   │   └── lib/
│   │       ├── api.ts         # HTTP 客户端
│   │       ├── types.ts       # TypeScript 类型定义
│   │       ├── stores/        # Svelte 5 runes 状态管理
│   │       └── components/    # UI 组件
│   ├── uno.config.ts          # UnoCSS 配置
│   └── vite.config.ts         # Vite + API 代理
├── backend/                   # Python Litestar API
│   ├── app/
│   │   ├── main.py            # Litestar 入口
│   │   ├── routers/images.py  # API 路由
│   │   ├── services/          # 解析器、代理、下载器
│   │   └── models/schemas.py  # Pydantic 数据模型
│   ├── diagnose.py            # 全链路诊断脚本
│   └── requirements.txt
└── .github/workflows/         # CI/CD 配置
```

## 快速开始

### 环境要求

- Node.js 22+（通过 fnm/nvm 管理）
- Python 3.10+
- pnpm

### 安装

```bash
# 克隆仓库
git clone https://github.com/Tofu-Xx/imgetter.git
cd imgetter

# 安装前端依赖
cd frontend
pnpm install

# 安装后端依赖
cd ../backend
pip install -r requirements.txt
```

### 本地运行

```bash
# 终端 1：启动后端
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002

# 终端 2：启动前端
cd frontend
pnpm dev
```

打开 http://localhost:5173

### 诊断测试

```bash
cd backend
python diagnose.py
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/parse` | 解析 URL，提取图片列表 |
| GET | `/api/proxy` | 图片代理（绕过 CORS） |
| POST | `/api/download-zip` | 打包下载为 ZIP |
| POST | `/api/download` | 下载图片到服务器 |

## 测试

```bash
# 前端单元测试
cd frontend
pnpm vitest run

# Lint 检查
pnpm oxlint src/

# 类型检查
pnpm svelte-check
```

## 部署

### Cloudflare Pages（前端）

```bash
cd frontend
pnpm build
wrangler pages deploy dist --project-name=imgetter
```

### GitHub Pages（备选）

推送到 `main` 分支，GitHub Actions 自动部署。

## 许可证

MIT
