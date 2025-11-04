#!/usr/bin/env python3
"""
Setup script for Argos Translate English→Chinese translation model.

This script provides instructions for manually downloading and installing
the English to Chinese translation model for offline translation functionality.

Argos Translate 1.0 requires manual model installation via pip.

Usage:
    python scripts/setup_translation.py

Expected Behavior:
    - Verifies argostranslate is installed
    - Tests if translation works
    - Provides installation instructions if models not found
"""

import sys
from pathlib import Path

try:
    import argostranslate.package
    import argostranslate.translate
except ImportError:
    print("ERROR: argostranslate not installed")
    print("Install it with: pip install argostranslate")
    sys.exit(1)


def check_and_test_model():
    """Check if English→Chinese model is installed and test it."""

    print("🔍 Checking for English→Chinese translation model...")

    # Check if already installed by attempting translation
    try:
        installed_packages = argostranslate.package.get_installed_packages()
        print(f"✅ Found {len(installed_packages)} installed language packages")

        # Try to find English→Chinese
        en_zh_installed = False
        for pkg in installed_packages:
            pkg_info = str(pkg)
            if "en" in pkg_info.lower() and "zh" in pkg_info.lower():
                en_zh_installed = True
                print(f"   Found: {pkg}")

        if not en_zh_installed:
            print("\n❌ English→Chinese model not found")
            print_installation_instructions()
            return False

        print("\n🧪 Testing translation...")
        if test_translation():
            print("\n✅ Translation model is working correctly!")
            return True
        else:
            print("\n❌ Translation test failed")
            print_installation_instructions()
            return False

    except Exception as e:
        print(f"❌ ERROR checking models: {e}")
        print_installation_instructions()
        return False


def print_installation_instructions():
    """Print manual installation instructions for Argos Translate 1.0."""

    print("\n" + "="*70)
    print("MANUAL INSTALLATION REQUIRED (Argos Translate 1.0)")
    print("="*70)
    print("\nArgos Translate 1.0 requires manual model installation.")
    print("\nOption 1: Install via pip (Recommended)")
    print("-" * 70)
    print("pip install argostranslate-translate-en-zh")
    print("\nOption 2: Use command-line tool")
    print("-" * 70)
    print("argospm install translate-en_zh")
    print("\nOption 3: Download from GitHub")
    print("-" * 70)
    print("1. Visit: https://github.com/argosopentech/argos-translate")
    print("2. Navigate to releases and download en-zh package")
    print("3. Install with: argostranslate-cli --install-language /path/to/package")
    print("\n" + "="*70)
    print("\nAfter installation, run this script again to verify.")
    print("="*70)


def test_translation():
    """Test the installed translation model."""

    # Test basic translation
    test_phrases = [
        "Hello, world!",
        "This is a test.",
        "How are you?"
    ]

    print("\n" + "="*60)
    print("Testing English→Chinese Translation")
    print("="*60)

    for phrase in test_phrases:
        try:
            translated = argostranslate.translate.translate(phrase, "en", "zh")
            print(f"EN: {phrase}")
            print(f"ZH: {translated}")
            print()
        except Exception as e:
            print(f"❌ Translation failed for '{phrase}': {e}")
            return False

    print("✅ All tests passed!")
    print("\n" + "="*60)
    print("Translation model is ready to use")
    print("="*60)

    return True


def main():
    """Main entry point."""
    print("="*70)
    print("Argos Translate Setup - English→Chinese Model")
    print("="*70)
    print()

    success = check_and_test_model()

    if success:
        print("\n✅ Setup complete!")
        print("\nNext steps:")
        print("1. The translation model is now available for offline use")
        print("2. First translation may take 2-4 seconds (model loading)")
        print("3. Subsequent translations are faster (<1 second)")
        print("\nTo test manually:")
        print("  python -c \"import argostranslate.translate; print(argostranslate.translate.translate('Hello', 'en', 'zh'))\"")
        sys.exit(0)
    else:
        print("\n⚠️  Setup incomplete - follow installation instructions above")
        sys.exit(1)


if __name__ == "__main__":
    main()
