"""
Phrase detector for identifying phrasal verbs and multi-word expressions.
"""
from typing import List, Optional, Set
import spacy
from spacy.tokens import Doc, Token

from ..models.phrase import Phrase


class PhraseDetector:
    """
    Detector for phrasal verbs and multi-word expressions in text.
    
    Uses spaCy dependency parsing to identify verb + particle combinations.
    """
    
    def __init__(self, nlp=None):
        """
        Initialize PhraseDetector.
        
        Args:
            nlp: spaCy language model (optional, will load default if None)
        """
        self.nlp = nlp
        if self.nlp is None:
            import spacy
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                raise RuntimeError(
                    "spaCy model 'en_core_web_sm' not found. "
                    "Install with: python -m spacy download en_core_web_sm"
                )
        
        # Particles that commonly form phrasal verbs
        self.common_particles = {
            "up", "down", "out", "in", "on", "off", "away", "back",
            "over", "through", "around", "about", "by", "along", "across",
            "forward", "forth", "together", "apart"
        }
        
        # Dependency relations indicating phrasal verbs
        self.phrasal_dependencies = {"prt", "prep", "advmod"}
    
    def detect_phrasal_verbs(self, doc: Doc) -> List[dict]:
        """
        Detect phrasal verbs in a spaCy Doc object.
        
        Args:
            doc: Processed spaCy Doc
            
        Returns:
            List of detected phrasal verb dictionaries
        """
        detected_phrases = []
        processed_tokens = set()  # Track processed tokens to avoid duplicates
        
        for token in doc:
            # Skip if already processed or not a verb
            if token.i in processed_tokens or token.pos_ not in ["VERB", "AUX"]:
                continue
            
            # Look for particles/prepositions related to this verb
            for child in token.children:
                if self._is_phrasal_particle(child, token):
                    # Found a potential phrasal verb
                    verb_phrase = self._extract_phrasal_verb(token, child)
                    
                    if verb_phrase:
                        detected_phrases.append(verb_phrase)
                        processed_tokens.add(token.i)
                        processed_tokens.add(child.i)
        
        return detected_phrases
    
    def _is_phrasal_particle(self, token: Token, verb: Token) -> bool:
        """
        Check if a token is a particle forming a phrasal verb.
        
        Args:
            token: Potential particle token
            verb: Verb token
            
        Returns:
            True if token is a phrasal particle
        """
        # Check dependency relation
        if token.dep_ not in self.phrasal_dependencies:
            return False
        
        # Check if it's a common particle
        if token.lemma_.lower() not in self.common_particles:
            return False
        
        # Check head is the verb
        if token.head != verb:
            return False
        
        return True
    
    def _extract_phrasal_verb(self, verb: Token, particle: Token) -> Optional[dict]:
        """
        Extract phrasal verb information.
        
        Args:
            verb: Verb token
            particle: Particle token
            
        Returns:
            Dictionary with phrasal verb info, or None
        """
        # Get lemmatized forms
        verb_lemma = verb.lemma_.lower()
        particle_lemma = particle.lemma_.lower()
        
        # Create phrasal verb string
        phrase_text = f"{verb_lemma} {particle_lemma}"
        
        # Check if separable (heuristic: if particle comes after direct object)
        separable = self._check_if_separable(verb, particle)
        
        # Get sentence context
        sent_text = verb.sent.text.strip()
        
        return {
            "phrase": phrase_text,
            "separable": separable,
            "sentence": sent_text,
            "start_char": verb.idx,
            "end_char": particle.idx + len(particle.text),
        }
    
    def _check_if_separable(self, verb: Token, particle: Token) -> bool:
        """
        Check if phrasal verb is separable.
        
        Heuristic: If there's a direct object between verb and particle,
        it's likely separable (e.g., "pick the book up").
        
        Args:
            verb: Verb token
            particle: Particle token
            
        Returns:
            True if likely separable
        """
        # Check if particle comes after verb
        if particle.i <= verb.i:
            return False
        
        # Check for direct object between verb and particle
        for child in verb.children:
            if child.dep_ in ["dobj", "obj"]:
                # Object exists and is between verb and particle
                if verb.i < child.i < particle.i:
                    return True
        
        # Default: not separable
        return False
    
    def detect_from_text(self, text: str) -> List[dict]:
        """
        Detect phrasal verbs from raw text.
        
        Args:
            text: Input text string
            
        Returns:
            List of detected phrasal verb dictionaries
        """
        doc = self.nlp(text)
        return self.detect_phrasal_verbs(doc)
    
    def batch_detect(self, texts: List[str], batch_size: int = 100) -> List[List[dict]]:
        """
        Detect phrasal verbs in multiple texts using batch processing.
        
        Args:
            texts: List of text strings
            batch_size: Batch size for spaCy processing
            
        Returns:
            List of lists of detected phrasal verbs
        """
        results = []
        
        for doc in self.nlp.pipe(texts, batch_size=batch_size):
            phrases = self.detect_phrasal_verbs(doc)
            results.append(phrases)
        
        return results
    
    def create_phrase_objects(
        self,
        detected_phrases: List[dict],
        level_matcher=None,
        default_level: str = "B2",
    ) -> List[Phrase]:
        """
        Convert detected phrase dictionaries to Phrase objects.
        
        Args:
            detected_phrases: List of detected phrase dicts
            level_matcher: LevelMatcher instance for level assignment
            default_level: Default level if matcher not provided
            
        Returns:
            List of Phrase objects
        """
        phrase_objects = []
        phrase_counts = {}  # Track frequency
        
        for phrase_dict in detected_phrases:
            phrase_text = phrase_dict["phrase"]
            
            # Count frequency
            if phrase_text not in phrase_counts:
                phrase_counts[phrase_text] = 0
            phrase_counts[phrase_text] += 1
            
            # Get level from matcher if available
            if level_matcher and level_matcher.is_phrases_loaded():
                phrase_info = level_matcher.match_phrase(phrase_text)
                if phrase_info:
                    level = phrase_info.get("level", default_level)
                    definition = phrase_info.get("definition", "")
                    separable = phrase_info.get("separable", phrase_dict.get("separable", False))
                else:
                    level = level_matcher.get_phrase_level(phrase_text, default_level)
                    definition = ""
                    separable = phrase_dict.get("separable", False)
            else:
                level = default_level
                definition = ""
                separable = phrase_dict.get("separable", False)
            
            # Create or update Phrase object
            existing = None
            for p in phrase_objects:
                if p.phrase == phrase_text:
                    existing = p
                    break
            
            if existing:
                # Update frequency and add example
                existing.frequency = phrase_counts[phrase_text]
                if phrase_dict.get("sentence"):
                    existing.add_example(phrase_dict["sentence"])
            else:
                # Create new Phrase object
                phrase_obj = Phrase(
                    phrase=phrase_text,
                    phrase_type="phrasal_verb",
                    level=level,
                    separable=separable,
                    definition=definition,
                    frequency=1,
                )
                
                if phrase_dict.get("sentence"):
                    phrase_obj.add_example(phrase_dict["sentence"])
                
                phrase_objects.append(phrase_obj)
        
        return phrase_objects


# Singleton instance for shared use
_phrase_detector = None


def get_phrase_detector(nlp=None) -> PhraseDetector:
    """
    Get global PhraseDetector instance.
    
    Args:
        nlp: spaCy model (optional)
        
    Returns:
        PhraseDetector instance
    """
    global _phrase_detector
    if _phrase_detector is None:
        _phrase_detector = PhraseDetector(nlp=nlp)
    return _phrase_detector
