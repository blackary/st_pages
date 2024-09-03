from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import streamlit as st
import toml
from streamlit.commands.page_config import get_random_emoji
from streamlit.navigation.page import StreamlitPage
from streamlit.runtime.metrics_util import gather_metrics
from streamlit.source_util import page_icon_and_name


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
        if (
            p.name not in st.session_state[HIDE_PAGES_KEY]
            and str(p.name).replace("_", " ") not in st.session_state[HIDE_PAGES_KEY]
        )
        or p.is_section
    ]

    has_sections = any(p.is_section for p in pages)

    pages_data: dict[str, list[StreamlitPage]] | list[StreamlitPage] = []

    if has_sections:
        pages_data = {}

        current_section = ""

        sections_to_drop = []

        for page in pages:
            if page.is_section:
                if hasattr(page, "icon") and page.icon != "":
                    current_section = f"{translate_icon(page.icon)} {page.name}"
                else:
                    current_section = cast(str, page.name)
                if page.name in st.session_state[HIDE_PAGES_KEY]:
                    sections_to_drop.append(current_section)
                continue
            if current_section not in pages_data:
                pages_data[current_section] = []
            pages_data[current_section].append(
                st.Page(
                    page.path,
                    title=page.name,
                    icon=translate_icon(page.icon if hasattr(page, "icon") else None),
                    url_path=page.url_path,
                )
            )

        for section in sections_to_drop:
            del pages_data[section]
    else:
        pages_data = []

        for page in pages:
            pages_data.append(
                st.Page(
                    page.path,
                    title=page.name,
                    icon=translate_icon(page.icon if hasattr(page, "icon") else None),
                    url_path=page.url_path,
                )
            )

    return pages_data
