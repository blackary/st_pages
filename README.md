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

### Method one: declare pages inside your streamlit code

```python
from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("other_pages/page2.py", "Page 2", ":books:"),
    ]
)
```

If you want to organize your pages into sections with indention showing which pages
belong to which section, you can do the following:

```python
from st_pages import Page, Section, show_pages, add_page_title

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("other_pages/page2.py", "Page 2", ":books:"),
        Section("My section", icon="🎈️"),
        # Pages after a section will be indented
        Page("Another page", icon="💪"),
        # Unless you explicitly say in_section=False
        Page("Not in a section", in_section=False)
    ]
)
```

### Method two: declare pages inside of a config file

Contents of `.streamlit/pages.toml`

```toml
[[pages]]
path = "streamlit_app.py"
name = "Home"
icon = "🏠"

[[pages]]
path = "other_pages/page2.py"
name = "Page 2"
icon = ":books:"
```

Example with sections:

```toml
[[pages]]
path = "streamlit_app.py"
name = "Home"
icon = "🏠"

[[pages]]
path = "other_pages/page2.py"
name = "Page 2"
icon = ":books:"

[[pages]]
name = "My second"
icon = "🎈️"
is_section = true

# Pages after an `is_section = true` will be indented
[[pages]]
name = "Another page"
icon = "💪"

# Unless you explicitly say in_section = false`
[[pages]]
name = "Not in a section"
in_section = false
```

Streamlit code:

```python
from st_pages import show_pages_from_config, add_page_title

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()

show_pages_from_config()
```

# Hiding pages

You can now pass a list of page names to `hide_pages` to hide pages dynamically for each
user. Note that these pages are only hidden via CSS, and can still be visited by the URL.
However, this could be a good option if you simply want a way to visually direct your
user where they should be able to go next.

NOTE: You should only hide pages that have also been added to the sidebar already.

```py
show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("another.py", "Another page"),
    ]
)

hide_pages(["Another page"])
```
