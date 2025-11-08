project = "aioyookassa"
copyright = "2022, Masa"
author = "Masa"
release = "2.0.3"


extensions = [
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_theme = "furo"
html_logo = "_static/logo.png"
html_static_path = ["_static"]

source_suffix = ".rst"
master_doc = "index"

add_function_parentheses = True

rst_prolog = """
.. role:: pycode(code)
   :language: python3
"""

latex_documents = [
    (master_doc, f"{project}.tex", f"{project} Documentation", author, "manual"),
]

man_pages = [(master_doc, project, f"{project} Documentation", [author], 1)]


texinfo_documents = [
    (
        master_doc,
        project,
        f"{project} Documentation",
        author,
        project,
        "Modern and fully asynchronous framework for yookassa.ru API",
        "Miscellaneous",
    ),
]

autoclass_content = "both"
autodoc_member_order = "bysource"
