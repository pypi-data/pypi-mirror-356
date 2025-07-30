"""Tests for the Makefile reader module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from automake.core.makefile_reader import (
    MakefileNotFoundError,
    MakefileReader,
    read_makefile_from_directory,
)


class TestMakefileReader:
    """Test cases for the MakefileReader class."""

    def test_init_default_directory(self) -> None:
        """Test MakefileReader initialization with default directory."""
        reader = MakefileReader()
        assert reader.directory == Path.cwd()

    def test_init_custom_directory(self) -> None:
        """Test MakefileReader initialization with custom directory."""
        custom_dir = Path("/tmp")
        reader = MakefileReader(custom_dir)
        assert reader.directory == custom_dir

    def test_makefile_names_constant(self) -> None:
        """Test that MAKEFILE_NAMES contains expected values."""
        expected_names = ["Makefile", "makefile", "GNUmakefile"]
        assert MakefileReader.MAKEFILE_NAMES == expected_names

    def test_find_makefile_success_makefile(self) -> None:
        """Test finding a Makefile named 'Makefile'."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "Makefile"
            makefile_path.write_text("all:\n\techo 'Hello World'")

            reader = MakefileReader(temp_path)
            found_path = reader.find_makefile()

            assert found_path == makefile_path
            assert found_path.name == "Makefile"

    def test_find_makefile_success_lowercase(self) -> None:
        """Test finding a Makefile named 'makefile' when no 'Makefile' exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "makefile"
            makefile_path.write_text("all:\n\techo 'Hello World'")

            reader = MakefileReader(temp_path)
            found_path = reader.find_makefile()

            # On case-insensitive file systems (like macOS), both "makefile"
            # and "Makefile"
            # will exist and point to the same file. The method will find the first one
            # in the priority list, which is "Makefile". We should check that we found
            # the correct file, regardless of the case returned by the file system.
            assert found_path.exists()
            assert found_path.read_text() == "all:\n\techo 'Hello World'"
            # The name might be "Makefile" on case-insensitive systems
            assert found_path.name.lower() == "makefile"

    def test_find_makefile_success_gnumakefile(self) -> None:
        """Test finding a Makefile named 'GNUmakefile' when others don't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "GNUmakefile"
            makefile_path.write_text("all:\n\techo 'Hello World'")

            reader = MakefileReader(temp_path)
            found_path = reader.find_makefile()

            assert found_path == makefile_path
            assert found_path.name == "GNUmakefile"

    def test_find_makefile_priority_order(self) -> None:
        """Test that Makefile has priority over makefile and GNUmakefile."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create all three types
            (temp_path / "Makefile").write_text("# Priority Makefile")
            (temp_path / "makefile").write_text("# Lower priority makefile")
            (temp_path / "GNUmakefile").write_text("# Lowest priority GNUmakefile")

            reader = MakefileReader(temp_path)
            found_path = reader.find_makefile()

            # Should find "Makefile" first due to priority
            assert found_path.name == "Makefile"

    def test_find_makefile_not_found(self) -> None:
        """Test MakefileNotFoundError when no Makefile exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            reader = MakefileReader(temp_path)

            with pytest.raises(MakefileNotFoundError) as exc_info:
                reader.find_makefile()

            error_message = str(exc_info.value)
            assert f"No Makefile found in directory: {temp_path}" in error_message
            assert "Looked for: Makefile, makefile, GNUmakefile" in error_message

    def test_find_makefile_directory_exists_but_is_file(self) -> None:
        """Test that directories named like Makefiles are ignored."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a directory named "Makefile"
            makefile_dir = temp_path / "Makefile"
            makefile_dir.mkdir()

            reader = MakefileReader(temp_path)

            with pytest.raises(MakefileNotFoundError):
                reader.find_makefile()

    def test_read_makefile_success(self) -> None:
        """Test successful reading of Makefile content."""
        makefile_content = """# Test Makefile
all: build test

build:
\techo "Building..."

test:
\techo "Testing..."

deploy:
\techo "Deploying..."
"""

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "Makefile"
            makefile_path.write_text(makefile_content)

            reader = MakefileReader(temp_path)
            content = reader.read_makefile()

            assert content == makefile_content

    def test_read_makefile_utf8_encoding(self) -> None:
        """Test reading Makefile with UTF-8 characters."""
        makefile_content = "# Makefile with UTF-8: 🚀 Deploy\nall:\n\techo 'Hello 世界'"

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "Makefile"
            makefile_path.write_text(makefile_content, encoding="utf-8")

            reader = MakefileReader(temp_path)
            content = reader.read_makefile()

            assert content == makefile_content

    def test_read_makefile_latin1_fallback(self) -> None:
        """Test reading Makefile with latin-1 encoding fallback."""
        # Create content with latin-1 specific characters
        makefile_content = "# Makefile with latin-1: café\nall:\n\techo 'Hello'"

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "Makefile"

            # Write with latin-1 encoding to simulate older Makefiles
            with open(makefile_path, "w", encoding="latin-1") as f:
                f.write(makefile_content)

            reader = MakefileReader(temp_path)

            # Mock the Path.read_text method to simulate UTF-8 decode error
            with patch("pathlib.Path.read_text") as mock_read_text:

                def side_effect(encoding="utf-8"):
                    if encoding == "utf-8":
                        raise UnicodeDecodeError(
                            "utf-8", b"", 0, 1, "invalid start byte"
                        )
                    # Return the actual content for latin-1
                    return makefile_content

                mock_read_text.side_effect = side_effect
                content = reader.read_makefile()
                assert "café" in content

    def test_read_makefile_encoding_error(self) -> None:
        """Test OSError when Makefile cannot be decoded with any encoding."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "Makefile"
            makefile_path.write_text("dummy content")  # Create the file first

            reader = MakefileReader(temp_path)

            # Mock Path.read_text to always raise UnicodeDecodeError
            with patch("pathlib.Path.read_text") as mock_read_text:
                mock_read_text.side_effect = UnicodeDecodeError(
                    "utf-8", b"", 0, 1, "invalid"
                )

                with pytest.raises(OSError) as exc_info:
                    reader.read_makefile()

                assert "Could not read Makefile" in str(exc_info.value)

    def test_read_makefile_file_not_found(self) -> None:
        """Test MakefileNotFoundError when no Makefile exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            reader = MakefileReader(temp_path)

            with pytest.raises(MakefileNotFoundError):
                reader.read_makefile()

    def test_read_makefile_permission_error(self) -> None:
        """Test OSError when Makefile cannot be read due to permissions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "Makefile"
            makefile_path.write_text("all:\n\techo 'test'")

            reader = MakefileReader(temp_path)

            # Mock Path.read_text to raise PermissionError
            with patch("pathlib.Path.read_text") as mock_read_text:
                mock_read_text.side_effect = PermissionError("Permission denied")

                with pytest.raises(OSError) as exc_info:
                    reader.read_makefile()

                assert "Could not read Makefile" in str(exc_info.value)
                assert "Permission denied" in str(exc_info.value)

    def test_get_makefile_info_success(self) -> None:
        """Test getting Makefile information."""
        makefile_content = "all:\n\techo 'Hello World'"

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "Makefile"
            makefile_path.write_text(makefile_content)

            reader = MakefileReader(temp_path)
            info = reader.get_makefile_info()

            assert info["path"] == str(makefile_path)
            assert info["name"] == "Makefile"
            assert info["directory"] == str(temp_path)
            assert int(info["size"]) > 0

    def test_get_makefile_info_not_found(self) -> None:
        """Test MakefileNotFoundError when getting info for non-existent Makefile."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            reader = MakefileReader(temp_path)

            with pytest.raises(MakefileNotFoundError):
                reader.get_makefile_info()

    @patch.object(MakefileReader, "find_makefile")
    @patch("pathlib.Path.read_text")
    def test_read_makefile_success_with_mocks(self, mock_read_text, mock_find):
        """Test successful Makefile reading with mocks."""
        mock_content = "all:\n\techo 'Hello World'"
        mock_read_text.return_value = mock_content
        mock_find.return_value = Path("Makefile")

        reader = MakefileReader()
        content = reader.read_makefile()

        assert content == mock_content
        mock_read_text.assert_called_once_with(encoding="utf-8")

    @patch.object(MakefileReader, "find_makefile")
    @patch("pathlib.Path.read_text")
    def test_read_makefile_unicode_fallback(self, mock_read_text, mock_find):
        """Test Makefile reading with unicode fallback."""
        mock_content = "all:\n\techo 'Hello World'"
        mock_read_text.side_effect = [
            UnicodeDecodeError("utf-8", b"", 0, 1, "invalid"),
            mock_content,
        ]
        mock_find.return_value = Path("Makefile")

        reader = MakefileReader()
        content = reader.read_makefile()

        assert content == mock_content
        assert mock_read_text.call_count == 2
        mock_read_text.assert_any_call(encoding="utf-8")
        mock_read_text.assert_any_call(encoding="latin-1")

    @patch.object(MakefileReader, "find_makefile")
    @patch("pathlib.Path.read_text")
    def test_read_makefile_encoding_error_with_mocks(self, mock_read_text, mock_find):
        """Test Makefile reading with encoding errors using mocks."""
        mock_read_text.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")
        mock_find.return_value = Path("Makefile")

        reader = MakefileReader()
        with pytest.raises(OSError) as exc_info:
            reader.read_makefile()

        assert "Could not read Makefile" in str(exc_info.value)

    @patch.object(MakefileReader, "find_makefile")
    @patch("pathlib.Path.read_text")
    def test_read_makefile_os_error(self, mock_read_text, mock_find):
        """Test Makefile reading with OS errors."""
        mock_read_text.side_effect = OSError("Permission denied")
        mock_find.return_value = Path("Makefile")

        reader = MakefileReader()
        with pytest.raises(OSError) as exc_info:
            reader.read_makefile()

        assert "Could not read Makefile" in str(exc_info.value)

    @patch.object(MakefileReader, "read_makefile")
    def test_extract_targets_basic(self, mock_read):
        """Test basic target extraction."""
        mock_read.return_value = """
all: build test
\techo "Running all"

build:
\techo "Building"

test: build
\techo "Testing"

clean:
\techo "Cleaning"
"""
        reader = MakefileReader()
        targets = reader.extract_targets()

        assert targets == ["all", "build", "test", "clean"]

    @patch.object(MakefileReader, "read_makefile")
    def test_extract_targets_with_variables(self, mock_read):
        """Test target extraction ignoring variables."""
        mock_read.return_value = """
CC = gcc
CFLAGS = -Wall

all: build
\techo "Running all"

build:
\t$(CC) $(CFLAGS) -o app main.c

.PHONY: clean
clean:
\trm -f app
"""
        reader = MakefileReader()
        targets = reader.extract_targets()

        # Should exclude variables (CC, CFLAGS) and special targets (.PHONY)
        assert targets == ["all", "build", "clean"]

    @patch.object(MakefileReader, "read_makefile")
    def test_extract_targets_duplicates(self, mock_read):
        """Test target extraction removes duplicates."""
        mock_read.return_value = """
all: build
\techo "First all"

build:
\techo "Building"

all: test
\techo "Second all"
"""
        reader = MakefileReader()
        targets = reader.extract_targets()

        # Should only include 'all' once
        assert targets == ["all", "build"]

    @patch.object(MakefileReader, "read_makefile")
    def test_extract_targets_complex_names(self, mock_read):
        """Test target extraction with complex target names."""
        mock_read.return_value = """
build-debug: src/main.c
\tgcc -g -o debug main.c

test_unit:
\tpython -m pytest tests/

install.local:
\tcp app /usr/local/bin/
"""
        reader = MakefileReader()
        targets = reader.extract_targets()

        assert targets == ["build-debug", "test_unit", "install.local"]

    @patch.object(MakefileReader, "read_makefile")
    def test_targets_property(self, mock_read):
        """Test the targets property."""
        mock_read.return_value = """
all:
\techo "all"

build:
\techo "build"
"""
        reader = MakefileReader()
        targets = reader.targets

        assert targets == ["all", "build"]
        # Test caching - should not call read_makefile again
        targets2 = reader.targets
        assert targets2 == targets
        mock_read.assert_called_once()

    @patch.object(MakefileReader, "find_makefile")
    @patch("pathlib.Path.stat")
    def test_get_makefile_info(self, mock_stat, mock_find):
        """Test getting Makefile information."""
        mock_path = Path("/test/Makefile")
        mock_find.return_value = mock_path

        # Mock stat result
        class MockStat:
            st_size = 1024

        mock_stat.return_value = MockStat()

        reader = MakefileReader(Path("/test"))
        info = reader.get_makefile_info()

        expected_info = {
            "path": "/test/Makefile",
            "name": "Makefile",
            "size": "1024",
            "directory": "/test",
        }
        assert info == expected_info


class TestConvenienceFunction:
    """Test cases for the convenience function."""

    def test_read_makefile_from_directory_success(self) -> None:
        """Test successful reading using convenience function."""
        makefile_content = "all:\n\techo 'Hello World'"

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "Makefile"
            makefile_path.write_text(makefile_content)

            content = read_makefile_from_directory(temp_path)
            assert content == makefile_content

    def test_read_makefile_from_directory_default(self) -> None:
        """Test convenience function with default directory."""
        # Mock the current working directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            makefile_path = temp_path / "Makefile"
            makefile_path.write_text("all:\n\techo 'test'")

            with patch(
                "automake.core.makefile_reader.Path.cwd", return_value=temp_path
            ):
                content = read_makefile_from_directory()
                assert "echo 'test'" in content

    def test_read_makefile_from_directory_not_found(self) -> None:
        """Test convenience function with non-existent Makefile."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            with pytest.raises(MakefileNotFoundError):
                read_makefile_from_directory(temp_path)


class TestMakefileNotFoundError:
    """Test cases for the MakefileNotFoundError exception."""

    def test_exception_inheritance(self) -> None:
        """Test that MakefileNotFoundError inherits from Exception."""
        error = MakefileNotFoundError("test message")
        assert isinstance(error, Exception)

    def test_exception_message(self) -> None:
        """Test that MakefileNotFoundError preserves the message."""
        message = "Custom error message"
        error = MakefileNotFoundError(message)
        assert str(error) == message
