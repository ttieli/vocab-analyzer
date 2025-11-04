#!/usr/bin/env python3
"""
Data preparation script for vocab-analyzer.

This script processes ECDICT data to create a CEFR-classified wordlist.
"""
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


class DataPreparer:
    """Prepare and convert vocabulary data."""

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "data"
        self.ecdict_path = self.data_dir / "dictionaries" / "ECDICT" / "ecdict.csv"
        self.output_path = self.data_dir / "vocabularies" / "cefr_wordlist.csv"

    def prepare_cefr_wordlist(self) -> None:
        """
        Extract and classify vocabulary from ECDICT.

        Creates a CEFR wordlist with levels based on:
        - Oxford 3000 markers
        - Word frequency (BNC/COCA)
        - Collins star ratings
        """
        print("Loading ECDICT data...")
        
        if not self.ecdict_path.exists():
            print(f"Error: ECDICT not found at {self.ecdict_path}")
            print("Please download ECDICT first.")
            return

        # Load ECDICT (may take a few seconds for 770K words)
        try:
            df = pd.read_csv(
                self.ecdict_path,
                usecols=["word", "translation", "pos", "collins", "oxford", "tag", "frq", "phonetic"],
                low_memory=False,
            )
            print(f"✓ Loaded {len(df):,} words from ECDICT")
        except Exception as e:
            print(f"Error loading ECDICT: {e}")
            return

        # Assign CEFR levels
        print("Assigning CEFR levels...")
        df["level"] = df.apply(self._assign_level, axis=1)

        # Filter to words with assigned levels
        df_classified = df[df["level"].notna()].copy()

        # Select and rename columns
        output_df = df_classified[
            ["word", "level", "pos", "translation", "phonetic", "collins", "oxford", "frq"]
        ].copy()

        # Sort by level then frequency
        level_order = {"A1": 0, "A2": 1, "B1": 2, "B2": 3, "C1": 4, "C2": 5, "C2+": 6}
        output_df["level_num"] = output_df["level"].map(level_order)
        output_df = output_df.sort_values(["level_num", "frq"], ascending=[True, False])
        output_df = output_df.drop(columns=["level_num"])

        # Save
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        output_df.to_csv(self.output_path, index=False, encoding="utf-8")

        print(f"\n✓ Created CEFR wordlist: {self.output_path}")
        print(f"  Total words: {len(output_df):,}")
        print("\nLevel distribution:")
        for level in ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]:
            count = len(output_df[output_df["level"] == level])
            pct = count / len(output_df) * 100
            print(f"  {level}: {count:6,} ({pct:5.1f}%)")

    def _assign_level(self, row) -> Optional[str]:
        """Assign CEFR level based on multiple factors."""
        collins = int(row.get("collins", 0)) if pd.notna(row.get("collins")) else 0
        oxford = int(row.get("oxford", 0)) if pd.notna(row.get("oxford")) else 0
        frq = int(row.get("frq", 0)) if pd.notna(row.get("frq")) else 0

        # Oxford 3000 words with high frequency -> A1/A2
        if oxford == 1:
            if collins >= 5 or frq >= 50000:
                return "A1"
            elif collins >= 4 or frq >= 30000:
                return "A2"
            elif frq >= 15000:
                return "B1"

        # Frequency and Collins-based classification
        if frq >= 15000 or collins >= 3:
            return "B1"
        elif frq >= 8000 or collins >= 2:
            return "B2"
        elif frq >= 3000 or collins >= 1:
            return "C1"
        elif frq >= 1000:
            return "C2"
        elif frq > 0 or collins > 0:
            return "C2+"

        return None  # Skip words with no frequency/rating data

    def convert_phrasal_verbs(self) -> None:
        """Convert phrasal verbs JSON to CSV format."""
        json_path = self.data_dir / "phrases" / "phrasal-verbs" / "common.json"
        csv_path = self.data_dir / "phrases" / "phrasal_verbs.csv"

        if not json_path.exists():
            print(f"Phrasal verbs JSON not found: {json_path}")
            return

        print("\nConverting phrasal verbs to CSV...")

        with open(json_path, "r", encoding="utf-8") as f:
            phrases = json.load(f)

        # Convert to CSV
        rows = []
        for phrase in phrases:
            verb = phrase.get("verb", "")
            # Parse separability
            separable = "*" in verb
            clean_verb = verb.replace("*", "").replace("+", "").strip()
            clean_verb = " ".join(clean_verb.split())  # Normalize spacing

            rows.append(
                {
                    "phrase": clean_verb,
                    "original_notation": verb,
                    "separable": separable,
                    "definition": phrase.get("definition", ""),
                    "examples": " | ".join(phrase.get("examples", [])),
                }
            )

        df = pd.DataFrame(rows)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_path, index=False, encoding="utf-8")

        print(f"✓ Converted {len(df)} phrasal verbs to: {csv_path}")


def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = "."

    preparer = DataPreparer(base_dir)

    print("=" * 60)
    print("Vocab Analyzer - Data Preparation")
    print("=" * 60)

    # Task 1: Create CEFR wordlist
    preparer.prepare_cefr_wordlist()

    # Task 2: Convert phrasal verbs
    preparer.convert_phrasal_verbs()

    print("\n" + "=" * 60)
    print("✅ Data preparation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
