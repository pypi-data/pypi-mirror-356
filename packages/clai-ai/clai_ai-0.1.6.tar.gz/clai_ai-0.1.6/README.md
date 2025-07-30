rm -rf dist/
uv run -m build
twine upload dist/*


uv pip install --force-reinstall -e .


v pip install build                 
uv run -m build

 pipx install clai-ai   