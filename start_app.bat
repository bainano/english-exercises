@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: ====================================================================
:: 英语学习应用一键启动脚本
:: 功能：启动Python HTTP服务器并在默认浏览器中打开应用
:: 编码：UTF-8
:: 版本：1.0
:: 使用方法：双击运行此脚本
:: ====================================================================

:: 设置颜色和标题
color 0A
title 英语学习应用启动器

:: 创建日志目录
if not exist "logs" mkdir "logs"

:: 设置日志文件
set LOG_FILE=logs\start_app_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%.log

:: 初始化日志
echo 开始记录日志于 %LOG_FILE% > "%LOG_FILE%"
echo 启动时间: %date% %time% >> "%LOG_FILE%"
echo ======================================================== >> "%LOG_FILE%"

:: 检查Python是否安装
echo 检查Python环境... >> "%LOG_FILE%"
python --version > nul 2>> "%LOG_FILE%"
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境，请先安装Python >> "%LOG_FILE%"
    echo.    
    echo ========================================================    
    echo 错误: 未找到Python环境！    
    echo 请先安装Python 3.x版本，然后再运行此脚本。    
    echo ========================================================
    pause
    exit /b 1
)

:: 显示当前目录信息
echo 当前工作目录: %cd% >> "%LOG_FILE%"
dir *.html > "%LOG_FILE%" 2>&1

:: 检查必要文件是否存在
if not exist "index.html" (
    echo 错误: 找不到index.html文件 >> "%LOG_FILE%"
    echo.    
    echo ========================================================    
    echo 错误: 找不到主要应用文件！    
    echo 请确保在正确的应用目录下运行此脚本。    
    echo ========================================================
    pause
    exit /b 1
)

:: 启动HTTP服务器
echo 正在启动HTTP服务器... >> "%LOG_FILE%"
start "Python HTTP Server" cmd /c "python -m http.server 8000 > logs\server.log 2>&1"

:: 等待服务器启动
echo 等待服务器启动... >> "%LOG_FILE%"
ping 127.0.0.1 -n 3 > nul

:: 打开默认浏览器访问应用
echo 正在打开默认浏览器... >> "%LOG_FILE%"
start http://localhost:8000/index.html

:: 显示成功信息
echo 服务器已启动，正在打开应用... >> "%LOG_FILE%"
echo 服务器日志位于: logs\server.log >> "%LOG_FILE%"
echo 启动完成于: %date% %time% >> "%LOG_FILE%"

echo ========================================================
echo 应用启动成功！
echo 1. HTTP服务器已在 http://localhost:8000 上运行
echo 2. 浏览器应已自动打开应用
 echo 3. 服务器日志保存在 logs\server.log
echo 4. 启动日志保存在 %LOG_FILE%
echo.
echo 注意：请不要关闭此窗口，关闭窗口将停止HTTP服务器
echo ========================================================

echo 按任意键退出...
pause > nul

:: 结束记录日志
echo 脚本结束于: %date% %time% >> "%LOG_FILE%"
echo ======================================================== >> "%LOG_FILE%"

:: 停止HTTP服务器
taskkill /FI "WINDOWTITLE eq Python HTTP Server" > nul
echo HTTP服务器已停止 >> "%LOG_FILE%"

:: 等待几秒钟让任务完全终止
ping 127.0.0.1 -n 2 > nul
exit /b 0