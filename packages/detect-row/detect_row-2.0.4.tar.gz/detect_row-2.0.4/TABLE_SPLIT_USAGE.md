# 📊 TABLE SPLITTER - Hướng dẫn sử dụng

## 🎯 Mục đích
Chia **1 bảng 4 cột** thành **2 bảng 3 cột**:

### Input:
```
| STT | Họ và Tên    | Đồng ý | Không đồng ý |
|-----|-------------|--------|---------------|
| 1   | Nguyễn A    | ✓      |               |
| 2   | Trần B      |        | ✓             |
| 3   | Lê C        | ✓      |               |
```

### Output:
**Bảng A** (Cột 1+2+3):
```
| STT | Họ và Tên    | Đồng ý |
|-----|-------------|--------|
| 1   | Nguyễn A    | ✓      |
| 2   | Trần B      |        |
| 3   | Lê C        | ✓      |
```

**Bảng B** (Cột 1+2+4):
```
| STT | Họ và Tên    | Không đồng ý |
|-----|-------------|---------------|
| 1   | Nguyễn A    |               |
| 2   | Trần B      | ✓             |
| 3   | Lê C        |               |
```

## 🚀 Cách sử dụng

### 1. Quick Version (Đơn giản)
```bash
python quick_table_split.py your_table.jpg
```

**Kết quả:**
- `output/table_A_cols_123.jpg` - Bảng A (STT + Họ tên + Đồng ý)
- `output/table_B_cols_124.jpg` - Bảng B (STT + Họ tên + Không đồng ý)
- `output/debug_splits.jpg` - Ảnh debug để kiểm tra

### 2. Advanced Version (Đầy đủ)
```python
from table_splitter_example import TableSplitter

splitter = TableSplitter("input.jpg", "my_output")
table_a, table_b = splitter.split_table()

print(f"Bảng A: {table_a}")
print(f"Bảng B: {table_b}")
```

## 📋 Yêu cầu file input

### ✅ Format tốt:
- Ảnh có **4 cột rõ ràng**
- Có **đường kẻ** phân cách cột
- Độ phân giải **≥ 800px** width
- Format: JPG, PNG, BMP

### ❌ Tránh:
- Ảnh mờ, nghiêng
- Không có đường kẻ
- Quá nhỏ (< 400px)
- Cột không đều

## 🛠️ Thuật toán

### Quick Version:
1. **Vertical Projection** - Tính tổng pixel theo cột
2. **Valley Detection** - Tìm vùng ít pixel (đường phân cách)
3. **Position Optimization** - Chọn 3 vị trí cân đối nhất
4. **Image Cropping** - Tạo 2 ảnh từ vị trí đã tìm

### Advanced Version:
1. **Multi-method Detection:**
   - Hough Transform (weight 3)
   - Vertical Projection (weight 2) 
   - Morphological Operations (weight 2)
   - Text Gap Analysis (weight 1)

2. **Weighted Clustering** - Combine kết quả với trọng số

3. **CV Optimization** - Tối ưu Coefficient of Variation

## 📁 Cấu trúc files

```
detectrow1806/
├── quick_table_split.py          # Version đơn giản - DÙNG NÀY!
├── table_splitter_example.py     # Version đầy đủ
├── TABLE_SPLIT_USAGE.md          # Hướng dẫn này
├── your_table.jpg                # Input của bạn
└── output/                       # Kết quả
    ├── table_A_cols_123.jpg      # Bảng A 
    ├── table_B_cols_124.jpg      # Bảng B
    └── debug_splits.jpg          # Debug
```

## 🎮 Demo nhanh

### Bước 1: Chuẩn bị
```bash
# Copy ảnh bảng 4 cột vào thư mục
cp your_table.jpg ./table_input.jpg
```

### Bước 2: Chạy
```bash
python quick_table_split.py table_input.jpg
```

### Bước 3: Kiểm tra kết quả
```bash
ls output/
# → table_A_cols_123.jpg  table_B_cols_124.jpg  debug_splits.jpg
```

## 🔧 Troubleshooting

### ❌ "Cannot read image"
- **Nguyên nhân:** File không tồn tại hoặc format sai
- **Giải pháp:** Kiểm tra path và đổi sang JPG/PNG

### ❌ "Using equal division fallback"
- **Nguyên nhân:** Không detect được cột
- **Giải pháp:** 
  - Tăng độ phân giải ảnh
  - Đảm bảo có đường kẻ rõ ràng
  - Thử advanced version

### ❌ Kết quả không chính xác
- **Kiểm tra:** `debug_splits.jpg` xem vị trí detect
- **Điều chỉnh:** Sử dụng advanced version với fine-tuning

## 💡 Tips sử dụng

### Cho kết quả tốt nhất:
1. **Ảnh chất lượng cao** (≥ 1200px width)
2. **Đường kẻ rõ ràng** giữa các cột
3. **Ảnh thẳng** (không nghiêng)
4. **Background trắng** hoặc sáng

### Tích hợp vào workflow:
```python
# Batch processing nhiều file
import glob

for img_path in glob.glob("tables/*.jpg"):
    try:
        table_a, table_b = quick_split(img_path)
        print(f"✅ Processed: {img_path}")
    except Exception as e:
        print(f"❌ Failed: {img_path} - {e}")
```

## 🔄 Customize

### Thay đổi output format:
```python
# Trong quick_table_split.py, line ~110:
table_a.save(table_a_path, format='PNG', quality=95)
```

### Thay đổi column layout:
```python
# Để tạo bảng khác (VD: cột 1+3+4):
table_c = pil_img.crop((0, 0, valley_positions[0], height))  # Cột 1
right_part = pil_img.crop((valley_positions[1], 0, width, height))  # Cột 3+4
# ... ghép như table_b
```

---

## 🎯 Kết luận

**Quick version** phù hợp với **80% trường hợp** sử dụng thông thường.

**Advanced version** dành cho các trường hợp **phức tạp** hoặc cần **độ chính xác cao**.

Chọn tool phù hợp với nhu cầu của bạn! 🚀 