# Streamlit-Pages

[![Releases](https://img.shields.io/pypi/v/st-pages)](https://pypi.org/project/st-pages/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/blackary/st_pages/testing.yml?branch=main)](https://github.com/blackary/st_pages/actions?query=workflow%3A%22testing%22+branch%3Amain)
![Python Versions](https://img.shields.io/pypi/pyversions/st_pages.svg)
![Streamlit versions](https://img.shields.io/badge/streamlit-1.15.0--1.18.0-white.svg)
![License](https://img.shields.io/github/license/blackary/st_pages)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

> Summary: st-pages allows you to set the page names, order, and icons (and optionally
> group the pages into sections) in a multipage Streamlit app from your code without
> having to rename the files.

![image](https://user-images.githubusercontent.com/4040678/204576356-a436713f-93e4-41e3-82b9-6efeff744355.png)

Streamlit has native support for [multi-page apps](https://blog.streamlit.io/introducing-multipage-apps/)
where page filenames are the source of truth for page settings. But, it's a bit annoying
to have to change the filename to change the names in the sidebar or reorder the pages
in your app. Even more, I really dislike having to put emojis in filenames.

This is an experimental package to try out how page-management might work if
you could name the pages whatever you wanted, and could manage which pages are visible,
and how they appear in the sidebar, via a setup function.

This enables you to set page _name_, _icon_ and _order_ independently of file name/path,
while still retaining the same sidebar & url behavior of current streamlit multi-page
apps.

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

add_page_title() # By default this also adds indentation

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("other_pages/page2.py", "Page 2", ":books:"),
        Section("My section", icon="🎈️"),
        # Pages after a section will be indented
        Page("Another page", icon="💪"),
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
```

Streamlit code:

```python
from st_pages import show_pages_from_config, add_page_title

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()

show_pages_from_config()
```
