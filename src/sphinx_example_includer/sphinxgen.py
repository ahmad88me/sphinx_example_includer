import os
import subprocess
from .common import get_logger
import tomli


def sphinx_workflow(conf_path, docs_path, project_path, index_fname, logger=None):
    if not logger:
        logger = get_logger(__name__)

    if not os.path.exists(conf_path):
        logger.error(f"{conf_path} is not found.")
        return

    meta_data = meta_from_conf(conf_path=conf_path)
    build_sphinx(meta_data=meta_data, docs_path=docs_path, logger=logger)
    fix_sphinx_conf(project_path=project_path, sphinx_conf_path=os.path.join(docs_path, "conf.py"))
    gen_project_docs(project_path=project_path, docs_path=docs_path, logger=logger)
    if "name" in meta_data:
        toc_fname = f"""{meta_data["name"]}.rst"""
        append_module_to_index(toc_fname=toc_fname, docs_path=docs_path, index_fname=index_fname, logger=logger)


def fix_sphinx_conf(project_path, sphinx_conf_path):

    pp = os.path.join(os.path.pardir, project_path)
    # fix python path
    pp = f"""
import sys
import os
sys.path.insert(0, os.path.abspath('{pp}'))
"""
    doc_gen = """
extensions += [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
]

autosummary_generate = True

"""
    with open(sphinx_conf_path, "r") as f:
        content = f.read()

    new_content = content
    if "import sys" not in content:
        new_content = pp + content

    if "autosummary_generate" not in content:
        new_content += doc_gen

    with open(sphinx_conf_path, "w") as f:
        f.write(new_content)


def run_command(comm, logger):
    logger.debug(comm)
    p = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        logger.debug(line.decode())


def gen_html(docs_path, logger):
    comm = f"cd {docs_path}; make html"
    run_command(comm, logger)


def gen_project_docs(project_path, docs_path, logger):
    """
    Generate the docs of a given directory
    :param project_path:
    :param docs_path:
    :param logger:
    :return:
    """
    comm = f"sphinx-apidoc -o {docs_path} {project_path}"
    run_command(comm, logger)


def meta_from_conf(conf_path):
    """
    Parse the configuration file
    :param conf_path: str. The configuration path.
    :return:
    """
    with open(conf_path, "rb") as f:
        toml_dict = tomli.load(f)
    return toml_dict["project"]


def meta_authors(meta_data, sep=", "):
    """
    Return the authors from the given meta dict
    :param meta_data: dict
    :param sep: str
    :return:
    """
    authors = []
    if "authors" in meta_data:
        for auth in meta_data["authors"]:
            if "name" in auth:
                authors.append(auth["name"])
    return sep.join(authors)


def meta_release(meta_data):
    """
    Get the release from the given meta dict
    :param meta_data: dict
    :param sep: str
    :return:
    """
    release = meta_data.get("version", "")
    return release


def build_sphinx(meta_data, docs_path, logger):
    """
    Build sphinx dpcs

    :param meta_data:
    :param docs_path:
    :param logger:
    :return:
    """
    project_name = meta_data["name"]
    authors = meta_authors(meta_data)
    release = meta_release(meta_data)
    comm = f"sphinx-quickstart {docs_path} -q "
    if project_name:
        comm += f""" --project "{project_name}" """
    if authors:
        comm += f""" --author "{authors}" """
    if release:
        comm += f""" --release "{release}" """

    run_command(comm, logger)


def append_indices(rst_fpath, logger):
    rst = """
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
    with open(rst_fpath, "r") as f:
        content = f.read()
    if "Indices and tables" not in content:
        logger.info("Adding Indices and tables section")
        with open(rst_fpath, "a") as f:
            f.write(rst)


def append_module_to_index(toc_fname, docs_path, index_fname, logger):
    """
    Include the examples or any other module into the index
    :param toc_fname:
    :param docs_path:
    :param index_fname:
    :return:
    """
    index_path = os.path.join(docs_path, index_fname)
    toc_name = toc_fname[:-4]
    line = f"   {toc_name}\n"
    with open(index_path, "r") as f:
        content = f.read()
    if line not in content:
        logger.info(f"Adding module {toc_name} to {index_fname}")
        with open(index_path, "a") as f:
            f.write(line)
