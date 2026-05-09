"""Typst package helper.

.. note:: In this module, "Package" means Typst package.

This module provides two features.

* Package registry to manage packages and to render import statements.
* Helper functions to install files as local package.
"""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

import platformdirs

logger = logging.getLogger(__name__)


def build_install_path(name: str, version: str | None = None) -> Path:
    """Retrieve path object of package Typst local package.

    If version is not specified, name is treated as the name of a published Python package,
    and the installed version is used.

    :param name: Package name
    :param version: Version of package.
    """

    if version is None:
        version = metadata.version(name)
    base_dir = platformdirs.user_data_path("typst", appauthor=False, roaming=True)
    target = Path(f"packages/local/{name}/{version}")
    return base_dir / target


def install_package(
    source: Path, name: str, version: str | None = None, *, force: bool = False
):
    """Copy package directory as Typst local package.

    Ref
    ---

    * https://github.com/typst/packages#local-packages

    :param source: Source directory of Typst package.
    :param name: The name of local package.
    :param version: The version of local package.
    :param force: Flag to override package.
    """
    logger.debug("Installing '%s' Typst package into local from %s.", name, str(source))
    dest = build_install_path(name, version)
    dest.parent.mkdir(exist_ok=True, parents=True)
    if not dest.exists():
        pass
    elif force:
        shutil.rmtree(dest)
    else:
        logger.info("Package is already installed.")
        return
    shutil.copytree(source, dest)


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
