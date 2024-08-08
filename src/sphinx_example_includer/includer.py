import os
import traceback


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


def generate_examples_rsts(examples, dest_dir, logger=None):
    if not os.path.exists(dest_dir):
        try:
            os.mkdir(dest_dir)
        except Exception as e:
            if logger:
                logger.debug(traceback.format_exc())
                logger.error(f"Exception: {e}")
            else:
                print(f"Exception: {e}")
            return

    for exfile in examples:
        fname, ext = split_fname_ext(exfile)
        rst_filename = f'{fname}.rst'
        example_name = get_name_from_fname(fname)
        with open(exfile, 'r') as example_file:
            code = example_file.read()
        rst_content = f"""
{example_name}
{'=' * len(example_name)}

.. code-block:: python

{code}

"""
        with open(os.path.join(dest_dir, rst_filename), 'w') as rst_file:
            rst_file.write(rst_content)
        if logger:
            logger.debug(f"Generated the docs {rst_filename}")
    print(".rst files are generated successfully.")
