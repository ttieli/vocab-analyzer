"""
Translation module for bilingual UI and offline translation.

This module provides:
- Translation caching (TranslationCache)
- Offline translation (ArgosTranslator)
- Mdict dictionary integration (MdictDictionary)
- Fallback translation chain (TranslationChain)
- Bilingual UI strings (BilingualStringLoader)
"""

from .cache import TranslationCache
from .translator import ArgosTranslator
from .dictionary import MdictDictionary
from .fallback import TranslationChain, TranslationResult
from .config import TranslationConfig, get_config, reload_config
from .strings import BilingualStringLoader, get_loader, reload_strings

__all__ = [
    "TranslationCache",
    "ArgosTranslator",
    "MdictDictionary",
    "TranslationChain",
    "TranslationResult",
    "TranslationConfig",
    "get_config",
    "reload_config",
    "BilingualStringLoader",
    "get_loader",
    "reload_strings",
]
