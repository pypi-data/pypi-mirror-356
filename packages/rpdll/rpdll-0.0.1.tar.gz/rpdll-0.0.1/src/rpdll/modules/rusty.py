"""A simple interface for some Rust utilities."""

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
import subprocess
from subprocess import PIPE


def is_cargo_installed() -> bool:
    """Checks if cargo is installed."""

    try:
        subprocess.run(['cargo', '--version'], check=True, stderr=PIPE, stdout=PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def cargo_new_lib(directory: Path) -> bool:
    """Creates a new Rust library project.

    Args:
        directory:
            the name of the new Rust library.
    """

    try:
        subprocess.run(['cargo', 'new', str(directory), '--lib'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False