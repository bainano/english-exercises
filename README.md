# 英语练习HTTP网页

## 应用简介

这是一个跨平台的英语练习HTTP服务器应用，旨在提供一个简单易用的英语学习环境。通过启动本地HTTP服务器，用户可以在浏览器中访问英语练习资源，进行英语学习和测试

![网页截图]([/assets/img/philly-magic-garden.jpg](https://github.com/bainano/english-exercises/blob/main/%E6%88%AA%E5%9B%BE/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_26-11-2025_213251_localhost.jpeg))

## 功能特点

- **跨平台支持**：兼容Windows、macOS和Linux系统
- **简单易用**：一键启动服务器，自动打开浏览器
- **中文友好**：完全支持中文编码，避免乱码问题
- **快捷方式创建**：支持在桌面创建快捷方式，方便下次使用
- **端口自定义**：可以根据需要指定服务器端口
- **自动浏览器打开**：启动服务器后自动打开浏览器访问
- **完整的资源管理**：包含HTML页面、图片、JavaScript和测试题库

## 系统要求

- Python 3.0或更高版本
- 现代Web浏览器（如Chrome、Firefox、Edge等）
- 支持的操作系统：
  - Windows 7及以上版本
  - macOS 10.10及以上版本
  - Linux（支持主流发行版）

## 安装说明

### 1. 安装Python

如果您的电脑上还没有安装Python，请先安装Python 3.0或更高版本：

- **Windows**：下载并安装[Python官方安装包](https://www.python.org/downloads/windows/)
- **macOS**：通过App Store或[Python官方网站](https://www.python.org/downloads/macos/)安装
- **Linux**：使用系统包管理器安装，例如：`sudo apt-get install python3`（Ubuntu/Debian）

### 2. 获取应用文件

将应用文件下载并解压到任意位置，确保包含以下文件：

```
english exercises/
├── index.html          # 主页面
├── questions.html      # 问题页面
├── start_server.py     # 主启动脚本
├── start_server.bat    # Windows批处理文件
├── start_server.sh     # macOS/Linux启动脚本
├── test_bank.json      # 测试题库
├── logo.ico            # 应用图标
├── favicon.png         # 网站图标
└── 其他资源文件...
```

## 使用方法

### Windows系统

#### 方法1：直接运行Python脚本

1. 双击打开 `start_server.py` 文件
2. 或在命令行中执行：
   ```
   python start_server.py
   ```

#### 方法2：使用批处理文件

1. 双击打开 `start_server.bat` 文件

### macOS/Linux系统

#### 方法1：直接运行Python脚本

1. 在终端中执行：
   ```
   python3 start_server.py
   ```

#### 方法2：使用Shell脚本

1. 赋予脚本执行权限：
   ```
   chmod +x start_server.sh
   ```
2. 运行脚本：
   ```
   ./start_server.sh
   ```

### 命令行选项

```
python start_server.py --help

用法：
  -p, --port PORT       服务器端口号（默认：8000）
  --create-shortcut     创建桌面快捷方式
```

## 创建桌面快捷方式

首次运行程序时，系统会询问是否创建桌面快捷方式：

```
==================================================
English Exercises Server 快捷方式设置
==================================================

是否要在桌面上创建HTTP服务器的快捷方式？

1. 是，创建快捷方式
2. 否，直接启动服务器
3. 否，以后不再询问

请选择操作 (1/2/3): 
```

- 选择 **1**：在桌面上创建快捷方式
- 选择 **2**：直接启动服务器，不创建快捷方式
- 选择 **3**：不再询问，直接启动服务器

您也可以使用命令行参数直接创建快捷方式：
```
python start_server.py --create-shortcut
```

## 项目结构

```
english exercises/
├── index.html              # 主页面
├── questions.html          # 英语问题页面
├── test_bank.json          # 测试题库数据
├── set_storage.js          # 本地存储管理脚本
├── start_server.py         # 主启动脚本
├── start_server.bat        # Windows批处理启动文件
├── start_server.sh         # macOS/Linux Shell启动脚本
├── logo.ico                # Windows应用图标
├── favicon.png             # 网站图标
├── image.png               # 示例图片
├── logs/                   # 日志文件夹
│   └── server.log          # 服务器日志
└── .shortcut_config.json   # 快捷方式配置文件
```

## 资源文件说明

- **index.html**：应用的主页面，提供应用介绍和导航
- **questions.html**：英语练习页面，包含问题展示和答题功能
- **test_bank.json**：存储英语测试题库的JSON文件
- **set_storage.js**：处理浏览器本地存储的JavaScript文件
- **logo.ico**：Windows系统下的应用图标
- **favicon.png**：浏览器标签页显示的网站图标

## 配置选项

### 自定义端口

默认情况下，服务器使用8000端口。您可以使用`--port`参数指定其他端口：

```
python start_server.py --port 8080
```

### 配置文件

- **.shortcut_config.json**：存储用户关于快捷方式的选择配置

## 故障排除

### 常见问题

1. **服务器启动失败**
   - 检查端口是否被占用，尝试使用其他端口
   - 确保Python已正确安装
   - 查看命令行输出的错误信息

2. **浏览器无法打开**
   - 手动在浏览器中访问：`http://localhost:8000`
   - 检查默认浏览器设置

3. **中文显示乱码**
   - 确保使用支持UTF-8的现代浏览器
   - Windows系统下检查批处理文件是否正常设置了UTF-8编码

4. **快捷方式创建失败**
   - 检查是否有足够的权限在桌面创建文件
   - 手动创建快捷方式指向启动脚本

### 日志查看

服务器日志保存在`logs/server.log`文件中，可以查看详细的运行信息和错误记录。

## 安全说明

- 本应用仅在本地网络启动HTTP服务器，不对外网开放
- 请确保下载的应用文件来自可信来源
- 定期检查并更新Python版本以获取安全更新

## 更新日志

### v1.0.0
- 初始版本发布
- 支持Windows、macOS和Linux系统
- 实现HTTP服务器功能
- 支持快捷方式创建
- 提供英语练习页面

## 开发说明

如果您想修改或扩展此应用：

1. **服务器代码**：主要逻辑在`start_server.py`文件中
2. **网页内容**：修改`index.html`和`questions.html`文件
3. **测试题库**：编辑`test_bank.json`文件添加新题目
4. **样式和交互**：修改相应的HTML、CSS和JavaScript文件

## 许可证

[MIT License](LICENSE)

---
