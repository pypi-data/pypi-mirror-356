"""Extracts data from PE files."""

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


from pathlib import Path

import pefile


type ExportedSymbols = list[tuple[str, int]]


def list_exported_symbols(path: Path) -> ExportedSymbols:
    """Extracts exported symbols from a PE file.

    Args:
        path:
            path to the PE file.
    """

    pe = pefile.PE(path, fast_load=True)
    pe.parse_data_directories()

    return [(exp.name.decode('utf-8'), exp.ordinal) for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols]


def generate_def_file(dll_path: Path, symbols: ExportedSymbols, path: Path):
    """Generates a .def file from a PE file.

    Args:
        dll_path:
            path to the DLL file.
        symbols:
            list of exported symbols.
        path:
            path to the output file.
    """

    with path.open('w+', encoding='utf-8') as f:
        f.write('EXPORTS\n')

        for name, ordinal in symbols:
            f.write(f'\t{name}={dll_path.parent / dll_path.stem}.{name} @{ordinal}\n')

