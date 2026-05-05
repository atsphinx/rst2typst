"""Management Typst custom package."""

import logging
import shutil
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
