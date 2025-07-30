"""
Placeholder for our i18n.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import sphinx.locale

if TYPE_CHECKING:
    from gettext import NullTranslations

locale_dir = Path(__file__).parent.resolve()

__all__ = [
    "init_console",
    "t_",
    "t__",
]

t_ = sphinx.locale._
t__ = sphinx.locale.__


def init_console(catalogue: str) -> tuple[NullTranslations, bool]:
    return sphinx.locale.init_console(str(locale_dir), catalogue)
