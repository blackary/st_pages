# Streamlit-Pages

[![Build Status](https://img.shields.io/github/workflow/status/blackary/st_pages/testing/main)](https://github.com/blackary/st_pages/actions?query=workflow%3A%22testing%22+branch%3Amain)

<!--![Python Versions]("https://img.shields.io/pypi/pyversions/st_pages.svg")-->

![Python versions](https://img.shields.io/badge/python-3.7--3.10-blue.svg)

![Streamlit versions](https://img.shields.io/badge/streamlit-1.10.0--1.14.0-white.svg)

![License](https://img.shields.io/github/license/blackary/st_pages)

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation

```sh
pip install st-pages
```

## Why st-pages?

Streamlit has native support for [multi-page apps](https://blog.streamlit.io/introducing-multipage-apps/)
where page filenames are the source of truth for page settings.

But, you might want to be able to change the names, icons or order of your pages
without having to rename the files themselves.

This is an experimental package to try out how page-management might work if
you could name the pages whatever you wanted, and could manage which pages are visible,
and how they appear in the sidebar, via a setup function.

This enables you to set page _name_, _icon_ and _order_ independently of file name/path,
while still retaining the same sidebar & url behavior of current streamlit multi-page
apps.

## How to use

```python
from st_pages import Page, show_pages

show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("other_pages/page2", "Page 2", ":books:"),
    ]
)
```
