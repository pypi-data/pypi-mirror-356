#!/usr/bin/env python3
"""
构建和上传脚本

使用方法:
    python build_and_upload.py --build        # 仅构建
    python build_and_upload.py --upload       # 构建并上传到 PyPI
    python build_and_upload.py --test-upload  # 构建并上传到 TestPyPI
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, cwd=None):
    """运行命令并打印输出"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, cwd=cwd,
            capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def check_requirements():
    """检查必要的工具是否已安装"""
    requirements = ["build", "twine"]
    missing = []
    
    for req in requirements:
        try:
            subprocess.run([sys.executable, "-m", req, "--help"], 
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            missing.append(req)
    
    if missing:
        print(f"Missing required packages: {', '.join(missing)}")
        print("Please install them with:")
        print(f"pip install {' '.join(missing)}")
        return False
    return True


def clean_build():
    """清理之前的构建文件"""
    print("Cleaning previous build files...")
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    
    for pattern in dirs_to_clean:
        if "*" in pattern:
            # 使用 glob 处理通配符
            import glob
            for path in glob.glob(pattern):
                if os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                    print(f"Removed directory: {path}")
        else:
            if os.path.exists(pattern):
                if os.path.isdir(pattern):
                    import shutil
                    shutil.rmtree(pattern)
                    print(f"Removed directory: {pattern}")
                else:
                    os.remove(pattern)
                    print(f"Removed file: {pattern}")


def build_package():
    """构建包"""
    print("Building package...")
    clean_build()
    
    if not run_command(f"{sys.executable} -m build"):
        print("Build failed!")
        return False
    
    print("Build completed successfully!")
    return True


def upload_to_pypi(test=False):
    """上传到 PyPI 或 TestPyPI"""
    if test:
        print("Uploading to TestPyPI...")
        cmd = f"{sys.executable} -m twine upload --repository testpypi dist/*"
    else:
        print("Uploading to PyPI...")
        cmd = f"{sys.executable} -m twine upload dist/*"
    
    if not run_command(cmd):
        print("Upload failed!")
        return False
    
    print("Upload completed successfully!")
    return True


def validate_package():
    """验证包的基本信息"""
    print("Validating package configuration...")
    
    # 检查 pyproject.toml
    if not os.path.exists("pyproject.toml"):
        print("Error: pyproject.toml not found!")
        return False
    
    # 检查必要文件
    required_files = ["README.md", "LICENSE", "__init__.py"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Warning: {file} not found!")
    
    print("Package validation completed.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Build and upload package to PyPI")
    parser.add_argument("--build", action="store_true", help="Only build the package")
    parser.add_argument("--upload", action="store_true", help="Build and upload to PyPI")
    parser.add_argument("--test-upload", action="store_true", help="Build and upload to TestPyPI")
    
    args = parser.parse_args()
    
    if not any([args.build, args.upload, args.test_upload]):
        parser.print_help()
        return
    
    # 检查依赖
    if not check_requirements():
        return
    
    # 验证包配置
    if not validate_package():
        return
    
    # 构建包
    if not build_package():
        return
    
    # 上传包
    if args.upload:
        upload_to_pypi(test=False)
    elif args.test_upload:
        upload_to_pypi(test=True)
    
    print("All operations completed!")


if __name__ == "__main__":
    main() 