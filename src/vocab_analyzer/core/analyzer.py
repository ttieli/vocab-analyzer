"""
Main VocabularyAnalyzer facade class.
"""
from pathlib import Path
from typing import Optional

from ..extractors import DocxExtractor, JsonExtractor, PdfExtractor, TxtExtractor
from ..matchers.level_matcher import LevelMatcher
from ..models import Phrase, VocabularyAnalysis, Word
from ..processors.phrase_detector import PhraseDetector
from ..processors.tokenizer import Tokenizer
from ..utils import get_file_extension, validate_file_for_analysis
from .config import Config


class VocabularyAnalyzer:
    """
    Main facade class for vocabulary analysis.

    Orchestrates the complete pipeline:
    1. Extract text from file
    2. Tokenize and process with NLP
    3. Match words to CEFR levels
    4. Generate analysis results
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize VocabularyAnalyzer.

        Args:
            config: Configuration object (uses default if not provided)
        """
        self.config = config or Config()

        # Initialize components
        self.tokenizer = Tokenizer(
            model_name=self.config.nlp_model,
            batch_size=self.config.nlp_batch_size,
            disable_components=self.config.get("nlp.disable_components", ["ner"]),
        )

        # Initialize level matcher
        vocab_file = self.config.get_data_path("ecdict")
        phrases_file = self.config.get_data_path("phrases")
        self.level_matcher = LevelMatcher(
            vocabulary_file=str(vocab_file),
            phrases_file=str(phrases_file) if phrases_file and phrases_file.exists() else None,
            use_cache=self.config.cache_vocabulary,
        )

        # Initialize phrase detector (shares spaCy model with tokenizer)
        self.phrase_detector = PhraseDetector(nlp=self.tokenizer._get_nlp_model())

        # Whether to detect phrases
        self.detect_phrases = self.config.get("analysis.detect_phrases", True)

        # Initialize extractors
        self.extractors = {
            "txt": TxtExtractor(encoding=self.config.get("extraction.encoding", "utf-8")),
            "pdf": PdfExtractor(
                max_pages=self.config.get("extraction.pdf_max_pages", 1000)
            ),
            "docx": DocxExtractor(
                max_paragraphs=self.config.get("extraction.docx_max_paragraphs", 10000)
            ),
            "json": JsonExtractor(text_field=self.config.get("extraction.text_field", "text")),
        }

    def analyze(self, file_path: str) -> VocabularyAnalysis:
        """
        Analyze vocabulary in a file.

        Complete pipeline:
        1. Validate file
        2. Extract text
        3. Tokenize
        4. Filter tokens
        5. Match levels
        6. Build Word objects
        7. Create VocabularyAnalysis

        Args:
            file_path: Path to file to analyze

        Returns:
            VocabularyAnalysis object with results

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format unsupported or invalid
        """
        # 1. Validate file
        is_valid, error = validate_file_for_analysis(file_path)
        if not is_valid:
            raise ValueError(error)

        # 2. Extract text
        text = self._extract_text(file_path)

        # 3. Tokenize
        tokens = self.tokenizer.tokenize(text)

        # 4. Filter tokens
        filtered_tokens = self.tokenizer.filter_tokens(
            tokens,
            exclude_stop_words=True,
            exclude_punctuation=self.config.exclude_punctuation,
            exclude_digits=self.config.exclude_numbers,
            min_length=self.config.min_word_length,
            max_length=self.config.max_word_length,
        )

        # 5-7. Process tokens and build analysis
        analysis = self._build_analysis(file_path, filtered_tokens, text)

        return analysis

    def _extract_text(self, file_path: str) -> str:
        """
        Extract text from file based on extension.

        Args:
            file_path: Path to file

        Returns:
            Extracted text

        Raises:
            ValueError: If file format is unsupported
        """
        ext = get_file_extension(file_path)

        if ext not in self.extractors:
            raise ValueError(
                f"Unsupported file format: .{ext}. "
                f"Supported formats: {list(self.extractors.keys())}"
            )

        extractor = self.extractors[ext]
        text = extractor.extract(file_path)

        return text

    def _build_analysis(
        self, file_path: str, tokens: list, full_text: str
    ) -> VocabularyAnalysis:
        """
        Build VocabularyAnalysis from processed tokens.

        Args:
            file_path: Source file path
            tokens: Filtered token list
            full_text: Original full text for example extraction

        Returns:
            VocabularyAnalysis object
        """
        analysis = VocabularyAnalysis(
            source_file=file_path,
            processed_text=full_text
        )

        # Group tokens by lemma
        word_data = {}

        for token in tokens:
            lemma = token["lemma"]

            if lemma not in word_data:
                word_data[lemma] = {
                    "original_forms": set(),
                    "count": 0,
                    "pos": token.get("pos", ""),
                }

            word_data[lemma]["original_forms"].add(token["text"])
            word_data[lemma]["count"] += 1

        # Create Word objects
        for lemma, data in word_data.items():
            # Get level and translation from matcher
            level = self.level_matcher.get_word_level(
                lemma, default=self.config.default_level_unknown
            )

            translation = self.level_matcher.get_translation(lemma)

            # Map spaCy POS to simpler categories
            pos = self._simplify_pos(data["pos"])

            # Create Word object
            word = Word(
                word=lemma,
                level=level,
                word_type=pos,
                definition_cn=translation,
                frequency=data["count"],
                original_forms=list(data["original_forms"]),
            )

            # Add examples if configured
            if self.config.include_examples:
                examples = self._extract_examples(
                    lemma, full_text, max_examples=self.config.max_examples_per_word
                )
                for example in examples:
                    word.add_example(example)

            # Add to analysis
            analysis.add_word(word)

        # Detect and add phrasal verbs if enabled
        if self.detect_phrases and self.level_matcher.is_phrases_loaded():
            phrases = self._detect_phrases(full_text)
            for phrase in phrases:
                analysis.add_phrase(phrase)

        return analysis

    def _extract_examples(self, word: str, text: str, max_examples: int = 3) -> list:
        """
        Extract example sentences containing a word.

        Args:
            word: Word to find examples for
            text: Full text to search
            max_examples: Maximum number of examples

        Returns:
            List of example sentences
        """
        from ..utils import extract_sentences_with_word

        sentences = extract_sentences_with_word(text, word, max_sentences=max_examples)
        return sentences

    def _detect_phrases(self, text: str) -> list:
        """
        Detect phrasal verbs in text.

        Args:
            text: Text to analyze for phrases

        Returns:
            List of Phrase objects
        """
        # Detect phrasal verbs
        detected = self.phrase_detector.detect_from_text(text)

        # Convert to Phrase objects with level matching
        phrases = self.phrase_detector.create_phrase_objects(
            detected,
            level_matcher=self.level_matcher,
            default_level=self.config.get("analysis.default_phrase_level", "B2"),
        )

        return phrases

    def _simplify_pos(self, pos: str) -> str:
        """
        Map spaCy POS tags to simpler categories.

        Args:
            pos: spaCy POS tag (NOUN, VERB, ADJ, etc.)

        Returns:
            Simplified POS tag (noun, verb, adj, adv, etc.)
        """
        pos_map = {
            "NOUN": "noun",
            "VERB": "verb",
            "ADJ": "adj",
            "ADV": "adv",
            "PRON": "pron",
            "DET": "det",
            "ADP": "prep",
            "NUM": "num",
            "CONJ": "conj",
            "INTJ": "intj",
            "PROPN": "propn",
        }

        return pos_map.get(pos, "other")

    def analyze_text(self, text: str, source_name: str = "text_input") -> VocabularyAnalysis:
        """
        Analyze vocabulary in raw text (without file).

        Args:
            text: Text to analyze
            source_name: Name to use for the source (default: "text_input")

        Returns:
            VocabularyAnalysis object
        """
        if not text.strip():
            raise ValueError("Text cannot be empty")

        # Tokenize
        tokens = self.tokenizer.tokenize(text)

        # Filter
        filtered_tokens = self.tokenizer.filter_tokens(
            tokens,
            exclude_stop_words=True,
            exclude_punctuation=self.config.exclude_punctuation,
            exclude_digits=self.config.exclude_numbers,
            min_length=self.config.min_word_length,
            max_length=self.config.max_word_length,
        )

        # Build analysis
        analysis = self._build_analysis(source_name, filtered_tokens, text)

        return analysis

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"VocabularyAnalyzer("
            f"model='{self.config.nlp_model}', "
            f"vocab_loaded={self.level_matcher.is_loaded()})"
        )
