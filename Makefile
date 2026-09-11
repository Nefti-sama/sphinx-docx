# Packaging targets. `dist` and `upload` need the build tooling:
#   .venv/bin/pip install build twine
PYTHON ?= .venv/bin/python

dist: clean-dist
	$(PYTHON) -m build
	$(PYTHON) -m twine check --strict dist/*

# Artefacts only. `clean` also drops the generated style.docx, which an
# editable install needs, so rebuild with `pip install -e .` afterwards.
clean-dist:
	-rm -rf build/ dist/ *.egg-info

clean: clean-dist
	-rm -rf sphinx_docx/docx/style.docx

update_style_file:
	./create_style_file.py
	(cd style_file; make docx)
	mv style_file/build/docx/style.docx sphinx_docx/docx/style.docx
	(cd style_file; make docx)
	unzip style_file/build/docx/style.docx -d style_file/docx

# Manual upload. The release workflow in .github/workflows/publish.yml does
# this from a tag with a PyPI trusted publisher instead, so no token is needed.
upload: dist
	$(PYTHON) -m twine upload --repository pypi dist/*

testupload: dist
	$(PYTHON) -m twine upload --repository testpypi dist/*

.PHONY: dist clean clean-dist update_style_file upload testupload
