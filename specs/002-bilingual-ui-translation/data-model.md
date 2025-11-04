# Data Model Specification

**Feature**: Bilingual UI with CEFR Descriptions and Local Translation
**Date**: 2025-11-04
**Status**: Draft
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md) | [research.md](./research.md)

---

## Table of Contents

1. [Overview](#overview)
2. [Entity Definitions](#entity-definitions)
   - [TranslationCache](#1-translationcache)
   - [CEFRDefinition](#2-cefrdefinition)
   - [TranslationRequest](#3-translationrequest)
   - [MdictDictionary](#4-mdictdictionary)
   - [BilingualString](#5-bilingualstring)
3. [Entity Relationships](#entity-relationships)
4. [Data Flow Diagrams](#data-flow-diagrams)
5. [Persistence Strategies](#persistence-strategies)
6. [Schema Examples](#schema-examples)
7. [Validation Rules](#validation-rules)

---

## Overview

This document defines the data model for the bilingual UI feature, including translation caching, CEFR level descriptions, Mdict dictionary management, and UI localization strings. The design supports:

- **Offline-first architecture**: All data stored locally
- **Three-tier translation fallback**: ECDICT → Mdict → Argos Translate
- **Persistent caching**: Reduce redundant translation operations
- **Bilingual UI**: Simultaneous English/Chinese display
- **Educational context**: CEFR level descriptions with learning guidance

### Design Principles

1. **Simplicity**: Prefer JSON over database for static/semi-static data
2. **Portability**: All data in human-readable formats (JSON, CSV)
3. **Performance**: Indexed lookups, LRU caching, lazy loading
4. **Graceful degradation**: Handle missing dictionaries/models gracefully
5. **Extensibility**: Easy to add new translation sources or languages

---

## Entity Definitions

### 1. TranslationCache

**Purpose**: Persistent cache for user-generated translations to reduce redundant API/model calls.

**Use Cases**:
- Cache ECDICT lookups for frequently accessed words
- Cache Mdict definitions to avoid HTML parsing overhead
- Cache Argos Translate results to avoid expensive ML inference
- Track translation source and confidence for quality assessment

#### 1.1 Fields

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `source_text` | `str` | Yes | Original English text | Non-empty, max 500 chars, lowercased for key |
| `target_text` | `str` | Yes | Chinese translation | Non-empty, max 2000 chars |
| `timestamp` | `datetime` | Yes | When cached (Unix timestamp) | Must be valid Unix timestamp |
| `translation_type` | `str` | Yes | Type of content | Enum: `word`, `phrase`, `sentence` |
| `source` | `str` | Yes | Translation source | Enum: `ecdict`, `mdict`, `argos`, `cached` |
| `confidence_score` | `float` | Yes | Translation quality estimate | Range: 0.0-1.0 |
| `access_count` | `int` | No | Number of times accessed | Default: 1, increments on each access |

#### 1.2 Validation Rules

```python
def validate_translation_cache_entry(entry: dict) -> tuple[bool, str]:
    """
    Validate translation cache entry.

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    required_fields = ["source_text", "target_text", "timestamp",
                       "translation_type", "source", "confidence_score"]

    for field in required_fields:
        if field not in entry or not entry[field]:
            return False, f"Missing required field: {field}"

    # Validate source_text
    if len(entry["source_text"]) == 0:
        return False, "source_text cannot be empty"
    if len(entry["source_text"]) > 500:
        return False, "source_text exceeds 500 characters"

    # Validate target_text
    if len(entry["target_text"]) == 0:
        return False, "target_text cannot be empty"
    if len(entry["target_text"]) > 2000:
        return False, "target_text exceeds 2000 characters"

    # Validate translation_type
    valid_types = ["word", "phrase", "sentence"]
    if entry["translation_type"] not in valid_types:
        return False, f"Invalid translation_type. Must be one of: {valid_types}"

    # Validate source
    valid_sources = ["ecdict", "mdict", "argos", "cached"]
    if entry["source"] not in valid_sources:
        return False, f"Invalid source. Must be one of: {valid_sources}"

    # Validate confidence_score
    if not (0.0 <= entry["confidence_score"] <= 1.0):
        return False, "confidence_score must be between 0.0 and 1.0"

    # Validate timestamp
    if not isinstance(entry["timestamp"], (int, float)) or entry["timestamp"] < 0:
        return False, "timestamp must be a positive Unix timestamp"

    return True, ""
```

#### 1.3 Persistence Strategy

**Format**: JSON file (`data/translation_cache.json`)

**Structure**:
```json
{
  "version": "1.0",
  "last_saved": 1730736000,
  "entries": {
    "word:example": {
      "source_text": "example",
      "target_text": "n. 例子, 榜样, 例题\nvt. 作为...的例子, 为...做出榜样\nvi. 举例, 作为...的示范",
      "timestamp": 1730736000,
      "translation_type": "word",
      "source": "ecdict",
      "confidence_score": 0.95,
      "access_count": 5
    },
    "phrase:run out": {
      "source_text": "run out",
      "target_text": "用完；耗尽",
      "timestamp": 1730736100,
      "translation_type": "phrase",
      "source": "argos",
      "confidence_score": 0.70,
      "access_count": 2
    }
  }
}
```

**Key Format**: `{translation_type}:{source_text.lower().strip()}`

**Indexes**: In-memory dict with O(1) lookup by key

#### 1.4 Operations

```python
class TranslationCache:
    """Operations for translation cache."""

    def get(self, text: str, text_type: str = "word") -> Optional[dict]:
        """
        Get cached translation.

        Args:
            text: Source text to look up
            text_type: Type of text (word/phrase/sentence)

        Returns:
            Cached entry or None if not found

        Time Complexity: O(1)
        """
        pass

    def set(self, text: str, translation: str, source: str,
            text_type: str = "word", confidence: float = 1.0) -> None:
        """
        Cache translation result.

        Args:
            text: Source text
            translation: Translation result
            source: Translation source (ecdict/mdict/argos)
            text_type: Type of text
            confidence: Quality score (0.0-1.0)

        Side Effects:
            - Updates access_count if entry exists
            - Sets dirty flag for save

        Time Complexity: O(1)
        """
        pass

    def exists(self, text: str, text_type: str = "word") -> bool:
        """
        Check if translation is cached.

        Args:
            text: Source text
            text_type: Type of text

        Returns:
            True if cached

        Time Complexity: O(1)
        """
        pass

    def clear_old(self, days: int = 30) -> int:
        """
        Remove entries older than specified days.

        Args:
            days: Age threshold in days

        Returns:
            Number of entries removed

        Time Complexity: O(n) where n = total entries
        """
        pass

    def save(self) -> bool:
        """
        Persist cache to disk.

        Returns:
            True if successful

        Side Effects:
            - Writes to data/translation_cache.json
            - Clears dirty flag

        Time Complexity: O(n)
        """
        pass

    def load(self) -> bool:
        """
        Load cache from disk.

        Returns:
            True if successful

        Side Effects:
            - Populates in-memory cache

        Time Complexity: O(n)
        """
        pass
```

#### 1.5 Example Data

```json
{
  "version": "1.0",
  "last_saved": 1730736000,
  "entries": {
    "word:sophisticated": {
      "source_text": "sophisticated",
      "target_text": "精密的；复杂的；久经世故的",
      "timestamp": 1730735000,
      "translation_type": "word",
      "source": "ecdict",
      "confidence_score": 0.95,
      "access_count": 3
    },
    "phrase:blow up": {
      "source_text": "blow up",
      "target_text": "爆炸；发怒",
      "timestamp": 1730735200,
      "translation_type": "phrase",
      "source": "mdict",
      "confidence_score": 0.90,
      "access_count": 1
    },
    "sentence:Time is running out.": {
      "source_text": "Time is running out.",
      "target_text": "时间不多了。",
      "timestamp": 1730735400,
      "translation_type": "sentence",
      "source": "argos",
      "confidence_score": 0.75,
      "access_count": 2
    }
  }
}
```

---

### 2. CEFRDefinition

**Purpose**: Static bilingual descriptions for CEFR levels (A1-C2+) to educate users about proficiency levels.

**Use Cases**:
- Display CEFR level badges with tooltips in UI
- Show detailed modal when user clicks level badge
- Provide context for vocabulary difficulty
- Help learners understand progression path

#### 2.1 Fields

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `level_code` | `str` | Yes | CEFR level identifier | Enum: `A1`, `A2`, `B1`, `B2`, `C1`, `C2`, `C2+` |
| `name_en` | `str` | Yes | English level name | Non-empty, max 50 chars |
| `name_cn` | `str` | Yes | Chinese level name | Non-empty, max 50 chars |
| `description_en` | `str` | Yes | Full English description | Non-empty, max 1000 chars |
| `description_cn` | `str` | Yes | Full Chinese description | Non-empty, max 1000 chars |
| `short_description_en` | `str` | Yes | Brief English summary | Non-empty, max 200 chars |
| `short_description_cn` | `str` | Yes | Brief Chinese summary | Non-empty, max 200 chars |
| `vocabulary_size` | `str` | Yes | Typical vocab range | Format: "500-1000" or "10000+" |
| `example_words` | `list[str]` | Yes | Representative words | 3-6 words, non-empty list |
| `learning_context` | `str` | No | Typical learner profile | Max 500 chars |

#### 2.2 Validation Rules

```python
def validate_cefr_definition(definition: dict) -> tuple[bool, str]:
    """
    Validate CEFR definition entry.

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    required_fields = [
        "level_code", "name_en", "name_cn",
        "description_en", "description_cn",
        "short_description_en", "short_description_cn",
        "vocabulary_size", "example_words"
    ]

    for field in required_fields:
        if field not in definition or not definition[field]:
            return False, f"Missing required field: {field}"

    # Validate level_code
    valid_levels = ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]
    if definition["level_code"] not in valid_levels:
        return False, f"Invalid level_code. Must be one of: {valid_levels}"

    # Validate bilingual names
    if len(definition["name_en"]) > 50:
        return False, "name_en exceeds 50 characters"
    if len(definition["name_cn"]) > 50:
        return False, "name_cn exceeds 50 characters"

    # Validate descriptions
    if len(definition["description_en"]) > 1000:
        return False, "description_en exceeds 1000 characters"
    if len(definition["description_cn"]) > 1000:
        return False, "description_cn exceeds 1000 characters"

    # Validate short descriptions
    if len(definition["short_description_en"]) > 200:
        return False, "short_description_en exceeds 200 characters"
    if len(definition["short_description_cn"]) > 200:
        return False, "short_description_cn exceeds 200 characters"

    # Validate example_words
    if not isinstance(definition["example_words"], list):
        return False, "example_words must be a list"
    if not (3 <= len(definition["example_words"]) <= 6):
        return False, "example_words must contain 3-6 words"

    return True, ""
```

#### 2.3 Persistence Strategy

**Format**: Static JSON file (`data/cefr_definitions.json`)

**Structure**:
```json
{
  "version": "1.0",
  "last_updated": "2025-11-04",
  "source": "Council of Europe CEFR + vocabulary context adaptation",
  "levels": {
    "A1": { /* definition */ },
    "A2": { /* definition */ },
    "B1": { /* definition */ },
    "B2": { /* definition */ },
    "C1": { /* definition */ },
    "C2": { /* definition */ },
    "C2+": { /* definition */ }
  }
}
```

**Load Strategy**:
- Load once at application startup
- Store in memory (small data size ~20KB)
- No persistence needed (read-only)

#### 2.4 Operations

```python
class CEFRDefinitionLoader:
    """Operations for CEFR definitions."""

    def load(self, file_path: str) -> bool:
        """
        Load CEFR definitions from JSON file.

        Args:
            file_path: Path to cefr_definitions.json

        Returns:
            True if successful

        Side Effects:
            - Populates in-memory dict
            - Validates all 7 levels present

        Time Complexity: O(1) - fixed 7 levels
        """
        pass

    def get_by_level(self, level_code: str) -> Optional[dict]:
        """
        Get definition for specific CEFR level.

        Args:
            level_code: CEFR level (A1-C2+)

        Returns:
            Definition dict or None if invalid level

        Time Complexity: O(1)
        """
        pass

    def get_all(self) -> dict[str, dict]:
        """
        Get all CEFR definitions.

        Returns:
            Dict mapping level_code to definition

        Time Complexity: O(1)
        """
        pass

    def validate_all(self) -> list[str]:
        """
        Validate all loaded definitions.

        Returns:
            List of validation errors (empty if valid)

        Time Complexity: O(1) - fixed 7 levels
        """
        pass
```

#### 2.5 Example Data

```json
{
  "version": "1.0",
  "last_updated": "2025-11-04",
  "source": "Council of Europe CEFR + vocabulary context adaptation",
  "levels": {
    "B2": {
      "level_code": "B2",
      "name_en": "Upper Intermediate",
      "name_cn": "中高级",
      "short_description_en": "Can interact with fluency and spontaneity",
      "short_description_cn": "能够流畅自发地互动",
      "description_en": "Can understand the main ideas of complex text on both concrete and abstract topics, including technical discussions in their field of specialization. Can interact with a degree of fluency and spontaneity that makes regular interaction with native speakers quite possible without strain for either party.",
      "description_cn": "能够理解具体和抽象主题的复杂文本的主要思想，包括其专业领域的技术讨论。能够以一定程度的流利和自发性进行互动，使与母语者的常规互动在双方都没有压力的情况下成为可能。",
      "vocabulary_size": "3000-5000",
      "example_words": ["sophisticated", "analyze", "circumstances", "nevertheless", "furthermore"],
      "learning_context": "Typical learner: University student, professional, 3-5 years of study / 典型学习者：大学生、专业人士、学习3-5年"
    }
  }
}
```

---

### 3. TranslationRequest

**Purpose**: Runtime-only entity representing a translation request. No persistence required.

**Use Cases**:
- API request validation
- Translation service input
- Logging and debugging
- Request tracking in web UI

#### 3.1 Fields

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `source_text` | `str` | Yes | Text to translate | Non-empty, max 500 chars |
| `translation_type` | `str` | Yes | Content type | Enum: `word`, `phrase`, `sentence` |
| `user_context` | `str` | No | Additional context hint | Max 200 chars, optional |
| `requested_at` | `datetime` | Yes | Request timestamp | Auto-generated |
| `request_id` | `str` | No | Unique request ID | UUID4 format |

#### 3.2 Lifecycle

```
Created → Validated → Processed → Discarded
   ↓          ↓            ↓            ↓
Request   Check      Call        No persistence
object    rules    translator     (ephemeral)
```

**State Transitions**:
1. **Created**: User submits translation request via API
2. **Validated**: Check source_text non-empty, translation_type valid
3. **Processed**: Pass to TranslationChain, get result
4. **Discarded**: Return result to user, object garbage collected

**No Persistence**: This entity is never saved to disk. Results are cached in `TranslationCache`, but requests themselves are transient.

#### 3.3 Validation Rules

```python
def validate_translation_request(request: dict) -> tuple[bool, str]:
    """
    Validate translation request.

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    if "source_text" not in request or not request["source_text"]:
        return False, "source_text is required"

    if "translation_type" not in request:
        return False, "translation_type is required"

    # Validate source_text
    if len(request["source_text"]) == 0:
        return False, "source_text cannot be empty"
    if len(request["source_text"]) > 500:
        return False, "source_text exceeds 500 characters"

    # Validate translation_type
    valid_types = ["word", "phrase", "sentence"]
    if request["translation_type"] not in valid_types:
        return False, f"Invalid translation_type. Must be one of: {valid_types}"

    # Validate user_context (optional)
    if "user_context" in request and request["user_context"]:
        if len(request["user_context"]) > 200:
            return False, "user_context exceeds 200 characters"

    return True, ""
```

#### 3.4 Operations

```python
class TranslationRequest:
    """Runtime translation request."""

    @classmethod
    def from_dict(cls, data: dict) -> "TranslationRequest":
        """
        Create request from API payload.

        Args:
            data: Request dictionary

        Returns:
            TranslationRequest instance

        Raises:
            ValidationError: If data invalid
        """
        pass

    def to_dict(self) -> dict:
        """
        Serialize request to dict.

        Returns:
            Request data as dictionary
        """
        pass

    def infer_type(self) -> str:
        """
        Infer translation type from source_text.

        Returns:
            Inferred type (word/phrase/sentence)

        Logic:
            - 1 word → "word"
            - 2-5 words → "phrase"
            - 6+ words → "sentence"
        """
        pass
```

#### 3.5 Example Data

```python
# Example 1: Word translation request
{
    "source_text": "sophisticated",
    "translation_type": "word",
    "user_context": "from vocabulary analysis",
    "requested_at": 1730736000,
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
}

# Example 2: Phrase translation request
{
    "source_text": "run out of patience",
    "translation_type": "phrase",
    "user_context": None,
    "requested_at": 1730736100,
    "request_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
}

# Example 3: Sentence translation request
{
    "source_text": "Time is running out for us to act.",
    "translation_type": "sentence",
    "user_context": "example sentence from results page",
    "requested_at": 1730736200,
    "request_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

---

### 4. MdictDictionary

**Purpose**: Reference to available Mdict (.mdx) dictionaries for enhanced translation.

**Use Cases**:
- Auto-discover .mdx files in data/dictionaries/
- Load dictionaries on-demand (lazy loading)
- Query words with SQLite-indexed lookups
- Handle missing/corrupted dictionaries gracefully

#### 4.1 Fields

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `dictionary_name` | `str` | Yes | Display name | Non-empty, derived from filename |
| `file_path` | `Path` | Yes | Path to .mdx file | Must exist if is_available=True |
| `priority` | `int` | Yes | Lookup order | Range: 1-10, lower = higher priority |
| `is_available` | `bool` | Yes | Successfully loaded | Set to False if load fails |
| `last_checked` | `datetime` | Yes | Last availability check | Unix timestamp |
| `index_path` | `Path` | No | SQLite index file | Auto-generated: {file_path}.db |
| `entry_count` | `int` | No | Total entries | Set after indexing |
| `load_error` | `str` | No | Error message if failed | Max 500 chars |

#### 4.2 Validation Rules

```python
def validate_mdict_dictionary(dictionary: dict) -> tuple[bool, str]:
    """
    Validate Mdict dictionary entry.

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    required_fields = ["dictionary_name", "file_path", "priority",
                       "is_available", "last_checked"]

    for field in required_fields:
        if field not in dictionary:
            return False, f"Missing required field: {field}"

    # Validate dictionary_name
    if not dictionary["dictionary_name"]:
        return False, "dictionary_name cannot be empty"

    # Validate file_path
    file_path = Path(dictionary["file_path"])
    if dictionary["is_available"] and not file_path.exists():
        return False, f"file_path does not exist: {file_path}"

    # Validate priority
    if not (1 <= dictionary["priority"] <= 10):
        return False, "priority must be between 1 and 10"

    # Validate is_available
    if not isinstance(dictionary["is_available"], bool):
        return False, "is_available must be boolean"

    return True, ""
```

#### 4.3 Persistence Strategy

**Auto-Discovery**: Scan `data/dictionaries/*.mdx` at startup

**In-Memory Storage**: Dictionary metadata stored in memory, .mdx files loaded on-demand

**No JSON File**: Dictionaries are discovered dynamically, not persisted to config

**SQLite Indexes**:
- Generated on first load: `{mdx_file}.db`
- Persisted to disk for fast subsequent loads
- Rebuilds if .mdx modified date changes

#### 4.4 Operations

```python
class DictionaryManager:
    """Operations for Mdict dictionaries."""

    def discover_dictionaries(self) -> dict[str, str]:
        """
        Discover available .mdx files in directory.

        Returns:
            Dict mapping dictionary_name to file_path

        Side Effects:
            - Scans data/dictionaries/ directory
            - Updates internal registry

        Time Complexity: O(n) where n = files in directory
        """
        pass

    def get_available(self) -> list[str]:
        """
        Get list of successfully loaded dictionaries.

        Returns:
            List of dictionary names

        Time Complexity: O(1)
        """
        pass

    def query_word(self, word: str, preferred_dict: Optional[str] = None) -> Optional[str]:
        """
        Query word in dictionaries.

        Args:
            word: Word to look up
            preferred_dict: Try this dictionary first (optional)

        Returns:
            HTML definition or None if not found

        Strategy:
            1. Try preferred_dict if specified
            2. Try dictionaries by priority order
            3. Return first match

        Time Complexity: O(k * log m) where k = dictionaries, m = entries per dict
        """
        pass

    def load_dictionary(self, dict_name: str) -> bool:
        """
        Load a specific dictionary (lazy loading).

        Args:
            dict_name: Dictionary identifier

        Returns:
            True if loaded successfully

        Side Effects:
            - Builds SQLite index if not exists
            - Updates is_available flag
            - Sets load_error if fails

        Time Complexity: O(n * log n) for initial indexing, O(1) for cached
        """
        pass

    def get_load_errors(self) -> dict[str, str]:
        """
        Get dictionary loading errors.

        Returns:
            Dict mapping dictionary_name to error message

        Time Complexity: O(1)
        """
        pass
```

#### 4.5 Example Data

```python
# In-memory registry (not persisted)
{
    "OALD9": {
        "dictionary_name": "OALD9",
        "file_path": Path("data/dictionaries/OALD9.mdx"),
        "priority": 1,
        "is_available": True,
        "last_checked": 1730736000,
        "index_path": Path("data/dictionaries/OALD9.mdx.db"),
        "entry_count": 100000,
        "load_error": None
    },
    "LDOCE6": {
        "dictionary_name": "LDOCE6",
        "file_path": Path("data/dictionaries/LDOCE6.mdx"),
        "priority": 2,
        "is_available": True,
        "last_checked": 1730736000,
        "index_path": Path("data/dictionaries/LDOCE6.mdx.db"),
        "entry_count": 230000,
        "load_error": None
    },
    "Collins": {
        "dictionary_name": "Collins",
        "file_path": Path("data/dictionaries/Collins.mdx"),
        "priority": 3,
        "is_available": False,
        "last_checked": 1730736000,
        "index_path": None,
        "entry_count": None,
        "load_error": "File corrupted: Invalid MDX header"
    }
}
```

---

### 5. BilingualString

**Purpose**: UI string localization for English/Chinese dual-display interface.

**Use Cases**:
- Render bilingual labels, buttons, headers
- Error messages in both languages
- Navigation menu items
- Form field labels

#### 5.1 Fields

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `key` | `str` | Yes | Unique identifier | Non-empty, snake_case, max 100 chars |
| `text_en` | `str` | Yes | English text | Non-empty, max 500 chars |
| `text_cn` | `str` | Yes | Chinese text | Non-empty, max 500 chars |
| `context` | `str` | No | Usage context | Max 200 chars, optional |
| `category` | `str` | No | Grouping category | Max 50 chars, e.g., "navigation", "errors" |

#### 5.2 Validation Rules

```python
def validate_bilingual_string(entry: dict) -> tuple[bool, str]:
    """
    Validate bilingual string entry.

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    required_fields = ["key", "text_en", "text_cn"]

    for field in required_fields:
        if field not in entry or not entry[field]:
            return False, f"Missing required field: {field}"

    # Validate key
    if len(entry["key"]) > 100:
        return False, "key exceeds 100 characters"
    if not entry["key"].replace("_", "").replace(".", "").isalnum():
        return False, "key must be alphanumeric with underscores/dots (snake_case)"

    # Validate text_en
    if len(entry["text_en"]) > 500:
        return False, "text_en exceeds 500 characters"

    # Validate text_cn
    if len(entry["text_cn"]) > 500:
        return False, "text_cn exceeds 500 characters"

    return True, ""
```

#### 5.3 Persistence Strategy

**Format**: JSON file (`data/ui_strings.json`) or embedded in templates

**Structure**:
```json
{
  "version": "1.0",
  "last_updated": "2025-11-04",
  "strings": {
    "navigation.home": {
      "key": "navigation.home",
      "text_en": "Home",
      "text_cn": "首页",
      "context": "Main navigation menu",
      "category": "navigation"
    },
    "errors.file_too_large": {
      "key": "errors.file_too_large",
      "text_en": "File size exceeds 10MB limit",
      "text_cn": "文件大小超过 10MB 限制",
      "context": "File upload validation error",
      "category": "errors"
    }
  }
}
```

**Load Strategy**:
- Load once at application startup
- Store in memory (small data size)
- Pass to templates via Flask context

#### 5.4 Operations

```python
class BilingualStringLoader:
    """Operations for bilingual UI strings."""

    def load(self, file_path: str) -> bool:
        """
        Load bilingual strings from JSON file.

        Args:
            file_path: Path to ui_strings.json

        Returns:
            True if successful

        Side Effects:
            - Populates in-memory dict

        Time Complexity: O(n) where n = total strings
        """
        pass

    def get_bilingual(self, key: str) -> Optional[dict]:
        """
        Get bilingual string by key.

        Args:
            key: String identifier

        Returns:
            Dict with text_en and text_cn, or None if not found

        Time Complexity: O(1)
        """
        pass

    def get_all_strings(self, category: Optional[str] = None) -> dict[str, dict]:
        """
        Get all strings or filter by category.

        Args:
            category: Optional category filter

        Returns:
            Dict mapping key to string data

        Time Complexity: O(n) for filtered, O(1) for all
        """
        pass

    def format_bilingual(self, key: str, separator: str = " / ") -> str:
        """
        Format bilingual string for display.

        Args:
            key: String identifier
            separator: Separator between languages

        Returns:
            Formatted string: "English / 中文"

        Example:
            format_bilingual("navigation.home") → "Home / 首页"

        Time Complexity: O(1)
        """
        pass
```

#### 5.5 Example Data

```json
{
  "version": "1.0",
  "last_updated": "2025-11-04",
  "strings": {
    "navigation.home": {
      "key": "navigation.home",
      "text_en": "Home",
      "text_cn": "首页",
      "context": "Main navigation menu",
      "category": "navigation"
    },
    "navigation.upload": {
      "key": "navigation.upload",
      "text_en": "Upload",
      "text_cn": "上传",
      "context": "Main navigation menu",
      "category": "navigation"
    },
    "buttons.analyze": {
      "key": "buttons.analyze",
      "text_en": "Analyze",
      "text_cn": "分析",
      "context": "Upload form submit button",
      "category": "buttons"
    },
    "errors.file_too_large": {
      "key": "errors.file_too_large",
      "text_en": "File size exceeds 10MB limit",
      "text_cn": "文件大小超过 10MB 限制",
      "context": "File upload validation error",
      "category": "errors"
    },
    "errors.invalid_format": {
      "key": "errors.invalid_format",
      "text_en": "Invalid file format",
      "text_cn": "无效的文件格式",
      "context": "File upload validation error",
      "category": "errors"
    },
    "labels.supported_formats": {
      "key": "labels.supported_formats",
      "text_en": "Supported formats: TXT, PDF, DOCX, JSON",
      "text_cn": "支持的格式: TXT, PDF, DOCX, JSON",
      "context": "File upload hint",
      "category": "labels"
    },
    "loading.translating": {
      "key": "loading.translating",
      "text_en": "Translating...",
      "text_cn": "翻译中...",
      "context": "Translation in progress",
      "category": "loading"
    }
  }
}
```

---

## Entity Relationships

### Relationship Diagram

```
┌─────────────────────┐
│  TranslationRequest │ (runtime only)
└──────────┬──────────┘
           │
           │ creates
           ▼
┌─────────────────────┐      ┌──────────────────┐
│  TranslationChain   │─────▶│ TranslationCache │
└──────────┬──────────┘      └──────────────────┘
           │                  (persistent)
           │ queries
           │
    ┌──────┴──────┬─────────────────┐
    │             │                 │
    ▼             ▼                 ▼
┌─────────┐  ┌──────────────┐  ┌───────────┐
│ ECDICT  │  │ MdictManager │  │   Argos   │
│ Matcher │  └──────┬───────┘  │ Translate │
└─────────┘         │          └───────────┘
                    │
                    │ manages
                    ▼
            ┌──────────────────┐
            │ MdictDictionary  │ (multiple instances)
            └──────────────────┘


┌──────────────────┐
│ CEFRDefinition   │ (static data)
└──────────────────┘
          │
          │ provides
          ▼
┌──────────────────┐
│   CEFR Badges    │ (UI components)
└──────────────────┘


┌──────────────────┐
│ BilingualString  │ (static data)
└──────────────────┘
          │
          │ provides
          ▼
┌──────────────────┐
│   UI Templates   │ (Flask/Jinja2)
└──────────────────┘
```

### Relationship Details

| Entity A | Entity B | Relationship | Cardinality | Description |
|----------|----------|--------------|-------------|-------------|
| `TranslationRequest` | `TranslationChain` | uses | 1:1 | Each request processed by chain |
| `TranslationChain` | `TranslationCache` | reads/writes | 1:1 | Chain checks cache before fallback |
| `TranslationChain` | `ECDICT` | queries | 1:1 | First tier of fallback |
| `TranslationChain` | `MdictManager` | queries | 1:1 | Second tier of fallback |
| `TranslationChain` | `ArgosTranslate` | queries | 1:1 | Third tier of fallback |
| `MdictManager` | `MdictDictionary` | manages | 1:N | Manager controls multiple dictionaries |
| `CEFRDefinition` | `UI Components` | provides data | 1:N | Definitions shown in badges/modals |
| `BilingualString` | `UI Templates` | provides data | 1:N | Strings rendered in templates |

---

## Data Flow Diagrams

### Translation Request Flow

```
User Request
    │
    ▼
┌───────────────────────┐
│ Validate Request      │
│ (TranslationRequest)  │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ Check Cache           │
│ (TranslationCache)    │
└───────┬───────────────┘
        │
    Cache Hit? ──Yes──▶ Return Cached Result
        │
        No
        │
        ▼
┌───────────────────────┐
│ Tier 1: ECDICT        │
└───────┬───────────────┘
        │
    Found? ──Yes──▶ Cache & Return
        │
        No
        │
        ▼
┌───────────────────────┐
│ Tier 2: Mdict         │
└───────┬───────────────┘
        │
    Found? ──Yes──▶ Cache & Return
        │
        No
        │
        ▼
┌───────────────────────┐
│ Tier 3: Argos         │
└───────┬───────────────┘
        │
    Found? ──Yes──▶ Cache & Return
        │
        No
        │
        ▼
Return "Translation Unavailable"
```

### CEFR Display Flow

```
Page Load
    │
    ▼
┌───────────────────────┐
│ Load CEFR Definitions │
│ (CEFRDefinitionLoader)│
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ Render Vocabulary     │
│ with CEFR Badges      │
└───────┬───────────────┘
        │
        ▼
User Hovers ──▶ Show Tooltip
        │          (short description)
        │
        ▼
User Clicks ──▶ Show Modal
                   (full description +
                    examples + context)
```

### Mdict Discovery Flow

```
Application Startup
    │
    ▼
┌───────────────────────┐
│ Scan dictionaries/    │
│ Directory for .mdx    │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ Create MdictDictionary│
│ Entries (lazy load)   │
└───────┬───────────────┘
        │
        ▼
First Lookup Request
    │
    ▼
┌───────────────────────┐
│ Load Dictionary       │
│ (build SQLite index)  │
└───────┬───────────────┘
        │
        ▼
Index Exists? ──Yes──▶ Load Fast
        │
        No
        │
        ▼
Build New Index
(30-60 seconds)
```

---

## Persistence Strategies

### Summary Table

| Entity | Storage Format | Location | Load Strategy | Write Strategy | Size Estimate |
|--------|---------------|----------|---------------|----------------|---------------|
| `TranslationCache` | JSON | `data/translation_cache.json` | On startup | On exit + periodic | ~100KB-1MB |
| `CEFRDefinition` | JSON | `data/cefr_definitions.json` | On startup | Never (static) | ~20KB |
| `TranslationRequest` | None | N/A | N/A | N/A | N/A (ephemeral) |
| `MdictDictionary` | .mdx + SQLite | `data/dictionaries/*.mdx` | Lazy (on first use) | Never (user-provided) | ~400MB per dict |
| `BilingualString` | JSON | `data/ui_strings.json` | On startup | Never (static) | ~5KB |

### File Structure

```
data/
├── translation_cache.json          # Persistent cache (read/write)
├── cefr_definitions.json           # Static data (read-only)
├── ui_strings.json                 # Static data (read-only)
├── dictionaries/
│   ├── OALD9.mdx                   # User-provided (read-only)
│   ├── OALD9.mdx.db                # Generated index (read-only after creation)
│   ├── LDOCE6.mdx                  # User-provided (read-only)
│   ├── LDOCE6.mdx.db               # Generated index (read-only after creation)
│   └── README.md                   # Setup instructions
└── translation_models/
    └── (Argos Translate packages)  # Auto-downloaded (~100MB)
```

### Backup and Recovery

**Translation Cache**:
- Auto-saved on application exit
- Periodic saves every 5 minutes if dirty
- Can be safely deleted (cache will rebuild)

**CEFR Definitions & UI Strings**:
- Version-controlled static files
- No backup needed (part of codebase)

**Mdict Dictionaries**:
- User-provided files (not version-controlled)
- SQLite indexes can be rebuilt if corrupted
- Users responsible for backing up .mdx files

---

## Schema Examples

### Complete TranslationCache Example

```json
{
  "version": "1.0",
  "last_saved": 1730736000,
  "metadata": {
    "total_entries": 150,
    "cache_hit_rate": 0.82,
    "last_cleanup": 1730700000
  },
  "entries": {
    "word:sophisticated": {
      "source_text": "sophisticated",
      "target_text": "a. 精密的, 复杂的, 久经世故的, 老练的",
      "timestamp": 1730735000,
      "translation_type": "word",
      "source": "ecdict",
      "confidence_score": 0.95,
      "access_count": 8
    },
    "phrase:blow up": {
      "source_text": "blow up",
      "target_text": "爆炸；(风、暴风雨等)发作；发怒；充气；放大(照片)",
      "timestamp": 1730735200,
      "translation_type": "phrase",
      "source": "mdict",
      "confidence_score": 0.90,
      "access_count": 3
    },
    "sentence:Time is running out.": {
      "source_text": "Time is running out.",
      "target_text": "时间不多了。",
      "timestamp": 1730735400,
      "translation_type": "sentence",
      "source": "argos",
      "confidence_score": 0.75,
      "access_count": 1
    }
  }
}
```

### Complete CEFRDefinition Example

```json
{
  "version": "1.0",
  "last_updated": "2025-11-04",
  "source": "Council of Europe CEFR + vocabulary context adaptation",
  "levels": {
    "A1": {
      "level_code": "A1",
      "name_en": "Beginner",
      "name_cn": "初级",
      "short_description_en": "Can understand and use familiar everyday expressions",
      "short_description_cn": "能够理解和使用熟悉的日常表达",
      "description_en": "Can understand and use familiar everyday expressions and very basic phrases aimed at the satisfaction of needs of a concrete type. Can introduce themselves and others and can ask and answer questions about personal details such as where they live, people they know and things they have.",
      "description_cn": "能够理解和使用旨在满足具体需求的熟悉的日常表达和非常基本的短语。能够介绍自己和他人，能够询问和回答有关个人详细信息的问题，例如他们住在哪里、认识的人和拥有的东西。",
      "vocabulary_size": "500-1000",
      "example_words": ["hello", "thank", "yes", "no", "please", "help"],
      "learning_context": "Typical learner: Absolute beginner, tourist learning survival phrases, 0-6 months of study / 典型学习者：绝对初学者、学习生存短语的游客、学习0-6个月"
    },
    "B2": {
      "level_code": "B2",
      "name_en": "Upper Intermediate",
      "name_cn": "中高级",
      "short_description_en": "Can interact with fluency and spontaneity",
      "short_description_cn": "能够流畅自发地互动",
      "description_en": "Can understand the main ideas of complex text on both concrete and abstract topics, including technical discussions in their field of specialization. Can interact with a degree of fluency and spontaneity that makes regular interaction with native speakers quite possible without strain for either party.",
      "description_cn": "能够理解具体和抽象主题的复杂文本的主要思想，包括其专业领域的技术讨论。能够以一定程度的流利和自发性进行互动，使与母语者的常规互动在双方都没有压力的情况下成为可能。",
      "vocabulary_size": "3000-5000",
      "example_words": ["sophisticated", "analyze", "circumstances", "nevertheless", "furthermore"],
      "learning_context": "Typical learner: University student, professional, 3-5 years of study / 典型学习者：大学生、专业人士、学习3-5年"
    }
  }
}
```

### Complete BilingualString Example

```json
{
  "version": "1.0",
  "last_updated": "2025-11-04",
  "categories": ["navigation", "buttons", "labels", "errors", "loading"],
  "strings": {
    "navigation.home": {
      "key": "navigation.home",
      "text_en": "Home",
      "text_cn": "首页",
      "context": "Main navigation menu - homepage link",
      "category": "navigation"
    },
    "navigation.upload": {
      "key": "navigation.upload",
      "text_en": "Upload",
      "text_cn": "上传",
      "context": "Main navigation menu - upload page link",
      "category": "navigation"
    },
    "navigation.results": {
      "key": "navigation.results",
      "text_en": "Results",
      "text_cn": "结果",
      "context": "Main navigation menu - results page link",
      "category": "navigation"
    },
    "buttons.analyze": {
      "key": "buttons.analyze",
      "text_en": "Analyze",
      "text_cn": "分析",
      "context": "Upload form submit button",
      "category": "buttons"
    },
    "buttons.translate": {
      "key": "buttons.translate",
      "text_en": "Translate",
      "text_cn": "翻译",
      "context": "Translation request button",
      "category": "buttons"
    },
    "labels.file_input": {
      "key": "labels.file_input",
      "text_en": "File",
      "text_cn": "文件",
      "context": "File upload input label",
      "category": "labels"
    },
    "labels.supported_formats": {
      "key": "labels.supported_formats",
      "text_en": "Supported formats: TXT, PDF, DOCX, JSON",
      "text_cn": "支持的格式: TXT, PDF, DOCX, JSON",
      "context": "File upload format hint",
      "category": "labels"
    },
    "errors.file_too_large": {
      "key": "errors.file_too_large",
      "text_en": "File size exceeds 10MB limit",
      "text_cn": "文件大小超过 10MB 限制",
      "context": "File upload size validation error",
      "category": "errors"
    },
    "errors.invalid_format": {
      "key": "errors.invalid_format",
      "text_en": "Invalid file format",
      "text_cn": "无效的文件格式",
      "context": "File upload format validation error",
      "category": "errors"
    },
    "errors.translation_unavailable": {
      "key": "errors.translation_unavailable",
      "text_en": "Translation unavailable",
      "text_cn": "翻译不可用",
      "context": "Translation service error",
      "category": "errors"
    },
    "loading.translating": {
      "key": "loading.translating",
      "text_en": "Translating...",
      "text_cn": "翻译中...",
      "context": "Translation in progress indicator",
      "category": "loading"
    },
    "loading.loading_model": {
      "key": "loading.loading_model",
      "text_en": "Loading translation model (first time only)...",
      "text_cn": "正在加载翻译模型（仅第一次）...",
      "context": "Argos Translate lazy loading indicator",
      "category": "loading"
    }
  }
}
```

---

## Validation Rules

### Cross-Entity Validation

**Translation Cache ↔ Translation Request**:
```python
def validate_cache_request_consistency(
    cache_entry: dict,
    request: dict
) -> tuple[bool, str]:
    """
    Validate cache entry matches request parameters.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if cache_entry["source_text"] != request["source_text"]:
        return False, "source_text mismatch"

    if cache_entry["translation_type"] != request["translation_type"]:
        return False, "translation_type mismatch"

    return True, ""
```

**CEFR Definition Completeness**:
```python
def validate_all_cefr_levels_present(definitions: dict) -> tuple[bool, str]:
    """
    Validate all 7 CEFR levels are defined.

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_levels = ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]

    for level in required_levels:
        if level not in definitions["levels"]:
            return False, f"Missing CEFR level: {level}"

    return True, ""
```

**Mdict Dictionary Availability**:
```python
def validate_mdict_availability(dictionary: dict) -> tuple[bool, str]:
    """
    Validate Mdict dictionary is usable.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if dictionary["is_available"]:
        # If marked available, file must exist
        if not Path(dictionary["file_path"]).exists():
            return False, "File does not exist but is_available=True"

        # If index_path specified, must exist
        if dictionary.get("index_path"):
            if not Path(dictionary["index_path"]).exists():
                return False, "Index file does not exist"

    return True, ""
```

### Business Logic Validation

**Translation Type Inference**:
```python
def infer_translation_type(text: str) -> str:
    """
    Infer translation type from text content.

    Logic:
        - 1 word → "word"
        - 2-5 words → "phrase"
        - 6+ words → "sentence"

    Returns:
        Inferred type
    """
    word_count = len(text.split())

    if word_count == 1:
        return "word"
    elif word_count <= 5:
        return "phrase"
    else:
        return "sentence"
```

**Cache Expiration Check**:
```python
def is_cache_entry_expired(entry: dict, max_age_days: int = 30) -> bool:
    """
    Check if cache entry should be evicted.

    Args:
        entry: Cache entry
        max_age_days: Maximum age in days

    Returns:
        True if expired
    """
    import time

    cutoff = int(time.time()) - (max_age_days * 24 * 60 * 60)
    return entry["timestamp"] < cutoff
```

---

## Summary

This data model specification defines five core entities for the bilingual UI feature:

1. **TranslationCache**: Persistent cache for translation results (JSON)
2. **CEFRDefinition**: Static CEFR level descriptions (JSON)
3. **TranslationRequest**: Runtime-only translation request (ephemeral)
4. **MdictDictionary**: Reference to optional .mdx dictionaries (auto-discovered)
5. **BilingualString**: UI localization strings (JSON)

### Key Design Decisions

- **JSON over Database**: Simplicity and portability for static/semi-static data
- **Lazy Loading**: Dictionaries and translation models loaded on-demand
- **Graceful Degradation**: Handle missing dictionaries/models without crashing
- **Dual-Display**: Always show English and Chinese simultaneously
- **Offline-First**: All data stored locally, no external dependencies

### File Locations

```
data/
├── translation_cache.json          # 100KB-1MB
├── cefr_definitions.json           # ~20KB
├── ui_strings.json                 # ~5KB
├── dictionaries/
│   ├── *.mdx                       # ~400MB each (user-provided)
│   └── *.mdx.db                    # ~50MB each (auto-generated)
└── translation_models/
    └── (Argos packages)            # ~100MB (auto-downloaded)
```

### Next Steps

1. Implement entity classes in `src/vocab_analyzer/translation/`
2. Create data files in `data/`
3. Write unit tests for validation rules
4. Integrate with existing ECDICT LevelMatcher
5. Build Flask API endpoints for translation requests

---

**Document Status**: ✅ Complete
**Last Updated**: 2025-11-04
**Next Document**: [API Contracts](./api-contracts.md)
