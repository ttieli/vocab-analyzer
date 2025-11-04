"""
Unit tests for MdictDictionary.

Tests dictionary discovery, lazy loading, word lookup, and graceful degradation.
Target coverage: 80%+ enforced by CI (pytest-cov with --cov-fail-under=80)
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

from src.vocab_analyzer.translation.dictionary import MdictDictionary


@pytest.fixture
def temp_dict_dir():
    """Create a temporary dictionaries directory for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture
def dict_manager(temp_dict_dir):
    """Create MdictDictionary instance with temp directory."""
    return MdictDictionary(dictionaries_dir=temp_dict_dir)


class TestMdictDictionaryInit:
    """Test dictionary manager initialization."""

    def test_init_creates_empty_manager(self, temp_dict_dir):
        """Manager initializes with empty dictionaries list."""
        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        assert manager.dictionaries_dir == temp_dict_dir
        assert manager.dictionaries == []
        assert manager.loaded_dicts == {}
        assert manager._readmdict is None

    def test_init_with_string_path(self):
        """Manager accepts string path for directory."""
        manager = MdictDictionary(dictionaries_dir="data/dictionaries")

        assert isinstance(manager.dictionaries_dir, Path)
        assert manager.dictionaries_dir == Path("data/dictionaries")

    def test_init_discovers_dictionaries(self, temp_dict_dir):
        """Manager auto-discovers dictionaries on init."""
        # Create fake .mdx files
        (temp_dict_dir / "oald9.mdx").touch()
        (temp_dict_dir / "ldoce6.mdx").touch()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        assert len(manager.dictionaries) == 2


class TestMdictDictionaryDiscovery:
    """Test dictionary discovery functionality."""

    def test_discover_no_dictionaries(self, dict_manager):
        """Discovery handles empty directory."""
        result = dict_manager.discover_dictionaries()

        assert result == []
        assert dict_manager.dictionaries == []

    def test_discover_single_dictionary(self, temp_dict_dir):
        """Discovery finds single .mdx file."""
        (temp_dict_dir / "test.mdx").touch()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        assert len(manager.dictionaries) == 1
        assert manager.dictionaries[0]["dictionary_name"] == "test"
        assert manager.dictionaries[0]["file_path"].name == "test.mdx"

    def test_discover_multiple_dictionaries(self, temp_dict_dir):
        """Discovery finds all .mdx files."""
        (temp_dict_dir / "dict1.mdx").touch()
        (temp_dict_dir / "dict2.mdx").touch()
        (temp_dict_dir / "dict3.mdx").touch()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        assert len(manager.dictionaries) == 3

    def test_discover_ignores_non_mdx_files(self, temp_dict_dir):
        """Discovery ignores non-.mdx files."""
        (temp_dict_dir / "test.mdx").touch()
        (temp_dict_dir / "test.txt").touch()
        (temp_dict_dir / "test.mdd").touch()
        (temp_dict_dir / "readme.md").touch()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        assert len(manager.dictionaries) == 1
        assert manager.dictionaries[0]["dictionary_name"] == "test"

    def test_discover_assigns_oald_priority(self, temp_dict_dir):
        """OALD dictionaries get priority 1."""
        (temp_dict_dir / "oald9.mdx").touch()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        assert manager.dictionaries[0]["priority"] == 1

    def test_discover_assigns_ldoce_priority(self, temp_dict_dir):
        """LDOCE dictionaries get priority 2."""
        (temp_dict_dir / "ldoce6.mdx").touch()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        assert manager.dictionaries[0]["priority"] == 2

    def test_discover_assigns_collins_priority(self, temp_dict_dir):
        """Collins dictionaries get priority 3."""
        (temp_dict_dir / "collins_cobuild.mdx").touch()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        assert manager.dictionaries[0]["priority"] == 3

    def test_discover_assigns_default_priority(self, temp_dict_dir):
        """Unknown dictionaries get default priority 5."""
        (temp_dict_dir / "custom_dict.mdx").touch()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        assert manager.dictionaries[0]["priority"] == 5

    def test_discover_sorts_by_priority(self, temp_dict_dir):
        """Dictionaries sorted by priority (lower first)."""
        (temp_dict_dir / "custom.mdx").touch()  # priority 5
        (temp_dict_dir / "collins.mdx").touch()  # priority 3
        (temp_dict_dir / "oald.mdx").touch()     # priority 1
        (temp_dict_dir / "ldoce.mdx").touch()    # priority 2

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        priorities = [d["priority"] for d in manager.dictionaries]
        assert priorities == [1, 2, 3, 5]

    def test_discover_sets_metadata_fields(self, temp_dict_dir):
        """Discovery sets all required metadata fields."""
        (temp_dict_dir / "test.mdx").touch()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        dict_info = manager.dictionaries[0]

        assert "dictionary_name" in dict_info
        assert "file_path" in dict_info
        assert "priority" in dict_info
        assert "is_available" in dict_info
        assert dict_info["is_available"] is False  # Not loaded yet
        assert "last_checked" in dict_info
        assert "index_path" in dict_info
        assert dict_info["index_path"] is None
        assert "entry_count" in dict_info
        assert dict_info["entry_count"] is None
        assert "load_error" in dict_info
        assert dict_info["load_error"] is None

    def test_discover_handles_missing_directory(self):
        """Discovery handles non-existent directory gracefully."""
        non_existent = Path("/nonexistent/path/dictionaries")
        manager = MdictDictionary(dictionaries_dir=non_existent)

        assert manager.dictionaries == []


class TestMdictDictionaryLoading:
    """Test dictionary lazy loading."""

    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_load_readmdict_success(self, mock_mdx, dict_manager):
        """readmdict library loads successfully."""
        with patch('src.vocab_analyzer.translation.dictionary.readmdict') as mock_readmdict:
            result = dict_manager._load_readmdict()

            assert result is True
            assert dict_manager._readmdict is not None

    def test_load_readmdict_import_error(self, dict_manager):
        """Returns False when readmdict not installed."""
        with patch.dict('sys.modules', {'readmdict': None}):
            result = dict_manager._load_readmdict()

            assert result is False

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    def test_load_readmdict_only_once(self, mock_readmdict, dict_manager):
        """readmdict loads only once (lazy loading)."""
        dict_manager._load_readmdict()
        first_ref = dict_manager._readmdict

        dict_manager._load_readmdict()
        second_ref = dict_manager._readmdict

        assert first_ref is second_ref

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_load_dictionary_success(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Dictionary loads successfully."""
        # Create fake .mdx file
        (temp_dict_dir / "test.mdx").touch()

        # Mock MDX instance
        mock_mdx = Mock()
        mock_mdx_class.return_value = mock_mdx

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        dict_info = manager.dictionaries[0]

        result = manager._load_dictionary(dict_info)

        assert result is mock_mdx
        assert dict_info["is_available"] is True
        assert dict_info["load_error"] is None

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_load_dictionary_caches_loaded(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Loaded dictionaries are cached."""
        (temp_dict_dir / "test.mdx").touch()

        mock_mdx = Mock()
        mock_mdx_class.return_value = mock_mdx

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        dict_info = manager.dictionaries[0]

        # Load twice
        result1 = manager._load_dictionary(dict_info)
        result2 = manager._load_dictionary(dict_info)

        assert result1 is result2
        assert mock_mdx_class.call_count == 1  # Only loaded once

    def test_load_dictionary_readmdict_not_installed(self, temp_dict_dir):
        """Loading fails gracefully when readmdict not installed."""
        (temp_dict_dir / "test.mdx").touch()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        dict_info = manager.dictionaries[0]

        with patch.object(manager, '_load_readmdict', return_value=False):
            result = manager._load_dictionary(dict_info)

        assert result is None
        assert dict_info["is_available"] is False
        assert dict_info["load_error"] == "readmdict not installed"

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_load_dictionary_mdx_error(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Loading handles MDX file errors."""
        (temp_dict_dir / "corrupted.mdx").touch()

        mock_mdx_class.side_effect = Exception("Corrupted MDX file")

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        dict_info = manager.dictionaries[0]

        result = manager._load_dictionary(dict_info)

        assert result is None
        assert dict_info["is_available"] is False
        assert "Failed to load dictionary" in dict_info["load_error"]


class TestMdictDictionaryQuery:
    """Test word query functionality."""

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_query_word_success(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Successfully queries word from dictionary."""
        (temp_dict_dir / "test.mdx").touch()

        # Mock dictionary lookup
        mock_mdx = Mock()
        mock_mdx.lookup = Mock(return_value="<html>test definition</html>")
        mock_mdx_class.return_value = mock_mdx

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        result = manager.query_word("test")

        assert result is not None
        assert result["word"] == "test"
        assert result["definition"] == "<html>test definition</html>"
        assert result["dictionary"] == "test"
        assert result["priority"] == 5

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_query_word_case_insensitive(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Word queries are case-insensitive."""
        (temp_dict_dir / "test.mdx").touch()

        mock_mdx = Mock()
        mock_mdx.lookup = Mock(return_value="definition")
        mock_mdx_class.return_value = mock_mdx

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        result1 = manager.query_word("Hello")
        result2 = manager.query_word("HELLO")
        result3 = manager.query_word("hello")

        # All should query lowercase
        assert mock_mdx.lookup.call_args_list[0][0][0] == "hello"
        assert mock_mdx.lookup.call_args_list[1][0][0] == "hello"
        assert mock_mdx.lookup.call_args_list[2][0][0] == "hello"

    def test_query_word_empty_returns_none(self, dict_manager):
        """Empty word returns None."""
        assert dict_manager.query_word("") is None
        assert dict_manager.query_word("   ") is None
        assert dict_manager.query_word(None) is None

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_query_word_not_found(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Returns None when word not in dictionary."""
        (temp_dict_dir / "test.mdx").touch()

        mock_mdx = Mock()
        mock_mdx.lookup = Mock(return_value=None)
        mock_mdx_class.return_value = mock_mdx

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        result = manager.query_word("nonexistent")

        assert result is None

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_query_word_list_result(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Handles list results from MDX lookup."""
        (temp_dict_dir / "test.mdx").touch()

        mock_mdx = Mock()
        mock_mdx.lookup = Mock(return_value=["definition1", "definition2"])
        mock_mdx_class.return_value = mock_mdx

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        result = manager.query_word("test")

        assert result["definition"] == "definition1"  # Takes first

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_query_word_priority_order(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Queries dictionaries in priority order."""
        # Create dictionaries with different priorities
        (temp_dict_dir / "custom.mdx").touch()   # priority 5
        (temp_dict_dir / "collins.mdx").touch()  # priority 3
        (temp_dict_dir / "oald.mdx").touch()     # priority 1

        # Mock MDX - only oald has the word
        def create_mock_mdx(file_path):
            mock = Mock()
            if "oald" in str(file_path):
                mock.lookup = Mock(return_value="OALD definition")
            else:
                mock.lookup = Mock(return_value=None)
            return mock

        mock_mdx_class.side_effect = create_mock_mdx

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        result = manager.query_word("test")

        # Should find in oald (priority 1)
        assert result["dictionary"] == "oald"
        assert result["priority"] == 1

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_query_word_skips_unavailable(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Skips unavailable dictionaries gracefully."""
        (temp_dict_dir / "broken.mdx").touch()
        (temp_dict_dir / "working.mdx").touch()

        def create_mock_mdx(file_path):
            if "broken" in str(file_path):
                raise Exception("Corrupted")
            mock = Mock()
            mock.lookup = Mock(return_value="working definition")
            return mock

        mock_mdx_class.side_effect = create_mock_mdx

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        result = manager.query_word("test")

        # Should skip broken, use working
        assert result is not None
        assert result["dictionary"] == "working"

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_query_word_handles_lookup_exception(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Handles exceptions during lookup gracefully."""
        (temp_dict_dir / "test.mdx").touch()

        mock_mdx = Mock()
        mock_mdx.lookup = Mock(side_effect=Exception("Lookup error"))
        mock_mdx_class.return_value = mock_mdx

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        result = manager.query_word("test")

        assert result is None  # Graceful failure


class TestMdictDictionaryAvailability:
    """Test availability checking."""

    def test_get_available_dictionaries_empty(self, dict_manager):
        """Returns empty list when no dictionaries."""
        available = dict_manager.get_available_dictionaries()

        assert available == []

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_get_available_dictionaries_success(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Returns available dictionaries."""
        (temp_dict_dir / "test1.mdx").touch()
        (temp_dict_dir / "test2.mdx").touch()

        mock_mdx_class.return_value = Mock()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        available = manager.get_available_dictionaries()

        assert len(available) == 2

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_get_available_dictionaries_filters_unavailable(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Filters out unavailable dictionaries."""
        (temp_dict_dir / "working.mdx").touch()
        (temp_dict_dir / "broken.mdx").touch()

        def create_mock_mdx(file_path):
            if "broken" in str(file_path):
                raise Exception("Corrupted")
            return Mock()

        mock_mdx_class.side_effect = create_mock_mdx

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)
        available = manager.get_available_dictionaries()

        assert len(available) == 1
        assert available[0]["dictionary_name"] == "working"

    def test_is_available_no_dictionaries(self, dict_manager):
        """Returns False when no dictionaries."""
        assert dict_manager.is_available() is False

    @patch('src.vocab_analyzer.translation.dictionary.readmdict')
    @patch('src.vocab_analyzer.translation.dictionary.MDX')
    def test_is_available_with_dictionaries(self, mock_mdx_class, mock_readmdict, temp_dict_dir):
        """Returns True when dictionaries available."""
        (temp_dict_dir / "test.mdx").touch()

        mock_mdx_class.return_value = Mock()

        manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

        assert manager.is_available() is True

    def test_is_available_readmdict_not_installed(self, temp_dict_dir):
        """Returns False when readmdict not installed."""
        (temp_dict_dir / "test.mdx").touch()

        with patch.dict('sys.modules', {'readmdict': None}):
            manager = MdictDictionary(dictionaries_dir=temp_dict_dir)

            assert manager.is_available() is False
