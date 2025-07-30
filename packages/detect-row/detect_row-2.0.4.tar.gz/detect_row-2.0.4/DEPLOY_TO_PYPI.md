# 🚀 DEPLOY DETECT-ROW LÊN PyPI

## 📦 Tình trạng hiện tại

✅ **Package đã sẵn sàng deploy!**

```
dist/
├── detect_row-2.0.0-py3-none-any.whl    (47KB)
└── detect_row-2.0.0.tar.gz               (143KB)
```

✅ **Quality check:** PASSED
✅ **Build:** SUCCESS  
✅ **All files included:** YES

## 🎯 Cách deploy

### 1. Test với TestPyPI trước (Khuyến nghị)

```bash
# Upload lên TestPyPI
twine upload --repository testpypi dist/*

# Test install từ TestPyPI
pip install --index-url https://test.pypi.org/simple/ detect-row
```

### 2. Deploy chính thức lên PyPI

```bash
# Upload lên PyPI chính thức
twine upload dist/*

# Người dùng có thể install:
pip install detect-row
```

## 🔑 Cần API Token

### Tạo PyPI Account & Token:

1. **Đăng ký tài khoản:** https://pypi.org/account/register/
2. **Tạo API token:** https://pypi.org/manage/account/token/
3. **Setup credentials:**

```bash
# Cách 1: Nhập khi upload
Username: __token__
Password: [your-api-token]

# Cách 2: Tạo file ~/.pypirc
[pypi]
username = __token__
password = [your-api-token]

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = [your-testpypi-token]
```

## 📋 Command Summary

```bash
# Build package (đã xong)
python -m build

# Check quality (đã pass)
twine check dist/*

# Test deploy
twine upload --repository testpypi dist/*

# Production deploy
twine upload dist/*
```

## 🎉 Sau khi deploy thành công

### Users có thể install:
```bash
# Basic install
pip install detect-row

# With GPU support
pip install detect-row[gpu]

# Full install
pip install detect-row[full]
```

### Usage:
```python
from detect_row import AdvancedColumnExtractor, AdvancedTableExtractor
from detect_row import BasicRowExtractor, TesseractRowExtractor

# Hoặc dùng CLI
detect-row-demo
detect-row-check
detect-row-column input.jpg
```

## 🔧 Package Info

- **Name:** detect-row  
- **Version:** 2.0.0
- **Python:** >=3.8
- **Size:** 47KB (wheel), 143KB (source)
- **Dependencies:** numpy, opencv-python, matplotlib, pytesseract, Pillow, scikit-image, scipy, psutil

## 📊 Features Include

✅ **Table Detection & Extraction**
✅ **Row Detection & Extraction** 
✅ **Column Detection & Extraction** 
✅ **OCR Integration (Tesseract)**
✅ **GPU Support (Optional)**
✅ **Vietnamese Language Support**
✅ **Command Line Tools**
✅ **Debug Visualization**
✅ **Table Splitting**

## 🌟 Next Steps

1. **Deploy lên TestPyPI** để test
2. **Test install và functionality**  
3. **Fix any issues**
4. **Deploy lên PyPI chính thức**
5. **Update documentation với PyPI links**
6. **Announce release**

---

**Package sẵn sàng để deploy! 🚀** 