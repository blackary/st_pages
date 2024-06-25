from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import streamlit as st
import toml
from streamlit import _gather_metrics  # type: ignore
from streamlit.commands.page_config import get_random_emoji
from streamlit.navigation.page import StreamlitPage


@st.cache_resource
def get_icons() -> dict[str, str]:
    emoji_path = Path(__file__).parent / "emoji.json"
    return json.loads(emoji_path.read_text(encoding="utf-8"))


def translate_icon(icon: str | None) -> str | None:
    """
    If you pass a name of an icon, like :dog:, translate it into the
    corresponding unicode character
    """
    if icon is None:
        return None

    if icon == "random":
        icon = get_random_emoji()
    elif icon.startswith(":") and icon.endswith(":") and ":material/" not in icon:
        icon = icon[1:-1]
        icon = get_icons().get(icon, icon)
    return icon


HIDE_PAGES_KEY = "_st_pages_pages_to_hide"


def _get_nav_from_toml(
    path: str = ".streamlit/pages.toml",
) -> list[StreamlitPage] | dict[str, list[StreamlitPage]]:
    """
    Given a path to a TOML file, return a list or dictionary that can be passed to
    st.navigation
    """
    pages = _get_pages_from_config(path)
    if pages is None:
        return []

    if HIDE_PAGES_KEY not in st.session_state:
        st.session_state[HIDE_PAGES_KEY] = []

    # Filter out pages that are in the pages_to_hide list
    pages = [
        p
        for p in pages
        if p.name not in st.session_state[HIDE_PAGES_KEY] or p.is_section
    ]

    has_sections = any(p.is_section for p in pages)

    pages_data: dict[str, list[StreamlitPage]] | list[StreamlitPage] = []

    if has_sections:
        pages_data = {}

        current_section = ""

        sections_to_drop = []

        for page in pages:
            if page.is_section:
                current_section = f"{translate_icon(page.icon)} {page.name}"
                if page.name in st.session_state[HIDE_PAGES_KEY]:
                    sections_to_drop.append(current_section)
                continue
            if current_section not in pages_data:
                pages_data[current_section] = []
            pages_data[current_section].append(
                st.Page(page.path, title=page.name, icon=translate_icon(page.icon))
            )

        for section in sections_to_drop:
            del pages_data[section]
    else:
        pages_data = []

        for page in pages:
            pages_data.append(
                st.Page(page.path, title=page.name, icon=translate_icon(page.icon))
            )

    return pages_data


get_nav_from_toml = _gather_metrics("st_pages.get_nav_from_toml", _get_nav_from_toml)


def hide_pages(pages: list[str]):
    if (
        HIDE_PAGES_KEY not in st.session_state
        or st.session_state[HIDE_PAGES_KEY] != pages
    ):
        st.session_state[HIDE_PAGES_KEY] = pages
        st.rerun()


def _add_page_title(page: StreamlitPage):
    """
    Adds the icon and page name to the page as an st.title.
    """
    page_title = page.title
    page_icon = translate_icon(page.icon)

    if page_icon and "/" in page_icon:
        page_icon = None

    st.title(f"{page_icon} {page_title}" if page_icon else page_title)


add_page_title = _gather_metrics("st_pages.add_page_title", _add_page_title)


@dataclass
class Page:
    path: str
    name: str | None = None
    icon: str | None = None
    is_section: bool = False


class Section(Page):
    def __init__(self, name: str, icon: str | None = None):
        super().__init__(path="", name=name, icon=icon, is_section=True)


def _get_pages_from_config(path: str = ".streamlit/pages.toml") -> list[Page] | None:
    """
    Given a path to a TOML file, read the file and return a list of Page objects
    """
    try:
        raw_pages: list[dict[str, str | bool]] = toml.loads(
            Path(path).read_text(encoding="utf-8")
        )["pages"]
    except (FileNotFoundError, toml.decoder.TomlDecodeError, KeyError):
        st.error(
            f"""
        Could not find a valid {path} file. Please create one
        with the following format:

        ```toml
        [[pages]]
        path = "example_app/streamlit_app.py"
        name = "Home"
        icon = ":house"

        [[pages]]
        path = "example_app/example_one.py"

        ...
            """
        )
        return None

    pages: list[Page] = []
    for page in raw_pages:
        if page.get("is_section"):
            page["path"] = ""
            pages.append(Section(page["name"], page["icon"]))  # type: ignore
        else:
            pages.append(Page(**page))  # type: ignore

    return pages
