# Reffinder

**Reffinder** is a static reference-finder for Python functions using [Pyright](https://github.com/microsoft/pyright) and the Language Server Protocol (LSP). It recursively traces references to functions and builds a dependency tree.


## ⚠️ Disclaimer

> **This project is currently a proof of concept.**  
> It may contain bugs, edge case limitations, or incomplete features.  
> Contributions and feedback are welcome.


## 🚀 Getting Started

### 🔧 Install
`pip install reffinder`

## 📌 Usage
`reffinder path/to/file.py <line_number> <definition_character>`
Notes:
- line_number is 0-based (e.g. if your IDE shows line 1, use 0)
- definition_character is the character offset of the function name's first letter

Example:
```
def example(...):
01234  <- character positions
```
To find references to example, run:
`reffinder my_module.py 0 4`

## 🛠 Development
### 📋 Prerequisites
- [Pyright](https://microsoft.github.io/pyright/#/installation?id=npm-package)
- [Poetry](https://python-poetry.org/docs/)

### ⚙️ Dev Setup
`poetry install`

### 🧪 Build
`poetry build`
To install the built wheel locally:
`pip install dist/reffinder-*.whl --force-reinstall`
