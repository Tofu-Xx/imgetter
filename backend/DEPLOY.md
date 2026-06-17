# 阿里云函数计算部署指南

## 前置条件

1. **阿里云账号**：https://www.aliyun.com/
2. **实名认证**：必须完成（身份证）
3. **开通函数计算**：https://fcnext.console.aliyun.com/

## 部署步骤

### 1. 安装 Serverless Devs

```bash
npm install -g @serverless-devs/s
```

### 2. 配置阿里云访问密钥

登录阿里云控制台 → AccessKey 管理 → 创建 AccessKey

```bash
s config add --access aliyunfs
# 按提示输入 AccessKey ID 和 Secret
```

### 3. 安装依赖并部署

```bash
cd E:/create/app/imgetter/backend

# 安装依赖到本地目录
pip install litestar httpx selectolax pydantic -t ./package

# 部署
s deploy
```

### 4. 获取访问地址

部署成功后，控制台会显示函数访问地址，格式类似：
```
https://cn-hangzhou.fcapp.cn/service/imgetter-api/imgetter-api
```

### 5. 配置前端

修改 `frontend/src/lib/api.ts`，将 `BASE` 改为函数计算地址：

```typescript
const BASE = "https://cn-hangzhou.fcapp.cn/service/imgetter-api/imgetter-api";
```

重新构建并部署前端：
```bash
cd frontend
pnpm build
wrangler pages deploy dist --project-name=imgetter
```

## 费用说明

阿里云函数计算免费额度（2024年）：
- 每月 100 万次调用
- 每月 400,000 GB·秒 执行时间
- 个人项目基本够用

## 常见问题

**Q: 部署报错 "AccessDenied"**
A: 检查 AccessKey 权限，确保有函数计算的管理权限

**Q: 函数调用超时**
A: 检查网络连接，可能需要配置 VPC 或公网访问

**Q: CORS 错误**
A: 后端已配置 CORS，确保 `Access-Control-Allow-Origin` 头正确返回
