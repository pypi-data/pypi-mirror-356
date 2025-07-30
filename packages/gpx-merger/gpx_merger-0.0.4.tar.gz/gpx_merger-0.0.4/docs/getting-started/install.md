# Installation


## 🐍 PyPI

### Install the package from PyPI

Download from [PyPI](https://pypi.org/):

```bash
pip install gpx-merge
```

### Run CLI from command line
```bash
gpx-merge [OPTIONS] path/to/file
```

### Run GUI from command line
```bash
gpx-merge-gui
```

## 🔽 Executable

Download the latest executable:

- [⬇️ Download for Windows](https://github.com/pamagister/gpx-merge/releases/latest/download/installer-win.zip)
- [⬇️ Download for macOS](https://github.com/pamagister/gpx-merge/releases/latest/download/package-macos.zip)


## 👩🏼‍💻 Run from source

### Clone the repository

```bash
git clone
```

### Navigate to the project directory

```bash
cd gpx-merge
```

### Install dependencies

```bash
uv venv
uv pip install -e .[dev,docs]
```


### Run with CLI from source

```bash
python -m gpx_merge.cli [OPTIONS] path/to/file
```


### Run with GUI from source

```bash
python -m gpx_merge.gui
```

