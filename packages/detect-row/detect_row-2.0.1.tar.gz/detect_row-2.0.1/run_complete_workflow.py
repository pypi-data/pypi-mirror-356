#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WORKFLOW TỰ ĐỘNG HOÀN CHỈNH - TRÍCH XUẤT BẢNG
==============================================

Script tự động chạy toàn bộ quy trình:
1. Kiểm tra hệ thống và GPU
2. Tối ưu cấu hình theo hardware
3. Trích xuất bảng từ tất cả ảnh
4. Trích xuất cột với merge tùy chỉnh
5. Quản lý bộ nhớ hiệu quả
6. Tạo báo cáo kết quả

Cách sử dụng:
    python run_complete_workflow.py
    python run_complete_workflow.py --config config_template.json
    python run_complete_workflow.py --column-groups "custom:1,2;result:3,4"
    python run_complete_workflow.py --max-memory 8 --use-gpu
"""

import os
import sys
import json
import time
import argparse
import logging
import traceback
from pathlib import Path
from datetime import datetime
import cv2
import numpy as np
import psutil
import gc

# Add current directory to path
sys.path.insert(0, '.')

try:
    from detect_row import AdvancedTableExtractor, AdvancedColumnExtractor
    from detect_row.gpu_support import GPUManager, MemoryManager
except ImportError as e:
    print(f"❌ Lỗi import: {e}")
    print("Vui lòng kiểm tra cài đặt package detect_row")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workflow.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WorkflowManager:
    """Quản lý workflow tự động"""
    
    def __init__(self, config_file=None, max_memory_gb=4, use_gpu=True):
        self.config_file = config_file
        self.max_memory_gb = max_memory_gb
        self.use_gpu = use_gpu
        self.start_time = time.time()
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize managers
        self.gpu_manager = GPUManager()
        self.memory_manager = MemoryManager(max_memory_gb=max_memory_gb)
        
        # Setup directories
        self.setup_directories()
        
        # Results tracking
        self.results = {
            'processed_images': 0,
            'detected_tables': 0,
            'extracted_columns': 0,
            'errors': [],
            'processing_times': []
        }
    
    def load_config(self):
        """Load cấu hình từ file"""
        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"✅ Đã load config từ {self.config_file}")
                return config
            except Exception as e:
                logger.warning(f"⚠️ Lỗi load config: {e}, sử dụng config mặc định")
        
        # Default config
        return {
            "table_extraction": {
                "min_area_ratio": 0.003,
                "max_area_ratio": 0.25,
                "min_aspect_ratio": 1.0,
                "max_aspect_ratio": 15.0
            },
            "column_extraction": {
                "min_column_width": 20,
                "vertical_line_threshold": 0.4
            },
            "performance": {
                "batch_size": 8,
                "num_workers": 4
            }
        }
    
    def setup_directories(self):
        """Thiết lập thư mục"""
        directories = [
            'input',
            'output/tables_and_columns/tables',
            'output/tables_and_columns/columns', 
            'debug/tables_and_columns',
            'reports'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        logger.info("✅ Đã thiết lập thư mục")
    
    def check_system_status(self):
        """Kiểm tra trạng thái hệ thống"""
        logger.info("🔍 Kiểm tra hệ thống...")
        
        # Memory check
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        
        logger.info(f"💾 RAM: {memory_gb:.1f}GB (sử dụng {memory.percent:.1f}%)")
        
        # GPU check
        if self.use_gpu and self.gpu_manager.is_gpu_available():
            gpu_info = self.gpu_manager.get_gpu_info()
            logger.info(f"🎮 GPU: {gpu_info}")
        else:
            logger.info("🖥️ Sử dụng CPU")
        
        # Disk space
        disk = psutil.disk_usage('.')
        disk_free_gb = disk.free / (1024**3)
        logger.info(f"💿 Disk free: {disk_free_gb:.1f}GB")
        
        # Warning checks
        if memory.percent > 80:
            logger.warning("⚠️ RAM sử dụng cao!")
        if disk_free_gb < 1:
            logger.warning("⚠️ Disk space thấp!")
    
    def find_input_images(self):
        """Tìm ảnh đầu vào"""
        input_dir = Path('input')
        
        if not input_dir.exists():
            logger.error("❌ Thư mục input/ không tồn tại")
            return []
        
        # Supported formats
        formats = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
        
        images = []
        for fmt in formats:
            images.extend(input_dir.glob(fmt))
            images.extend(input_dir.glob(fmt.upper()))
        
        logger.info(f"📁 Tìm thấy {len(images)} ảnh trong input/")
        return sorted(images)
    
    def optimize_batch_size(self, images):
        """Tối ưu batch size theo memory"""
        if not images:
            return 1
        
        # Estimate memory per image
        sample_image = cv2.imread(str(images[0]))
        if sample_image is None:
            return 1
        
        # Estimate memory usage (rough calculation)
        image_size_mb = sample_image.nbytes / (1024 * 1024)
        available_memory_gb = psutil.virtual_memory().available / (1024**3)
        
        # Conservative estimate: use 50% of available memory
        usable_memory_gb = min(available_memory_gb * 0.5, self.max_memory_gb)
        
        optimal_batch_size = max(1, int((usable_memory_gb * 1024) / (image_size_mb * 3)))  # 3x safety factor
        
        # Limit to reasonable range
        optimal_batch_size = min(optimal_batch_size, 16)
        optimal_batch_size = max(optimal_batch_size, 1)
        
        logger.info(f"⚙️ Batch size tối ưu: {optimal_batch_size}")
        return optimal_batch_size
    
    def process_image_batch(self, image_batch, column_groups=None):
        """Xử lý một batch ảnh"""
        batch_results = []
        
        for image_path in image_batch:
            try:
                start_time = time.time()
                
                logger.info(f"🔄 Xử lý: {image_path.name}")
                
                # 1. Table extraction
                table_extractor = AdvancedTableExtractor(
                    input_dir=str(image_path.parent),
                    output_dir="output/tables_and_columns/tables",
                    debug_dir="debug/tables_and_columns"
                )
                
                tables = table_extractor.extract_tables_from_image(image_path.name)
                
                if not tables:
                    logger.warning(f"⚠️ Không phát hiện bảng trong {image_path.name}")
                    continue
                
                logger.info(f"✅ Phát hiện {len(tables)} bảng")
                self.results['detected_tables'] += len(tables)
                
                # 2. Column extraction cho mỗi bảng
                for i, table_info in enumerate(tables):
                    table_name = f"{image_path.stem}_table_{i}"
                    
                    # Column extraction
                    column_extractor = AdvancedColumnExtractor(
                        input_dir="output/tables_and_columns/tables",
                        output_dir=f"output/tables_and_columns/columns/{table_name}",
                        debug_dir=f"debug/tables_and_columns/columns/{table_name}"
                    )
                    
                    table_image_name = f"{table_name}.jpg"
                    columns = column_extractor.extract_columns_from_image(
                        table_image_name, 
                        column_groups=column_groups
                    )
                    
                    if columns:
                        logger.info(f"✅ Trích xuất {len(columns)} cột từ {table_name}")
                        self.results['extracted_columns'] += len(columns)
                
                # Track processing time
                processing_time = time.time() - start_time
                self.results['processing_times'].append(processing_time)
                
                logger.info(f"⏱️ Hoàn thành {image_path.name} trong {processing_time:.2f}s")
                
                batch_results.append({
                    'image': image_path.name,
                    'tables': len(tables),
                    'processing_time': processing_time
                })
                
                self.results['processed_images'] += 1
                
            except Exception as e:
                error_msg = f"Lỗi xử lý {image_path.name}: {e}"
                logger.error(f"❌ {error_msg}")
                self.results['errors'].append(error_msg)
                
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(traceback.format_exc())
        
        return batch_results
    
    def process_all_images(self, images, column_groups=None):
        """Xử lý tất cả ảnh theo batch"""
        if not images:
            logger.warning("⚠️ Không có ảnh để xử lý")
            return []
        
        # Optimize batch size
        batch_size = self.optimize_batch_size(images)
        
        all_results = []
        total_batches = (len(images) + batch_size - 1) // batch_size
        
        logger.info(f"🚀 Bắt đầu xử lý {len(images)} ảnh trong {total_batches} batch")
        
        for batch_idx in range(0, len(images), batch_size):
            batch_num = (batch_idx // batch_size) + 1
            
            logger.info(f"📦 Batch {batch_num}/{total_batches}")
            
            # Get batch
            batch = images[batch_idx:batch_idx + batch_size]
            
            # Monitor memory before processing
            memory_before = psutil.virtual_memory().percent
            
            # Process batch
            batch_results = self.process_image_batch(batch, column_groups)
            all_results.extend(batch_results)
            
            # Memory management
            memory_after = psutil.virtual_memory().percent
            logger.info(f"💾 Memory: {memory_before:.1f}% → {memory_after:.1f}%")
            
            if memory_after > 85:
                logger.warning("⚠️ Memory cao, chạy garbage collection...")
                gc.collect()
                
                if self.gpu_manager.is_gpu_available():
                    try:
                        import torch
                        torch.cuda.empty_cache()
                        logger.info("🗑️ Đã dọn cache GPU")
                    except:
                        pass
            
            # Progress report
            processed = min(batch_idx + batch_size, len(images))
            progress = (processed / len(images)) * 100
            logger.info(f"📊 Tiến độ: {progress:.1f}% ({processed}/{len(images)})")
        
        return all_results
    
    def generate_report(self, processing_results):
        """Tạo báo cáo chi tiết"""
        report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"reports/workflow_report_{report_time}.json"
        
        # Calculate statistics
        total_time = time.time() - self.start_time
        avg_time_per_image = (
            sum(self.results['processing_times']) / len(self.results['processing_times'])
            if self.results['processing_times'] else 0
        )
        
        # Create detailed report
        report = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_runtime": f"{total_time:.2f}s",
                "config_file": self.config_file,
                "max_memory_gb": self.max_memory_gb,
                "use_gpu": self.use_gpu
            },
            "system_info": {
                "platform": os.name,
                "cpu_count": psutil.cpu_count(),
                "total_memory_gb": psutil.virtual_memory().total / (1024**3),
                "gpu_available": self.gpu_manager.is_gpu_available(),
                "gpu_info": self.gpu_manager.get_gpu_info() if self.gpu_manager.is_gpu_available() else None
            },
            "processing_summary": {
                "total_images_processed": self.results['processed_images'],
                "total_tables_detected": self.results['detected_tables'],
                "total_columns_extracted": self.results['extracted_columns'],
                "total_errors": len(self.results['errors']),
                "avg_time_per_image": f"{avg_time_per_image:.2f}s",
                "success_rate": f"{(self.results['processed_images'] / (self.results['processed_images'] + len(self.results['errors'])) * 100):.1f}%" if (self.results['processed_images'] + len(self.results['errors'])) > 0 else "0.0%"
            },
            "detailed_results": processing_results,
            "errors": self.results['errors'],
            "performance_metrics": {
                "processing_times": self.results['processing_times'],
                "memory_usage": self.memory_manager.get_usage_history() if hasattr(self.memory_manager, 'get_usage_history') else []
            }
        }
        
        # Save report
        os.makedirs('reports', exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📋 Báo cáo đã lưu: {report_file}")
        
        # Print summary
        self.print_summary(report)
        
        return report_file
    
    def print_summary(self, report):
        """In tóm tắt kết quả"""
        print("\n" + "="*60)
        print("📊 TÓM TẮT KẾT QUẢ WORKFLOW")
        print("="*60)
        
        summary = report['processing_summary']
        metadata = report['metadata']
        
        print(f"⏱️  Thời gian chạy: {metadata['total_runtime']}")
        print(f"📸 Ảnh đã xử lý: {summary['total_images_processed']}")
        print(f"📋 Bảng phát hiện: {summary['total_tables_detected']}")
        print(f"📊 Cột trích xuất: {summary['total_columns_extracted']}")
        print(f"❌ Lỗi: {summary['total_errors']}")
        print(f"✅ Tỉ lệ thành công: {summary['success_rate']}")
        print(f"⚡ Thời gian TB/ảnh: {summary['avg_time_per_image']}")
        
        if self.results['errors']:
            print(f"\n🚨 CÁC LỖI:")
            for error in self.results['errors'][:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(self.results['errors']) > 5:
                print(f"   ... và {len(self.results['errors']) - 5} lỗi khác")
        
        # File structure
        print(f"\n📁 KẾT QUẢ TRONG:")
        print(f"   📋 Bảng: output/tables_and_columns/tables/")
        print(f"   📊 Cột: output/tables_and_columns/columns/")
        print(f"   🐛 Debug: debug/tables_and_columns/")
        print(f"   📋 Báo cáo: reports/")
        
        print("="*60)
    
    def run_complete_workflow(self, column_groups=None):
        """Chạy workflow hoàn chỉnh"""
        try:
            logger.info("🚀 BẮT ĐẦU WORKFLOW TỰ ĐỘNG")
            
            # 1. System check
            self.check_system_status()
            
            # 2. Find images
            images = self.find_input_images()
            if not images:
                logger.error("❌ Không có ảnh để xử lý!")
                return None
            
            # 3. Process all images
            processing_results = self.process_all_images(images, column_groups)
            
            # 4. Generate report
            report_file = self.generate_report(processing_results)
            
            logger.info("🎉 WORKFLOW HOÀN THÀNH!")
            return report_file
            
        except KeyboardInterrupt:
            logger.info("⏹️ Workflow bị dừng bởi người dùng")
            return None
        except Exception as e:
            logger.error(f"💥 Lỗi nghiêm trọng: {e}")
            logger.debug(traceback.format_exc())
            return None

def parse_column_groups(groups_str):
    """Parse column groups từ string"""
    if not groups_str:
        return None
    
    groups = {}
    for group_def in groups_str.split(';'):
        if ':' in group_def:
            name, cols = group_def.split(':', 1)
            col_list = [int(c.strip()) for c in cols.split(',')]
            groups[name.strip()] = col_list
    
    return groups

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Workflow tự động trích xuất bảng',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python run_complete_workflow.py
  python run_complete_workflow.py --config config_template.json
  python run_complete_workflow.py --column-groups "header:1;content:2,3;footer:4"
  python run_complete_workflow.py --max-memory 8 --use-gpu
  python run_complete_workflow.py --no-gpu --max-memory 2
        """
    )
    
    parser.add_argument('--config', 
                       help='File cấu hình JSON')
    parser.add_argument('--column-groups',
                       help='Định nghĩa nhóm cột (format: name:1,2;name2:3)')
    parser.add_argument('--max-memory', type=float, default=4,
                       help='Giới hạn memory (GB), mặc định: 4')
    parser.add_argument('--use-gpu', action='store_true', default=True,
                       help='Sử dụng GPU (mặc định)')
    parser.add_argument('--no-gpu', action='store_true',
                       help='Không sử dụng GPU')
    parser.add_argument('--verbose', action='store_true',
                       help='Hiển thị log chi tiết')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Parse column groups
    column_groups = parse_column_groups(args.column_groups)
    
    # Determine GPU usage
    use_gpu = args.use_gpu and not args.no_gpu
    
    # Create and run workflow
    workflow = WorkflowManager(
        config_file=args.config,
        max_memory_gb=args.max_memory,
        use_gpu=use_gpu
    )
    
    if column_groups:
        logger.info(f"📊 Sử dụng nhóm cột: {column_groups}")
    
    report_file = workflow.run_complete_workflow(column_groups)
    
    if report_file:
        print(f"\n📋 Báo cáo chi tiết: {report_file}")
    else:
        print("\n❌ Workflow không hoàn thành")
        sys.exit(1)

if __name__ == "__main__":
    main() 