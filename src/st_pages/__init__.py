from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

import requests
import streamlit as st
from streamlit.commands.page_config import get_random_emoji

try:
    from streamlit.web.server import Server
except ImportError:
    from streamlit.server.server import Server  # type: ignore

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
    path: str
    name: Optional[str] = None
    icon: Optional[str] = None

    @property
    def page_name(self) -> str:
        standard_name = page_icon_and_name(Path(self.path))[1]
        standard_name = standard_name.replace("_", " ").title()
        if self.name is None:
            return standard_name
        return self.name

    @property
    def page_icon(self) -> str:
        standard_icon = page_icon_and_name(Path(self.path))[0]
        icon = self.icon or standard_icon or ""
        return translate_icon(icon)

    @property
    def page_hash(self) -> str:
        return calc_md5(self.path)


def show_pages(pages: Iterable[Page]):
    current_pages = get_pages(DEFAULT_PAGE)
    if set(current_pages.keys()) == set(p.page_hash for p in pages):
        return

    current_pages.clear()
    for page in pages:
        current_pages[page.page_hash] = {
            "page_script_hash": page.page_hash,
            "page_name": page.page_name,
            "icon": page.page_icon,
            "script_path": page.path,
        }

    _on_pages_changed.send()
