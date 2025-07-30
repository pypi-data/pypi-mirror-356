#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Column Groups Helper - Trợ giúp tạo cấu hình nhóm cột
====================================================

Script này giúp người dùng:
1. Tạo cấu hình nhóm cột một cách trực quan
2. Lưu và tải cấu hình từ file
3. Tạo templates cho các trường hợp thường gặp
"""

import json
import os
from typing import Dict, List

class ColumnGroupsHelper:
    """Class trợ giúp quản lý nhóm cột"""
    
    def __init__(self):
        self.config_dir = "configs"
        os.makedirs(self.config_dir, exist_ok=True)
    
    def get_predefined_templates(self) -> Dict[str, Dict[str, List[int]]]:
        """Trả về các template định sẵn"""
        return {
            "basic": {
                "cols_1_2": [1, 2],
                "col_3": [3],
                "col_4": [4]
            },
            "enhanced": {
                "cols_1_2": [1, 2],
                "col_3": [3],
                "col_4": [4],
                "cols_1_2_3": [1, 2, 3],
                "cols_1_2_4": [1, 2, 4]
            },
            "comprehensive": {
                "header": [1],
                "content": [2, 3],
                "footer": [4],
                "left_side": [1, 2],
                "right_side": [3, 4],
                "full_table": [1, 2, 3, 4],
                "main_content": [2, 3, 4]
            },
            "document_structure": {
                "stt": [1],
                "ho_ten": [2],
                "dong_y": [3],
                "khong_dong_y": [4],
                "thong_tin_ca_nhan": [1, 2],
                "ket_qua_binh_chon": [3, 4],
                "toan_bo": [1, 2, 3, 4]
            },
            "custom_pairs": {
                "pair_1_2": [1, 2],
                "pair_2_3": [2, 3],
                "pair_3_4": [3, 4],
                "trio_1_2_3": [1, 2, 3],
                "trio_2_3_4": [2, 3, 4]
            }
        }
    
    def show_templates(self):
        """Hiển thị các template có sẵn"""
        templates = self.get_predefined_templates()
        
        print("🎯 CÁC TEMPLATE NHÓM CỘT CÓ SẴN:")
        print("=" * 60)
        
        for template_name, groups in templates.items():
            print(f"\n📋 Template '{template_name}':")
            for group_name, cols in groups.items():
                print(f"   - {group_name}: cột {cols}")
    
    def create_interactive(self) -> Dict[str, List[int]]:
        """Tạo nhóm cột tương tác"""
        print("🎯 TẠO NHÓM CỘT TƯƠNG TÁC")
        print("=" * 50)
        
        # Hiển thị templates
        templates = self.get_predefined_templates()
        print("📋 Các template có sẵn:")
        for i, name in enumerate(templates.keys(), 1):
            print(f"   {i}. {name}")
        print(f"   {len(templates) + 1}. Tạo từ đầu")
        
        # Chọn template
        try:
            choice = input(f"\n👉 Chọn template (1-{len(templates) + 1}): ").strip()
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(templates):
                    template_name = list(templates.keys())[choice_num - 1]
                    column_groups = templates[template_name].copy()
                    print(f"✅ Sử dụng template '{template_name}'")
                    self._show_current_groups(column_groups)
                elif choice_num == len(templates) + 1:
                    column_groups = {}
                    print("✅ Tạo từ đầu")
                else:
                    print("❌ Lựa chọn không hợp lệ, tạo từ đầu")
                    column_groups = {}
            else:
                print("❌ Lựa chọn không hợp lệ, tạo từ đầu")
                column_groups = {}
        except:
            print("❌ Lỗi input, tạo từ đầu")
            column_groups = {}
        
        # Menu chỉnh sửa
        while True:
            print(f"\n{'='*40}")
            print("🔧 TÙY CHỌN:")
            print("1. Thêm nhóm mới")
            print("2. Xóa nhóm")
            print("3. Chỉnh sửa nhóm")
            print("4. Xem nhóm hiện tại")
            print("5. Lưu cấu hình")
            print("6. Hoàn thành")
            print("0. Hủy")
            
            try:
                action = input("👉 Chọn hành động: ").strip()
                
                if action == "1":
                    self._add_group(column_groups)
                elif action == "2":
                    self._remove_group(column_groups)
                elif action == "3":
                    self._edit_group(column_groups)
                elif action == "4":
                    self._show_current_groups(column_groups)
                elif action == "5":
                    self._save_config(column_groups)
                elif action == "6":
                    break
                elif action == "0":
                    return {}
                else:
                    print("❌ Lựa chọn không hợp lệ")
                    
            except KeyboardInterrupt:
                print("\n⏹️ Hủy")
                return {}
        
        return column_groups
    
    def _add_group(self, column_groups: Dict[str, List[int]]):
        """Thêm nhóm mới"""
        try:
            name = input("📝 Tên nhóm: ").strip()
            if not name:
                print("❌ Tên nhóm không được trống")
                return
            
            if name in column_groups:
                print(f"⚠️ Nhóm '{name}' đã tồn tại")
                return
            
            cols_str = input("📝 Danh sách cột (cách nhau bởi dấu phay): ").strip()
            cols = [int(c.strip()) for c in cols_str.split(',') if c.strip().isdigit()]
            
            if not cols:
                print("❌ Không có cột hợp lệ")
                return
            
            column_groups[name] = cols
            print(f"✅ Đã thêm nhóm '{name}': cột {cols}")
            
        except ValueError:
            print("❌ Số cột không hợp lệ")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    def _remove_group(self, column_groups: Dict[str, List[int]]):
        """Xóa nhóm"""
        if not column_groups:
            print("❌ Không có nhóm nào để xóa")
            return
        
        print("📋 Các nhóm hiện có:")
        for i, name in enumerate(column_groups.keys(), 1):
            print(f"   {i}. {name}")
        
        try:
            choice = input("👉 Chọn nhóm để xóa (số): ").strip()
            if choice.isdigit():
                choice_num = int(choice)
                names = list(column_groups.keys())
                if 1 <= choice_num <= len(names):
                    name_to_remove = names[choice_num - 1]
                    del column_groups[name_to_remove]
                    print(f"✅ Đã xóa nhóm '{name_to_remove}'")
                else:
                    print("❌ Lựa chọn không hợp lệ")
            else:
                print("❌ Vui lòng nhập số")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    def _edit_group(self, column_groups: Dict[str, List[int]]):
        """Chỉnh sửa nhóm"""
        if not column_groups:
            print("❌ Không có nhóm nào để chỉnh sửa")
            return
        
        print("📋 Các nhóm hiện có:")
        for i, (name, cols) in enumerate(column_groups.items(), 1):
            print(f"   {i}. {name}: cột {cols}")
        
        try:
            choice = input("👉 Chọn nhóm để chỉnh sửa (số): ").strip()
            if choice.isdigit():
                choice_num = int(choice)
                names = list(column_groups.keys())
                if 1 <= choice_num <= len(names):
                    name_to_edit = names[choice_num - 1]
                    current_cols = column_groups[name_to_edit]
                    
                    print(f"📝 Nhóm '{name_to_edit}' hiện có: cột {current_cols}")
                    cols_str = input("📝 Danh sách cột mới (Enter để giữ nguyên): ").strip()
                    
                    if cols_str:
                        new_cols = [int(c.strip()) for c in cols_str.split(',') if c.strip().isdigit()]
                        if new_cols:
                            column_groups[name_to_edit] = new_cols
                            print(f"✅ Đã cập nhật nhóm '{name_to_edit}': cột {new_cols}")
                        else:
                            print("❌ Không có cột hợp lệ")
                    else:
                        print("📋 Giữ nguyên cấu hình")
                else:
                    print("❌ Lựa chọn không hợp lệ")
            else:
                print("❌ Vui lòng nhập số")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    def _show_current_groups(self, column_groups: Dict[str, List[int]]):
        """Hiển thị nhóm hiện tại"""
        if not column_groups:
            print("📋 Chưa có nhóm nào")
            return
        
        print("📋 CÁC NHÓM HIỆN TẠI:")
        for name, cols in column_groups.items():
            print(f"   - {name}: cột {cols}")
    
    def _save_config(self, column_groups: Dict[str, List[int]]):
        """Lưu cấu hình"""
        try:
            name = input("📝 Tên file cấu hình (không cần .json): ").strip()
            if not name:
                print("❌ Tên file không được trống")
                return
            
            filename = f"{name}.json"
            filepath = os.path.join(self.config_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(column_groups, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Đã lưu cấu hình vào: {filepath}")
            
        except Exception as e:
            print(f"❌ Lỗi lưu file: {e}")
    
    def load_config(self, filename: str) -> Dict[str, List[int]]:
        """Tải cấu hình từ file"""
        try:
            if not filename.endswith('.json'):
                filename += '.json'
            
            filepath = os.path.join(self.config_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                column_groups = json.load(f)
            
            print(f"✅ Đã tải cấu hình từ: {filepath}")
            return column_groups
            
        except FileNotFoundError:
            print(f"❌ Không tìm thấy file: {filepath}")
            return {}
        except Exception as e:
            print(f"❌ Lỗi đọc file: {e}")
            return {}
    
    def list_configs(self):
        """Liệt kê các file cấu hình có sẵn"""
        try:
            files = [f for f in os.listdir(self.config_dir) if f.endswith('.json')]
            
            if not files:
                print("📋 Không có file cấu hình nào")
                return
            
            print("📋 CÁC FILE CẤU HÌNH CÓ SẴN:")
            for i, filename in enumerate(files, 1):
                name = filename[:-5]  # Bỏ .json
                print(f"   {i}. {name}")
                
        except Exception as e:
            print(f"❌ Lỗi đọc thư mục: {e}")
    
    def generate_command_line(self, column_groups: Dict[str, List[int]]) -> str:
        """Tạo command line từ cấu hình nhóm cột"""
        if not column_groups:
            return ""
        
        groups_parts = []
        for name, cols in column_groups.items():
            cols_str = ','.join(map(str, cols))
            groups_parts.append(f"{name}:{cols_str}")
        
        groups_str = ';'.join(groups_parts)
        return f'--column-groups "{groups_str}"'

def main():
    """Hàm chính"""
    helper = ColumnGroupsHelper()
    
    while True:
        print("\n" + "="*60)
        print("🎯 COLUMN GROUPS HELPER")
        print("="*60)
        print("1. Hiển thị templates có sẵn")
        print("2. Tạo cấu hình nhóm cột tương tác")
        print("3. Tải cấu hình từ file")
        print("4. Liệt kê file cấu hình")
        print("5. Tạo command line từ cấu hình")
        print("0. Thoát")
        
        try:
            choice = input("\n👉 Chọn tùy chọn: ").strip()
            
            if choice == "1":
                helper.show_templates()
                
            elif choice == "2":
                column_groups = helper.create_interactive()
                if column_groups:
                    print("\n✅ Cấu hình nhóm cột đã tạo:")
                    for name, cols in column_groups.items():
                        print(f"   - {name}: cột {cols}")
                    
                    # Tạo command line
                    cmd = helper.generate_command_line(column_groups)
                    if cmd:
                        print(f"\n📋 Command line tương ứng:")
                        print(f"   python extract_tables_and_columns.py image.png {cmd}")
                
            elif choice == "3":
                helper.list_configs()
                filename = input("\n📝 Nhập tên file: ").strip()
                if filename:
                    column_groups = helper.load_config(filename)
                    if column_groups:
                        print("✅ Cấu hình đã tải:")
                        for name, cols in column_groups.items():
                            print(f"   - {name}: cột {cols}")
                        
                        cmd = helper.generate_command_line(column_groups)
                        if cmd:
                            print(f"\n📋 Command line:")
                            print(f"   python extract_tables_and_columns.py image.png {cmd}")
            
            elif choice == "4":
                helper.list_configs()
                
            elif choice == "5":
                print("📝 Nhập cấu hình nhóm cột:")
                print("Format: group_name:col1,col2;another_group:col3")
                groups_str = input("👉 Cấu hình: ").strip()
                
                if groups_str:
                    # Parse để validate
                    column_groups = {}
                    try:
                        groups = groups_str.split(';')
                        for group in groups:
                            if ':' in group:
                                name, cols = group.split(':', 1)
                                name = name.strip()
                                col_indices = [int(c.strip()) for c in cols.split(',') if c.strip().isdigit()]
                                if name and col_indices:
                                    column_groups[name] = col_indices
                        
                        if column_groups:
                            cmd = helper.generate_command_line(column_groups)
                            print(f"\n📋 Command line:")
                            print(f"   python extract_tables_and_columns.py image.png {cmd}")
                        else:
                            print("❌ Cấu hình không hợp lệ")
                            
                    except Exception as e:
                        print(f"❌ Lỗi parse: {e}")
                
            elif choice == "0":
                print("👋 Tạm biệt!")
                break
                
            else:
                print("❌ Lựa chọn không hợp lệ")
                
        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main() 