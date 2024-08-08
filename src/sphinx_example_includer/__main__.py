import argparse
import includer
import logging


def cli():
    parser = argparse.ArgumentParser(prog='Sphinx Example Includer',
        description='A tool to include example code or any other files into sphinx documentation automatically')

    parser.add_argument('--debug', action='store_true', help="Showing debug messages")

    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        type=argparse.FileType('r'),
        help='one or more files to be '
    )

    parser.add_argument(
        '--dest_dir',
        default="docs/sources/examples",
        help='The output directory'
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
    includer.generate_examples_rsts(dest_dir=args.dest_dir, examples=args.files, logger=logger)


if __name__ == '__main__':
    cli()
