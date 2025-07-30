"""Main argument parser module."""

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


from argparse import (
    ArgumentParser, Namespace,
)
from collections.abc import Sequence
import logging
from pathlib import Path
from typing import Optional, override

from ..modules import metadata, pe
from ..modules.parsing.parsers import MainArgumentParserTemplate
from . import types


logger = logging.getLogger(__name__)


def _construct() -> ArgumentParser:
    """Returns an instance of the module's argument parser.

    Invoked by the `argparse` directive in the docs.
    For more information, see https://sphinx-argparse.readthedocs.io/en/stable.
    """

    return MainArgumentParser()


class MainArgumentParser(MainArgumentParserTemplate):
    """Handles the arguments that get passed to the package when its invoked
    directly from the command line (python -m package_name ...).
    """

    @override
    def __init__(self):
        super().__init__(
            prog=metadata.package(),
            description=metadata.summary(),
            prefix_chars='-',
        )

    def _extend_arguments(self) -> None:
        self.add_argument(
            'project',
            action='store',
            help='rust project folder name',
            type=types.absolute_path,
        )

        source_group = self.add_mutually_exclusive_group(required=True)

        source_group.add_argument(
            '-d', '--dll',
            action='store',
            dest='source_dll',
            help='extract exported functions from this DLL',
            metavar='path',
            type=Path,
        )

    def _extend_subparsers(self) -> None:
        pass

    @override
    def parse_args(
            self,
            args: Optional[Sequence[str]] = None,
            namespace: Optional[Namespace] = None
    ) -> Namespace:

        namespace = super().parse_args(args=args, namespace=namespace)

        namespace.dll_path = ''
        namespace.exported_symbols = []

        if namespace.source_dll:
            namespace.dll_path = namespace.source_dll
            namespace.exported_symbols = pe.list_exported_symbols(namespace.source_dll)

        # arguments = vars(namespace)

        return namespace
