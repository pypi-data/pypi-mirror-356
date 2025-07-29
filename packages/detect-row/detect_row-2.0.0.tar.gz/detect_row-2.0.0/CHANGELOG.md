# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-06-18

### Added
- 🚀 **Complete table, row, and column extraction system**
- 📊 **Advanced column extraction with intelligent merging**
- 🎮 **GPU support with CUDA acceleration**
- 🧠 **Memory management and optimization**
- 🔧 **Comprehensive configuration system**
- 📋 **Interactive column grouping helper**
- 🐛 **Extensive debugging and troubleshooting tools**
- 📖 **Complete Vietnamese and English documentation**
- ⚡ **Automated workflow scripts**
- 🔍 **System health check utilities**

### New Features
- `AdvancedColumnExtractor` - Intelligent column detection and merging
- `GPUManager` - CUDA support and memory management
- `MemoryManager` - Efficient memory usage monitoring
- Column groups with templates (basic, enhanced, comprehensive, document_structure)
- Interactive configuration builder
- Automated workflow with batch processing
- Performance optimization presets
- Comprehensive error handling and logging

### New Scripts
- `extract_tables_and_columns.py` - All-in-one extraction workflow
- `run_complete_workflow.py` - Automated processing with monitoring
- `column_groups_helper.py` - Interactive column merge configuration
- `system_check.py` - Complete system health check
- `quick_demo.py` - Quick demonstration and testing
- `auto_workflow.sh` - Automated shell script for Linux/Mac

### New Documentation
- `COMPLETE_USAGE_GUIDE.md` - Comprehensive usage guide
- `HUONG_DAN_NHANH.md` - Quick start guide in Vietnamese
- `config_template.json` - Configuration template with all options

### Enhanced
- **Table detection accuracy improved by 50%** (2→3 tables per image)
- Support for faint border tables with high aspect ratios
- Adaptive threshold and morphological operations
- Intelligent overlap removal
- Better Vietnamese document support

### Command Line Tools
- `detect-row-extract` - Main extraction command
- `detect-row-workflow` - Complete workflow
- `detect-row-check` - System check
- `detect-row-demo` - Quick demo
- `detect-row-helper` - Column groups helper
- `detect-row-gpu-test` - GPU testing
- `detect-row-summary` - Results summary

### Performance
- Smart batch processing with memory monitoring
- GPU acceleration for supported operations
- Automatic memory cleanup and garbage collection
- Adaptive batch sizing based on available resources
- Multi-threading support for CPU operations

### Breaking Changes
- Minimum Python version raised to 3.8
- New dependency requirements (scikit-image, scipy, psutil)
- API changes in some extractor classes
- Output directory structure reorganized

### Fixed
- Memory leaks in batch processing
- GPU memory management issues
- Column detection accuracy for complex tables
- Unicode handling in Vietnamese text
- Path handling on Windows systems

## [1.0.7] - 2024-XX-XX

### Added
- Basic table and row extraction
- OCR support with Tesseract
- Simple column detection

### Fixed
- Basic bug fixes and improvements

## [1.0.0] - 2024-XX-XX

### Added
- Initial release
- Basic row detection functionality
- OpenCV integration
- Simple table extraction

---

## Migration Guide from 1.x to 2.0

### Installation
```bash
# Uninstall old version
pip uninstall detect-row

# Install new version
pip install detect-row>=2.0.0

# For GPU support
pip install detect-row[gpu]

# For full features
pip install detect-row[full]
```

### Code Changes
```python
# Old (1.x)
from detect_row import BasicRowExtractor
extractor = BasicRowExtractor()

# New (2.0)
from detect_row import AdvancedTableExtractor, AdvancedColumnExtractor
table_extractor = AdvancedTableExtractor(input_dir="input", output_dir="output")
column_extractor = AdvancedColumnExtractor(input_dir="tables", output_dir="columns")
```

### Command Line
```bash
# Old
detect-row-basic image.jpg

# New
detect-row-extract image.jpg --column-groups "header:1;content:2,3;footer:4"
```

For detailed migration instructions, see `COMPLETE_USAGE_GUIDE.md`. 