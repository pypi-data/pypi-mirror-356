# 🚀 Hướng dẫn Build và Deploy Package DetectRow

## 📋 Mục lục
- [Chuẩn bị môi trường](#chuẩn-bị-môi-trường)
- [Cấu trúc project](#cấu-trúc-project)
- [Build package](#build-package)
- [Kiểm tra package](#kiểm-tra-package)
- [Deploy lên PyPI](#deploy-lên-pypi)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## 🛠️ Chuẩn bị môi trường

### 1. Cài đặt build tools
```bash
pip install build twine wheel setuptools
```

### 2. Cấu hình PyPI credentials
```bash
# Tạo file ~/.pypirc
[distutils]
index-servers = 
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

### 3. Kiểm tra cấu trúc project
```bash
python setup.py check --strict
```

## 📁 Cấu trúc project

Đảm bảo project có cấu trúc đúng:

```
detect-row/
├── detect_row/                 # Package chính
│   ├── __init__.py            # Version và imports
│   ├── base.py                # Base classes
│   ├── advanced_table_extractor.py
│   ├── advanced_row_extractor.py
│   └── tesseract_ocr_extractor.py
├── setup.py                   # Setup configuration
├── pyproject.toml            # Modern Python packaging
├── requirements.txt          # Dependencies
├── MANIFEST.in              # Include/exclude files
├── README.md                # Documentation
└── LICENSE                  # License file
```

### Kiểm tra các file cấu hình:

**setup.py:**
```python
version="1.0.7"  # Cập nhật version
```

**pyproject.toml:**
```toml
version = "1.0.7"  # Phải khớp với setup.py
```

**detect_row/__init__.py:**
```python
__version__ = "1.0.7"  # Phải khớp với setup.py
```

## 🔨 Build package

### 1. Clean build artifacts
```bash
# Windows
rmdir /s build dist detect_row.egg-info

# Linux/Mac
rm -rf build/ dist/ *.egg-info/
```

### 2. Build package
```bash
python -m build
```

### 3. Kiểm tra nội dung wheel
```bash
python -c "
import zipfile
import os

wheel_file = None
for file in os.listdir('dist'):
    if file.endswith('.whl'):
        wheel_file = f'dist/{file}'
        break

if wheel_file:
    with zipfile.ZipFile(wheel_file, 'r') as z:
        print('📦 Nội dung wheel:')
        for file in z.namelist():
            if 'detect_row' in file:
                info = z.getinfo(file)
                print(f'  {file}: {info.file_size:,} bytes')
else:
    print('❌ Không tìm thấy wheel file')
"
```

### 4. Kiểm tra file size quan trọng
```bash
python -c "
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
                    print('⚠️  WARNING: File quá nhỏ, có thể thiếu code!')
                else:
                    print('✅ File size OK')
                break
"
```

## ✅ Kiểm tra package

### 1. Kiểm tra package integrity
```bash
twine check dist/*
```

### 2. Test install local
```bash
pip install dist/detect_row-1.0.7-py3-none-any.whl --force-reinstall
```

### 3. Test import và functionality
```bash
python -c "
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
"
```

### 4. Test với script demo
```bash
python -c "
import os
if os.path.exists('extract_table_pip_package.py'):
    print('✅ Demo script có sẵn')
    # Có thể test run script nếu có ảnh mẫu
else:
    print('⚠️  Demo script không tìm thấy')
"
```

## 🚀 Deploy lên PyPI

### 1. Upload lên Test PyPI (khuyến nghị)
```bash
twine upload --repository testpypi dist/*
```

### 2. Test install từ Test PyPI
```bash
pip install --index-url https://test.pypi.org/simple/ detect-row==1.0.7
```

### 3. Test package từ Test PyPI
```bash
python -c "
from detect_row import AdvancedTableExtractor, AdvancedRowExtractorMain
print('✅ Test PyPI package OK!')
"
```

### 4. Upload lên PyPI chính thức
```bash
twine upload dist/*
```

### 5. Verify trên PyPI
```bash
pip install detect-row==1.0.7 --force-reinstall
python -c "
from detect_row import AdvancedTableExtractor, AdvancedRowExtractorMain
print('✅ PyPI package OK!')
"
```

## 🔄 Cập nhật version

### 1. Bump version
```bash
# Cập nhật trong setup.py
sed -i 's/version="1.0.7"/version="1.0.8"/' setup.py

# Cập nhật trong pyproject.toml
sed -i 's/version = "1.0.7"/version = "1.0.8"/' pyproject.toml

# Cập nhật trong __init__.py
sed -i 's/__version__ = "1.0.7"/__version__ = "1.0.8"/' detect_row/__init__.py
```

### 2. Commit và tag
```bash
git add .
git commit -m "Bump version to 1.0.8"
git tag v1.0.8
git push origin main --tags
```

### 3. Build và deploy
```bash
rm -rf build/ dist/ *.egg-info/
python -m build
twine check dist/*
twine upload dist/*
```

## 🔧 Troubleshooting

### Lỗi thường gặp:

#### 1. File size quá nhỏ trong wheel
**Triệu chứng:** advanced_row_extractor.py chỉ có vài KB thay vì ~29KB

**Giải pháp:**
```bash
# Kiểm tra MANIFEST.in
echo "include detect_row/*.py" > MANIFEST.in
echo "recursive-include detect_row *.py" >> MANIFEST.in

# Rebuild
rm -rf build/ dist/ *.egg-info/
python -m build
```

#### 2. Import error sau khi install
**Triệu chứng:** `ModuleNotFoundError` hoặc `ImportError`

**Giải pháp:**
```bash
# Kiểm tra __init__.py
cat detect_row/__init__.py

# Đảm bảo có đầy đủ imports:
# from .advanced_table_extractor import AdvancedTableExtractor
# from .advanced_row_extractor import AdvancedRowExtractorMain
```

#### 3. Version conflict
**Triệu chứng:** Version không khớp giữa các file

**Giải pháp:**
```bash
# Script kiểm tra version consistency
python -c "
import re

# Đọc version từ setup.py
with open('setup.py', 'r') as f:
    setup_content = f.read()
    setup_version = re.search(r'version=[\"\'](.*?)[\"\']', setup_content).group(1)

# Đọc version từ pyproject.toml
with open('pyproject.toml', 'r') as f:
    toml_content = f.read()
    toml_version = re.search(r'version = [\"\'](.*?)[\"\']', toml_content).group(1)

# Đọc version từ __init__.py
with open('detect_row/__init__.py', 'r') as f:
    init_content = f.read()
    init_version = re.search(r'__version__ = [\"\'](.*?)[\"\']', init_content).group(1)

print(f'setup.py: {setup_version}')
print(f'pyproject.toml: {toml_version}')
print(f'__init__.py: {init_version}')

if setup_version == toml_version == init_version:
    print('✅ Versions consistent!')
else:
    print('❌ Version mismatch!')
"
```

#### 4. Upload permission denied
**Triệu chứng:** `403 Forbidden` khi upload

**Giải pháp:**
```bash
# Kiểm tra API token
twine upload --repository testpypi dist/* --verbose

# Hoặc sử dụng username/password
twine upload dist/* --username __token__ --password your-api-token
```

## 📝 Best Practices

### 1. Pre-commit checklist
```bash
# 1. Kiểm tra code quality
python -m flake8 detect_row/
python -m pylint detect_row/

# 2. Run tests (nếu có)
python -m pytest tests/

# 3. Kiểm tra version consistency
python check_versions.py

# 4. Clean build
rm -rf build/ dist/ *.egg-info/

# 5. Build và test
python -m build
twine check dist/*
pip install dist/*.whl --force-reinstall
python -c "from detect_row import *; print('OK')"
```

### 2. Automated deployment script
```bash
#!/bin/bash
# deploy.sh

set -e

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Usage: ./deploy.sh 1.0.8"
    exit 1
fi

echo "🚀 Deploying version $VERSION"

# Update versions
sed -i "s/version=\".*\"/version=\"$VERSION\"/" setup.py
sed -i "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml
sed -i "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" detect_row/__init__.py

# Clean and build
rm -rf build/ dist/ *.egg-info/
python -m build

# Test
twine check dist/*
pip install dist/*.whl --force-reinstall
python -c "from detect_row import AdvancedTableExtractor, AdvancedRowExtractorMain; print('✅ Test OK')"

# Deploy
echo "Uploading to Test PyPI..."
twine upload --repository testpypi dist/*

echo "Test install from Test PyPI..."
pip install --index-url https://test.pypi.org/simple/ detect-row==$VERSION --force-reinstall

echo "Uploading to PyPI..."
twine upload dist/*

# Git tag
git add .
git commit -m "Release version $VERSION"
git tag v$VERSION
git push origin main --tags

echo "🎉 Deployment complete!"
```

### 3. Monitoring deployment
```bash
# Kiểm tra package trên PyPI
curl -s https://pypi.org/pypi/detect-row/json | jq '.info.version'

# Kiểm tra download stats
pip install pypistats
pypistats recent detect-row
```

---

## 📞 Hỗ trợ

Nếu gặp vấn đề trong quá trình build/deploy:

1. Kiểm tra [PyPI status](https://status.python.org/)
2. Xem [PyPI help](https://pypi.org/help/)
3. Tham khảo [Python Packaging Guide](https://packaging.python.org/)
4. Tạo issue trên GitHub repository

---

**Happy Packaging! 🎉** 