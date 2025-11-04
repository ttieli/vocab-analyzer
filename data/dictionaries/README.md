# Dictionary Files

This directory contains dictionary data files used by the vocabulary analyzer for translations and definitions.

## ECDICT (Included)

The `ECDICT/` subdirectory contains the English-Chinese dictionary database (SQLite format) that provides:
- Fast word lookups (<1ms per query)
- Chinese translations for common English words
- Base definitions and word forms

**Status**: ✅ Already configured and working

## Mdict Dictionaries (Optional)

You can optionally add professional English dictionaries in Mdict (.mdx) format to enhance translation quality and provide detailed definitions.

### Recommended Dictionaries

1. **Oxford Advanced Learner's Dictionary 9th Edition (OALD9)**
   - File: `oald9.mdx` + `oald9.mdd` (resources)
   - Size: ~150MB
   - Best for: Detailed definitions, usage examples, learner-friendly explanations

2. **Longman Dictionary of Contemporary English 6th Edition (LDOCE6)**
   - File: `ldoce6.mdx` + `ldoce6.mdd`
   - Size: ~180MB
   - Best for: Natural English usage, collocations, spoken/written distinctions

3. **Collins COBUILD Advanced Dictionary**
   - File: `collins.mdx`
   - Size: ~120MB
   - Best for: Full-sentence definitions, real-world examples

### How to Obtain Mdict Dictionaries

**Important**: Due to copyright restrictions, we cannot provide dictionary files directly. You must obtain them through legal channels:

1. **Purchase**: Buy official dictionaries that include .mdx files
2. **Personal Use**: If you own physical/digital dictionaries, some communities share .mdx conversions for personal use
3. **Search**: Look for "mdx dictionary download" with the specific dictionary name

**Note**: Ensure you comply with copyright laws in your jurisdiction.

### Installation

1. Download the .mdx file (and .mdd resource file if available)
2. Place the files in this `data/dictionaries/` directory:
   ```
   data/dictionaries/
   ├── ECDICT/           # Existing
   ├── oald9.mdx         # Optional
   ├── oald9.mdd         # Optional
   ├── ldoce6.mdx        # Optional
   └── README.md         # This file
   ```

3. Restart the application - dictionaries will be auto-detected

### Verification

Run this command to verify dictionaries are detected:

```bash
python -c "from vocab_analyzer.translation.dictionary import MdictDictionaryManager; mgr = MdictDictionaryManager(); print(mgr.list_available())"
```

You should see a list of available dictionaries with their priorities.

## Translation Fallback Chain

The system uses dictionaries in the following order:

1. **ECDICT** (Primary) - Fast lookup for basic translations
2. **Mdict** (Secondary) - Professional dictionaries for detailed definitions
3. **Argos Translate** (Fallback) - Neural translation for any content not in dictionaries

This ensures you always get a translation, with the best quality available for each word.

## Troubleshooting

**Issue**: "Dictionary not detected"
- **Solution**: Ensure .mdx file is directly in `data/dictionaries/`, not in a subdirectory

**Issue**: "Dictionary query slow"
- **Solution**: Place .mdd resource files next to .mdx files for faster lookup

**Issue**: "Permission denied"
- **Solution**: Run `chmod 644 *.mdx *.mdd` to fix file permissions

## More Information

See `specs/002-bilingual-ui-translation/quickstart.md` for detailed setup instructions.
