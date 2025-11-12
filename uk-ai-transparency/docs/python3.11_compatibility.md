# Python 3.11 Compatibility Notes

This document explains why the selected package versions are appropriate for use with Python 3.11 and gives installation hints for a Windows (PowerShell) environment.

Selected requirements (in `requirements.txt`):

- pandas>=2.1.0
- streamlit>=1.28.0
- plotly>=5.17.0
- numpy>=1.24.0

Why these versions work with Python 3.11

- NumPy (>=1.24.0): NumPy 1.24.x was the first series providing broad, official wheel support for Python 3.11 on common platforms. It contains compiled binary wheels for Windows, macOS and manylinux which avoids the need to build from source.

- pandas (>=2.1.0): pandas 2.x depends on NumPy 1.24+ and the pandas project publishes pre-built wheels compatible with Python 3.11. Choosing pandas>=2.1 ensures you're on a release that explicitly supports Python 3.11 and includes upstream fixes and compatibility improvements.

- Streamlit (>=1.28.0): Streamlit releases in the 1.28+ line include compatibility with modern Python versions including 3.11 and have pinned dependencies that work with NumPy/pandas 1.24+/2.x. Streamlit also distributes wheels so installation on Windows is generally straightforward.

- Plotly (>=5.17.0): Plotly is a pure-Python package (with optional binary extras) and the 5.17+ series supports newer Python interpreters; compatibility with Python 3.11 is available via the published wheels.

Practical installation notes

1. Upgrade pip first. Newer pip versions handle modern wheel tags and manylinux variants better, and they will pick up pre-built wheels for Python 3.11:

```powershell
python -m pip install --upgrade pip
```

2. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install the requirements:

```powershell
pip install -r requirements.txt
```

4. If you see any package trying to build from source (e.g., long compile times or errors), ensure you have a recent pip and wheel, and prefer installing binary wheels. On Windows, having a current wheel and pip usually prevents source builds. For particularly tricky cases, consider installing platform wheels from PyPI or using conda which provides prebuilt binaries.

Notes on pandas/NumPy ordering

- Because pandas depends on NumPy, pip will normally sort installations so that a compatible NumPy wheel is installed first. If you encounter a version conflict, explicitly installing NumPy (pip install "numpy>=1.24.0") before `pip install -r requirements.txt` can help.

Troubleshooting

- If you get a "required a different Python version" error, double-check that the `python` used in the venv is the Python 3.11 interpreter.
- If a package fails to build from source on Windows, install the Visual C++ build tools or prefer binary distributions (or use conda).

Recommended extras

- Add a `requirements-dev.txt` with tools such as `pytest`, `black` and `flake8` (this repo already includes one).
- Consider pinning exact versions for reproducible installs (e.g. `numpy==1.24.4`) in a production environment or for CI.

References

- NumPy release notes: https://numpy.org
- pandas release notes: https://pandas.pydata.org
- Streamlit installation docs: https://docs.streamlit.io
- Plotly docs: https://plotly.com/python
