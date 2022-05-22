#!/bin/bash

python -m venv .venv
source .venv/bin/activate
pip install mypy autopep8
ln -s ~/.config/blender/3.1/scripts/modules/* .venv/lib/python3.10/site-packages/
