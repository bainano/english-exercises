#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台HTTP服务器启动脚本
支持Windows、macOS和Linux系统
自动处理中文编码问题
"""

import os
import sys
import platform
import subprocess
import webbrowser
import argparse
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse


class UTF8HTTPRequestHandler(SimpleHTTPRequestHandler):
    """支持UTF-8编码的HTTP请求处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def guess_type(self, path):
        """重写guess_type方法以确保正确的Content-Type"""
        ctype = super().guess_type(path)
        # 对于HTML文件，确保使用UTF-8编码
        if ctype.startswith('text/html'):
            return 'text/html; charset=utf-8'
        elif ctype.startswith('text/css'):
            return 'text/css; charset=utf-8'
        elif ctype.startswith('application/javascript'):
            return 'application/javascript; charset=utf-8'
        elif ctype.startswith('text/plain'):
            return 'text/plain; charset=utf-8'
        return ctype


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 0):
        print("错误: 需要Python 3.0或更高版本")
        return False
    return True


def start_http_server(port=8000):
    """启动HTTP服务器"""
    try:
        # 设置当前工作目录为脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # 启动服务器
        server_address = ('', port)
        httpd = HTTPServer(server_address, UTF8HTTPRequestHandler)
        
        print(f"HTTP服务器已在端口 {port} 上启动")
        print(f"服务器根目录: {script_dir}")
        print(f"请在浏览器中访问: http://localhost:{port}")
        print("按 Ctrl+C 停止服务器")
        
        # 自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{port}')
        except Exception as e:
            print(f"无法自动打开浏览器: {e}")
            print("请手动在浏览器中访问上述地址")
        
        # 启动服务器
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except PermissionError:
        print(f"错误: 端口 {port} 可能已被占用或其他程序正在使用")
        print("请尝试使用其他端口，例如: python start_server.py --port 8001")
    except OSError as e:
        if "Address already in use" in str(e) or "通常每个套接字地址" in str(e):
            print(f"错误: 端口 {port} 已被占用")
            print("请尝试使用其他端口，例如: python start_server.py --port 8001")
        else:
            print(f"启动服务器时出错: {e}")
    except Exception as e:
        print(f"启动服务器时出错: {e}")


class ShortcutManager:
    """跨平台桌面快捷方式管理类"""
    
    def __init__(self, name="English Exercises Server", icon_name="logo.ico"):
        """初始化快捷方式管理器"""
        self.name = name
        self.icon_name = icon_name
        self.script_path = os.path.abspath(__file__)
        self.script_dir = os.path.dirname(self.script_path)
        self.config_file = os.path.join(self.script_dir, ".shortcut_config.json")
        self.system = platform.system()
        self.desktop_path = self._get_desktop_path()
        self.shortcut_path = self._get_shortcut_path()
    
    def _get_desktop_path(self):
        """获取桌面路径，兼容不同操作系统"""
        try:
            if self.system == "Windows":
                return os.path.join(os.path.expanduser('~'), 'Desktop')
            elif self.system == "Darwin":  # macOS
                return os.path.join(os.path.expanduser('~'), 'Desktop')
            elif self.system == "Linux":
                # Linux有多种桌面环境，尝试常见的桌面路径
                possible_paths = [
                    os.path.join(os.path.expanduser('~'), 'Desktop'),
                    os.path.join(os.path.expanduser('~'), '.desktop')
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        return path
                return os.path.join(os.path.expanduser('~'), 'Desktop')  # 默认返回
            else:
                return os.path.join(os.path.expanduser('~'), 'Desktop')
        except Exception as e:
            print(f"获取桌面路径时出错: {e}")
            return os.path.join(os.path.expanduser('~'), 'Desktop')
    
    def _get_shortcut_path(self):
        """获取快捷方式的完整路径"""
        if self.system == "Windows":
            return os.path.join(self.desktop_path, f"{self.name}.lnk")
        elif self.system == "Darwin":  # macOS
            return os.path.join(self.desktop_path, f"{self.name}.app")
        elif self.system == "Linux":
            return os.path.join(self.desktop_path, f"{self.name}.desktop")
        else:
            return os.path.join(self.desktop_path, f"{self.name}.lnk")
    
    def _get_config(self):
        """获取配置信息"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"读取配置文件时出错: {e}")
        return {}
    
    def _save_config(self, config):
        """保存配置信息"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件时出错: {e}")
    
    def exists(self):
        """检测快捷方式是否存在"""
        try:
            return os.path.exists(self.shortcut_path)
        except Exception as e:
            print(f"检测快捷方式时出错: {e}")
            return False
    
    def create(self):
        """创建桌面快捷方式"""
        try:
            if self.system == "Windows":
                return self._create_windows_shortcut()
            elif self.system == "Darwin":  # macOS
                return self._create_macos_shortcut()
            elif self.system == "Linux":
                return self._create_linux_shortcut()
            else:
                print(f"不支持的操作系统: {self.system}")
                return False
        except Exception as e:
            print(f"创建快捷方式时出错: {e}")
            return False
    
    def _create_windows_shortcut(self):
        """在Windows上创建桌面快捷方式"""
        try:
            # 获取图标路径
            icon_path = os.path.join(self.script_dir, self.icon_name)
            if not os.path.exists(icon_path):
                print(f"警告: 未找到图标文件 {icon_path}")
                icon_path = ''
            
            # 创建批处理文件路径
            bat_path = os.path.join(self.script_dir, 'start_server.bat')
            if not os.path.exists(bat_path):
                print(f"错误: 未找到批处理文件 {bat_path}")
                # 尝试创建批处理文件
                create_bat_file()
                if not os.path.exists(bat_path):
                    print("无法创建批处理文件，无法继续创建快捷方式")
                    return False
            
            # 使用更简单可靠的方式创建VBS脚本内容
            # 写入完整的VBS脚本，避免字符串转义问题
            vbs_code = '''
Set oWS = WScript.CreateObject("WScript.Shell")
strDesktop = oWS.SpecialFolders("Desktop")
Set oLink = oWS.CreateShortcut(strDesktop & "\\English Exercises Server.lnk")
oLink.TargetPath = "''' + bat_path + '''"
oLink.WorkingDirectory = "''' + self.script_dir + '''"
oLink.Description = "English Exercises HTTP Server"
'''
            
            # 添加图标信息（如果有）
            if icon_path:
                vbs_code += '''oLink.IconLocation = "''' + icon_path + '''"
'''
            
            # 添加保存命令
            vbs_code += '''oLink.Save
'''
            
            # 写入VBS脚本
            vbs_path = os.path.join(self.script_dir, 'create_shortcut.vbs')
            with open(vbs_path, 'w', encoding='utf-8') as f:
                f.write(vbs_code)
            
            print(f"VBS脚本已创建: {vbs_path}")
            print("VBS脚本内容:")
            print(vbs_code)
            
            # 执行VBS脚本
            print("正在执行VBS脚本创建快捷方式...")
            result = subprocess.run(['cscript.exe', vbs_path, '/nologo'], 
                                  capture_output=True, text=True, encoding='utf-8')
            
            # 显示详细输出
            if result.stdout:
                print(f"VBS脚本输出: {result.stdout}")
            if result.stderr:
                print(f"VBS脚本错误: {result.stderr}")
            print(f"VBS脚本返回代码: {result.returncode}")
            
            # 检查执行结果
            if result.returncode == 0:
                # 删除临时VBS文件
                try:
                    os.remove(vbs_path)
                    print(f"临时VBS文件已删除: {vbs_path}")
                except:
                    print(f"无法删除临时VBS文件: {vbs_path}")
                
                # 验证快捷方式是否真的创建成功
                shortcut_path = os.path.join(self.desktop_path, "English Exercises Server.lnk")
                if os.path.exists(shortcut_path):
                    print(f"桌面快捷方式创建成功: {shortcut_path}")
                    # 更新配置
                    config = self._get_config()
                    config['shortcut_created'] = True
                    self._save_config(config)
                    return True
                else:
                    print(f"错误: 快捷方式文件未在预期位置创建: {shortcut_path}")
                    return False
            else:
                print(f"创建快捷方式失败，VBS脚本返回代码: {result.returncode}")
                print("您可以手动运行以下命令来查看详细错误:")
                print(f"cscript.exe \"{vbs_path}\" /nologo")
                return False
            
        except Exception as e:
            print(f"创建Windows快捷方式时出错: {e}")
            import traceback
            print("详细错误信息:")
            traceback.print_exc()
            return False
    
    def _create_macos_shortcut(self):
        """在macOS上创建桌面快捷方式"""
        try:
            # 在macOS上，.app是一个目录结构，我们创建一个启动脚本
            shortcut_script = os.path.join(self.desktop_path, f"{self.name}.command")
            
            # 创建启动脚本内容
            with open(shortcut_script, 'w', encoding='utf-8') as f:
                f.write(f'''
#!/bin/bash
# {self.name} 启动脚本
cd "{self.script_dir}"
python3 "{self.script_path}"
''')
            
            # 添加执行权限
            os.chmod(shortcut_script, 0o755)
            
            # 更新配置
            config = self._get_config()
            config['shortcut_created'] = True
            self._save_config(config)
            
            print("桌面快捷方式创建成功!")
            return True
            
        except Exception as e:
            print(f"创建macOS快捷方式时出错: {e}")
            return False
    
    def _create_linux_shortcut(self):
        """在Linux上创建桌面快捷方式"""
        try:
            # 获取图标路径
            icon_path = os.path.join(self.script_dir, self.icon_name)
            if not os.path.exists(icon_path):
                icon_path = ''
            
            # 创建.desktop文件内容
            desktop_content = f'''
[Desktop Entry]
Name={self.name}
Comment={self.name} HTTP Server
Exec=python3 "{self.script_path}"
Icon={icon_path}
Terminal=true
Type=Application
Categories=Utility;
'''
            
            # 写入.desktop文件
            with open(self.shortcut_path, 'w', encoding='utf-8') as f:
                f.write(desktop_content)
            
            # 添加执行权限
            os.chmod(self.shortcut_path, 0o755)
            
            # 更新配置
            config = self._get_config()
            config['shortcut_created'] = True
            self._save_config(config)
            
            print("桌面快捷方式创建成功!")
            return True
            
        except Exception as e:
            print(f"创建Linux快捷方式时出错: {e}")
            return False
    
    def ask_to_create(self):
        """询问用户是否创建快捷方式"""
        try:
            # 先检查是否已经存在
            if self.exists():
                print(f"检测到桌面快捷方式已存在，跳过创建步骤...")
                return False
            
            # 获取用户选择配置
            config = self._get_config()
            never_ask = config.get('never_ask', False)
            
            if never_ask:
                return False
            
            # 询问用户
            print("=" * 50)
            print(f"{self.name} 快捷方式设置")
            print("=" * 50)
            print()
            print("是否要在桌面上创建HTTP服务器的快捷方式？")
            print()
            print("1. 是，创建快捷方式")
            print("2. 否，直接启动服务器")
            print("3. 否，以后不再询问")
            print()
            
            # 使用更简单可靠的方式获取用户输入，适用于所有系统
            # 避免使用复杂的choice命令，直接使用input函数
            try:
                # 直接使用input函数获取用户输入
                print("请选择操作 (1/2/3): ")
                # 使用try-except处理可能的输入异常
                try:
                    choice = input().strip()
                    print(f"您选择了: {choice}")
                except (EOFError, KeyboardInterrupt):
                    print("\n输入被中断，默认选择启动服务器")
                    return False
                
                # 验证输入是否有效
                if choice not in ['1', '2', '3']:
                    print("输入无效，默认选择启动服务器")
                    return False
                
                # 处理用户选择
                if choice == '1':
                    return self.create()
                elif choice == '3':
                    # 记录用户选择，以后不再询问
                    config['never_ask'] = True
                    self._save_config(config)
                    print("将不再询问创建快捷方式")
                
            except Exception as e:
                print(f"获取用户输入时出错: {e}")
                print("默认选择启动服务器")
            
            return False
            
        except Exception as e:
            print(f"询问用户时出错: {e}")
            return False


def create_windows_shortcut():
    """兼容旧版本的函数，调用新的ShortcutManager"""
    manager = ShortcutManager()
    return manager.create()


def create_bat_file():
    """创建Windows批处理文件"""
    try:
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        
        bat_content = f'''@echo off
chcp 65001 > nul
cd /d "{script_dir}"
python "{script_path}"
pause
'''
        
        bat_path = os.path.join(script_dir, 'start_server.bat')
        with open(bat_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        
        print(f"批处理文件已创建: {bat_path}")
        return bat_path
        
    except Exception as e:
        print(f"创建批处理文件时出错: {e}")
        return None


def create_shell_script():
    """创建macOS/Linux shell脚本"""
    try:
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        
        shell_content = f'''#!/bin/bash
cd "{script_dir}"
python3 "{script_path}"
'''
        
        shell_path = os.path.join(script_dir, 'start_server.sh')
        with open(shell_path, 'w', encoding='utf-8') as f:
            f.write(shell_content)
        
        # 添加执行权限
        os.chmod(shell_path, 0o755)
        
        print(f"Shell脚本已创建: {shell_path}")
        return shell_path
        
    except Exception as e:
        print(f"创建Shell脚本时出错: {e}")
        return None


def main():
    """主函数"""
    # 检查Python版本
    if not check_python_version():
        # 打开Python安装指南
        script_dir = os.path.dirname(os.path.abspath(__file__))
        guide_path = os.path.join(script_dir, 'python_install_guide.html')
        if os.path.exists(guide_path):
            webbrowser.open(f'file://{guide_path}')
        else:
            print("未找到Python安装指南文件")
        return
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='启动HTTP服务器')
    parser.add_argument('-p', '--port', type=int, default=8000, help='服务器端口号 (默认: 8000)')
    parser.add_argument('--create-shortcut', action='store_true', help='创建桌面快捷方式')
    args = parser.parse_args()
    
    # 初始化快捷方式管理器
    shortcut_manager = ShortcutManager()
    
    # 根据操作系统创建相应的启动脚本
    system = platform.system()
    if system == 'Windows':
        create_bat_file()
        if args.create_shortcut:
            shortcut_manager.create()
        else:
            # 自动检测并询问是否创建快捷方式
            shortcut_manager.ask_to_create()
    elif system in ['Darwin', 'Linux']:  # macOS是Darwin
        create_shell_script()
        if args.create_shortcut:
            shortcut_manager.create()
        else:
            # 自动检测并询问是否创建快捷方式
            shortcut_manager.ask_to_create()
    
    # 启动HTTP服务器
    start_http_server(args.port)


if __name__ == '__main__':
    main()