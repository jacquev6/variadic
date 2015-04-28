# coding: utf-8

# Copyright 2014-2015 Vincent Jacques <vincent@vincent-jacques.net>

master_doc = "index"
project = "variadic"
copyright = "2015, Vincent Jacques"
author = "Vincent Jacques"
extensions = []
nitpicky = True

# https://github.com/bitprophet/alabaster
# html_theme_path
extensions.append("alabaster")
html_theme = "alabaster"
html_sidebars = {
    "**": [
        "about.html", "searchbox.html",
    ]
}
html_theme_options = {
    "github_user": "jacquev6",
    "github_repo": "variadic",
    "github_banner": True,
    "travis_button": True,
}

# http://sphinx-doc.org/ext/autodoc.html
extensions.append("sphinx.ext.autodoc")
# autoclass_content
autodoc_member_order = "bysource"
# autodoc_default_flags
# autodoc_docstring_signature
# autodoc_mock_imports
add_module_names = False
add_class_names = False


# http://sphinx-doc.org/ext/doctest.html
extensions.append("sphinx.ext.doctest")
# doctest_path
doctest_global_setup = "from variadic import variadic"
# doctest_global_cleanup
doctest_test_doctest_blocks=True
