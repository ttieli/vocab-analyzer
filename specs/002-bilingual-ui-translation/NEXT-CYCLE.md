# Feature 002: Next Development Cycle

**Cycle 2 Focus**: Web UI Integration (Phase 3 completion)
**Target**: Complete T018-T028 (11 tasks)
**Estimated Progress**: 28% → 45% overall

---

## 🎯 Cycle 2 Objectives

Complete bilingual web interface integration by:
1. Creating/updating HTML templates with bilingual structure
2. Adding CSS styling for dual-language display
3. Implementing JavaScript utilities for client-side features
4. Integrating BilingualStringLoader into Flask routes
5. Creating translation API endpoints
6. Writing integration and unit tests

---

## 📋 Task Checklist (T018-T028)

### Templates & Styling (T018-T021)

- [ ] **T018**: Update `src/vocab_analyzer/web/templates/base.html`
  - Add bilingual layout structure
  - Integrate BilingualStringLoader
  - Create Jinja2 macros for bilingual text
  - Add language toggle (optional)

- [ ] **T019**: Update `src/vocab_analyzer/web/templates/upload.html`
  - Use bilingual strings for labels and buttons
  - Update form with dual-language hints
  - Add translated error messages

- [ ] **T020**: Update `src/vocab_analyzer/web/templates/results.html`
  - Bilingual headings and labels
  - CEFR badges with tooltips
  - Statistics in both languages
  - Vocabulary tables with translations

- [ ] **T021**: Create `src/vocab_analyzer/web/static/styles.css`
  - Bilingual text layout styles
  - English/Chinese font stacks
  - Responsive dual-language display
  - CEFR badge styling

### JavaScript & Interactivity (T022)

- [ ] **T022** [P]: Create `src/vocab_analyzer/web/static/bilingual.js`
  - String formatting utilities
  - Language toggle functionality (if implemented)
  - Client-side string caching
  - Dynamic content updates

### Backend Integration (T023-T024)

- [ ] **T023**: Update `src/vocab_analyzer/web/routes.py`
  - Import and initialize BilingualStringLoader
  - Pass string loader to all templates
  - Add `ui_strings` to Jinja2 context
  - Update existing routes (upload, results, index)

- [ ] **T024**: Add API endpoint in `src/vocab_analyzer/web/app.py`
  - GET `/api/ui/strings` - Return all UI strings
  - GET `/api/ui/strings/<key>` - Return specific string
  - Optional: GET `/api/ui/strings?category=<cat>`

### Testing (T025-T026-T028)

- [ ] **T025** [P]: Create `tests/web/test_bilingual_ui.py`
  - Test template rendering with bilingual strings
  - Test string loader integration in routes
  - Test missing string handling
  - Test category filtering

- [ ] **T026**: Manual browser testing
  - Test in Chrome, Firefox, Safari
  - Verify Chinese font rendering
  - Check responsive layouts
  - Test on mobile devices

- [ ] **T028** [P]: Create `tests/web/test_translation_api.py`
  - Test translation API endpoints
  - Test error handling
  - Test caching behavior
  - Test confidence scores

### Translation API (T027)

- [ ] **T027**: Add translation endpoint in `src/vocab_analyzer/web/app.py`
  - POST `/api/translate` - Translation requests
  - Request body: `{"text": "...", "type": "word|phrase|sentence"}`
  - Response: TranslationResult as JSON
  - Integrate TranslationChain
  - Add rate limiting (optional)

---

## 🔧 Implementation Guide

### 1. Start with Backend (T023)

**File**: `src/vocab_analyzer/web/routes.py`

```python
from vocab_analyzer.translation import get_loader

# Initialize loader at module level
ui_strings = get_loader()

@app.route('/')
def index():
    return render_template('index.html', ui_strings=ui_strings)

@app.route('/upload')
def upload():
    return render_template('upload.html', ui_strings=ui_strings)
```

### 2. Update Base Template (T018)

**File**: `src/vocab_analyzer/web/templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{{ ui_strings.get_bilingual('headings.app_title')['text_en'] }}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <nav>
        <a href="/">{{ ui_strings.format_bilingual('navigation.home') }}</a>
        <a href="/upload">{{ ui_strings.format_bilingual('navigation.upload') }}</a>
        <a href="/results">{{ ui_strings.format_bilingual('navigation.results') }}</a>
    </nav>

    {% block content %}{% endblock %}

    <script src="{{ url_for('static', filename='bilingual.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### 3. Create Jinja2 Macro

**In base.html**:

```jinja2
{% macro bilingual(key, separator=' / ') %}
    {{ ui_strings.format_bilingual(key, separator) }}
{% endmacro %}

{% macro english(key) %}
    {{ ui_strings.get_english(key) }}
{% endmacro %}

{% macro chinese(key) %}
    {{ ui_strings.get_chinese(key) }}
{% endmacro %}
```

### 4. Add Translation API (T027)

**File**: `src/vocab_analyzer/web/app.py`

```python
from vocab_analyzer.translation import TranslationChain
from flask import request, jsonify

# Initialize translation chain
translation_chain = TranslationChain(
    ecdict_matcher=level_matcher  # From existing setup
)

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400

    text = data['text']
    translation_type = data.get('type', 'word')

    result = translation_chain.translate(text, translation_type)

    return jsonify(result.to_dict())
```

---

## 📦 Required Imports

For Flask routes:
```python
from vocab_analyzer.translation import (
    get_loader,           # Bilingual strings
    TranslationChain,     # Translation service
    get_config           # Configuration
)
```

For tests:
```python
from vocab_analyzer.translation import (
    BilingualStringLoader,
    TranslationChain,
    TranslationResult
)
```

---

## ✅ Success Criteria

Phase 3 is complete when:
- [X] All HTML templates use bilingual strings
- [X] UI displays English and Chinese simultaneously
- [X] Translation API endpoints functional
- [X] All integration tests passing
- [X] Manual browser testing complete
- [X] No hardcoded English-only text in templates

---

## 🚀 Quick Start Commands

```bash
# Run all tests
pytest tests/translation/ tests/web/ -v --cov

# Run web server for manual testing
python -m vocab_analyzer.web.app

# Test translation API
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "hello", "type": "word"}'

# Get UI strings via API
curl http://localhost:5000/api/ui/strings
```

---

## 📚 Reference Files

**Infrastructure (already complete)**:
- `src/vocab_analyzer/translation/strings.py` - BilingualStringLoader
- `src/vocab_analyzer/translation/fallback.py` - TranslationChain
- `data/ui_strings.json` - UI string data

**To be created/modified**:
- `src/vocab_analyzer/web/templates/base.html`
- `src/vocab_analyzer/web/templates/upload.html`
- `src/vocab_analyzer/web/templates/results.html`
- `src/vocab_analyzer/web/static/styles.css`
- `src/vocab_analyzer/web/static/bilingual.js`
- `src/vocab_analyzer/web/routes.py` (update)
- `src/vocab_analyzer/web/app.py` (update)
- `tests/web/test_bilingual_ui.py`
- `tests/web/test_translation_api.py`

---

**Estimated Time**: 4-6 hours
**Complexity**: Medium (mostly integration work)
**Dependencies**: All Phase 2 infrastructure complete ✅
