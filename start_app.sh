#!/bin/bash

# ====================================================================
# 英语学习应用一键启动脚本 (Linux/Mac 版本)
# 功能：启动Python HTTP服务器并在默认浏览器中打开应用
# 编码：UTF-8
# 版本：1.0
# 使用方法：chmod +x start_app.sh && ./start_app.sh
# ====================================================================

# 设置颜色输出
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
NC="\033[0m" # No Color

# 清除屏幕并设置标题
echo -e "${GREEN}英语学习应用启动器${NC}"
echo "========================================"

# 创建日志目录
mkdir -p logs

# 设置日志文件
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/start_app_${TIMESTAMP}.log"

# 初始化日志
echo "开始记录日志于 ${LOG_FILE}" > "${LOG_FILE}"
echo "启动时间: $(date)" >> "${LOG_FILE}"
echo "========================================================" >> "${LOG_FILE}"

# 检查Python是否安装
echo -e "${YELLOW}检查Python环境...${NC}"
echo "检查Python环境..." >> "${LOG_FILE}"
python3 --version > /dev/null 2>> "${LOG_FILE}"
if [ $? -ne 0 ]; then
    # 尝试使用python命令
    python --version > /dev/null 2>> "${LOG_FILE}"
    if [ $? -ne 0 ]; then
        echo "错误: 未找到Python环境，请先安装Python" >> "${LOG_FILE}"
        echo -e "\n${RED}========================================================${NC}"
        echo -e "${RED}错误: 未找到Python环境！${NC}"
        echo -e "请先安装Python 3.x版本，然后再运行此脚本。"
        echo -e "${RED}========================================================${NC}"
        read -p "按Enter键退出..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# 显示当前目录信息
echo "当前工作目录: $(pwd)" >> "${LOG_FILE}"
echo "目录文件列表:" >> "${LOG_FILE}"
ls -la *.html >> "${LOG_FILE}" 2>&1

# 检查必要文件是否存在
if [ ! -f "index.html" ]; then
    echo "错误: 找不到index.html文件" >> "${LOG_FILE}"
    echo -e "\n${RED}========================================================${NC}"
    echo -e "${RED}错误: 找不到主要应用文件！${NC}"
    echo -e "请确保在正确的应用目录下运行此脚本。"
    echo -e "${RED}========================================================${NC}"
    read -p "按Enter键退出..."
    exit 1
fi

# 检查端口是否被占用
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "警告: 端口8000已被占用" >> "${LOG_FILE}"
    echo -e "${YELLOW}警告: 端口8000已被占用，可能是之前的服务器未完全关闭${NC}"
    read -p "是否继续? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "用户取消启动" >> "${LOG_FILE}"
        exit 0
    fi
fi

# 启动HTTP服务器
echo -e "${YELLOW}正在启动HTTP服务器...${NC}"
echo "正在启动HTTP服务器..." >> "${LOG_FILE}"
${PYTHON_CMD} -m http.server 8000 > logs/server.log 2>&1 &
SERVER_PID=$!

# 等待服务器启动
echo "等待服务器启动..." >> "${LOG_FILE}"
sleep 2

# 检查服务器是否正常启动
if ! ps -p $SERVER_PID > /dev/null; then
    echo "错误: 服务器启动失败" >> "${LOG_FILE}"
    echo -e "${RED}错误: HTTP服务器启动失败！${NC}"
    echo -e "请查看日志文件获取详细信息。"
    read -p "按Enter键退出..."
    exit 1
fi

# 打开默认浏览器访问应用
echo "正在打开默认浏览器..." >> "${LOG_FILE}"

# 根据不同操作系统打开浏览器
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:8000/index.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open > /dev/null; then
        xdg-open http://localhost:8000/index.html
    elif command -v firefox > /dev/null; then
        firefox http://localhost:8000/index.html
    elif command -v google-chrome > /dev/null; then
        google-chrome http://localhost:8000/index.html
    else
        echo "警告: 无法自动打开浏览器，请手动访问 http://localhost:8000/index.html" >> "${LOG_FILE}"
        echo -e "${YELLOW}警告: 无法自动打开浏览器，请手动访问 http://localhost:8000/index.html${NC}"
    fi
fi

# 显示成功信息
echo "服务器已启动，正在打开应用..." >> "${LOG_FILE}"
echo "服务器PID: $SERVER_PID" >> "${LOG_FILE}"
echo "服务器日志位于: logs/server.log" >> "${LOG_FILE}"
echo "启动完成于: $(date)" >> "${LOG_FILE}"

echo -e "\n${GREEN}========================================================${NC}"
echo -e "${GREEN}应用启动成功！${NC}"
echo -e "1. HTTP服务器已在 http://localhost:8000 上运行"
echo -e "2. 浏览器应已自动打开应用"
echo -e "3. 服务器日志保存在 logs/server.log"
echo -e "4. 启动日志保存在 ${LOG_FILE}"
echo -e "\n注意：请不要关闭此窗口，使用以下方式停止服务"
echo -e "${GREEN}========================================================${NC}"

# 等待用户输入以停止服务
echo -e "\n按 Enter 键停止服务并退出..."
read

# 停止HTTP服务器
echo "正在停止HTTP服务器..." >> "${LOG_FILE}"
kill $SERVER_PID 2>/dev/null
sleep 1

# 确保服务器已停止
if ps -p $SERVER_PID > /dev/null; then
    kill -9 $SERVER_PID 2>/dev/null
fi

echo "HTTP服务器已停止" >> "${LOG_FILE}"

# 结束记录日志
echo "脚本结束于: $(date)" >> "${LOG_FILE}"
echo "========================================================" >> "${LOG_FILE}"

echo -e "\n${GREEN}服务已停止，感谢使用！${NC}"

# 等待几秒钟让用户看到消息
sleep 1
exit 0