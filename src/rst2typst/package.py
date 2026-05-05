"""Management Typst package.

In this module, "Package" means Typst package.
"""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

import platformdirs

logger = logging.getLogger(__name__)

package_dir = Path(__file__).parent / "package"


def build_install_path() -> Path:
    """Create path object of package Typst local package."""
    data_dir = platformdirs.user_data_dir("typst", appauthor=False, roaming=True)
    version = metadata.version("rst2typst")
    target = Path(f"packages/local/rst2typst/{version}")
    return data_dir / target


def install_package(*, force: bool = False):
    """Copy package directory as Typst local package.

    Ref
    ---

    * https://github.com/typst/packages#local-packages
    """
    logger.debug("Installing 'rst2typst' Typst package into local.")
    target_dir = build_install_path()
    target_dir.parent.mkdir(exist_ok=True, parents=True)
    if not target_dir.exists():
        pass
    elif force:
        shutil.rmtree(target_dir)
    else:
        logger.info("Package is already installed.")
        return
    shutil.copytree(package_dir, target_dir)


@dataclass(frozen=True)
class Entrypoint:
    """Importing target and alias of package."""

    name: str
    alias: str | None = None

    @property
    def code(self) -> str:
        """As Typst code."""
        return f"{self.name} as {self.alias}" if self.alias else self.name


class PackageRegistry(dict[str, set[Entrypoint]]):
    """Package management store."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(
        self, name: str, entrypoint: str | tuple[str, str] | Entrypoint | None = None
    ):
        """Add package path and entrypoints."""
        self.setdefault(name, set())
        if entrypoint is None:
            entrypoint = Entrypoint(name="*")
        elif isinstance(entrypoint, str):
            entrypoint = Entrypoint(name=entrypoint)
        elif isinstance(entrypoint, tuple):
            e_name, e_alias = entrypoint
            entrypoint = Entrypoint(name=e_name, alias=e_alias)  # ty: ignore[invalid-argument-type]
        if entrypoint.name == "*":
            self[name] = set()
        self[name].add(entrypoint)

    @property
    def code(self) -> str:
        """As Typst code."""
        lines = []
        for name, entrypoints in self.items():
            value = ", ".join([e.code for e in entrypoints])
            lines.append(f'#import "{name}": {value}')
        return "\n".join(lines)
