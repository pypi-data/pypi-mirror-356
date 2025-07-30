#!/bin/bash
git pull

PYPI_TOKEN="pypi-AgEIcHlwaS5vcmcCJDRhZDQxYzlkLWI4NDMtNDgyYi05M2NjLTdiNzI0ZTJjYWYwNwACC1sxLFsiZmRxIl1dAAIsWzIsWyIyODA0MDMwZi1jZDFhLTRlMjEtOTcxYi04MDE2OTkwYzJhYjciXV0AAAYg0feX37LdQLFOJrQMCBjkNtYf1o3Sxh-kJ7xy07SXOZc"

rm -Rf /home/marc/dev/fonduecaquelon/dist/*
python3 -m build
python3 -m twine upload -u __token__ -p "$PYPI_TOKEN" dist/*