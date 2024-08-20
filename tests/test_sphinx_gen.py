import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import subprocess

# Importing the module with the correct name
from sphinx_example_includer.sphinxgen import (
    sphinx_workflow, fix_sphinx_conf, run_command, gen_html,
    gen_project_docs, meta_from_conf, meta_authors, meta_release,
    build_sphinx, append_indices, append_module_to_index
)


class TestSphinxWorkflow(unittest.TestCase):

    @patch("sphinx_example_includer.sphinxgen.get_logger")
    @patch("sphinx_example_includer.sphinxgen.os.path.exists", return_value=True)
    @patch("sphinx_example_includer.sphinxgen.meta_from_conf", return_value={"name": "TestProject"})
    @patch("sphinx_example_includer.sphinxgen.build_sphinx")
    @patch("sphinx_example_includer.sphinxgen.fix_sphinx_conf")
    @patch("sphinx_example_includer.sphinxgen.gen_project_docs")
    @patch("sphinx_example_includer.sphinxgen.append_module_to_index")
    @patch("sphinx_example_includer.sphinxgen.cleanup_index")
    def test_sphinx_workflow(
        self, mock_cleanup_index, mock_append_module_to_index, mock_gen_project_docs,
        mock_fix_sphinx_conf, mock_build_sphinx, mock_meta_from_conf,
        mock_exists, mock_get_logger
    ):
        logger = MagicMock()
        mock_get_logger.return_value = logger

        sphinx_workflow(
            conf_path="conf.toml",
            docs_path="docs",
            project_path="project",
            index_fname="index.rst"
        )

        mock_exists.assert_called_once_with("conf.toml")
        mock_meta_from_conf.assert_called_once_with(conf_path="conf.toml")
        mock_build_sphinx.assert_called_once()
        mock_fix_sphinx_conf.assert_called_once_with(
            project_path="project",
            sphinx_conf_path=os.path.join("docs", "conf.py")
        )
        mock_gen_project_docs.assert_called_once()
        mock_append_module_to_index.assert_called_once()

    @patch("sphinx_example_includer.sphinxgen.open", new_callable=mock_open, read_data="old content")
    def test_fix_sphinx_conf(self, mock_open):
        mock_open.return_value.__iter__ = lambda self: iter(self.readline, '')
        fix_sphinx_conf("project", "docs/conf.py")
        mock_open.assert_called_with("docs/conf.py", "w")
        handle = mock_open()
        handle.write.assert_called()

    @patch("sphinx_example_includer.sphinxgen.subprocess.Popen")
    def test_run_command(self, mock_popen):
        logger = MagicMock()
        process_mock = MagicMock()
        attrs = {'stdout.readlines.return_value': [b'output']}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock
        run_command("echo 'hello'", logger)
        mock_popen.assert_called_once_with("echo 'hello'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logger.debug.assert_any_call("echo 'hello'")
        logger.debug.assert_any_call("output")

    @patch("sphinx_example_includer.sphinxgen.run_command")
    def test_gen_html(self, mock_run_command):
        logger = MagicMock()
        gen_html("docs", logger)
        mock_run_command.assert_called_once_with("cd docs; make html", logger)

    @patch("sphinx_example_includer.sphinxgen.run_command")
    def test_gen_project_docs(self, mock_run_command):
        logger = MagicMock()
        gen_project_docs("project", "docs", logger)
        mock_run_command.assert_called_once_with("sphinx-apidoc -o docs project", logger)

    @patch("sphinx_example_includer.sphinxgen.open", new_callable=mock_open, read_data=b'[project]\nname="TestProject"\n')
    def test_meta_from_conf(self, mock_open):
        result = meta_from_conf("conf.toml")
        self.assertEqual(result, {"name": "TestProject"})
        mock_open.assert_called_once_with("conf.toml", "rb")

    def test_meta_authors(self):
        meta_data = {"authors": [{"name": "Author1"}, {"name": "Author2"}]}
        result = meta_authors(meta_data)
        self.assertEqual(result, "Author1, Author2")

    def test_meta_release(self):
        meta_data = {"version": "1.0.0"}
        result = meta_release(meta_data)
        self.assertEqual(result, "1.0.0")

    @patch("sphinx_example_includer.sphinxgen.run_command")
    def test_build_sphinx(self, mock_run_command):
        logger = MagicMock()
        meta_data = {"name": "TestProject", "authors": [{"name": "Author1"}], "version": "1.0.0"}
        build_sphinx(meta_data, "docs", logger)
        mock_run_command.assert_called_once_with(
            'sphinx-quickstart docs -q  --project "TestProject"  --author "Author1"  --release "1.0.0" ',
            logger
        )

    @patch("sphinx_example_includer.sphinxgen.open", new_callable=mock_open, read_data="Existing content")
    def test_append_indices(self, mock_open):
        logger = MagicMock()
        append_indices("index.rst", logger)
        mock_open.assert_any_call("index.rst", "r")
        handle = mock_open()
        handle.write.assert_called()

    @patch("sphinx_example_includer.sphinxgen.open", new_callable=mock_open, read_data=".. toctree::\n")
    @patch("sphinx_example_includer.sphinxgen.write_above_or_end")
    def test_append_module_to_index(self, mock_write_above_or_end, mock_open):
        logger = MagicMock()
        append_module_to_index("module.rst", "docs", "index.rst", logger)
        mock_open.assert_called_with(os.path.join("docs", "index.rst"), "r")
        mock_write_above_or_end.assert_called_once()


if __name__ == "__main__":
    unittest.main()
