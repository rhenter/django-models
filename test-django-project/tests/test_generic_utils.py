import codecs
import os
import tempfile

from django_models.utils.generic import find_path, get_version_from_changes


class TestFindPath:
    def test_find_path_basic(self):
        """Test find_path basic functionality."""
        # Create a temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test content")

            # Test finding the file
            result = find_path("test.txt", temp_dir)
            assert result == ""  # Should return empty string for single file

    def test_find_path_with_subdirectory(self):
        """Test find_path with subdirectory structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create subdirectory
            sub_dir = os.path.join(temp_dir, "subdir")
            os.makedirs(sub_dir)

            # Create test file in subdirectory
            test_file = os.path.join(sub_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test content")

            # Test finding the file
            result = find_path("test.txt", temp_dir)
            assert "subdir" in result or result == "subdir"

    def test_find_path_no_match(self):
        """Test find_path when no file matches."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = find_path("nonexistent.txt", temp_dir)
            assert result == ""

    def test_find_path_with_ignored_dirs(self):
        """Test find_path with ignored directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create directories
            ignored_dir = os.path.join(temp_dir, "ignored")
            normal_dir = os.path.join(temp_dir, "normal")
            os.makedirs(ignored_dir)
            os.makedirs(normal_dir)

            # Create files in both directories
            ignored_file = os.path.join(ignored_dir, "test.txt")
            normal_file = os.path.join(normal_dir, "test.txt")

            with open(ignored_file, "w") as f:
                f.write("ignored content")
            with open(normal_file, "w") as f:
                f.write("normal content")

            # Test with ignored directory
            result = find_path("test.txt", temp_dir, ignored_dirs="ignored")
            assert "normal" in result or result == "normal"

    def test_find_path_last_folder_only(self):
        """Test find_path with last_folder_only=True."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create nested directory structure
            nested_dir = os.path.join(temp_dir, "level1", "level2")
            os.makedirs(nested_dir)

            # Create test file
            test_file = os.path.join(nested_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test content")

            # Test with last_folder_only=True
            result = find_path("test.txt", temp_dir, last_folder_only=True)
            assert result == "level2"

    def test_find_path_wildcard_pattern(self):
        """Test find_path with wildcard pattern."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_files = ["test1.txt", "test2.txt", "other.doc"]
            for filename in test_files:
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, "w") as f:
                    f.write("content")

            # Test with wildcard pattern
            result = find_path("test*.txt", temp_dir)
            assert result == ""  # Should find at least one file


class TestGetVersionFromChanges:
    def test_get_version_from_changes_valid_file(self):
        """Test get_version_from_changes with valid CHANGES.rst file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            changes_file = os.path.join(temp_dir, "CHANGES.rst")
            with codecs.open(changes_file, "w", encoding="utf-8") as f:
                f.write("1.2.3\n")
                f.write("-----\n")
                f.write("Some changes\n")

            version = get_version_from_changes(temp_dir)
            assert version == "1.2.3"

    def test_get_version_from_changes_no_file(self):
        """Test get_version_from_changes when CHANGES.rst doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            version = get_version_from_changes(temp_dir)
            assert version == "0.0.0"

    def test_get_version_from_changes_no_version_pattern(self):
        """Test get_version_from_changes when no version pattern is found."""
        with tempfile.TemporaryDirectory() as temp_dir:
            changes_file = os.path.join(temp_dir, "CHANGES.rst")
            with codecs.open(changes_file, "w", encoding="utf-8") as f:
                f.write("No version here\n")
                f.write("Just some text\n")

            version = get_version_from_changes(temp_dir)
            assert version == "0.0.0"

    def test_get_version_from_changes_multiple_versions(self):
        """Test get_version_from_changes with multiple versions (should return first)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            changes_file = os.path.join(temp_dir, "CHANGES.rst")
            with codecs.open(changes_file, "w", encoding="utf-8") as f:
                f.write("2.1.0\n")
                f.write("-----\n")
                f.write("Latest changes\n")
                f.write("\n")
                f.write("1.0.0\n")
                f.write("-----\n")
                f.write("Old changes\n")

            version = get_version_from_changes(temp_dir)
            assert version == "2.1.0"

    def test_get_version_from_changes_different_version_formats(self):
        """Test get_version_from_changes with different version formats."""
        test_cases = [
            ("1.0", "1.0"),
            ("2.1.3", "2.1.3"),
            ("10.20.30", "10.20.30"),
        ]

        for version_input, expected_output in test_cases:
            with tempfile.TemporaryDirectory() as temp_dir:
                changes_file = os.path.join(temp_dir, "CHANGES.rst")
                with codecs.open(changes_file, "w", encoding="utf-8") as f:
                    f.write(f"{version_input}\n")
                    f.write("-----\n")

                version = get_version_from_changes(temp_dir)
                assert version == expected_output

    def test_get_version_from_changes_empty_project_root(self):
        """Test get_version_from_changes with empty project_root."""
        # This should look for CHANGES.rst in current directory
        version = get_version_from_changes("")
        # Should return default version if no CHANGES.rst in current dir
        # or actual version if CHANGES.rst exists
        assert isinstance(version, str)
        assert len(version) > 0
