#!/bin/bash

# Script để chạy workflow tách bảng và trích xuất cột
# =====================================================

echo "🚀 WORKFLOW TÁCH BẢNG VÀ TRÍCH XUẤT CỘT"
echo "========================================"

# Kiểm tra tham số
if [ "$#" -eq 0 ]; then
    echo "📖 Cách sử dụng:"
    echo "   $0 <ten_anh>"
    echo "   $0 image064.png"
    echo ""
    echo "🔧 Hoặc để xử lý tất cả ảnh trong thư mục input:"
    echo "   $0 --all"
    echo ""
    exit 1
fi

# Thiết lập thư mục
INPUT_DIR="test_image064/input"
OUTPUT_DIR="output/separate_tables_columns"
DEBUG_DIR="debug/separate_tables_columns"

echo "📂 Cấu hình thư mục:"
echo "   Input:  $INPUT_DIR"
echo "   Output: $OUTPUT_DIR" 
echo "   Debug:  $DEBUG_DIR"
echo ""

# Tạo thư mục nếu chưa có
mkdir -p "$INPUT_DIR" "$OUTPUT_DIR" "$DEBUG_DIR"

if [ "$1" = "--all" ]; then
    echo "🔄 Xử lý tất cả ảnh trong $INPUT_DIR..."
    python extract_tables_and_columns.py \
        --input-dir "$INPUT_DIR" \
        --output-dir "$OUTPUT_DIR" \
        --debug-dir "$DEBUG_DIR"
else
    IMAGE_FILE="$1"
    echo "🖼️  Xử lý ảnh: $IMAGE_FILE"
    
    # Kiểm tra file có tồn tại không
    if [ ! -f "$INPUT_DIR/$IMAGE_FILE" ]; then
        echo "❌ Không tìm thấy file: $INPUT_DIR/$IMAGE_FILE"
        echo "💡 Các file có sẵn:"
        ls -la "$INPUT_DIR"/ 2>/dev/null || echo "   (thư mục trống)"
        exit 1
    fi
    
    python extract_tables_and_columns.py \
        "$IMAGE_FILE" \
        --input-dir "$INPUT_DIR" \
        --output-dir "$OUTPUT_DIR" \
        --debug-dir "$DEBUG_DIR"
fi

# Hiển thị kết quả
echo ""
echo "✅ HOÀN THÀNH!"
echo "📁 Kết quả được lưu tại:"
echo "   📋 Bảng tách:     $OUTPUT_DIR/tables/"
echo "   📊 Cột từng bảng: $OUTPUT_DIR/columns/"
echo ""

# Hiển thị thống kê nhanh
if [ -d "$OUTPUT_DIR" ]; then
    TABLES_COUNT=$(ls "$OUTPUT_DIR/tables/"*.jpg 2>/dev/null | wc -l)
    COLUMNS_DIRS=$(ls -d "$OUTPUT_DIR/columns/"*/ 2>/dev/null | wc -l)
    
    echo "📊 THỐNG KÊ:"
    echo "   🔢 Số bảng tách: $TABLES_COUNT"
    echo "   🔢 Số thư mục cột: $COLUMNS_DIRS"
    
    # Đếm tổng số file cột
    INDIVIDUAL_FILES=0
    MERGED_FILES=0
    
    for table_dir in "$OUTPUT_DIR/columns/"*/; do
        if [ -d "$table_dir" ]; then
            table_name=$(basename "$table_dir")
            individual_count=$(ls "$table_dir/individual_columns/"*.jpg 2>/dev/null | wc -l)
            merged_count=$(ls "$table_dir/merged_columns/"*.jpg 2>/dev/null | wc -l)
            
            INDIVIDUAL_FILES=$((INDIVIDUAL_FILES + individual_count))
            MERGED_FILES=$((MERGED_FILES + merged_count))
            
            echo "   📋 $table_name: $individual_count cột riêng + $merged_count cột gộp"
        fi
    done
    
    echo "   🔢 Tổng file cột riêng: $INDIVIDUAL_FILES"
    echo "   🔢 Tổng file cột gộp: $MERGED_FILES"
fi

echo ""
echo "🔍 Để xem chi tiết kết quả:"
echo "   ls -la $OUTPUT_DIR/tables/"
echo "   ls -la $OUTPUT_DIR/columns/" 