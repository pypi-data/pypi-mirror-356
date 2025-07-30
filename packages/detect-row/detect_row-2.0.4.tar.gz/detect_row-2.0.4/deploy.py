#!/usr/bin/env python3
"""
Script tự động deploy DetectRow package lên PyPI
"""

import os
import sys
import subprocess
import argparse
import re
from pathlib import Path

def run_command(cmd, check=True):
    """Chạy command và hiển thị output"""
    print(f"🔧 Chạy: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    if check and result.returncode != 0:
        print(f"❌ Command failed with exit code {result.returncode}")
        sys.exit(1)
    
    return result

def update_version(new_version):
    """Cập nhật version trong tất cả files"""
    print(f"📝 Cập nhật version thành {new_version}...")
    
    files_to_update = [
        ('setup.py', r'version\s*=\s*["\']([^"\']+)["\']', f'version="{new_version}"'),
        ('pyproject.toml', r'version\s*=\s*["\']([^"\']+)["\']', f'version = "{new_version}"'),
        ('detect_row/__init__.py', r'__version__\s*=\s*["\']([^"\']+)["\']', f'__version__ = "{new_version}"')
    ]
    
    for file_path, pattern, replacement in files_to_update:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = re.sub(pattern, replacement, content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Cập nhật {file_path}")
        else:
            print(f"⚠️  File {file_path} không tồn tại")

def check_version_consistency():
    """Kiểm tra tính nhất quán của version"""
    print("🔍 Kiểm tra version consistency...")
    result = run_command("python check_versions.py", check=False)
    return result.returncode == 0

def clean_build():
    """Xóa build artifacts"""
    print("🧹 Dọn dẹp build artifacts...")
    
    dirs_to_remove = ['build', 'dist', 'detect_row.egg-info']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            if os.name == 'nt':  # Windows
                run_command(f'rmdir /s /q "{dir_name}"', check=False)
            else:  # Linux/Mac
                run_command(f'rm -rf "{dir_name}"', check=False)

def build_package():
    """Build package"""
    print("🔨 Building package...")
    run_command("python -m build")

def check_package():
    """Kiểm tra package integrity"""
    print("✅ Kiểm tra package...")
    
    # Check với twine
    run_command("twine check dist/*")
    
    # Kiểm tra file size
    print("📊 Kiểm tra file size...")
    result = run_command("""python -c "
import zipfile
import os

wheel_file = None
for file in os.listdir('dist'):
    if file.endswith('.whl'):
        wheel_file = f'dist/{file}'
        break

if wheel_file:
    with zipfile.ZipFile(wheel_file, 'r') as z:
        for file in z.namelist():
            if 'advanced_row_extractor.py' in file:
                info = z.getinfo(file)
                size = info.file_size
                print(f'advanced_row_extractor.py: {size:,} bytes')
                if size < 20000:
                    print('⚠️  WARNING: File quá nhỏ!')
                    exit(1)
                else:
                    print('✅ File size OK')
                break
"""", check=False)
    
    if result.returncode != 0:
        print("❌ Package có vấn đề về file size!")
        return False
    
    return True

def test_local_install(version):
    """Test cài đặt local"""
    print("🧪 Test local install...")
    
    wheel_file = f"dist/detect_row-{version}-py3-none-any.whl"
    if not os.path.exists(wheel_file):
        # Tìm wheel file
        for file in os.listdir('dist'):
            if file.endswith('.whl'):
                wheel_file = f"dist/{file}"
                break
    
    run_command(f"pip install {wheel_file} --force-reinstall")
    
    # Test import
    test_result = run_command("""python -c "
try:
    from detect_row import AdvancedTableExtractor, AdvancedRowExtractorMain
    print('✅ Import thành công!')
    
    # Test tạo instance
    extractor = AdvancedTableExtractor('input', 'output')
    print('✅ AdvancedTableExtractor OK!')
    
    row_extractor = AdvancedRowExtractorMain()
    print('✅ AdvancedRowExtractorMain OK!')
    
    print('🎉 Package hoạt động hoàn hảo!')
except Exception as e:
    print(f'❌ Lỗi: {e}')
    exit(1)
" """, check=False)
    
    return test_result.returncode == 0

def upload_to_testpypi():
    """Upload lên Test PyPI"""
    print("🚀 Upload lên Test PyPI...")
    result = run_command("twine upload --repository testpypi dist/*", check=False)
    return result.returncode == 0

def test_testpypi_install(version):
    """Test install từ Test PyPI"""
    print("🧪 Test install từ Test PyPI...")
    
    # Uninstall current version
    run_command("pip uninstall detect-row -y", check=False)
    
    # Install từ Test PyPI
    result = run_command(f"pip install --index-url https://test.pypi.org/simple/ detect-row=={version}", check=False)
    
    if result.returncode == 0:
        # Test import
        test_result = run_command("""python -c "
from detect_row import AdvancedTableExtractor, AdvancedRowExtractorMain
print('✅ Test PyPI package OK!')
" """, check=False)
        return test_result.returncode == 0
    
    return False

def upload_to_pypi():
    """Upload lên PyPI chính thức"""
    print("🚀 Upload lên PyPI...")
    run_command("twine upload dist/*")

def git_commit_and_tag(version):
    """Git commit và tag"""
    print(f"📝 Git commit và tag v{version}...")
    
    run_command("git add .")
    run_command(f'git commit -m "Release version {version}"')
    run_command(f"git tag v{version}")
    run_command("git push origin main --tags")

def main():
    parser = argparse.ArgumentParser(description="Deploy DetectRow package")
    parser.add_argument("version", help="Version to deploy (e.g., 1.0.8)")
    parser.add_argument("--skip-test", action="store_true", help="Skip Test PyPI")
    parser.add_argument("--skip-git", action="store_true", help="Skip git operations")
    parser.add_argument("--force", action="store_true", help="Force deploy even if tests fail")
    
    args = parser.parse_args()
    version = args.version
    
    print(f"🚀 Deploying DetectRow version {version}")
    print("=" * 50)
    
    # 1. Cập nhật version
    update_version(version)
    
    # 2. Kiểm tra version consistency
    if not check_version_consistency():
        print("❌ Version không nhất quán!")
        if not args.force:
            sys.exit(1)
    
    # 3. Clean build
    clean_build()
    
    # 4. Build package
    build_package()
    
    # 5. Kiểm tra package
    if not check_package():
        print("❌ Package có vấn đề!")
        if not args.force:
            sys.exit(1)
    
    # 6. Test local install
    if not test_local_install(version):
        print("❌ Local install test failed!")
        if not args.force:
            sys.exit(1)
    
    # 7. Upload lên Test PyPI (nếu không skip)
    if not args.skip_test:
        if upload_to_testpypi():
            print("✅ Upload Test PyPI thành công!")
            
            # Test install từ Test PyPI
            if test_testpypi_install(version):
                print("✅ Test PyPI install OK!")
            else:
                print("❌ Test PyPI install failed!")
                if not args.force:
                    sys.exit(1)
        else:
            print("⚠️  Upload Test PyPI failed, tiếp tục...")
    
    # 8. Xác nhận upload lên PyPI chính thức
    if not args.force:
        confirm = input(f"\n🤔 Bạn có chắc muốn upload version {version} lên PyPI? (y/N): ")
        if confirm.lower() != 'y':
            print("❌ Hủy deploy")
            sys.exit(0)
    
    # 9. Upload lên PyPI
    upload_to_pypi()
    print("✅ Upload PyPI thành công!")
    
    # 10. Git commit và tag (nếu không skip)
    if not args.skip_git:
        git_commit_and_tag(version)
        print("✅ Git operations hoàn thành!")
    
    print(f"\n🎉 Deploy version {version} hoàn thành!")
    print(f"📦 Package có thể cài đặt: pip install detect-row=={version}")

if __name__ == "__main__":
    main() 