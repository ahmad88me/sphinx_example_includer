import os
import traceback
import logging
from . import common


def split_fname_ext(fpath):
    fname_ext = fpath.split(os.path.sep)[-1]
    tokens = fname_ext.split(".")
    ext = tokens[-1]
    fname_tokens = tokens[:-1]
    fname = ".".join(fname_tokens)
    return fname, ext


def get_name_from_fname(fname):
    s = fname.replace("_", " ").replace("-", " ")
    return s.title()


def generate_examples_rsts(examples, dest_dir, logger=None, overwrite=False):
    if logger is None:
        logger = common.get_logger(__name__)
    rst_ex_paths = []
    if not os.path.exists(dest_dir):
        try:
            os.mkdir(dest_dir)
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(f"Exception: {e}")
            return rst_ex_paths
    for exfile in examples:
        fname, ext = split_fname_ext(exfile)
        rst_filename = f'{fname}.rst'
        example_name = get_name_from_fname(fname)
        with open(exfile, 'r') as example_file:
            code = example_file.read()
        code = code.strip()
        icode = ""
        for line in code.split("\n"):
            icode += f"\t{line}\n"
        rst_content = f"""
{example_name}
{'=' * len(example_name)}

.. code-block:: python

{icode}

"""
        rst_path = os.path.join(dest_dir, rst_filename)
        rst_ex_paths.append(rst_path)
        if os.path.exists(rst_path) and not overwrite:
            logger.warning(f"{rst_path} already exists and won't be overwritten")
        else:
            with open(rst_path, 'w') as rst_file:
                rst_file.write(rst_content)
            logger.debug(f"Generated the docs {rst_filename}")
    logger.debug(".rst files are generated successfully.")
    return rst_ex_paths


def generate_toc_rst(toc_fname, examples_paths, toc_parent_path, logger=None, overwrite=False):
    if logger is None:
        logger = common.get_logger(__name__)
    toc_name, _ = split_fname_ext(toc_fname)
    example_name = get_name_from_fname(toc_name)
    examples_txt = ""
    for expath in examples_paths:
        tokens = expath.split(os.path.sep)
        ex_rel_path = os.path.sep.join(tokens[-2:])
        examples_txt += f"   {ex_rel_path}\n"

    rst_content = f""".. _{toc_name}:

{example_name}
{'=' * len(example_name)}

.. toctree::
   :maxdepth: 1

{examples_txt}

"""
    rst_path = os.path.join(toc_parent_path, toc_fname)
    if os.path.exists(rst_path) and not overwrite:
        logger.warning(f"{rst_path} already exists and won't be overwritten.")
    else:
        with open(rst_path, 'w') as rst_file:
            rst_file.write(rst_content)
        logger.debug(f"Generated the toc {rst_path} successfully!")
