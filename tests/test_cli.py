import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO
import logging
from unittest.mock import ANY

import argparse
import sphinx_example_includer


class TestCli(unittest.TestCase):

    @patch('sphinx_example_includer.common.get_logger')
    @patch('sphinx_example_includer.__main__.sphinx_workflow')
    @patch('sphinx_example_includer.__main__.generate_examples_rsts')
    @patch('sphinx_example_includer.__main__.generate_toc_rst')
    @patch('sphinx_example_includer.__main__.append_module_to_index')
    @patch('sphinx_example_includer.__main__.append_indices')
    @patch('sphinx_example_includer.__main__.gen_html')
    @patch('os.path.join')
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_with_build(self, mock_parse_args, mock_join, mock_gen_html, mock_append_indices,
                            mock_append_module_to_index,
                            mock_generate_toc_rst, mock_generate_examples_rsts, mock_sphinx_workflow, mock_get_logger):
        # Set up the mock arguments
        mock_parse_args.return_value = argparse.Namespace(
            debug=False,
            info=False,
            overwrite=False,
            files=['example.py'],
            dest_dir='docs/examples',
            toc_fname='examples.rst',
            build=True,
            conf='pyproject.toml',
            docs_dir='docs',
            project_dir='src',
            index='index.rst'
        )

        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_join.return_value = 'docs/index.rst'

        # Run the cli function
        sphinx_example_includer.__main__.cli()

        # Assertions to ensure all necessary functions are called
        mock_sphinx_workflow.assert_called_once_with(
            conf_path='pyproject.toml',
            docs_path='docs',
            index_fname='index.rst',
            project_path='src',
            logger=mock_logger
        )

        mock_generate_examples_rsts.assert_called_once_with(
            dest_dir='docs/examples',
            examples=['example.py'],
            logger=mock_logger,
            overwrite=False
        )

        mock_generate_toc_rst.assert_called_once_with(
            toc_fname='examples.rst',
            examples_paths=mock_generate_examples_rsts.return_value,
            toc_parent_path='docs',
            overwrite=False,
            logger=mock_logger
        )

        mock_append_module_to_index.assert_called_once_with(
            toc_fname='examples.rst',
            docs_path='docs',
            index_fname='index.rst',
            logger=mock_logger
        )

        mock_append_indices.assert_called_once_with('docs/index.rst', logger=mock_logger)
        mock_gen_html.assert_called_once_with(docs_path='docs', logger=mock_logger)

    @patch('sphinx_example_includer.__main__.gen_html')
    @patch('sphinx_example_includer.__main__.append_indices')
    @patch('sphinx_example_includer.common.get_logger')
    @patch('sphinx_example_includer.__main__.sphinx_workflow')
    @patch('os.path.join')
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_without_files(self, mock_parse_args, mock_join, mock_sphinx_workflow, mock_get_logger,
                               mock_append_indices, mock_gen_html):
        # Set up the mock arguments
        mock_parse_args.return_value = argparse.Namespace(
            debug=True,
            info=False,
            overwrite=False,
            files=None,
            dest_dir='docs/examples',
            toc_fname='examples.rst',
            build=True,
            conf='pyproject.toml',
            docs_dir='docs',
            project_dir='src',
            index='index.rst'
        )

        mock_join.return_value = 'docs/index.rst'

        # Run the cli function
        sphinx_example_includer.__main__.cli()

        args = {
            "conf_path": 'pyproject.toml',
            "docs_path": 'docs',
            "index_fname": 'index.rst',
            "project_path": 'src',
            "logger": ANY
        }

        mock_sphinx_workflow.assert_called_once_with(
            **args
        )

        args = {
            "docs_path": 'docs',
            "logger": ANY
        }

        mock_gen_html.assert_called_once_with(
            **args
        )


if __name__ == '__main__':
    unittest.main()
