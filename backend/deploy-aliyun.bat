@echo off
REM 阿里云函数计算部署脚本
REM 用法: deploy-aliyun.bat

echo ========================================
echo ImGetter 后端部署到阿里云函数计算
echo ========================================
echo.

REM 1. 检查 Serverless Devs
echo [1/5] 检查 s 命令...
where s >nul 2>nul
if %errorlevel% neq 0 (
    echo 安装 Serverless Devs...
    npm install -g @serverless-devs/s
)

REM 2. 配置阿里云凭证
echo [2/5] 配置阿里云访问凭证...
echo 请确保已运行: s config add --access aliyunfs
echo.

REM 3. 安装依赖
echo [3/5] 安装 Python 依赖...
pip install litestar httpx selectolax pydantic -t ./package --quiet

REM 4. 打包
echo [4/5] 打包部署文件...
cd package
tar -czf ../deploy.zip .
cd ..
tar -rf deploy.zip app/
tar -rf deploy.zip s.yaml
tar -rf deploy.zip requirements.txt

REM 5. 部署
echo [5/5] 部署到阿里云...
s deploy

echo.
echo 部署完成！
echo 函数访问地址将显示在上面的输出中
pause
