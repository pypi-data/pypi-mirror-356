#!/usr/bin/env python3
"""
版本号管理脚本
用法: python version_bump.py [major|minor|patch]
"""

import re
import sys
import argparse
from pathlib import Path

def get_current_version():
    """获取当前版本号"""
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        raise FileNotFoundError("pyproject.toml 文件不存在")
    
    content = pyproject_file.read_text()
    match = re.search(r'version = "(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        raise ValueError("无法找到版本号")
    
    return tuple(map(int, match.groups()))

def bump_version(version_type):
    """增加版本号"""
    major, minor, patch = get_current_version()
    
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        raise ValueError("无效的版本类型，请使用 major, minor, 或 patch")
    
    return f"{major}.{minor}.{patch}"

def update_version(new_version):
    """更新 pyproject.toml 中的版本号"""
    pyproject_file = Path("pyproject.toml")
    content = pyproject_file.read_text()
    
    new_content = re.sub(
        r'version = "\d+\.\d+\.\d+"',
        f'version = "{new_version}"',
        content
    )
    
    pyproject_file.write_text(new_content)
    print(f"✅ 版本号已更新为: {new_version}")

def main():
    parser = argparse.ArgumentParser(description="版本号管理工具")
    parser.add_argument("type", choices=["major", "minor", "patch"], 
                       help="版本增加类型")
    parser.add_argument("--show", action="store_true", 
                       help="只显示当前版本，不进行更新")
    
    if len(sys.argv) == 1:
        # 没有参数时显示当前版本
        try:
            current = ".".join(map(str, get_current_version()))
            print(f"当前版本: {current}")
        except Exception as e:
            print(f"错误: {e}")
        return
    
    args = parser.parse_args()
    
    if args.show:
        try:
            current = ".".join(map(str, get_current_version()))
            print(f"当前版本: {current}")
        except Exception as e:
            print(f"错误: {e}")
        return
    
    try:
        current = ".".join(map(str, get_current_version()))
        new_version = bump_version(args.type)
        
        print(f"当前版本: {current}")
        print(f"新版本: {new_version}")
        
        confirm = input("确认更新版本号？ (y/N): ")
        if confirm.lower() in ['y', 'yes']:
            update_version(new_version)
        else:
            print("取消更新")
            
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 