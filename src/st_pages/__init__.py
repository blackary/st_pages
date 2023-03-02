from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import toml

try:
    from streamlit import _gather_metrics  # type: ignore
except ImportError:

    def _gather_metrics(name, func, *args, **kwargs):
        return func


import requests
import streamlit as st
from streamlit.commands.page_config import get_random_emoji
from streamlit.errors import StreamlitAPIException

try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx
except ImportError:
    from streamlit.scriptrunner.script_run_context import (  # type: ignore
        get_script_run_ctx,
    )

from streamlit.source_util import _on_pages_changed, get_pages

try:
    from streamlit.source_util import page_icon_and_name
except ImportError:
    from streamlit.source_util import page_name_and_icon  # type: ignore

    def page_icon_and_name(script_path: Path) -> tuple[str, str]:
        icon, name = page_name_and_icon(script_path)
        return name, icon


try:
    from streamlit import cache_resource
except ImportError:
    from streamlit import experimental_singleton as cache_resource

from streamlit.util import calc_md5


def _add_page_title(add_icon: bool = True, also_indent: bool = True, **kwargs):
    """
    Adds the icon and page name to the page as an st.title, and also sets the
    page title and favicon in the browser tab.

    All **kwargs are passed to st.set_page_config
    """
    pages = get_pages("")
    ctx = get_script_run_ctx()

    if ctx is not None:
        try:
            current_page = pages[ctx.page_script_hash]
        except KeyError:
            try:
                current_page = [
                    p
                    for p in pages.values()
                    if p["relative_page_hash"] == ctx.page_script_hash
                ][0]
            except IndexError:
                return

        if "page_title" not in kwargs:
            kwargs["page_title"] = current_page["page_name"]

        if "page_icon" not in kwargs:
            kwargs["page_icon"] = current_page["icon"]

        page_title = current_page["page_name"]
        page_icon = current_page["icon"]

        try:
            st.set_page_config(**kwargs)
        except StreamlitAPIException:
            pass

        if add_icon:
            st.title(f"{translate_icon(page_icon)} {page_title}")
        else:
            st.title(page_title)

        if also_indent:
            add_indentation()


add_page_title = _gather_metrics("st_pages.add_page_title", _add_page_title)


@cache_resource
def get_icons() -> dict[str, str]:
    url = "https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json"
    return requests.get(url).json()


def translate_icon(icon: str) -> str:
    """
    If you pass a name of an icon, like :dog:, translate it into the
    corresponding unicode character
    """
    if icon == "random":
        icon = get_random_emoji()
    elif icon.startswith(":") and icon.endswith(":"):
        icon = icon[1:-1]
        icons = get_icons()
        if icon in icons:
            return icons[icon]
    return icon


@dataclass
class Page:
    """
    Utility class for working with pages

    Parameters
    ----------
    path: str
        The path to the page
    name: str (optional)
        The name of the page. If not provided, the name will be inferred from
        the path
    icon: str (optional)
        The icon of the page. If not provided, the icon will be inferred from
        the path
    """

    path: str
    name: str | None = None
    icon: str | None = None
    is_section: bool = False

    @property
    def page_path(self) -> Path:
        return Path(str(self.path))

    @property
    def page_name(self) -> str:
        standard_name = page_icon_and_name(self.page_path)[1]
        standard_name = standard_name.replace("_", " ").title()
        if self.name is None:
            return standard_name
        return self.name

    @property
    def page_icon(self) -> str:
        standard_icon = page_icon_and_name(self.page_path)[0]
        icon = self.icon or standard_icon or ""
        return translate_icon(icon)

    @property
    def relative_page_hash(self) -> str:
        if self.is_section:
            return calc_md5(f"{self.page_path}_{self.page_name}")
        return calc_md5(str(self.page_path))

    @property
    def page_hash(self) -> str:
        if self.is_section:
            return calc_md5(f"{self.page_path}_{self.page_name}")
        return calc_md5(str(self.page_path.absolute()))

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "page_script_hash": self.page_hash,
            "page_name": self.page_name,
            "icon": self.page_icon,
            "script_path": str(self.page_path),
            "is_section": self.is_section,
            "relative_page_hash": self.relative_page_hash,
        }

    @classmethod
    def from_dict(cls, page_dict: dict[str, str | bool]) -> Page:
        return cls(
            path=str(page_dict["script_path"]),
            name=str(page_dict["page_name"]),
            icon=str(page_dict["icon"]),
            is_section=bool(page_dict["is_section"]),
        )


class Section(Page):
    def __init__(self, name: str, icon: str | None = None):
        super().__init__(path="", name=name, icon=icon, is_section=True)


def _show_pages(pages: list[Page]):
    """
    Given a list of Page objects, overwrite whatever pages are currently being
    shown in the sidebar, and overwrite them with this new set of pages.

    NOTE: This changes the list of pages globally, not just for the current user, so
    it is not appropriate for dymaically changing the list of pages.
    """
    current_pages: dict[str, dict[str, str | bool]] = get_pages("")  # type: ignore
    if set(current_pages.keys()) == set(p.page_hash for p in pages):
        return

    try:
        default_page = [p.path for p in pages if p.path][0]
    except IndexError:
        raise ValueError("Must pass at least one page to show_pages")

    for page in pages:
        if page.is_section:
            page.path = default_page

    current_pages.clear()
    for page in pages:
        current_pages[page.page_hash] = page.to_dict()

    _on_pages_changed.send()


show_pages = _gather_metrics("st_pages.show_pages", _show_pages)


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


def _show_pages_from_config(path: str = ".streamlit/pages.toml"):
    """
    Show the pages listed in the config file at the given path
    (default: .streamlit/pages.toml)
    """
    pages = _get_pages_from_config(path)

    if pages is not None:
        show_pages(pages)


show_pages_from_config = _gather_metrics(
    "st_pages.show_pages_from_config", _show_pages_from_config
)


def _get_indentation_code() -> str:
    styling = ""
    current_pages = get_pages("")

    is_indented = False

    for idx, val in enumerate(current_pages.values()):
        if val.get("is_section"):
            styling += f"""
                li:nth-child({idx + 1}) a {{
                    pointer-events: none; /* Disable clicking on section header */
                }}
            """
            is_indented = True
        elif is_indented:
            # Unless specifically unnested, indent all pages that aren't section headers
            styling += f"""
                li:nth-child({idx + 1}) span:nth-child(1) {{
                    margin-left: 1.5rem;
                }}
            """

    styling = f"""
        <style>
            {styling}
        </style>
    """

    return styling


def _add_indentation():
    """
    For an app that has set one or more "sections", this will add indentation
    to the files "within" a section, and make the sections itself
    unclickable. Makes the sidebar look like something like this:

    - page 1
    - section 1
        - page 2
        - page 3
    - section 2
        - page 4
    """

    styling = _get_indentation_code()

    st.write(
        styling,
        unsafe_allow_html=True,
    )


add_indentation = _gather_metrics("st_pages.add_indentation", _add_indentation)
