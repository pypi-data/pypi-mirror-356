#!/bin/bash
git pull

PYPI_TOKEN="pypi-AgEIcHlwaS5vcmcCJGRhYTJkMjM5LTMyZTAtNDE5YS05YWFjLTFmMTRiZjk3MTg1OQACC1sxLFsiZmRxIl1dAAIsWzIsWyIyODA0MDMwZi1jZDFhLTRlMjEtOTcxYi04MDE2OTkwYzJhYjciXV0AAAYgrXucBxNPtIFEKJmcwNjgUqm6toDDw4UsViOEhTMRTWw"

rm -Rf /home/marc/dev/fonduecaquelon/dist/*
python3 -m build
python3 -m twine upload -u __token__ -p "$PYPI_TOKEN" dist/*