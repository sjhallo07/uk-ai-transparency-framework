def check(pkgs):
    # Placeholder function; implement as needed
    pass

#!/usr/bin/env python3
"""
Environment verification script for UK AI Transparency Framework
"""

import sys
import importlib.util

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"🐍 Python version: {sys.version}")
    
    if version.major == 3 and version.minor >= 11:
        print("✅ Python version is compatible (3.11+)")
        return True
    else:
        print("❌ Python version too old. Required: 3.11+")
        return False

def check_package(package_name, min_version=None):
    """Check if a package is installed and meets version requirements"""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            print(f"❌ {package_name}: Not installed")
            return False
        
        if min_version:
            module = importlib.import_module(package_name)
            if hasattr(module, '__version__'):
                installed_version = module.__version__
                if installed_version >= min_version:
                    print(f"✅ {package_name}: {installed_version} (>= {min_version})")
                    return True
                else:
                    print(f"❌ {package_name}: {installed_version} (required: >= {min_version})")
                    return False
            else:
                print(f"⚠️ {package_name}: Version unknown")
                return True
        else:
            print(f"✅ {package_name}: Installed")
            return True
            
    except ImportError:
        print(f"❌ {package_name}: Import failed")
        return False

def main():
    print("🔍 Verifying UK AI Transparency Framework Environment...")
    print("=" * 60)
    
    # Check Python version
    python_ok = check_python_version()
    print()
    
    # Check required packages
    packages = {
        "pandas": "2.1.0",
        "streamlit": "1.28.0", 
        "plotly": "5.17.0",
        "numpy": "1.24.0"
    }
    
    all_ok = python_ok
    for package, version in packages.items():
        if not check_package(package, version):
            all_ok = False
    
    print()
    print("=" * 60)
    if all_ok:
        print("🎉 Environment verification PASSED!")
        print("You can now run: streamlit run src/transparency_dashboard.py")
    else:
        print("❌ Environment verification FAILED!")
        print("Please install missing dependencies: pip install -r requirements.txt")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
