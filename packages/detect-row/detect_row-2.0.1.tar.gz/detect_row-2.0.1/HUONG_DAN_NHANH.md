# 🚀 HƯỚNG DẪN NHANH - HỆ THỐNG TRÍCH XUẤT BẢNG

> **Phiên bản**: 2.0  
> **Ngày**: 18/06/2025  
> **Hỗ trợ**: Vietnamese AI Assistant

---

## ⚡ BẮT ĐẦU NHANH (5 PHÚT)

### 1️⃣ **Kiểm tra hệ thống**
```bash
# Kiểm tra toàn bộ
python system_check.py

# Kiểm tra chi tiết + tự động sửa lỗi
python system_check.py --detailed --fix-issues
```

### 2️⃣ **Demo nhanh**
```bash
# Tạo ảnh mẫu và test
python quick_demo.py

# Chỉ xem kết quả
python quick_demo.py --show-results
```

### 3️⃣ **Chạy workflow thực tế**
```bash
# Đặt ảnh vào input/ rồi chạy:
python run_complete_workflow.py

# Hoặc dùng script tự động (Linux/Mac):
./auto_workflow.sh
```

---

## 🎯 CÁC LỆNH CHÍNH

### 📋 **Trích xuất bảng + cột (All-in-one)**
```bash
# Cơ bản
python extract_tables_and_columns.py image.png

# Với nhóm cột tùy chỉnh
python extract_tables_and_columns.py image.png \
  --column-groups "header:1;content:2,3;footer:4"

# Chế độ tương tác
python extract_tables_and_columns.py --interactive
```

### 🔧 **Công cụ hỗ trợ**
```bash
# Trợ giúp tạo nhóm cột
python column_groups_helper.py

# Kiểm tra GPU
python test_gpu_support.py

# Xem kết quả
python show_results_summary.py
```

### 🏃 **Workflow tự động**
```bash
# Windows
python run_complete_workflow.py --max-memory 4 --use-gpu

# Linux/Mac  
./auto_workflow.sh --gpu --max-memory 8

# Với cấu hình tùy chỉnh
python run_complete_workflow.py --config config_template.json
```

---

## 📊 NHÓM CỘT THÔNG DỤNG

### 🇻🇳 **Tài liệu Việt Nam**
```bash
--column-groups "stt:1;ho_ten:2;dong_y:3;khong_dong_y:4;thong_tin:1,2;ket_qua:3,4"
```

### 📄 **Tài liệu cơ bản**
```bash
--column-groups "header:1;content:2,3;footer:4;full:1,2,3,4"
```

### 📊 **Bảng dữ liệu**
```bash
--column-groups "id:1;data:2,3,4;summary:3,4;all:1,2,3,4"
```

---

## 🗂️ CẤU TRÚC KẾT QUẢ

```
📁 output/tables_and_columns/
├── 📁 tables/                  # Các bảng đã tách
│   ├── image_table_0.jpg
│   ├── image_table_1.jpg  
│   └── image_table_2.jpg
│
└── 📁 columns/                 # Cột từ từng bảng
    ├── 📁 image_table_0/
    │   ├── 📁 individual_columns/    # Cột riêng
    │   └── 📁 merged_columns/        # Cột merge
    ├── 📁 image_table_1/
    └── 📁 image_table_2/

📁 debug/tables_and_columns/    # Debug files
📁 reports/                     # Báo cáo JSON
```

---

## ⚙️ THIẾT LẬP THÔNG SỐ

### 🎮 **GPU & Memory**
```bash
# Sử dụng GPU với 8GB memory
python run_complete_workflow.py --use-gpu --max-memory 8

# Chỉ CPU với 2GB memory
python run_complete_workflow.py --no-gpu --max-memory 2

# Tự động phát hiện
python run_complete_workflow.py  # GPU auto, 4GB default
```

### 📝 **Cấu hình file**
```bash
# Sử dụng config template
python run_complete_workflow.py --config config_template.json

# Tạo config tùy chỉnh từ template
cp config_template.json my_config.json
# Chỉnh sửa my_config.json theo nhu cầu
python run_complete_workflow.py --config my_config.json
```

---

## 🐛 DEBUG & TROUBLESHOOTING

### ❌ **Lỗi thường gặp**

**1. Không phát hiện bảng**
```bash
# Kiểm tra debug files
ls debug/tables_and_columns/
# Điều chỉnh threshold trong code hoặc config
```

**2. Memory lỗi**
```bash
# Giảm memory limit
python run_complete_workflow.py --max-memory 2

# Hoặc tắt GPU
python run_complete_workflow.py --no-gpu
```

**3. Cột tách sai**
```bash
# Xem debug cột
ls debug/tables_and_columns/columns/*/
# Điều chỉnh min_column_width trong config
```

### 🔍 **Debug files quan trọng**
- `debug/*/final_binary.jpg` → Kiểm tra threshold
- `debug/*/final_structure.jpg` → Xem cấu trúc bảng
- `debug/*/vertical_lines.jpg` → Kiểm tra phát hiện cột
- `reports/*.json` → Thống kê chi tiết

---

## 🚀 PERFORMANCE TIPS

### ⚡ **Tăng tốc**
1. **Sử dụng GPU**: `--use-gpu` (nếu có NVIDIA GPU)
2. **Tăng memory**: `--max-memory 8` (nếu có RAM đủ)
3. **Batch processing**: Tự động theo memory available
4. **Resize ảnh**: Giảm kích thước ảnh đầu vào nếu quá lớn

### 🧠 **Quản lý memory**
1. **Auto cleanup**: Tự động dọn memory sau mỗi batch
2. **Memory monitoring**: Theo dõi usage real-time
3. **Smart batching**: Tự động điều chỉnh batch size
4. **GPU cache**: Tự động clear CUDA cache khi cần

---

## 📱 WORKFLOW SHORTCUTS

### 🔄 **Workflow cơ bản**
```bash
# 1. Kiểm tra
python system_check.py

# 2. Demo
python quick_demo.py

# 3. Chạy thực tế
python run_complete_workflow.py

# 4. Xem kết quả
python show_results_summary.py
```

### 🏃 **Workflow nhanh** 
```bash
# All-in-one với default settings
python extract_tables_and_columns.py *.png

# Với nhóm cột Việt Nam
python extract_tables_and_columns.py *.jpg \
  --column-groups "stt:1;ho_ten:2;dong_y:3;khong_dong_y:4;info:1,2;result:3,4"
```

### 🛠️ **Workflow tùy chỉnh**
```bash
# 1. Tạo config
python column_groups_helper.py  # Tạo nhóm cột
cp config_template.json my_config.json  # Copy config

# 2. Test với config
python run_complete_workflow.py --config my_config.json

# 3. Production với monitoring
python run_complete_workflow.py \
  --config my_config.json \
  --max-memory 8 \
  --use-gpu \
  --verbose
```

---

## 📞 HỖ TRỢ NHANH

### 🆘 **Khi gặp lỗi**
1. Chạy `python system_check.py --detailed` 
2. Xem log trong `workflow.log`
3. Kiểm tra debug files
4. Thử giảm `--max-memory`
5. Thử `--no-gpu` nếu có vấn đề GPU

### 💡 **Tips hay**
- **Ảnh chất lượng cao** → Kết quả tốt hơn
- **Contrast rõ ràng** → Phát hiện bảng chính xác
- **Format PNG/TIFF** → Tốt hơn JPG cho OCR
- **Resize ảnh lớn** → Tăng tốc xử lý
- **Batch nhiều ảnh** → Hiệu quả hơn từng ảnh

### 🔗 **Files quan trọng**
- `COMPLETE_USAGE_GUIDE.md` → Hướng dẫn chi tiết đầy đủ
- `config_template.json` → Template cấu hình
- `system_check.py` → Kiểm tra hệ thống
- `run_complete_workflow.py` → Workflow tự động
- `column_groups_helper.py` → Trợ giúp merge cột

---

**🎉 Chúc bạn sử dụng hiệu quả!**

*Được tạo bởi Vietnamese AI Assistant - 2025* 