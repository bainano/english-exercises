#!/bin/bash

# 设置UTF-8编码
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 切换到脚本目录
cd "$SCRIPT_DIR"

# 检查Python3是否可用
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3或Python3未正确安装"
    echo "正在打开Python安装指南..."
    sleep 2
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if [ -f "$SCRIPT_DIR/python_install_guide.html" ]; then
            open "$SCRIPT_DIR/python_install_guide.html"
        else
            echo "未找到Python安装指南文件"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if [ -f "$SCRIPT_DIR/python_install_guide.html" ]; then
            xdg-open "$SCRIPT_DIR/python_install_guide.html"
        else
            echo "未找到Python安装指南文件"
        fi
    fi
    
    echo
    echo "请安装Python3后重新运行此脚本"
    exit 1
fi

# 显示启动信息
echo "正在启动HTTP服务器..."
echo "服务器根目录: $SCRIPT_DIR"
echo "请在浏览器中访问: http://localhost:8000"
echo "按Ctrl+C可以停止服务器"
echo

# 运行Python脚本启动服务器
python3 "$SCRIPT_DIR/start_server.py"

# 显示停止信息
echo "服务器已停止"


# 启动Python服务器
python3 start_server.py