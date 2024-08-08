import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import os
from sphinx_example_includer import includer


class TestExampleGenerator(unittest.TestCase):

    def test_split_fname_ext(self):
        self.assertEqual(includer.split_fname_ext("path/to/file.txt"), ("file", "txt"))
        self.assertEqual(includer.split_fname_ext("file.with.dots.py"), ("file.with.dots", "py"))

    def test_get_name_from_fname(self):
        self.assertEqual(includer.get_name_from_fname("file_name"), "File Name")
        self.assertEqual(includer.get_name_from_fname("another-file-name"), "Another File Name")

    @patch('os.path.exists')
    @patch('os.mkdir')
    @patch('builtins.open', new_callable=mock_open, read_data="print('Hello, World!')")
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join', side_effect=lambda *args: "/".join(args))
    def test_generate_examples_rsts(self, mock_join, mock_open_write, mock_open_read, mock_mkdir, mock_exists):
        mock_exists.side_effect = lambda path: False if path == "dest_dir" else True
        logger = MagicMock()

        example_files = ["example1.py", "example2.py"]
        dest_dir = "dest_dir"

        # Mock the file read and write operations
        mock_read_open = mock_open(read_data="print('Hello, World!')")
        mock_write_open = mock_open()
        mock_open_read.side_effect = mock_read_open
        mock_open_write.side_effect = mock_write_open

        includer.generate_examples_rsts(example_files, dest_dir, logger)

        mock_mkdir.assert_called_once_with(dest_dir)
        expected_calls = [
            mock_open_write().write(
                "\nExample1\n=========\n\n.. code-block:: python\n\nprint('Hello, World!')\n\n"
            ),
            mock_open_write().write(
                "\nExample2\n=========\n\n.. code-block:: python\n\nprint('Hello, World!')\n\n"
            ),
        ]

        expected_calls = [
            call().write("\nExample1\n=========\n\n.. code-block:: python\n\nprint('Hello, World!')\n\n"),
            call().write("\nExample2\n=========\n\n.. code-block:: python\n\nprint('Hello, World!')\n\n")
        ]

        mock_open_write().write.assert_has_calls(expected_calls, any_order=True)

        logger.debug.assert_any_call("Generated the docs example1.rst")
        logger.debug.assert_any_call("Generated the docs example2.rst")

    @patch('os.path.exists')
    @patch('os.mkdir')
    @patch('builtins.open', new_callable=mock_open, read_data="print('Hello, World!')")
    def test_generate_examples_rsts_no_logger(self, mock_open_read, mock_mkdir, mock_exists):
        mock_exists.side_effect = lambda path: False if path == "dest_dir" else True

        example_files = ["example1.py", "example2.py"]
        dest_dir = "dest_dir"

        with patch('builtins.print') as mock_print:
            includer.generate_examples_rsts(example_files, dest_dir)

            mock_mkdir.assert_called_once_with(dest_dir)
            mock_print.assert_called_with(".rst files are generated successfully.")


if __name__ == '__main__':
    unittest.main()
