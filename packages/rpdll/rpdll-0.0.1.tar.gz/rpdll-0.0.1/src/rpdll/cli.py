"""Command Line Interface entry point."""

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


from argparse import Namespace
import logging
import shutil
import sys
from typing import Any

import toml

from .modules import pe, template
from .modules.rusty import cargo_new_lib, is_cargo_installed


logger = logging.getLogger(__name__)


def main(namespace: Namespace) -> None:
    """Main CLI function.

    Args:
        namespace:
          Namespace containing the command line parsing.
    """

    if not is_cargo_installed():
        logger.error('cargo is not installed. Please install Rust from https://www.rust-lang.org/tools/install.')

        sys.exit(1)

    if not cargo_new_lib(namespace.project):
        sys.exit(1)

    try:
        # add `.cargo/config.toml`.
        cargo_conf: dict[str, Any] = {
            'build': {
                'target': 'x86_64-pc-windows-msvc',  # default target.
            },
            'target': {
                'i686-pc-windows-msvc': {
                    'rustflags': ['-C', f'link-arg=/DEF:{'./exports.def'}'],
                },
                'x86_64-pc-windows-msvc': {
                    'rustflags': ['-C', f'link-arg=/DEF:{'./exports.def'}'],
                },
            },
        }

        (namespace.project / '.cargo').mkdir(parents=False, exist_ok=True)
        with (namespace.project / '.cargo' / 'config.toml').open('w+', encoding='utf-8') as f:
            toml.dump(cargo_conf, f)

        # add `exports.def`.
        pe.generate_def_file(namespace.dll_path, namespace.exported_symbols, namespace.project / 'exports.def')

        # update `src/lib.rs`.
        (namespace.project / 'src').mkdir(parents=False, exist_ok=True)
        with (namespace.project / 'src' / 'lib.rs').open('w+', encoding='utf-8') as f:
            f.write(template.get('lib').render({
                'exported_symbols': namespace.exported_symbols,
            }))

        # update `Cargo.toml`.
        project_conf: dict[str, Any] = toml.load(namespace.project / 'Cargo.toml')

        project_conf |= {
            'dependencies': {
                'windows': {
                    'version': '0.*',
                    'features': [
                        'Win32_Foundation',
                        'Win32_Security',
                        'Win32_System_SystemServices',
                        'Win32_System_Threading',
                        'Win32_UI_WindowsAndMessaging',
                    ],
                },
                'windows-strings': {
                    'version': '0.4',
                }
            },
            'lib': {
                'crate-type': ['cdylib']  # https://doc.rust-lang.org/reference/linkage.html#r-link.cdylib.
            }
        }

        with (namespace.project / 'Cargo.toml').open('w+', encoding='utf-8') as f:
            toml.dump(project_conf, f)

    except Exception as e:
        shutil.rmtree(namespace.project)

        raise Exception from e
