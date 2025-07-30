#!/bin/bash
# =============================================================================
# AUTO WORKFLOW - HỆ THỐNG TRÍCH XUẤT BẢNG TỰ ĐỘNG
# =============================================================================
# 
# Script tự động hoàn chỉnh cho hệ thống trích xuất bảng:
# - Kiểm tra hệ thống và dependencies
# - Tối ưu cấu hình theo hardware
# - Chạy workflow với quản lý memory
# - Tạo báo cáo chi tiết
#
# Cách sử dụng:
#   chmod +x auto_workflow.sh
#   ./auto_workflow.sh
#   ./auto_workflow.sh --gpu --max-memory 8
#   ./auto_workflow.sh --config custom_config.json
#   ./auto_workflow.sh --column-groups "header:1;content:2,3;footer:4"
#
# =============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default settings
USE_GPU="auto"
MAX_MEMORY="4"
CONFIG_FILE=""
COLUMN_GROUPS=""
VERBOSE=false
CHECK_ONLY=false
CLEAN_BEFORE=false

# Function definitions
print_header() {
    echo -e "\n${BLUE}================================================================${NC}"
    echo -e "${BLUE}🚀 $1${NC}"
    echo -e "${BLUE}================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --gpu)
            USE_GPU="true"
            shift
            ;;
        --no-gpu)
            USE_GPU="false"
            shift
            ;;
        --max-memory)
            MAX_MEMORY="$2"
            shift 2
            ;;
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --column-groups)
            COLUMN_GROUPS="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --check-only)
            CHECK_ONLY=true
            shift
            ;;
        --clean)
            CLEAN_BEFORE=true
            shift
            ;;
        --help)
            echo "Cách sử dụng: $0 [OPTIONS]"
            echo ""
            echo "OPTIONS:"
            echo "  --gpu               Bắt buộc sử dụng GPU"
            echo "  --no-gpu            Không sử dụng GPU"
            echo "  --max-memory GB     Giới hạn memory (mặc định: 4GB)"
            echo "  --config FILE       File cấu hình JSON"
            echo "  --column-groups STR Định nghĩa nhóm cột"
            echo "  --verbose           Hiển thị log chi tiết"
            echo "  --check-only        Chỉ kiểm tra hệ thống"
            echo "  --clean             Dọn dẹp output trước khi chạy"
            echo "  --help              Hiển thị help này"
            echo ""
            echo "Ví dụ:"
            echo "  $0 --gpu --max-memory 8"
            echo "  $0 --config config_template.json"
            echo "  $0 --column-groups \"header:1;content:2,3;footer:4\""
            exit 0
            ;;
        *)
            print_error "Tham số không hợp lệ: $1"
            echo "Sử dụng --help để xem hướng dẫn"
            exit 1
            ;;
    esac
done

# System information
print_header "KIỂM TRA HỆ THỐNG"

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_success "Hệ điều hành: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    print_success "Hệ điều hành: macOS"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    print_success "Hệ điều hành: Windows"
else
    print_warning "Hệ điều hành không xác định: $OSTYPE"
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version | cut -d' ' -f2)
    print_success "Python: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    print_error "Python không được cài đặt!"
    exit 1
fi

# Check if we're in the right directory
if [[ ! -f "detect_row/__init__.py" ]]; then
    print_error "Vui lòng chạy script từ thư mục gốc của project!"
    exit 1
fi

# System check
print_info "Chạy kiểm tra hệ thống chi tiết..."
if [[ -f "system_check.py" ]]; then
    if $VERBOSE; then
        $PYTHON_CMD system_check.py --detailed
    else
        $PYTHON_CMD system_check.py
    fi
    
    if [[ $? -ne 0 ]]; then
        print_error "Kiểm tra hệ thống thất bại!"
        exit 1
    fi
else
    print_warning "File system_check.py không tồn tại, bỏ qua kiểm tra chi tiết"
fi

# Exit if check-only mode
if $CHECK_ONLY; then
    print_success "Kiểm tra hệ thống hoàn thành!"
    exit 0
fi

# Clean previous output if requested
if $CLEAN_BEFORE; then
    print_header "DỌN DẸP OUTPUT CŨ"
    
    if [[ -d "output" ]]; then
        rm -rf output/*
        print_success "Đã dọn dẹp thư mục output/"
    fi
    
    if [[ -d "debug" ]]; then
        rm -rf debug/*
        print_success "Đã dọn dẹp thư mục debug/"
    fi
    
    if [[ -d "reports" ]]; then
        rm -rf reports/*
        print_success "Đã dọn dẹp thư mục reports/"
    fi
fi

# Check input directory
print_header "KIỂM TRA ẢNH ĐẦU VÀO"

if [[ ! -d "input" ]]; then
    print_error "Thư mục input/ không tồn tại!"
    print_info "Tạo thư mục input/ và đặt ảnh vào đó"
    mkdir -p input
    exit 1
fi

# Count images
IMAGE_COUNT=$(find input/ -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.bmp" -o -iname "*.tiff" -o -iname "*.tif" \) | wc -l)

if [[ $IMAGE_COUNT -eq 0 ]]; then
    print_error "Không có ảnh trong thư mục input/!"
    print_info "Vui lòng đặt ảnh (.jpg, .png, .tiff, ...) vào thư mục input/"
    exit 1
else
    print_success "Tìm thấy $IMAGE_COUNT ảnh trong input/"
fi

# Check GPU setup
print_header "KIỂM TRA GPU"

GPU_AVAILABLE=false
if command -v nvidia-smi &> /dev/null; then
    if nvidia-smi &> /dev/null; then
        GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -1)
        print_success "GPU: $GPU_INFO"
        GPU_AVAILABLE=true
    else
        print_warning "nvidia-smi có lỗi"
    fi
else
    print_warning "nvidia-smi không có sẵn"
fi

# Determine final GPU setting
if [[ "$USE_GPU" == "auto" ]]; then
    if $GPU_AVAILABLE; then
        USE_GPU="true"
        print_info "Tự động bật GPU"
    else
        USE_GPU="false"
        print_info "Tự động tắt GPU (không có GPU)"
    fi
elif [[ "$USE_GPU" == "true" ]] && ! $GPU_AVAILABLE; then
    print_warning "Yêu cầu GPU nhưng không có GPU, chuyển sang CPU"
    USE_GPU="false"
fi

# Memory check
print_header "KIỂM TRA MEMORY"

if command -v free &> /dev/null; then
    TOTAL_MEM_KB=$(free | awk 'NR==2{print $2}')
    TOTAL_MEM_GB=$((TOTAL_MEM_KB / 1024 / 1024))
    USED_MEM_KB=$(free | awk 'NR==2{print $3}')
    USED_PERCENT=$((USED_MEM_KB * 100 / TOTAL_MEM_KB))
    
    print_success "RAM: ${TOTAL_MEM_GB}GB (sử dụng ${USED_PERCENT}%)"
    
    if [[ $USED_PERCENT -gt 80 ]]; then
        print_warning "Memory sử dụng cao! Có thể cần giảm --max-memory"
    fi
    
    if [[ $TOTAL_MEM_GB -lt 4 ]]; then
        print_warning "RAM thấp (<4GB), khuyến nghị --max-memory 2"
        if [[ "$MAX_MEMORY" == "4" ]]; then
            MAX_MEMORY="2"
            print_info "Tự động giảm max-memory xuống 2GB"
        fi
    fi
else
    print_warning "Không thể kiểm tra memory (lệnh 'free' không có)"
fi

# Build command
print_header "CHUẨN BỊ CHẠY WORKFLOW"

CMD="$PYTHON_CMD run_complete_workflow.py"

# Add GPU setting
if [[ "$USE_GPU" == "true" ]]; then
    CMD="$CMD --use-gpu"
    print_info "Sử dụng GPU"
else
    CMD="$CMD --no-gpu"
    print_info "Sử dụng CPU"
fi

# Add memory setting
CMD="$CMD --max-memory $MAX_MEMORY"
print_info "Giới hạn memory: ${MAX_MEMORY}GB"

# Add config file
if [[ -n "$CONFIG_FILE" ]]; then
    if [[ -f "$CONFIG_FILE" ]]; then
        CMD="$CMD --config $CONFIG_FILE"
        print_info "Sử dụng config: $CONFIG_FILE"
    else
        print_error "File config không tồn tại: $CONFIG_FILE"
        exit 1
    fi
fi

# Add column groups
if [[ -n "$COLUMN_GROUPS" ]]; then
    CMD="$CMD --column-groups \"$COLUMN_GROUPS\""
    print_info "Nhóm cột: $COLUMN_GROUPS"
fi

# Add verbose
if $VERBOSE; then
    CMD="$CMD --verbose"
    print_info "Chế độ verbose bật"
fi

print_success "Lệnh sẽ chạy: $CMD"

# Create necessary directories
mkdir -p output/tables_and_columns/tables
mkdir -p output/tables_and_columns/columns
mkdir -p debug/tables_and_columns
mkdir -p reports

# Run the workflow
print_header "CHẠY WORKFLOW"

START_TIME=$(date +%s)

print_info "Bắt đầu lúc: $(date)"
print_info "Số ảnh xử lý: $IMAGE_COUNT"

# Execute the command
eval $CMD
WORKFLOW_EXIT_CODE=$?

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Results
print_header "KẾT QUẢ"

if [[ $WORKFLOW_EXIT_CODE -eq 0 ]]; then
    print_success "Workflow hoàn thành thành công!"
else
    print_error "Workflow có lỗi (exit code: $WORKFLOW_EXIT_CODE)"
fi

print_info "Thời gian chạy: ${DURATION}s"
print_info "Kết thúc lúc: $(date)"

# Show output structure
if [[ -d "output/tables_and_columns" ]]; then
    print_info "Cấu trúc kết quả:"
    
    # Count tables
    TABLE_COUNT=$(find output/tables_and_columns/tables/ -name "*.jpg" 2>/dev/null | wc -l)
    print_info "  📋 Bảng: $TABLE_COUNT files trong output/tables_and_columns/tables/"
    
    # Count column directories
    COLUMN_DIRS=$(find output/tables_and_columns/columns/ -type d -mindepth 1 2>/dev/null | wc -l)
    if [[ $COLUMN_DIRS -gt 0 ]]; then
        print_info "  📊 Cột: $COLUMN_DIRS thư mục trong output/tables_and_columns/columns/"
    fi
    
    # Count debug files
    DEBUG_COUNT=$(find debug/tables_and_columns/ -name "*.jpg" 2>/dev/null | wc -l)
    if [[ $DEBUG_COUNT -gt 0 ]]; then
        print_info "  🐛 Debug: $DEBUG_COUNT files trong debug/tables_and_columns/"
    fi
    
    # Show reports
    REPORT_COUNT=$(find reports/ -name "*.json" 2>/dev/null | wc -l)
    if [[ $REPORT_COUNT -gt 0 ]]; then
        LATEST_REPORT=$(find reports/ -name "*.json" -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
        if [[ -n "$LATEST_REPORT" ]]; then
            print_info "  📋 Báo cáo mới nhất: $LATEST_REPORT"
        fi
    fi
fi

# Final recommendations
print_header "KHUYẾN NGHỊ"

if [[ $WORKFLOW_EXIT_CODE -eq 0 ]]; then
    print_success "Workflow thành công! Bạn có thể:"
    echo "  1. Kiểm tra kết quả trong output/tables_and_columns/"
    echo "  2. Xem debug files trong debug/tables_and_columns/"
    echo "  3. Đọc báo cáo chi tiết trong reports/"
    echo "  4. Chạy lại với cấu hình khác nếu cần"
else
    print_warning "Workflow có vấn đề! Bạn nên:"
    echo "  1. Kiểm tra log errors ở trên"
    echo "  2. Chạy system_check.py để kiểm tra hệ thống"
    echo "  3. Thử với --verbose để xem chi tiết"
    echo "  4. Giảm --max-memory nếu bị out of memory"
    echo "  5. Thử --no-gpu nếu có vấn đề với GPU"
fi

# Performance tips
if [[ $DURATION -gt 300 ]]; then  # > 5 minutes
    print_info "Tips để tăng tốc:"
    echo "  • Sử dụng GPU với --gpu (nếu có)"
    echo "  • Tăng memory với --max-memory"
    echo "  • Giảm kích thước ảnh đầu vào"
    echo "  • Xử lý theo batch nhỏ hơn"
fi

print_info "Workflow hoàn thành!"

exit $WORKFLOW_EXIT_CODE 