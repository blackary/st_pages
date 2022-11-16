from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import toml

try:
    from streamlit import _gather_metrics
except ImportError:

    def _gather_metrics(name, func, *args, **kwargs):
        return func


import requests
import streamlit as st
from streamlit.commands.page_config import get_random_emoji
from streamlit.errors import StreamlitAPIException

try:
    from streamlit.web.server import Server
except ImportError:
    from streamlit.server.server import Server  # type: ignore

try:

    from streamlit.runtime.scriptrunner import get_script_run_ctx
except ImportError:
    from streamlit.scriptrunner.script_run_context import get_script_run_ctx  # type: ignore

from streamlit.source_util import _on_pages_changed, get_pages

try:
    from streamlit.source_util import page_icon_and_name
except ImportError:
    from streamlit.source_util import page_name_and_icon  # type: ignore

    def page_icon_and_name(script_path: Path) -> Tuple[str, str]:
        icon, name = page_name_and_icon(script_path)
        return name, icon


from streamlit.util import calc_md5

DEFAULT_PAGE: str = Server.main_script_path  # type: ignore


def _add_page_title(add_icon: bool = True):
    """
    Adds the icon and page name to the page as an st.title, and also sets the
    page title and favicon in the browser tab.
    """
    pages = get_pages(DEFAULT_PAGE)
    ctx = get_script_run_ctx()
    if ctx is not None:
        try:
            current_page = pages[ctx.page_script_hash]
        except KeyError:
            return

        page_title = current_page["page_name"]
        page_icon = current_page["icon"]
        try:
            st.set_page_config(page_title=page_title, page_icon=page_icon)
        except StreamlitAPIException:
            pass

        if add_icon:
            st.title(f"{translate_icon(page_icon)} {page_title}")
        else:
            st.title(page_title)


add_page_title = _gather_metrics("st_pages.add_page_title", _add_page_title)


@st.experimental_singleton
def get_icons() -> Dict[str, str]:
    url = "https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json"
    return requests.get(url).json()


def translate_icon(icon: str) -> str:
    """
    If you pass a name of an icon, like :dog:, translate it into the
    corresponding unicode character
    """
    icons = get_icons()
    if icon == "random":
        icon = get_random_emoji()
    if icon.startswith(":") and icon.endswith(":"):
        icon = icon[1:-1]
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
    name: Optional[str] = None
    icon: Optional[str] = None

    @property
    def page_path(self) -> Path:
        return Path(self.path)

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
    def page_hash(self) -> str:
        return calc_md5(str(self.page_path))


def _show_pages(pages: Iterable[Page]):
    """
    Given a list of Page objects, overwrite whatever pages are currently being
    shown in the sidebar, and overwrite them with this new set of pages.

    NOTE: This changes the list of pages globally, not just for the current user, so
    it is not appropriate for dymaically changing the list of pages.
    """
    current_pages = get_pages(DEFAULT_PAGE)
    if set(current_pages.keys()) == set(p.page_hash for p in pages):
        return

    current_pages.clear()
    for page in pages:
        current_pages[page.page_hash] = {
            "page_script_hash": page.page_hash,
            "page_name": page.page_name,
            "icon": page.page_icon,
            "script_path": str(page.page_path),
        }

    _on_pages_changed.send()


show_pages = _gather_metrics("st_pages.show_pages", _show_pages)


def _get_pages_from_config(path: str = ".streamlit/pages.toml") -> Optional[List[Page]]:
    """
    Given a path to a TOML file, read the file and return a list of Page objects
    """
    try:
        raw_pages = toml.loads(Path(path).read_text())["pages"]
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

    pages: List[Page] = []
    for page in raw_pages:
        pages.append(Page(**page))

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
