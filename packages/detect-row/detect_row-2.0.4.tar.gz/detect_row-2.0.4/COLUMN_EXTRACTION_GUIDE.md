# Hướng Dẫn Trích Xuất Cột Từ Bảng

## Tổng quan

Module `AdvancedColumnExtractor` cho phép:
- **Tìm tối đa 3 bảng** trong mỗi ảnh
- **Crop từng bảng** một cách chính xác  
- **Trích xuất cột** từ mỗi bảng đã crop
- **Lưu cột riêng biệt** và **gộp cột theo nhóm**

## Cách sử dụng nhanh

### 1. Chạy demo tự động

```bash
# Đặt ảnh vào thư mục input/
cp your_table_image.jpg input/

# Chạy script demo
bash run_column_extraction.sh
```

### 2. Chạy với Python trực tiếp

```bash
python3 extract_columns_demo.py
```

### 3. Chạy với file cụ thể

```bash
python3 -m detect_row.advanced_column_extractor input/your_image.jpg
```

## Tính năng chính

### 🔍 Phát hiện bảng thông minh
- Tự động tìm **tối đa 3 bảng** trong ảnh
- Crop từng bảng với độ chính xác cao
- Lưu ảnh crop để kiểm tra

### 📏 Trích xuất cột chính xác
- Phát hiện đường kẻ dọc bằng morphology và histogram
- Lọc cột theo chiều rộng tối thiểu (mặc định: 30px)
- Hỗ trợ bảng có đường kẻ mờ hoặc không hoàn chỉnh

### 📁 Lưu file linh hoạt
- **Cột riêng biệt**: Mỗi cột thành 1 file riêng
- **Cột gộp**: Gộp nhiều cột theo nhóm

## Cấu trúc kết quả

```
output/columns/
├── individual_columns/      # Cột riêng biệt
│   ├── table_01_column_01.jpg
│   ├── table_01_column_02.jpg
│   ├── table_02_column_01.jpg
│   └── ...
└── merged_columns/          # Cột đã gộp
    ├── table_01_columns_1_2_first_two.jpg
    ├── table_01_columns_3_third.jpg
    ├── table_02_columns_1_2_first_two.jpg
    └── ...

debug/columns/               # Ảnh debug
├── table_01_cropped.jpg     # Bảng đã crop
├── table_02_cropped.jpg
├── vertical_lines_original.jpg  # Đường kẻ dọc gốc
├── vertical_lines_filtered.jpg  # Đường kẻ dọc đã lọc
├── detected_vertical_lines.jpg  # Đường kẻ phát hiện
└── v_projection.png         # Histogram dọc
```

## Cấu hình nhóm cột

### Cấu hình mặc định

```python
column_groups = {
    "first_two": [1, 2],        # Cột 1+2 thành 1 file
    "third": [3],               # Cột 3 riêng
    "fourth": [4],              # Cột 4 riêng  
    "last_columns": [5, 6, 7]   # Cột 5+6+7 thành 1 file
}
```

### Tùy chỉnh nhóm cột

```python
# Ví dụ: Gộp cột cho bảng có 8 cột
column_groups = {
    "header": [1],              # Cột tiêu đề
    "data_1_2": [2, 3],         # Dữ liệu nhóm 1
    "data_3_4": [4, 5],         # Dữ liệu nhóm 2
    "summary": [6, 7, 8]        # Cột tổng kết
}
```

## Tham số điều chỉnh

### Trong script Python

```python
extractor = AdvancedColumnExtractor(
    input_dir="input",
    output_dir="output/columns", 
    debug_dir="debug/columns",
    min_column_width=30          # Chiều rộng cột tối thiểu
)

result = extractor.process_image(
    image_path="table_image.jpg",
    save_individual=True,        # Lưu cột riêng
    column_groups=column_groups, # Nhóm cột
    max_tables=3                 # Tối đa 3 bảng
)
```

### Command line

```bash
python3 -m detect_row.advanced_column_extractor \
    image.jpg \
    --input-dir input \
    --output-dir output/columns \
    --debug-dir debug/columns \
    --max-tables 3
```

## Xử lý lỗi thường gặp

### ❌ Không phát hiện được bảng
**Nguyên nhân**: Ảnh không rõ ràng hoặc không có đường viền bảng

**Giải pháp**:
- Kiểm tra ảnh trong `debug/columns/binary.jpg`
- Điều chỉnh threshold hoặc morphology trong code
- Đảm bảo ảnh có độ tương phản tốt

### ❌ Không trích xuất được cột
**Nguyên nhân**: Không phát hiện được đường kẻ dọc

**Giải pháp**:
- Xem `debug/columns/vertical_lines_*.jpg`
- Xem `debug/columns/v_projection.png` 
- Giảm `min_column_width` nếu cột quá nhỏ
- Điều chỉnh `min_line_length_ratio` trong code

### ❌ Cột bị cắt sai
**Nguyên nhân**: Đường kẻ dọc phát hiện không chính xác

**Giải pháp**:
- Kiểm tra `debug/columns/detected_vertical_lines.jpg`
- Điều chỉnh ngưỡng lọc histogram
- Tăng `min_column_width` để lọc cột nhỏ

## Ví dụ kết quả

### Input
```
input/
└── financial_table.jpg      # Bảng tài chính 3 cột
```

### Output  
```
output/columns/
├── individual_columns/
│   ├── table_01_column_01.jpg  # Cột tên khoản mục
│   ├── table_01_column_02.jpg  # Cột số liệu năm trước  
│   └── table_01_column_03.jpg  # Cột số liệu năm nay
└── merged_columns/
    ├── table_01_columns_1_2_first_two.jpg    # Tên + năm trước
    └── table_01_columns_3_third.jpg          # Năm nay
```

## Tips và thủ thuật

### 🎯 Tối ưu chất lượng ảnh đầu vào
- Sử dụng ảnh có độ phân giải cao (ít nhất 300 DPI)
- Đảm bảo đường kẻ bảng rõ ràng và tương phản cao
- Tránh ảnh bị nghiêng hoặc méo

### 🔧 Điều chỉnh tham số
- `min_column_width`: Tăng để lọc cột nhỏ, giảm để giữ cột nhỏ
- `max_tables`: Điều chỉnh theo số lượng bảng mong muốn
- `min_line_length_ratio`: Điều chỉnh độ nhạy phát hiện đường kẻ

### 📊 Sử dụng debug
- Luôn kiểm tra thư mục `debug/columns/` để hiểu quá trình xử lý
- Sử dụng histogram để điều chỉnh ngưỡng phát hiện đường kẻ
- Kiểm tra ảnh crop để đảm bảo bảng được cắt chính xác

## Liên hệ và hỗ trợ

Nếu gặp vấn đề, hãy:
1. Kiểm tra log file `column_extraction.log`
2. Xem ảnh debug trong `debug/columns/`
3. Điều chỉnh tham số phù hợp với ảnh của bạn 