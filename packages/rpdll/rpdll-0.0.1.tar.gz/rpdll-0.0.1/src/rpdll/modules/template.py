"""Allows easy access to project templates."""

# Copyright (C) 2025  Stefano Cuizza

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, TypedDict

from jinja2 import Environment, FileSystemLoader, Template

from ..modules import metadata


TEMPLATES_DIRECTORY: Traversable = resources.files(metadata.package()) / 'templates'

ENVIRONMENT = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIRECTORY))
)


class BuildRsTemplateParameters(TypedDict):
    """Parameters accepted by the `build.rs` template."""

    exported_symbols: list[tuple[str, int]]
    dll_path: PureWindowsPath


class ConfigRsTemplateParameters(TypedDict):
    """Parameters accepted by the `config.rs` template."""

    package_name: str


class LibRsTemplateParameters(TypedDict):
    """Parameters accepted by the `config.rs` template."""


def get(name: str) -> Template:
    """Loads template by name.

    Args:
        name:
            the name of the template.

    Raises:
        TemplateNotFound:
            if the template doesn't exist.
    """

    return ENVIRONMENT.get_template(f'{name}.jinja' if not name.endswith('.jinja') else name)


def enum() -> list[str]:
    """Lists all available templates."""

    available_templates = (
        PurePosixPath(template) for template in ENVIRONMENT.list_templates()
    )

    return [
        template_path.as_posix().rsplit('.', maxsplit=1)[0]
        for template_path in available_templates
    ]
