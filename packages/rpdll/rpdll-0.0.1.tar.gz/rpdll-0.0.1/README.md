
# 📦 proxy-dll

[![License: GPL v3](https://img.shields.io/badge/License-GPL_v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![Python version: 3.12+](https://img.shields.io/badge/python-3.12+-blue)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)


## Overview

This package simplifies the creation of a [proxy DLL](https://www.ired.team/offensive-security/persistence/dll-proxying-for-persistence) in Rust.


## Installation

Install the package from PyPI by running:

```bash
$ pip install rpdll
```


## Usage

To generate the Rust project folder, use the `rpdll` utility:

```bash
$ rpdll proxy -d target.dll
```

Note that this tool only works on **Windows**.


## Documentation

- [Official Documentation](https://x55xaa.github.io/proxy-dll)
- [CHANGELOG](https://github.com/x55xaa/proxy-dll/blob/main/CHANGELOG.md)
