import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from sphinx_example_includer import includer


# Unit tests
class TestGenerateTocRst(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.sep', new="/")
    def test_generate_toc_rst(self, mock_open):

        toc_fname = "example_toc.rst"
        examples_paths = ["p/to/example1.py", "p/to/example2.py"]
        toc_parent_path = "docs"

        includer.generate_toc_rst(toc_fname, examples_paths, toc_parent_path)

        expected_examples_txt = "   to/example1.py\n   to/example2.py\n"
        expected_example_name = "Example Toc"
        expected_rst_content = f""".. _example_toc:

Example Toc
{'=' * len("Example Toc")}

.. toctree::
   :maxdepth: 1

{expected_examples_txt}

"""



        mock_open.assert_called_once_with("docs/example_toc.rst", 'w')
        mock_open().write.assert_called_once_with(expected_rst_content)


if __name__ == '__main__':
    unittest.main()
