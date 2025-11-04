#!/usr/bin/env python3
"""
Automatic setup for translation dependencies.

This module automatically installs and configures:
1. Argos Translate English→Chinese model
2. ECDICT dictionary (optional)

Called automatically when the Flask app starts.
"""

import logging
import subprocess
import sys
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)


def check_argos_model_installed() -> bool:
    """Check if Argos Translate English→Chinese model is installed."""
    try:
        import argostranslate.package

        installed_packages = argostranslate.package.get_installed_packages()

        # Look for English→Chinese package
        for pkg in installed_packages:
            pkg_info = str(pkg)
            if "en" in pkg_info.lower() and "zh" in pkg_info.lower():
                logger.info(f"Found Argos translation package: {pkg}")
                return True

        return False
    except ImportError:
        logger.warning("argostranslate not installed")
        return False
    except Exception as e:
        logger.error(f"Error checking Argos packages: {e}")
        return False


def install_argos_model() -> Tuple[bool, str]:
    """
    Download and install Argos Translate English→Chinese model.

    Downloads the .argosmodel package from the official Argos package index
    and installs it using argostranslate.package.install_from_path().

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        import urllib.request
        import json
        import argostranslate.package

        project_root = Path(__file__).parent.parent.parent.parent
        models_dir = project_root / "data" / "translation_models"
        models_dir.mkdir(parents=True, exist_ok=True)

        # Model file path
        model_file = models_dir / "translate-en_zh.argosmodel"

        # Check if model file already exists locally
        if model_file.exists():
            logger.info(f"Found cached model file: {model_file}")
            logger.info("Installing from cached file...")
            try:
                argostranslate.package.install_from_path(str(model_file))

                # Verify installation
                if check_argos_model_installed():
                    return True, "Installed from cached model file"
                else:
                    logger.warning("Installation from cache failed, trying download...")
            except Exception as e:
                logger.warning(f"Failed to install from cache: {e}, trying download...")

        # Step 1: Download package index
        logger.info("Fetching Argos Translate package index...")
        index_url = "https://raw.githubusercontent.com/argosopentech/argospm-index/main/index.json"

        try:
            with urllib.request.urlopen(index_url, timeout=30) as response:
                index_data = json.loads(response.read().decode('utf-8'))
                logger.info(f"✅ Package index loaded ({len(index_data)} packages)")
        except Exception as e:
            msg = f"Failed to fetch package index: {e}"
            logger.error(msg)
            return False, msg

        # Step 2: Find English→Chinese package
        en_zh_package = None
        for package in index_data:
            if package.get('from_code') == 'en' and package.get('to_code') == 'zh':
                en_zh_package = package
                logger.info(f"Found en→zh package: {package.get('package_version', 'unknown version')}")
                break

        if not en_zh_package:
            msg = "English→Chinese package not found in index"
            logger.error(msg)
            return False, msg

        # Step 3: Download the model package
        links = en_zh_package.get('links', [])
        if not links or len(links) == 0:
            msg = "Package download URL not found in index"
            logger.error(msg)
            return False, msg

        # Links is a list of URL strings
        package_url = links[0]

        logger.info(f"Downloading model from: {package_url}")
        logger.info("This may take a few minutes (model is ~100MB)...")

        try:
            with urllib.request.urlopen(package_url, timeout=300) as response:
                data = response.read()

                # Save to cache
                with open(model_file, 'wb') as f:
                    f.write(data)

                logger.info(f"✅ Model downloaded successfully ({len(data) / 1024 / 1024:.1f} MB)")

        except urllib.error.HTTPError as e:
            msg = f"HTTP error downloading model: {e.code}"
            logger.error(msg)
            return False, msg
        except Exception as e:
            msg = f"Error downloading model: {e}"
            logger.error(msg)
            return False, msg

        # Step 4: Install the downloaded model
        logger.info("Installing downloaded model...")
        try:
            argostranslate.package.install_from_path(str(model_file))
        except Exception as e:
            msg = f"Error installing model: {e}"
            logger.error(msg)
            return False, msg

        # Step 5: Verify installation
        if check_argos_model_installed():
            logger.info("✅ Model installed successfully!")
            return True, "Model downloaded and installed successfully"
        else:
            msg = "Installation completed but model not detected. Please restart the application."
            logger.warning(msg)
            return False, msg

    except ImportError as e:
        msg = f"Missing required library: {e}. Please ensure argostranslate is installed."
        logger.error(msg)
        return False, msg
    except Exception as e:
        msg = f"Error during automatic installation: {e}"
        logger.error(msg)
        logger.info("You can try manual installation:")
        logger.info("  1. Visit: https://www.argosopentech.com/argospm/index/")
        logger.info("  2. Download the English-Chinese package")
        logger.info("  3. Install: python -c \"import argostranslate.package; argostranslate.package.install_from_path('path/to/translate-en_zh.argosmodel')\"")
        return False, msg


def check_ecdict_installed() -> bool:
    """Check if ECDICT dictionary is available."""
    project_root = Path(__file__).parent.parent.parent.parent
    ecdict_path = project_root / "data" / "dictionaries" / "ECDICT" / "ecdict.csv"

    exists = ecdict_path.exists()
    if exists:
        logger.info(f"✅ ECDICT dictionary found at {ecdict_path}")
    else:
        logger.info(f"❌ ECDICT dictionary not found at {ecdict_path}")

    return exists


def download_ecdict() -> Tuple[bool, str]:
    """
    Attempt to download ECDICT dictionary.

    Note: This is optional and may not work due to GitHub rate limits.

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        import urllib.request
        import gzip
        import csv

        project_root = Path(__file__).parent.parent.parent.parent
        ecdict_dir = project_root / "data" / "dictionaries" / "ECDICT"
        ecdict_dir.mkdir(parents=True, exist_ok=True)

        ecdict_path = ecdict_dir / "ecdict.csv"

        if ecdict_path.exists():
            logger.info("ECDICT already exists, skipping download")
            return True, "ECDICT already installed"

        logger.info("Downloading ECDICT dictionary from GitHub...")

        # ECDICT GitHub raw URL
        url = "https://github.com/skywind3000/ECDICT/raw/master/ecdict.csv"

        # Download with timeout
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()

            # Save directly (it's not gzipped on GitHub)
            with open(ecdict_path, 'wb') as f:
                f.write(data)

        # Verify it's a valid CSV
        with open(ecdict_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            if 'word' not in [h.lower() for h in header]:
                raise ValueError("Downloaded file doesn't appear to be valid ECDICT")

        logger.info(f"✅ ECDICT dictionary downloaded successfully to {ecdict_path}")
        return True, f"ECDICT dictionary downloaded successfully"

    except urllib.error.HTTPError as e:
        if e.code == 403:
            msg = "GitHub rate limit exceeded. Please download ECDICT manually from: https://github.com/skywind3000/ECDICT"
        else:
            msg = f"HTTP error downloading ECDICT: {e}"
        logger.warning(msg)
        return False, msg
    except Exception as e:
        msg = f"Error downloading ECDICT: {e}. You can download it manually from: https://github.com/skywind3000/ECDICT"
        logger.warning(msg)
        return False, msg


def auto_setup(force_reinstall: bool = False) -> dict:
    """
    Automatically set up translation dependencies.

    Args:
        force_reinstall: If True, reinstall even if already installed

    Returns:
        Dictionary with setup status:
        {
            'argos_installed': bool,
            'argos_message': str,
            'ecdict_installed': bool,
            'ecdict_message': str,
            'ready': bool  # True if all critical components are ready
        }
    """
    logger.info("Starting automatic translation setup...")

    status = {
        'argos_installed': False,
        'argos_message': '',
        'ecdict_installed': False,
        'ecdict_message': '',
        'ready': False
    }

    # Check/install Argos model
    if force_reinstall or not check_argos_model_installed():
        logger.info("Argos model not found, attempting automatic installation...")
        success, message = install_argos_model()
        status['argos_installed'] = success
        status['argos_message'] = message

        if success:
            # Verify installation
            status['argos_installed'] = check_argos_model_installed()
    else:
        logger.info("✅ Argos model already installed")
        status['argos_installed'] = True
        status['argos_message'] = "Argos model already installed"

    # Check/download ECDICT (optional, but recommended)
    if force_reinstall or not check_ecdict_installed():
        logger.info("ECDICT not found, attempting download...")
        success, message = download_ecdict()
        status['ecdict_installed'] = success
        status['ecdict_message'] = message
    else:
        logger.info("✅ ECDICT already installed")
        status['ecdict_installed'] = True
        status['ecdict_message'] = "ECDICT already installed"

    # System is ready if Argos is installed (ECDICT is optional)
    status['ready'] = status['argos_installed']

    if status['ready']:
        logger.info("✅ Translation system is ready!")
    else:
        logger.warning("⚠️ Translation system not fully configured")
        logger.warning("Some translation features may not work properly")

    return status


def get_setup_instructions() -> str:
    """
    Get manual setup instructions for when automatic setup fails.

    Returns:
        Formatted instruction string
    """
    return """
╔════════════════════════════════════════════════════════════════════╗
║          MANUAL TRANSLATION SETUP REQUIRED                         ║
╚════════════════════════════════════════════════════════════════════╝

Automatic installation failed. Please install manually:

1. ARGOS TRANSLATE MODEL (Required for translation):
   ────────────────────────────────────────────────────────────────
   Method 1 - Python API (Recommended):
     python -c "import argostranslate.package; \
                argostranslate.package.update_package_index(); \
                pkg = [p for p in argostranslate.package.get_available_packages() \
                       if p.from_code=='en' and p.to_code=='zh'][0]; \
                pkg.install()"

   Method 2 - Re-run setup script:
     python -m vocab_analyzer.translation.auto_setup

   Method 3 - Visit GitHub:
     https://github.com/argosopentech/argos-translate
     Download and install the English-Chinese (en-zh) package

2. ECDICT DICTIONARY (Optional, improves word translation quality):
   ────────────────────────────────────────────────────────────────
   Download from: https://github.com/skywind3000/ECDICT
   Place ecdict.csv in: data/dictionaries/ECDICT/ecdict.csv

After manual installation, restart the application.

╚════════════════════════════════════════════════════════════════════╝
"""


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("="*70)
    print("Automatic Translation Setup")
    print("="*70)
    print()

    status = auto_setup()

    print()
    print("="*70)
    print("Setup Results:")
    print("="*70)
    print(f"Argos Model:  {'✅ Installed' if status['argos_installed'] else '❌ Not Installed'}")
    print(f"              {status['argos_message']}")
    print(f"ECDICT:       {'✅ Installed' if status['ecdict_installed'] else '❌ Not Installed'}")
    print(f"              {status['ecdict_message']}")
    print(f"Status:       {'✅ Ready' if status['ready'] else '⚠️  Incomplete'}")
    print("="*70)

    if not status['ready']:
        print()
        print(get_setup_instructions())
        sys.exit(1)
    else:
        print()
        print("✅ Translation system is ready to use!")
        sys.exit(0)
