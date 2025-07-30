#!/bin/bash

# Script chạy demo trích xuất cột từ bảng
# ====================================

echo "🚀 Chạy Demo Trích Xuất Cột Từ Bảng"
echo "=================================="

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được tìm thấy!"
    echo "   Vui lòng cài đặt Python3 và thử lại."
    exit 1
fi

echo "✅ Python3 đã sẵn sàng"

# Kiểm tra các thư mục cần thiết
echo "📂 Tạo thư mục cần thiết..."
mkdir -p input
mkdir -p output/columns/individual_columns
mkdir -p output/columns/merged_columns  
mkdir -p debug/columns

echo "📂 Cấu trúc thư mục:"
echo "   📥 input/                           (đặt ảnh chứa bảng vào đây)"
echo "   📤 output/columns/individual_columns/ (cột riêng biệt)"
echo "   📤 output/columns/merged_columns/    (cột đã gộp)"
echo "   🔧 debug/columns/                   (ảnh debug)"

# Kiểm tra file ảnh trong thư mục input
echo ""
echo "🔍 Kiểm tra file ảnh trong thư mục input..."
image_count=$(find input -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.bmp" -o -iname "*.tiff" \) | wc -l)

if [ $image_count -eq 0 ]; then
    echo "⚠️  Không tìm thấy file ảnh nào trong thư mục input/"
    echo ""
    echo "📋 Hướng dẫn:"
    echo "   1. Đặt file ảnh chứa bảng vào thư mục input/"
    echo "   2. Hỗ trợ các định dạng: .jpg, .jpeg, .png, .bmp, .tiff"
    echo "   3. Chạy lại script này"
    echo ""
    echo "💡 Ví dụ:"
    echo "   cp your_table_image.jpg input/"
    echo "   bash run_column_extraction.sh"
    exit 1
else
    echo "✅ Tìm thấy $image_count file ảnh"
    echo "📄 Danh sách file:"
    find input -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.bmp" -o -iname "*.tiff" \) | while read file; do
        echo "   📷 $(basename "$file")"
    done
fi

echo ""
echo "🔧 Cấu hình xử lý:"
echo "   📊 Tối đa 3 bảng mỗi ảnh"
echo "   📏 Chiều rộng cột tối thiểu: 30px"
echo "   🔗 Nhóm cột:"
echo "      • first_two: cột 1+2"
echo "      • third: cột 3"  
echo "      • fourth: cột 4"
echo "      • last_columns: cột 5+6+7"

echo ""
echo "🚀 Bắt đầu xử lý..."
echo "==================="

# Chạy script Python
python3 extract_columns_demo.py

exit_code=$?

echo ""
echo "📊 Hoàn thành xử lý!"
echo "=================="

if [ $exit_code -eq 0 ]; then
    echo "✅ Script chạy thành công!"
    
    # Hiển thị thống kê kết quả
    individual_count=$(find output/columns/individual_columns -name "*.jpg" 2>/dev/null | wc -l)
    merged_count=$(find output/columns/merged_columns -name "*.jpg" 2>/dev/null | wc -l)
    debug_count=$(find debug/columns -name "*.jpg" 2>/dev/null | wc -l)
    
    echo ""
    echo "📈 Thống kê kết quả:"
    echo "   📁 File cột riêng: $individual_count"
    echo "   📁 File cột gộp: $merged_count"
    echo "   🔧 File debug: $debug_count"
    
    # Hiển thị một số file mẫu
    if [ $individual_count -gt 0 ]; then
        echo ""
        echo "📄 Ví dụ file cột riêng (5 file đầu):"
        find output/columns/individual_columns -name "*.jpg" | head -5 | while read file; do
            echo "   📷 $(basename "$file")"
        done
    fi
    
    if [ $merged_count -gt 0 ]; then
        echo ""
        echo "📄 Ví dụ file cột gộp (5 file đầu):"
        find output/columns/merged_columns -name "*.jpg" | head -5 | while read file; do
            echo "   📷 $(basename "$file")"
        done
    fi
    
    echo ""
    echo "🎉 Kiểm tra kết quả tại:"
    echo "   📂 output/columns/"
    echo "   🔧 debug/columns/ (để kiểm tra quá trình xử lý)"
    
else
    echo "❌ Script gặp lỗi (exit code: $exit_code)"
    echo "🔍 Kiểm tra log để biết thêm chi tiết"
fi

echo ""
echo "📋 Các bước tiếp theo:"
echo "   1. Kiểm tra file kết quả trong output/columns/"
echo "   2. Xem ảnh debug trong debug/columns/ nếu cần"
echo "   3. Điều chỉnh tham số trong extract_columns_demo.py nếu cần" 