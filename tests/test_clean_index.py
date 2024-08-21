import unittest
import os
import tempfile
import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import subprocess

# Importing the module with the correct name
from sphinx_example_includer.sphinxgen import cleanup_index


class TestCleanupIndex(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to hold the index file
        self.test_dir = tempfile.TemporaryDirectory()
        self.docs_path = self.test_dir.name
        self.index_fname = "index.rst"

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def create_index_file(self, content):
        # Helper method to create an index file with specified content
        index_path = os.path.join(self.docs_path, self.index_fname)
        with open(index_path, "w") as f:
            f.write(content)

    def read_index_file(self):
        # Helper method to read the content of the index file
        index_path = os.path.join(self.docs_path, self.index_fname)
        with open(index_path, "r") as f:
            return f.read()

    def test_cleanup_index_without_title(self):
        # Test the function without providing a title
        initial_content = (
            "Welcome to the documentation!\n"
            "\n"
            ".. toctree::\n"
            "   :maxdepth: 2\n"
            "   :caption: Contents:\n"
            "\n"
            "   module1\n"
            "   module2\n"
        )
        expected_content = (
            ".. toctree::\n"
            "   :maxdepth: 2\n"
            "   :caption: Contents:\n"
            "\n"
            "   module1\n"
            "   module2\n"
        )

        self.create_index_file(initial_content)
        cleanup_index(self.docs_path, self.index_fname)
        result_content = self.read_index_file()

        self.assertEqual(result_content.strip(), expected_content.strip())

    def test_cleanup_index_with_title(self):
        # Test the function with a title provided
        title = "New Documentation"
        initial_content = (
            "Welcome to the documentation!\n"
            "\n"
            ".. toctree::\n"
            "   :maxdepth: 2\n"
            "   :caption: Contents:\n"
            "\n"
            "   module1\n"
            "   module2\n"
        )
        expected_content = (
            "New Documentation\n"
            "=================\n"
            ".. toctree::\n"
            "   :maxdepth: 2\n"
            "   :caption: Contents:\n"
            "\n"
            "   module1\n"
            "   module2\n"
        )

        self.create_index_file(initial_content)
        cleanup_index(self.docs_path, self.index_fname, title=title)
        result_content = self.read_index_file()

        self.assertEqual(result_content.strip(), expected_content.strip())

    def test_cleanup_index_no_toctree(self):
        # Test the function when no ".. toctree::" is present in the content
        initial_content = (
            "This is some introduction text.\n"
            "This is more text without a toctree directive.\n"
        )
        expected_content = initial_content  # No change expected

        self.create_index_file(initial_content)
        cleanup_index(self.docs_path, self.index_fname)
        result_content = self.read_index_file()

        self.assertEqual(result_content.strip(), expected_content.strip())


if __name__ == "__main__":
    unittest.main()
