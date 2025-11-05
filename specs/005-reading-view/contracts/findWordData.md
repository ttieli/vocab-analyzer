# Contract: findWordData()

**Purpose**: Look up word data from analysis results by normalized token

**Location**: `src/vocab_analyzer/web/static/app.js` (new function)

---

## Function Signature

```javascript
/**
 * Find word data in analysis results lookup map
 * 
 * @param {string} token - Raw token from text (e.g., "ambitious", "make-up", "WORD!")
 * @param {Map<string, Object>} wordLookupMap - Pre-indexed map of words/phrasal verbs
 * @returns {Object|null} - Word data object or null if not found
 */
function findWordData(token, wordLookupMap) {
    // Implementation...
}
```

---

## Input Specification

### Parameter 1: `token` (string)

**Source**: Tokenized word from `processedText.split(/(\s+)/)`

**Format**: Raw token with possible punctuation, mixed case

**Examples**:
- `"ambitious"` → matches "ambitious"
- `"Ambitious"` → matches "ambitious" (case-insensitive)
- `"ambitious."` → matches "ambitious" (punctuation stripped)
- `"make-up"` → matches "make-up" (hyphenated phrasal verb)
- `"WORD!"` → matches "word" (case-insensitive + punctuation)
- `"   "` → returns null (whitespace only)

**Validation**:
- MUST handle null/undefined gracefully (return null)
- MUST normalize: lowercase + strip non-word characters

### Parameter 2: `wordLookupMap` (Map<string, Object>)

**Source**: Built in `parseTextForReading()` from `analysisResults`

**Structure**:
```javascript
Map {
    "ambitious" => {
        word: "ambitious",
        cefr_level: "C1",
        count: 12,
        examples: [...],
        type: "word"
    },
    "make up" => {
        word: "make up",  // Normalized from "phrase" key
        cefr_level: "B1",
        count: 5,
        examples: [...],
        type: "phrasal_verb"
    },
    // ... more entries
}
```

**Keys**: Lowercase normalized word/phrase  
**Values**: Word data object with `type` field added

---

## Output Specification

### Return Value: `Object | null`

**Success Case** (word found):
```javascript
{
    word: "ambitious",
    cefr_level: "C1",
    count: 12,
    examples: ["The ambitious entrepreneur...", "..."],
    type: "word"  // or "phrasal_verb"
}
```

**Failure Case** (word not found):
```javascript
null
```

---

## Processing Algorithm

### Step 1: Validate Input

```javascript
if (!token || typeof token !== 'string') {
    return null;
}
```

### Step 2: Normalize Token

```javascript
// Lowercase + strip non-word characters (keep hyphens for phrasal verbs)
const normalized = token.toLowerCase().replace(/[^\w-]/g, '');

if (!normalized || normalized.length === 0) {
    return null;  // Empty after normalization
}
```

### Step 3: Lookup in Map

```javascript
const wordData = wordLookupMap.get(normalized);
return wordData || null;
```

---

## Normalization Rules

| Input Token | Normalized | Rationale |
|-------------|-----------|-----------|
| `"Ambitious"` | `"ambitious"` | Case-insensitive matching |
| `"ambitious."` | `"ambitious"` | Remove trailing punctuation |
| `"'ambitious'"` | `"ambitious"` | Remove quotes |
| `"make-up"` | `"make-up"` | Preserve hyphens (phrasal verbs) |
| `"make up"` | `"makeup"` | Space removed (but map should have "make up" key) |
| `"WORD!!!"` | `"word"` | Lowercase + remove punctuation |
| `"123"` | `"123"` | Numbers preserved (rare edge case) |
| `"   "` | `""` | Empty string → null |

**Note**: Multi-word phrasal verbs are NOT handled in this function. Only first word is colored (per spec clarification). Full phrasal verb detection happens in `handleWordClick()`.

---

## Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| **Token is null/undefined** | Return null |
| **Token is empty string** | Return null |
| **Token is whitespace only** | Return null after normalization |
| **Token not in map** | Return null |
| **Token has unicode characters** | Normalize and lookup (should work) |
| **Token is number** | Preserve number, lookup (unlikely to match) |
| **Token has multiple hyphens** | Preserve hyphens, lookup |

---

## Performance Requirements

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Lookup Time** | O(1) | Map lookup is constant time |
| **Per-Token Processing** | <0.001ms | Simple string operations |
| **50,000 Tokens** | <50ms total | Acceptable for rendering budget |

---

## Integration Points

### Called By:
- `parseTextForReading()` - For each token in processed text

### Calls:
- None (pure function, no external dependencies)

---

## Testing Checklist

- [ ] Returns correct word data for exact match
- [ ] Returns correct word data for case-insensitive match
- [ ] Returns correct word data for punctuation-stripped match
- [ ] Returns null for token not in map
- [ ] Returns null for empty string
- [ ] Returns null for whitespace-only string
- [ ] Returns null for null/undefined input
- [ ] Handles unicode characters correctly
- [ ] Preserves hyphens in phrasal verbs
- [ ] Performs O(1) lookup (verified with profiling)

---

**Status**: ✅ Contract Defined - Ready for Implementation
