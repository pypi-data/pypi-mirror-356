#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT KIỂM TRA HỆ THỐNG HOÀN CHỈNH
======================================

Kiểm tra tất cả các thành phần cần thiết cho hệ thống trích xuất bảng:
- Dependencies và packages
- GPU support và CUDA
- Memory và storage
- Input/output directories  
- Configuration files
- Sample data

Cách sử dụng:
    python system_check.py
    python system_check.py --detailed
    python system_check.py --fix-issues
"""

import os
import sys
import json
import platform
import subprocess
import importlib
import logging
import argparse
from pathlib import Path
import psutil
import cv2
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemChecker:
    """Kiểm tra hệ thống hoàn chỉnh"""
    
    def __init__(self, detailed=False, fix_issues=False):
        self.detailed = detailed
        self.fix_issues = fix_issues
        self.issues = []
        self.warnings = []
        self.successes = []
        
    def print_header(self, title):
        """In header đẹp"""
        print(f"\n{'='*60}")
        print(f"🔍 {title}")
        print(f"{'='*60}")
    
    def print_status(self, message, status="info", details=None):
        """In status với màu sắc"""
        icons = {
            "success": "✅",
            "warning": "⚠️", 
            "error": "❌",
            "info": "ℹ️"
        }
        
        icon = icons.get(status, "ℹ️")
        print(f"{icon} {message}")
        
        if details and self.detailed:
            print(f"   └─ {details}")
            
        # Track issues
        if status == "error":
            self.issues.append(message)
        elif status == "warning":
            self.warnings.append(message)
        elif status == "success":
            self.successes.append(message)
    
    def check_python_version(self):
        """Kiểm tra phiên bản Python"""
        self.print_header("KIỂM TRA PYTHON")
        
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        if version.major == 3 and version.minor >= 8:
            self.print_status(f"Python {version_str}", "success")
        elif version.major == 3 and version.minor >= 6:
            self.print_status(f"Python {version_str} (khuyến nghị >= 3.8)", "warning")
        else:
            self.print_status(f"Python {version_str} không được hỗ trợ", "error")
        
        # Platform info
        self.print_status(f"Platform: {platform.system()} {platform.release()}", "info")
        self.print_status(f"Architecture: {platform.machine()}", "info")
    
    def check_dependencies(self):
        """Kiểm tra các dependencies"""
        self.print_header("KIỂM TRA DEPENDENCIES")
        
        # Core dependencies
        required_packages = {
            'cv2': 'opencv-python',
            'numpy': 'numpy', 
            'PIL': 'Pillow',
            'scipy': 'scipy',
            'skimage': 'scikit-image'
        }
        
        # Optional dependencies
        optional_packages = {
            'torch': 'torch',
            'torchvision': 'torchvision',
            'psutil': 'psutil',
            'matplotlib': 'matplotlib'
        }
        
        # Check required
        for module, package in required_packages.items():
            try:
                mod = importlib.import_module(module)
                version = getattr(mod, '__version__', 'unknown')
                self.print_status(f"{package}: {version}", "success")
            except ImportError:
                self.print_status(f"{package}: Chưa cài đặt", "error")
                if self.fix_issues:
                    self._install_package(package)
        
        # Check optional  
        for module, package in optional_packages.items():
            try:
                mod = importlib.import_module(module)
                version = getattr(mod, '__version__', 'unknown')
                self.print_status(f"{package}: {version}", "success")
            except ImportError:
                self.print_status(f"{package}: Không có (tùy chọn)", "warning")
    
    def check_gpu_support(self):
        """Kiểm tra GPU support"""
        self.print_header("KIỂM TRA GPU SUPPORT")
        
        # Check CUDA
        try:
            result = subprocess.run(['nvidia-smi'], 
                                   capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Driver Version' in line:
                        driver_info = line.strip()
                        self.print_status(f"NVIDIA GPU detected: {driver_info}", "success")
                        break
            else:
                self.print_status("nvidia-smi không khả dụng", "warning")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.print_status("NVIDIA GPU không phát hiện", "warning")
        
        # Check PyTorch CUDA
        try:
            import torch
            if torch.cuda.is_available():
                device_count = torch.cuda.device_count()
                current_device = torch.cuda.current_device()
                device_name = torch.cuda.get_device_name(current_device)
                
                self.print_status(f"PyTorch CUDA: Có ({device_count} GPU)", "success")
                self.print_status(f"Current GPU: {device_name}", "info")
                
                # Memory info
                memory_info = torch.cuda.get_device_properties(current_device)
                memory_gb = memory_info.total_memory / (1024**3)
                self.print_status(f"GPU Memory: {memory_gb:.1f}GB", "info")
                
            else:
                self.print_status("PyTorch CUDA: Không khả dụng", "warning")
        except ImportError:
            self.print_status("PyTorch: Chưa cài đặt", "warning")
    
    def check_memory_storage(self):
        """Kiểm tra memory và storage"""
        self.print_header("KIỂM TRA MEMORY & STORAGE")
        
        # System memory
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        used_percent = memory.percent
        
        if memory_gb >= 8:
            self.print_status(f"RAM: {memory_gb:.1f}GB (sử dụng {used_percent:.1f}%)", "success")
        elif memory_gb >= 4:
            self.print_status(f"RAM: {memory_gb:.1f}GB (khuyến nghị ≥8GB)", "warning")
        else:
            self.print_status(f"RAM: {memory_gb:.1f}GB (không đủ)", "error")
        
        # Disk space
        disk = psutil.disk_usage('.')
        disk_free_gb = disk.free / (1024**3)
        
        if disk_free_gb >= 5:
            self.print_status(f"Disk free: {disk_free_gb:.1f}GB", "success")
        elif disk_free_gb >= 1:
            self.print_status(f"Disk free: {disk_free_gb:.1f}GB (khuyến nghị ≥5GB)", "warning")
        else:
            self.print_status(f"Disk free: {disk_free_gb:.1f}GB (không đủ)", "error")
        
        # CPU info
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        self.print_status(f"CPU: {cpu_count} cores (sử dụng {cpu_percent:.1f}%)", "info")
    
    def check_directories(self):
        """Kiểm tra cấu trúc thư mục"""
        self.print_header("KIỂM TRA THU MỤC")
        
        required_dirs = [
            'input',
            'output', 
            'debug',
            'detect_row'
        ]
        
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                self.print_status(f"Thư mục {dir_name}/", "success")
            else:
                self.print_status(f"Thư mục {dir_name}/ không tồn tại", "warning")
                if self.fix_issues:
                    os.makedirs(dir_name, exist_ok=True)
                    self.print_status(f"Đã tạo thư mục {dir_name}/", "success")
        
        # Check permissions
        for dir_name in ['input', 'output', 'debug']:
            if os.path.exists(dir_name):
                if os.access(dir_name, os.W_OK):
                    self.print_status(f"Quyền ghi {dir_name}/", "success")
                else:
                    self.print_status(f"Không có quyền ghi {dir_name}/", "error")
    
    def check_config_files(self):
        """Kiểm tra config files"""
        self.print_header("KIỂM TRA CONFIG FILES")
        
        config_files = [
            'config_template.json',
            'requirements.txt',
            'setup.py'
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    if config_file.endswith('.json'):
                        with open(config_file, 'r') as f:
                            json.load(f)
                    self.print_status(f"Config {config_file}", "success")
                except json.JSONDecodeError:
                    self.print_status(f"Config {config_file} (JSON không hợp lệ)", "error")
                except Exception as e:
                    self.print_status(f"Config {config_file} (lỗi: {e})", "error")
            else:
                self.print_status(f"Config {config_file} không tồn tại", "warning")
    
    def check_sample_data(self):
        """Kiểm tra sample data"""
        self.print_header("KIỂM TRA SAMPLE DATA")
        
        input_dir = Path('input')
        if input_dir.exists():
            image_files = list(input_dir.glob('*.jpg')) + \
                         list(input_dir.glob('*.png')) + \
                         list(input_dir.glob('*.jpeg'))
            
            if image_files:
                self.print_status(f"Tìm thấy {len(image_files)} ảnh mẫu", "success")
                
                # Check first image
                first_image = image_files[0]
                try:
                    img = cv2.imread(str(first_image))
                    if img is not None:
                        h, w = img.shape[:2]
                        self.print_status(f"Ảnh mẫu: {first_image.name} ({w}x{h})", "info")
                    else:
                        self.print_status(f"Không thể đọc ảnh {first_image.name}", "error")
                except Exception as e:
                    self.print_status(f"Lỗi đọc ảnh: {e}", "error")
            else:
                self.print_status("Không có ảnh mẫu trong input/", "warning")
                if self.fix_issues:
                    self._create_sample_image()
        else:
            self.print_status("Thư mục input/ không tồn tại", "error")
    
    def check_core_modules(self):
        """Kiểm tra core modules của package"""
        self.print_header("KIỂM TRA CORE MODULES")
        
        core_modules = [
            'detect_row/__init__.py',
            'detect_row/base.py',
            'detect_row/advanced_table_extractor.py',
            'detect_row/advanced_row_extractor.py', 
            'detect_row/advanced_column_extractor.py',
            'detect_row/gpu_support.py'
        ]
        
        for module_path in core_modules:
            if os.path.exists(module_path):
                try:
                    with open(module_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if len(content) > 100:  # Basic check
                            self.print_status(f"Module {module_path}", "success")
                        else:
                            self.print_status(f"Module {module_path} (quá ngắn)", "warning")
                except Exception as e:
                    self.print_status(f"Module {module_path} (lỗi: {e})", "error")
            else:
                self.print_status(f"Module {module_path} không tồn tại", "error")
    
    def test_basic_functionality(self):
        """Test chức năng cơ bản"""
        self.print_header("TEST CHỨC NĂNG CƠ BẢN")
        
        try:
            # Test import package
            sys.path.insert(0, '.')
            from detect_row import AdvancedTableExtractor
            self.print_status("Import AdvancedTableExtractor", "success")
            
            # Test tạo instance
            extractor = AdvancedTableExtractor(
                input_dir="input",
                output_dir="output/test",
                debug_dir="debug/test"
            )
            self.print_status("Tạo TableExtractor instance", "success")
            
        except ImportError as e:
            self.print_status(f"Lỗi import: {e}", "error")
        except Exception as e:
            self.print_status(f"Lỗi test: {e}", "error")
    
    def _install_package(self, package):
        """Cài đặt package"""
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                          check=True, capture_output=True)
            self.print_status(f"Đã cài đặt {package}", "success")
        except subprocess.CalledProcessError:
            self.print_status(f"Lỗi cài đặt {package}", "error")
    
    def _create_sample_image(self):
        """Tạo ảnh mẫu"""
        try:
            # Tạo ảnh trắng đơn giản với text
            img = np.ones((600, 800, 3), dtype=np.uint8) * 255
            cv2.putText(img, 'Sample Table Image', (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            # Vẽ khung bảng đơn giản
            cv2.rectangle(img, (50, 100), (750, 400), (0, 0, 0), 2)
            cv2.line(img, (50, 200), (750, 200), (0, 0, 0), 1)
            cv2.line(img, (250, 100), (250, 400), (0, 0, 0), 1)
            cv2.line(img, (500, 100), (500, 400), (0, 0, 0), 1)
            
            # Save
            cv2.imwrite('input/sample_table.jpg', img)
            self.print_status("Đã tạo ảnh mẫu sample_table.jpg", "success")
            
        except Exception as e:
            self.print_status(f"Lỗi tạo ảnh mẫu: {e}", "error")
    
    def print_summary(self):
        """In tóm tắt kết quả"""
        self.print_header("TÓM TẮT KẾT QUẢ")
        
        print(f"✅ Thành công: {len(self.successes)}")
        print(f"⚠️  Cảnh báo: {len(self.warnings)}") 
        print(f"❌ Lỗi: {len(self.issues)}")
        
        if self.issues:
            print(f"\n🚨 CÁC VẤN ĐỀ CẦN SỬA:")
            for issue in self.issues:
                print(f"   • {issue}")
        
        if self.warnings:
            print(f"\n⚠️  CÁC CẢNH BÁO:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        # Đánh giá tổng thể
        if not self.issues:
            if not self.warnings:
                print(f"\n🎉 HỆ THỐNG HOÀN HẢO! Sẵn sàng sử dụng.")
            else:
                print(f"\n✅ HỆ THỐNG OK! Có một số cảnh báo nhỏ.")
        else:
            print(f"\n🔧 HỆ THỐNG CẦN SỬA! Vui lòng xử lý các lỗi trên.")
    
    def run_full_check(self):
        """Chạy kiểm tra toàn bộ"""
        print("🚀 KIỂM TRA HỆ THỐNG TRÍCH XUẤT BẢNG")
        print("=" * 60)
        
        self.check_python_version()
        self.check_dependencies()
        self.check_gpu_support()
        self.check_memory_storage()
        self.check_directories()
        self.check_config_files()
        self.check_sample_data()
        self.check_core_modules()
        self.test_basic_functionality()
        
        self.print_summary()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Kiểm tra hệ thống trích xuất bảng')
    parser.add_argument('--detailed', action='store_true', 
                       help='Hiển thị thông tin chi tiết')
    parser.add_argument('--fix-issues', action='store_true',
                       help='Tự động sửa một số vấn đề')
    
    args = parser.parse_args()
    
    checker = SystemChecker(detailed=args.detailed, fix_issues=args.fix_issues)
    checker.run_full_check()

if __name__ == "__main__":
    main() 