#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Deploy Script - DetectRow 2.0
=====================================

Script đơn giản để deploy package lên PyPI

Usage:
    python simple_deploy.py              # Deploy to TestPyPI
    python simple_deploy.py --prod       # Deploy to PyPI
    python simple_deploy.py --build      # Build only
"""

import subprocess
import sys
import argparse
import os

def run_command(cmd, description=""):
    """Run command và hiển thị kết quả"""
    if description:
        print(f"🔄 {description}...")
    
    print(f"   Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"   ✅ Success")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
    else:
        print(f"   ❌ Failed")
        if result.stderr.strip():
            print(f"   Error: {result.stderr.strip()}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Deploy detect-row package')
    parser.add_argument('--prod', action='store_true', help='Deploy to production PyPI')
    parser.add_argument('--build', action='store_true', help='Build only, no deploy')
    parser.add_argument('--test', action='store_true', help='Test package after build')
    
    args = parser.parse_args()
    
    print("🚀 DetectRow 2.0 Deployment Script")
    print("=" * 40)
    
    # 1. Clean old builds
    print("\n📂 Cleaning old build artifacts...")
    if os.name == 'nt':  # Windows
        run_command("if exist build rmdir /s /q build", "Remove build dir")
        run_command("if exist dist rmdir /s /q dist", "Remove dist dir") 
        run_command("for /d %i in (*.egg-info) do rmdir /s /q \"%i\"", "Remove egg-info")
    else:  # Linux/Mac
        run_command("rm -rf build/ dist/ *.egg-info/", "Clean artifacts")
    
    # 2. Build package
    print("\n🏗️ Building package...")
    if not run_command("python -m build", "Build wheel and source dist"):
        print("❌ Build failed!")
        sys.exit(1)
    
    # 3. Check package quality
    print("\n🔍 Checking package quality...")
    if not run_command("twine check dist/*", "Quality check"):
        print("❌ Quality check failed!")
        sys.exit(1)
    
    # 4. List built files
    print("\n📦 Built packages:")
    if os.path.exists("dist"):
        for file in os.listdir("dist"):
            size = os.path.getsize(f"dist/{file}")
            print(f"   📄 {file} ({size:,} bytes)")
    
    # 5. Test package locally (if requested)
    if args.test:
        print("\n🧪 Testing package locally...")
        if not run_command("pip install dist/*.whl --force-reinstall", "Install wheel"):
            print("❌ Local test failed!")
            sys.exit(1)
        
        if not run_command("python -c \"import detect_row; print(f'Version: {detect_row.__version__}')\"", "Test import"):
            print("❌ Import test failed!")
            sys.exit(1)
    
    # 6. Deploy (if not build-only)
    if not args.build:
        print("\n🚀 Deploying package...")
        
        if args.prod:
            print("   🎯 Target: Production PyPI")
            print("   ⚠️  WARNING: This will deploy to production!")
            confirm = input("   Continue? [y/N]: ").lower()
            if confirm != 'y':
                print("   Deployment cancelled.")
                sys.exit(0)
            
            deploy_cmd = "twine upload dist/*"
        else:
            print("   🎯 Target: TestPyPI")
            # For TestPyPI without config, use direct URL
            deploy_cmd = "twine upload --repository-url https://test.pypi.org/legacy/ dist/*"
        
        if run_command(deploy_cmd, "Upload to repository"):
            if args.prod:
                print("\n🎉 Successfully deployed to PyPI!")
                print("   📦 Install with: pip install detect-row")
                print("   🔗 View at: https://pypi.org/project/detect-row/")
            else:
                print("\n🎉 Successfully deployed to TestPyPI!")
                print("   📦 Install with: pip install --index-url https://test.pypi.org/simple/ detect-row")
                print("   🔗 View at: https://test.pypi.org/project/detect-row/")
        else:
            print("❌ Deployment failed!")
            print("   💡 Tips:")
            print("     - Check your PyPI credentials")
            print("     - Verify package name is available")
            print("     - Try TestPyPI first: python simple_deploy.py")
            sys.exit(1)
    
    else:
        print("\n✅ Build completed successfully!")
        print("   To deploy to TestPyPI: python simple_deploy.py")
        print("   To deploy to PyPI: python simple_deploy.py --prod")

if __name__ == "__main__":
    main() 