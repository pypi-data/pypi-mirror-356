# itkwasm-transform-emscripten

[![PyPI version](https://badge.fury.io/py/itkwasm-transform-emscripten.svg)](https://badge.fury.io/py/itkwasm-transform-emscripten)

Common operations with and on spatial transformations. Emscripten implementation.

This package provides the Emscripten WebAssembly implementation. It is usually not called directly. Please use the [`itkwasm-transform`](https://pypi.org/project/itkwasm-transform/) instead.


## Installation

```sh
import micropip
await micropip.install('itkwasm-transform-emscripten')
```

## Development

```sh
pip install hatch
hatch run download-pyodide
hatch run test
```
