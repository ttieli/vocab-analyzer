#!/usr/bin/env python3
"""
Data validation script for vocab-analyzer.

Validates vocabulary data, phrasal verbs, and sample books.
"""
import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd


class DataValidator:
    """Validate vocabulary and phrase data."""

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "data"
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """Run all validations."""
        print("=" * 60)
        print("Vocab Analyzer - Data Validation")
        print("=" * 60)

        # Validate vocabulary
        self.validate_vocabulary()

        # Validate phrasal verbs
        self.validate_phrasal_verbs()

        # Validate sample books
        self.validate_sample_books()

        # Summary
        print("\n" + "=" * 60)
        if self.errors:
            print(f"❌ Validation FAILED with {len(self.errors)} errors")
            for error in self.errors:
                print(f"  ERROR: {error}")
        else:
            print("✅ Validation PASSED")

        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} warnings:")
            for warning in self.warnings:
                print(f"  WARNING: {warning}")

        print("=" * 60)

        return len(self.errors) == 0, self.errors, self.warnings

    def validate_vocabulary(self) -> None:
        """Validate CEFR wordlist."""
        print("\n1. Validating vocabulary data...")

        wordlist_path = self.data_dir / "vocabularies" / "cefr_wordlist.csv"
        ecdict_path = self.data_dir / "dictionaries" / "ECDICT" / "ecdict.csv"

        # Check ECDICT exists
        if not ecdict_path.exists():
            self.errors.append(f"ECDICT not found: {ecdict_path}")
            return

        try:
            df = pd.read_csv(ecdict_path, low_memory=False)
            print(f"  ✓ ECDICT loaded: {len(df):,} words")

            # Validate columns
            required_cols = ["word", "translation", "pos", "collins", "oxford", "frq"]
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                self.errors.append(f"ECDICT missing columns: {missing}")
            else:
                print(f"  ✓ ECDICT has all required columns")

            # Check for duplicates
            duplicates = df["word"].duplicated().sum()
            if duplicates > 0:
                self.warnings.append(f"ECDICT has {duplicates} duplicate words")

            # Validate CEFR wordlist if it exists
            if wordlist_path.exists():
                wl_df = pd.read_csv(wordlist_path)
                print(f"  ✓ CEFR wordlist loaded: {len(wl_df):,} words")

                # Check level distribution
                if "level" in wl_df.columns:
                    levels = wl_df["level"].value_counts()
                    print("  ✓ Level distribution:")
                    for level in ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]:
                        if level in levels:
                            print(f"    {level}: {levels[level]:,}")

                    # Validate minimum words per level
                    if levels.get("A1", 0) < 100:
                        self.warnings.append("Low A1 word count (< 100)")
                else:
                    self.errors.append("CEFR wordlist missing 'level' column")
            else:
                self.warnings.append(
                    f"CEFR wordlist not found: {wordlist_path} (run prepare_data.py)"
                )

        except Exception as e:
            self.errors.append(f"Failed to load vocabulary: {e}")

    def validate_phrasal_verbs(self) -> None:
        """Validate phrasal verbs data."""
        print("\n2. Validating phrasal verbs...")

        json_path = self.data_dir / "phrases" / "phrasal-verbs" / "common.json"
        csv_path = self.data_dir / "phrases" / "phrasal_verbs.csv"

        # Check JSON file
        if not json_path.exists():
            self.errors.append(f"Phrasal verbs JSON not found: {json_path}")
            return

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                phrases = json.load(f)

            print(f"  ✓ Loaded {len(phrases)} phrasal verbs from JSON")

            # Validate structure
            required_keys = {"verb", "definition"}
            for i, phrase in enumerate(phrases[:5]):  # Check first 5
                missing = required_keys - set(phrase.keys())
                if missing:
                    self.errors.append(f"Phrase {i} missing keys: {missing}")
                    break
            else:
                print(f"  ✓ Phrasal verb structure valid")

            # Check CSV if it exists
            if csv_path.exists():
                csv_df = pd.read_csv(csv_path)
                print(f"  ✓ CSV version loaded: {len(csv_df)} phrasal verbs")
            else:
                self.warnings.append(
                    f"CSV version not found: {csv_path} (run prepare_data.py)"
                )

        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in phrasal verbs: {e}")
        except Exception as e:
            self.errors.append(f"Failed to load phrasal verbs: {e}")

    def validate_sample_books(self) -> None:
        """Validate sample books."""
        print("\n3. Validating sample books...")

        books_dir = self.data_dir / "sample_books"

        if not books_dir.exists():
            self.warnings.append(f"Sample books directory not found: {books_dir}")
            return

        books = list(books_dir.glob("*.txt"))

        if not books:
            self.warnings.append("No sample books found")
            return

        print(f"  ✓ Found {len(books)} sample book(s)")

        for book_path in books:
            try:
                with open(book_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if len(content) < 100:
                    self.warnings.append(f"{book_path.name} is very short (< 100 chars)")
                else:
                    word_count = len(content.split())
                    print(f"    {book_path.name}: {word_count:,} words")

            except UnicodeDecodeError:
                self.errors.append(f"{book_path.name} has encoding issues (not UTF-8)")
            except Exception as e:
                self.errors.append(f"Failed to read {book_path.name}: {e}")


def main():
    """Main entry point."""
    import sys

    base_dir = sys.argv[1] if len(sys.argv) > 1 else "."

    validator = DataValidator(base_dir)
    success, errors, warnings = validator.validate_all()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
