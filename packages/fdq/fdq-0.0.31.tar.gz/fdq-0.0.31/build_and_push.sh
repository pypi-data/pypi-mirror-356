#!/bin/bash

PYPI_TOKEN="pypi-AgEIcHlwaS5vcmcCJDc1OWM5OTRjLTJhYjAtNDhjYS04ZDYwLTAyODFmY2QwZmUwMwACKlszLCJhODg3ZmFiNy1jOTUzLTQzNjYtYTE2Yi02NzhmYTAxMjM3NjkiXQAABiAc56vL8lmEu0v1GjwqY53m67c0sQ-kyawAeiORygwc5Q"

rm -Rf /home/marc/dev/fonduecaquelon/dist/*
python3 -m build
python3 -m twine upload -u __token__ -p "$PYPI_TOKEN" dist/*