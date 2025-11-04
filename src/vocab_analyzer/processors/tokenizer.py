"""
Tokenizer for text processing using spaCy.
"""
from typing import ClassVar, List, Optional

import spacy
from spacy.language import Language


class Tokenizer:
    """
    Tokenizer using spaCy for NLP processing.

    Features:
    - Global spaCy model loading (singleton pattern)
    - Batch processing for performance
    - Lemmatization and POS tagging
    - Sentence segmentation
    """

    _nlp: ClassVar[Optional[Language]] = None  # Global spaCy model instance

    def __init__(
        self,
        model_name: str = "en_core_web_sm",
        batch_size: int = 100,
        disable_components: Optional[List[str]] = None,
    ):
        """
        Initialize Tokenizer.

        Args:
            model_name: spaCy model name (default: en_core_web_sm)
            batch_size: Batch size for nlp.pipe processing (default: 100)
            disable_components: Components to disable for performance (default: ["ner"])
        """
        self.model_name = model_name
        self.batch_size = batch_size
        self.disable_components = disable_components or ["ner"]

        # Load spaCy model (globally)
        self.nlp = self._get_nlp_model()

    @classmethod
    def _get_nlp_model(cls) -> Language:
        """
        Get or load the global spaCy model instance.

        Uses singleton pattern to load model only once.

        Returns:
            spaCy Language model

        Raises:
            OSError: If spaCy model cannot be loaded
        """
        if cls._nlp is None:
            try:
                cls._nlp = spacy.load("en_core_web_sm")
            except OSError:
                raise OSError(
                    "spaCy model 'en_core_web_sm' not found. "
                    "Please install it: python -m spacy download en_core_web_sm"
                )

        return cls._nlp

    def tokenize(self, text: str) -> List[dict]:
        """
        Tokenize text and extract linguistic features.

        Args:
            text: Input text to tokenize

        Returns:
            List of token dictionaries with keys:
                - text: Original token text
                - lemma: Lemmatized form
                - pos: Part of speech tag
                - is_alpha: Whether token is alphabetic
                - is_stop: Whether token is a stop word
                - is_punct: Whether token is punctuation
        """
        if not text.strip():
            return []

        # Process text with spaCy
        doc = self.nlp(text)

        tokens = []
        for token in doc:
            tokens.append(
                {
                    "text": token.text,
                    "lemma": token.lemma_.lower(),
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "is_alpha": token.is_alpha,
                    "is_stop": token.is_stop,
                    "is_punct": token.is_punct,
                    "is_digit": token.is_digit,
                }
            )

        return tokens

    def tokenize_batch(self, texts: List[str]) -> List[List[dict]]:
        """
        Tokenize multiple texts using batch processing for performance.

        Args:
            texts: List of texts to tokenize

        Returns:
            List of token lists (one per input text)
        """
        if not texts:
            return []

        # Use spaCy's pipe for batch processing
        results = []
        for doc in self.nlp.pipe(
            texts, batch_size=self.batch_size, disable=self.disable_components
        ):
            tokens = []
            for token in doc:
                tokens.append(
                    {
                        "text": token.text,
                        "lemma": token.lemma_.lower(),
                        "pos": token.pos_,
                        "tag": token.tag_,
                        "is_alpha": token.is_alpha,
                        "is_stop": token.is_stop,
                        "is_punct": token.is_punct,
                        "is_digit": token.is_digit,
                    }
                )
            results.append(tokens)

        return results

    def get_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using spaCy's sentence segmentation.

        Args:
            text: Input text

        Returns:
            List of sentences
        """
        if not text.strip():
            return []

        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    def lemmatize_word(self, word: str) -> str:
        """
        Lemmatize a single word.

        Args:
            word: Word to lemmatize

        Returns:
            Lemmatized form (lowercase)
        """
        doc = self.nlp(word)
        if doc:
            return doc[0].lemma_.lower()
        return word.lower()

    def get_pos_tag(self, word: str) -> str:
        """
        Get part-of-speech tag for a word.

        Args:
            word: Word to analyze

        Returns:
            POS tag (e.g., "NOUN", "VERB", "ADJ")
        """
        doc = self.nlp(word)
        if doc:
            return doc[0].pos_
        return ""

    def filter_tokens(
        self,
        tokens: List[dict],
        exclude_stop_words: bool = True,
        exclude_punctuation: bool = True,
        exclude_digits: bool = True,
        min_length: int = 2,
        max_length: int = 45,
    ) -> List[dict]:
        """
        Filter tokens based on criteria.

        Args:
            tokens: List of token dictionaries
            exclude_stop_words: Whether to exclude stop words
            exclude_punctuation: Whether to exclude punctuation
            exclude_digits: Whether to exclude digit tokens
            min_length: Minimum token length
            max_length: Maximum token length

        Returns:
            Filtered list of tokens
        """
        filtered = []

        for token in tokens:
            # Skip based on criteria
            if exclude_stop_words and token.get("is_stop"):
                continue

            if exclude_punctuation and token.get("is_punct"):
                continue

            if exclude_digits and token.get("is_digit"):
                continue

            # Check if alphabetic
            if not token.get("is_alpha"):
                continue

            # Check length
            lemma_length = len(token.get("lemma", ""))
            if lemma_length < min_length or lemma_length > max_length:
                continue

            filtered.append(token)

        return filtered

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"Tokenizer(model='{self.model_name}', "
            f"batch_size={self.batch_size}, "
            f"disable={self.disable_components})"
        )
