# SPDX-FileCopyrightText: 2023-2024 Alexandru Fikl <alexfikl@gmail.com>
# SPDX-License-Identifier: CC0-1.0

# https://www.sphinx-doc.org/en/master/usage/configuration.html
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

from __future__ import annotations

import os
import sys
from importlib import metadata

from docutils import nodes

# {{{ project information

m = metadata.metadata("pymittagleffler")
project = m["Name"]
author = m["Author-email"]
copyright = f"2024 {author}"  # noqa: A001
version = m["Version"]
release = version
url = "https://github.com/alexfikl/mittagleffler"

# }}}

# {{{ github roles


def autolink(pattern: str):
    def role(name, rawtext, text, lineno, inliner, options=None, context=None):
        if options is None:
            options = {}

        if context is None:
            context = []

        url = pattern.format(number=text)
        node = nodes.reference(rawtext, f"#{text}", refuri=url, **options)
        return [node], []

    return role


def linkcode_resolve(domain, info):
    if domain != "py" or not info["module"]:
        return None

    modname = info["module"]
    objname = info["fullname"]

    mod = sys.modules.get(modname)
    if not mod:
        return None

    obj = mod
    for part in objname.split("."):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    import inspect

    try:
        moduleparts = obj.__module__.split(".")
        filepath = f"{os.path.join(*moduleparts)}.py"
    except Exception:
        return None

    # FIXME: this checks if the module is actually the `__init__.py`. Is there
    # any easier way to figure that out?
    if mod.__name__ == obj.__module__ and mod.__spec__.submodule_search_locations:
        filepath = os.path.join(*moduleparts, "__init__.py")

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        return None
    else:
        linestart, linestop = lineno, lineno + len(source) - 1

    return f"{url}/blob/main/src/{filepath}#L{linestart}-L{linestop}"


def setup(app) -> None:
    (tmp_url,) = (
        v for k, v in m.items() if k.startswith("Project-URL") and "Repository" in v
    )
    project_url = tmp_url.split(" ")[-1]

    app.add_role("ghpr", autolink(f"{project_url}/pull/{{number}}"))
    app.add_role("ghissue", autolink(f"{project_url}/issues/{{number}}"))


# }}}

# {{{ general configuration

# needed extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.mathjax",
]

# extension for source files
source_suffix = ".rst"
# name of the main (master) document
master_doc = "index"
# min sphinx version
needs_sphinx = "6.0"
# files to ignore
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
# highlighting
pygments_style = "sphinx"

html_theme = "sphinx_book_theme"
html_title = project
html_theme_options = {
    "show_toc_level": 3,
    "use_source_button": True,
    "use_repository_button": True,
    "navigation_with_keys": True,
    "repository_url": "https://github.com/alexfikl/mittagleffler",
    "repository_branch": "main",
    "icon_links": [
        {
            "name": "Release",
            "url": "https://github.com/alexfikl/mittagleffler/releases",
            "icon": "https://img.shields.io/github/v/release/alexfikl/mittagleffler",
            "type": "url",
        },
        {
            "name": "License",
            "url": "https://github.com/alexfikl/mittagleffler/tree/main/LICENSES",
            "icon": "https://img.shields.io/badge/License-MIT-blue.svg",
            "type": "url",
        },
        {
            "name": "CI",
            "url": "https://github.com/alexfikl/mittagleffler",
            "icon": "https://github.com/alexfikl/mittagleffler/workflows/CI/badge.svg",
            "type": "url",
        },
        {
            "name": "Issues",
            "url": "https://github.com/alexfikl/mittagleffler/issues",
            "icon": "https://img.shields.io/github/issues/alexfikl/mittagleffler",
            "type": "url",
        },
    ],
}

# }}}

# {{{ internationalization

language = "en"

# }}

# {{{ extension settings

autoclass_content = "class"
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": None,
    "show-inheritance": None,
}

# }}}

# {{{ links

intersphinx_mapping = {
    "numpy": ("https://numpy.org/doc/stable", None),
    "python": ("https://docs.python.org/3", None),
    "rich": ("https://rich.readthedocs.io/en/stable", None),
}

# }}}
