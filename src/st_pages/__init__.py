from __future__ import annotations

import json
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

import streamlit as st
import toml
from streamlit import (
    _gather_metrics,  # type: ignore
    runtime,
)
from streamlit.commands.page_config import Layout, get_random_emoji
from streamlit.errors import StreamlitAPIException
from streamlit.navigation.page import StreamlitPage
from streamlit.source_util import _on_pages_changed, get_pages


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

    if "pages_to_hide" not in st.session_state:
        st.session_state["pages_to_hide"] = []

    # Filter out pages that are in the pages_to_hide list
    pages = [
        p
        for p in pages
        if p.name not in st.session_state["pages_to_hide"] or p.is_section
    ]

    has_sections = any(p.is_section for p in pages)

    if has_sections:
        pages_data = {}

        current_section = ""

        for page in pages:
            if page.is_section:
                current_section = f"{translate_icon(page.icon)} {page.name}"
                continue
            if current_section not in pages_data:
                pages_data[current_section] = []
            pages_data[current_section].append(
                st.Page(page.path, title=page.name, icon=translate_icon(page.icon))
            )

        for section in pages_data:
            if section in st.session_state["pages_to_hide"]:
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
        "pages_to_hide" not in st.session_state
        or st.session_state["pages_to_hide"] != pages
    ):
        st.session_state["pages_to_hide"] = pages
        st.rerun()


def _add_page_title(
    page: StreamlitPage,
    layout: Layout = "centered",
    **kwargs,
):
    """
    Adds the icon and page name to the page as an st.title, and also sets the
    page title and favicon in the browser tab.

    All **kwargs are passed to st.set_page_config
    """
    page_title = page.title
    page_icon = translate_icon(page.icon)

    with suppress(StreamlitAPIException):
        st.set_page_config(
            page_title=page_title,
            page_icon=page_icon,
            layout=layout,
            **kwargs,
        )

    print(page_icon)

    st.title(f"{page_icon} {page_title}")


add_page_title = _gather_metrics("st_pages.add_page_title", _add_page_title)


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
    in_section: bool = True
    # use_relative_hash: bool = False

    # @property
    # def page_path(self) -> Path:
    #     return Path(str(self.path))

    # @property
    # def page_name(self) -> str:
    #     standard_name = page_icon_and_name(self.page_path)[1]
    #     standard_name = standard_name.replace("_", " ").title()
    #     if self.name is None:
    #         return standard_name
    #     return self.name

    # @property
    # def page_icon(self) -> str:
    #     standard_icon = page_icon_and_name(self.page_path)[0]
    #     icon = self.icon or standard_icon or ""
    #     return icon

    # @property
    # def relative_page_hash(self) -> str:
    #     if self.is_section:
    #         return calc_md5(f"{self.page_path}_{self.page_name}")
    #     return calc_md5(str(self.page_path))

    # @property
    # def page_hash(self) -> str:
    #     if self.use_relative_hash:
    #         return self.relative_page_hash
    #     if self.is_section:
    #         return calc_md5(f"{self.page_path}_{self.page_name}")
    #     return calc_md5(str(self.page_path.absolute()))

    # def to_dict(self) -> dict[str, str | bool]:
    #     return {
    #         "page_script_hash": self.page_hash,
    #         "page_name": self.page_name,
    #         "icon": self.page_icon,
    #         "script_path": str(self.page_path.absolute()),
    #         "is_section": self.is_section,
    #         "in_section": self.in_section,
    #         "relative_page_hash": self.relative_page_hash,
    #     }

    @classmethod
    def from_dict(cls, page_dict: dict[str, str | bool]) -> Page:
        return cls(
            path=str(page_dict["script_path"]),
            name=str(page_dict["page_name"]),
            icon=str(page_dict["icon"]),
            is_section=bool(page_dict["is_section"]),
            in_section=bool(page_dict["in_section"]),
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

    # if "show_pages_ran" in st.session_state:
    #     return

    if "show_pages_ran" not in st.session_state:
        st.set_option("client.showSidebarNavigation", False)
        st.session_state["show_pages_ran"] = True

    st.session_state["pages"] = pages

    has_sections = any(p.is_section for p in pages)

    if has_sections:
        pages_data = {}

        current_section = ""

        for page in pages:
            if page.is_section:
                current_section = page.name
                continue
            if current_section not in pages_data:
                pages_data[current_section] = []
            pages_data[current_section].append(
                st.Page(page.path, title=page.name, icon=page.icon)
            )
    else:
        pages_data = []

        for page in pages:
            pages_data.append(st.Page(page.path, title=page.name, icon=page.icon))

    pg = st.navigation(pages_data)

    pg.run()

    return

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

    first_page_hash = list(current_pages.keys())[0]

    current_pages.clear()
    for idx, page in enumerate(pages):
        if idx == 0:
            if page.relative_page_hash == first_page_hash:
                page.use_relative_hash = True
        current_pages[page.page_hash] = page.to_dict()

    _on_pages_changed.send()

    rt = runtime.get_instance()

    # if hasattr(rt, "_script_cache"):
    #     sleep(1)  # Not sure why this is needed, but it seems to be.

    #     rt._sources_watcher = LocalSourcesWatcher(rt._main_script_path)
    #     rt._sources_watcher.register_file_change_callback(
    #         lambda _: rt._script_cache.clear()
    #     )


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


# def _get_indentation_code() -> str:
#     styling = ""
#     current_pages = get_pages("")
#     is_indented = False
#     for idx, val in enumerate(current_pages.values()):
#         if val.get("is_section"):
#             styling += f"""
#                 div[data-testid=\"stSidebarNav\"] li:nth-child({idx + 1}) a {{
#                     pointer-events: none; /* Disable clicking on section header */
#                 }}
#             """
#             is_indented = True
#         elif is_indented and not val.get("in_section"):
#             # Page is specifically unnested
#             # Un-indent all pages until next section
#             is_indented = False
#         elif is_indented:
#             # Unless specifically unnested, indent all pages that aren't section headers
#             styling += f"""
#                 div[data-testid=\"stSidebarNav\"] li:nth-child({idx + 1})
#                     span:nth-child(1) {{
#                         margin-left: 1.5rem;
#                 }}
#             """

#     styling = f"""
#         <style>
#             {styling}
#         </style>
#     """

#     return styling


# def _add_indentation():
#     """
#     For an app that has set one or more "sections", this will add indentation
#     to the files "within" a section, and make the sections itself
#     unclickable. Makes the sidebar look like something like this:

#     - page 1
#     - section 1
#         - page 2
#         - page 3
#     - section 2
#         - page 4
#     """

#     styling = _get_indentation_code()

#     st.write(
#         styling,
#         unsafe_allow_html=True,
#     )


# add_indentation = _gather_metrics("st_pages.add_indentation", _add_indentation)


# def _get_page_hiding_code(pages_to_hide: list[str]) -> str:
#     styling = ""
#     current_pages = get_pages("")
#     section_hidden = False
#     for idx, val in enumerate(current_pages.values()):
#         page_name = val.get("page_name")
#         if val.get("is_section"):
#             # Set whole section as hidden
#             section_hidden = page_name in pages_to_hide
#         elif not val.get("in_section"):
#             # Reset whole section hiding if we hit a page thats not in a section
#             section_hidden = False
#         if page_name in pages_to_hide or section_hidden:
#             styling += f"""
#                 div[data-testid=\"stSidebarNav\"] li:nth-child({idx + 1}) {{
#                     display: none;
#                 }}
#             """

#     styling = f"""
#         <style>
#             {styling}
#         </style>
#     """

#     return styling


# def _hide_pages(hidden_pages: list[str]):
#     """
#     For an app that wants to dynmically hide specific pages from the navigation bar.
#     Note - this simply uses CSS to hide the menu item, it does not remove the page
#     If using this with any security / permissions in mind,
#     you also need to block the hidden page from executing
#     """

#     styling = _get_page_hiding_code(hidden_pages)

#     st.write(
#         styling,
#         unsafe_allow_html=True,
#     )


# hide_pages = _gather_metrics("st_pages.hide_pages", _hide_pages)
