#!/bin/bash

echo "TRICH XUAT BANG CUOI CUNG - HOAN HAO"
echo "===================================="

# Kiểm tra thư mục input
if [ ! -d "input" ]; then
    echo "Tao thu muc input..."
    mkdir -p input
    echo "Vui long copy cac file anh vao thu muc input/"
    exit 1
fi

# Xóa output cũ
echo "Xoa ket qua cu..."
rm -rf output/final_tables
rm -rf debug/final_extraction

# Tạo thư mục mới
mkdir -p output/final_tables
mkdir -p debug/final_extraction

echo "Bat dau trich xuat bang cuoi cung..."

# Chạy script Python
py extract_tables_final.py

echo ""
echo "===================================="
echo "HOAN THANH!"
echo "===================================="

# Hiển thị kết quả
if [ -d "output/final_tables" ] && [ "$(ls -A output/final_tables 2>/dev/null)" ]; then
    echo "CAC BANG DA DUOC TRICH XUAT:"
    dir output/final_tables
else
    echo "KHONG CO BANG NAO DUOC TRICH XUAT"
fi 