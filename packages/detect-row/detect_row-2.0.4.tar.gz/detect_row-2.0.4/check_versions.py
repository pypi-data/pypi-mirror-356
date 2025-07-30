#!/usr/bin/env python3
"""
Script kiểm tra tính nhất quán của version trong các file cấu hình
"""

import re
import sys
import os
from pathlib import Path

def read_version_from_setup_py():
    """Đọc version từ setup.py"""
    try:
        with open('setup.py', 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    return None

def read_version_from_pyproject_toml():
    """Đọc version từ pyproject.toml"""
    try:
        with open('pyproject.toml', 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    return None

def read_version_from_init_py():
    """Đọc version từ detect_row/__init__.py"""
    try:
        with open('detect_row/__init__.py', 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    return None

def main():
    """Main function"""
    print("🔍 Kiểm tra version consistency...")
    print("=" * 50)
    
    # Đọc versions từ các file
    setup_version = read_version_from_setup_py()
    toml_version = read_version_from_pyproject_toml()
    init_version = read_version_from_init_py()
    
    # Hiển thị kết quả
    print(f"📄 setup.py:           {setup_version or '❌ Không tìm thấy'}")
    print(f"📄 pyproject.toml:     {toml_version or '❌ Không tìm thấy'}")
    print(f"📄 __init__.py:        {init_version or '❌ Không tìm thấy'}")
    print("=" * 50)
    
    # Kiểm tra consistency
    versions = [v for v in [setup_version, toml_version, init_version] if v is not None]
    
    if not versions:
        print("❌ Không tìm thấy version nào!")
        return 1
    
    if len(set(versions)) == 1:
        print(f"✅ Tất cả versions đều nhất quán: {versions[0]}")
        
        # Kiểm tra thêm các file khác
        check_additional_files(versions[0])
        
        return 0
    else:
        print("❌ Versions không nhất quán!")
        print("🔧 Cần cập nhật để đồng bộ tất cả versions")
        
        # Gợi ý fix
        suggest_fix(versions)
        
        return 1

def check_additional_files(version):
    """Kiểm tra version trong các file khác"""
    print("\n🔍 Kiểm tra các file khác...")
    
    # Kiểm tra README.md
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
            if version in content:
                print(f"✅ README.md có chứa version {version}")
            else:
                print(f"⚠️  README.md không chứa version {version}")
    
    # Kiểm tra CHANGELOG.md nếu có
    if os.path.exists('CHANGELOG.md'):
        with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
            content = f.read()
            if version in content:
                print(f"✅ CHANGELOG.md có chứa version {version}")
            else:
                print(f"⚠️  CHANGELOG.md không chứa version {version}")

def suggest_fix(versions):
    """Gợi ý cách fix version mismatch"""
    print("\n🔧 Gợi ý fix:")
    
    # Tìm version phổ biến nhất
    from collections import Counter
    version_counts = Counter(versions)
    most_common_version = version_counts.most_common(1)[0][0]
    
    print(f"💡 Khuyến nghị sử dụng version: {most_common_version}")
    print("\n📝 Commands để fix:")
    
    # Setup.py
    setup_version = read_version_from_setup_py()
    if setup_version != most_common_version:
        print(f"# Fix setup.py:")
        print(f"sed -i 's/version=\"{setup_version}\"/version=\"{most_common_version}\"/' setup.py")
    
    # pyproject.toml
    toml_version = read_version_from_pyproject_toml()
    if toml_version != most_common_version:
        print(f"# Fix pyproject.toml:")
        print(f"sed -i 's/version = \"{toml_version}\"/version = \"{most_common_version}\"/' pyproject.toml")
    
    # __init__.py
    init_version = read_version_from_init_py()
    if init_version != most_common_version:
        print(f"# Fix __init__.py:")
        print(f"sed -i 's/__version__ = \"{init_version}\"/__version__ = \"{most_common_version}\"/' detect_row/__init__.py")

if __name__ == "__main__":
    sys.exit(main()) 