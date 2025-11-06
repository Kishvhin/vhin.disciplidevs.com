#!/usr/bin/env python3
"""
Test script to verify NDTA News Pipeline installation
Run this after installing to ensure everything is configured correctly
"""

import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def test_python_version():
    """Check Python version"""
    print("\n✓ Testing Python version...")
    major, minor = sys.version_info[:2]
    
    if major >= 3 and minor >= 8:
        print(f"  ✅ Python {major}.{minor} - OK")
        return True
    else:
        print(f"  ❌ Python {major}.{minor} - Need 3.8+")
        return False

def test_dependencies():
    """Check if all required packages are installed"""
    print("\n✓ Testing dependencies...")
    
    required_packages = [
        'requests',
        'beautifulsoup4',
        'feedparser',
        'pandas',
        'openai',
        'anthropic',
        'PIL',  # Pillow
        'tweepy',
        'facebook',
        'dotenv',
        'yaml',
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                __import__('PIL')
            elif package == 'dotenv':
                __import__('dotenv')
            elif package == 'yaml':
                __import__('yaml')
            elif package == 'facebook':
                __import__('facebook')
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"   Run: pip install -r requirements.txt")
        return False
    
    print(f"\n  ✅ All dependencies installed")
    return True

def test_directory_structure():
    """Check if all required directories exist"""
    print("\n✓ Testing directory structure...")
    
    required_dirs = [
        'config',
        'scrapers',
        'content_generator',
        'graphics',
        'distribution',
        'data/raw_news',
        'data/processed_news',
        'data/graphics',
        'data/approved_content',
        'logs',
    ]
    
    missing = []
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/ - MISSING")
            missing.append(dir_path)
    
    if missing:
        print(f"\n❌ Missing directories: {', '.join(missing)}")
        print(f"   Create them manually or check installation")
        return False
    
    print(f"\n  ✅ All directories present")
    return True

def test_env_file():
    """Check if .env file exists and has required keys"""
    print("\n✓ Testing environment configuration...")
    
    if not Path('.env').exists():
        print(f"  ❌ .env file not found")
        print(f"   Create it from: cp .env.template .env")
        return False
    
    from dotenv import dotenv_values
    env = dotenv_values('.env')
    
    required_keys = [
        'OPENAI_API_KEY',
        'NEWS_API_KEY',
    ]
    
    optional_keys = [
        'TWITTER_API_KEY',
        'FACEBOOK_APP_ID',
    ]
    
    missing_required = []
    
    for key in required_keys:
        value = env.get(key, '')
        if value and value != f'your_{key.lower()}_here':
            print(f"  ✅ {key}")
        else:
            print(f"  ❌ {key} - NOT SET")
            missing_required.append(key)
    
    for key in optional_keys:
        value = env.get(key, '')
        if value and value != f'your_{key.lower()}_here':
            print(f"  ✅ {key} (optional)")
        else:
            print(f"  ⚠️  {key} - Not set (optional)")
    
    if missing_required:
        print(f"\n❌ Required API keys missing: {', '.join(missing_required)}")
        print(f"   Add them to .env file")
        return False
    
    print(f"\n  ✅ Environment configured")
    return True

def test_config_files():
    """Check if configuration files exist"""
    print("\n✓ Testing configuration files...")
    
    required_configs = [
        'config/news_sources.yaml',
    ]
    
    missing = []
    
    for config_file in required_configs:
        if Path(config_file).exists():
            print(f"  ✅ {config_file}")
        else:
            print(f"  ❌ {config_file} - MISSING")
            missing.append(config_file)
    
    if missing:
        print(f"\n❌ Missing config files: {', '.join(missing)}")
        return False
    
    print(f"\n  ✅ All config files present")
    return True

def test_api_connections():
    """Test API connections (if keys are configured)"""
    print("\n✓ Testing API connections...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test OpenAI
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key and openai_key != 'your_openai_api_key_here':
        try:
            import openai
            openai.api_key = openai_key
            # Simple test - just check if key format is valid
            if openai_key.startswith('sk-'):
                print(f"  ✅ OpenAI API key format valid")
            else:
                print(f"  ⚠️  OpenAI API key format unusual")
        except Exception as e:
            print(f"  ❌ OpenAI API error: {e}")
    else:
        print(f"  ⚠️  OpenAI API key not configured")
    
    # Test NewsAPI
    news_key = os.getenv('NEWS_API_KEY')
    if news_key and news_key != 'your_newsapi_key_here':
        try:
            import requests
            response = requests.get(
                f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_key}',
                timeout=10
            )
            if response.status_code == 200:
                print(f"  ✅ NewsAPI connection successful")
            else:
                print(f"  ❌ NewsAPI error: Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ NewsAPI connection error: {e}")
    else:
        print(f"  ⚠️  NewsAPI key not configured")
    
    return True

def main():
    """Run all tests"""
    print_header("NDTA NEWS PIPELINE - INSTALLATION TEST")
    
    print("\nTesting system configuration...\n")
    
    results = []
    
    # Run tests
    results.append(("Python Version", test_python_version()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Configuration Files", test_config_files()))
    results.append(("Environment Variables", test_env_file()))
    results.append(("API Connections", test_api_connections()))
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print(f"\n  Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "="*60)
        print("  🎉 SUCCESS! System is ready to use!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Review config/news_sources.yaml")
        print("  2. Run: python main.py scrape")
        print("  3. Follow the daily workflow in README.md")
        print("\n")
        return 0
    else:
        print("\n" + "="*60)
        print("  ⚠️  SETUP INCOMPLETE")
        print("="*60)
        print("\nPlease fix the failed tests above.")
        print("Refer to SETUP_GUIDE.md for detailed instructions.\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())