import argparse
import logging
import os
from .includer import generate_examples_rsts, generate_toc_rst
from .sphinxgen import sphinx_workflow, append_indices, append_module_to_index, gen_html
from . import common


def cli():
    parser = argparse.ArgumentParser(prog='Sphinx Example Includer',
                                     description="A Sphinx docs generation tool")

    parser.add_argument('--debug', action='store_true', help="Showing debug messages")
    parser.add_argument('--info', action='store_true', help="Showing info messages")

    parser.add_argument('--overwrite', action='store_true', help="Overwrite files that already exists")

    parser.add_argument(
        '--files',
        nargs='+',
        help='one or more files to be '
    )

    parser.add_argument(
        '--dest-dir',
        default="docs/examples",
        help='The output directory of the included files inside the docs dir (e.g., docs/examples)'
    )

    parser.add_argument(
        '--toc-fname',
        default="examples.rst",
        help='The name of the toc file'
    )

    parser.add_argument("--title", default="", help="The title of the documentation in the index page.")
    parser.add_argument("--readme", help="The readme file to include in the docs index page.")
    parser.add_argument("--build", action='store_true', help="Build Sphinx docs.")
    parser.add_argument("--conf", default="pyproject.toml", help="The configuration file (e.g., pyproject.toml)")
    parser.add_argument('--docs-dir', default="docs", help="The directory of the documentation")
    parser.add_argument("--project-dir", default="src", help="The path of the project's code")
    parser.add_argument("--index", default="index.rst", help="The name of the index file.")

    args = parser.parse_args()
    if args.debug:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
    elif args.info:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)
    else:
        logger = common.get_logger(__name__)
    args = parser.parse_args()
    index_fname = args.index
    docs_index_path = os.path.join(args.docs_dir, index_fname)

    if args.build:
        if not args.conf.endswith("pyproject.toml"):
            logger.error(f"Expecting pyproject.toml. Other configuration formats are not yet supported")
        else:
            sphinx_workflow(conf_path=args.conf, docs_path=args.docs_dir, index_fname=index_fname,
                            project_path=args.project_dir, logger=logger, readme=args.readme, title=args.title)

    if args.files:
        rst_files = generate_examples_rsts(dest_dir=args.dest_dir, examples=args.files, logger=logger,
                                           overwrite=args.overwrite)

        parent_tokens = args.dest_dir.split(os.path.sep)[:-1]
        toc_parent_path = os.path.sep.join(parent_tokens)
        generate_toc_rst(toc_fname=args.toc_fname, examples_paths=rst_files, toc_parent_path=toc_parent_path,
                         overwrite=args.overwrite, logger=logger)

        append_module_to_index(toc_fname=args.toc_fname, docs_path=args.docs_dir, index_fname=index_fname, logger=logger)
    if args.build:
        append_indices(docs_index_path, logger=logger)
        gen_html(docs_path=args.docs_dir, logger=logger)


if __name__ == '__main__':
    cli()
