# Streamlit-Pages

[![Releases](https://img.shields.io/pypi/v/st-pages)](https://pypi.org/project/st-pages/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/blackary/st_pages/testing.yml?branch=main)](https://github.com/blackary/st_pages/actions?query=workflow%3A%22testing%22+branch%3Amain)
![Python Versions](https://img.shields.io/pypi/pyversions/st_pages.svg)
![Streamlit versions](https://img.shields.io/badge/streamlit-1.36.0-white.svg)
![License](https://img.shields.io/github/license/blackary/st_pages)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://st-pages.streamlit.app)

Author: [@blackary](https://github.com/blackary)

Code: https://github.com/blackary/st_pages

## Installation

```sh
pip install st-pages
```

## See it in action

Basic example: https://st-pages.streamlit.app/

Example with sections: https://st-pages-sections.streamlit.app/

## Why st-pages?

Previously, st-pages allowed for a much more customizable and flexible declaration of
pages in a Streamlit app, and was independent of the actual filenames of the python
files in your project.

As of 1.0.0, st-pages is now a tiny wrapper that provides an easy method for defining
the pages in your app in a toml file, as well as a few utility methods to let you
add the current page's title to all pages, etc.

You are welcome to continue to use older versions of this package, but most of the
old use-cases are now easy to do with native streamlit, so I would recommend
checking out the [documentation](https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation)
for more information.

## How to use

### Declare pages inside of a toml file

Contents of `.streamlit/pages.toml`

```toml
[[pages]]
path = "page1.py"
name = "Home"
icon = "🏠"

[[pages]]
path = "other_pages/page2.py"
name = "Page 2"
icon = ":books:"
url_path = "my_books" # You can override the default url path for a page
```

Example with sections, `.stremalit/pages_sections.toml`:

```toml
[[pages]]
path = "page1.py"
name = "Home"
icon = "🏠"

[[pages]]
path = "other_pages/page2.py"
name = "Page 2"
icon = ":books:"

[[pages]]
name = "My section"
icon = "🎈️"
is_section = true

# Pages after an `is_section = true` will be indented
[[pages]]
name = "Another page"
icon = "💪"
```

Streamlit code:

```python
import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(layout="wide")

# If you want to use the no-sections version, this
# defaults to looking in .streamlit/pages.toml, so you can
# just call `get_nav_from_toml()`
nav = get_nav_from_toml(".streamlit/pages_sections.toml")

st.logo("logo.png")

pg = st.navigation(nav)

add_page_title(pg)

pg.run()
```

# Hiding pages

You can now pass a list of page names to `hide_pages` to hide pages from now on.

This list of pages is custom to each viewer of the app, so you can hide pages
from one viewer but not from another using this method. You can see another example of
hiding pages in the docs [here](https://docs.streamlit.io/develop/tutorials/multipage/dynamic-navigation)

```py
from st_pages import hide_pages

hide_pages(["Another page"])
```
