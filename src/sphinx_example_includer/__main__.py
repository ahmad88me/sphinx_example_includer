import argparse
import logging
import os
from .includer import generate_examples_rsts, generate_toc_rst


def cli():
    parser = argparse.ArgumentParser(prog='Sphinx Example Includer',
        description='A tool to include example code or any other files into sphinx documentation automatically')

    parser.add_argument('--debug', action='store_true', help="Showing debug messages")
    parser.add_argument('--overwrite', action='store_true', help="Overwrite files that already exists")


    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        # type=argparse.FileType('r'),
        help='one or more files to be '
    )

    parser.add_argument(
        '--dest_dir',
        default="docs/source/examples",
        help='The output directory'
    )

    parser.add_argument(
        '--toc-fname',
        default="examples_test.rst",
        help='The name of the toc file'
    )

    args = parser.parse_args()
    if args.debug:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
    else:
        logger = None
    args = parser.parse_args()
    rst_files = generate_examples_rsts(dest_dir=args.dest_dir, examples=args.files, logger=logger, overwrite=args.overwrite)

    parent_tokens = args.dest_dir.split(os.path.sep)[:-1]
    toc_parent_path = os.path.sep.join(parent_tokens)
    generate_toc_rst(toc_fname=args.toc_fname, examples_paths=rst_files, toc_parent_path=toc_parent_path,
                     overwrite=args.overwrite, logger=logger)


if __name__ == '__main__':
    cli()
