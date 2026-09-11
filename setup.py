# -*- coding: utf-8 -*-
"""Build hook only. All packaging metadata lives in pyproject.toml.

``sphinx_docx/docx/style.docx`` is not in the repository: it is a zip of
``style_file/docx/``, rebuilt here so the wheel and the editable install both
get an up-to-date copy. It has to run before ``build_py``, which is the step
that collects ``package_data``.
"""
import importlib.util
import os

from setuptools import setup
from setuptools.command.build_py import build_py

HERE = os.path.dirname(os.path.abspath(__file__))


def _create_style_file():
    """Run create_style_file.py by path.

    A PEP 517 build does not put the project root on ``sys.path``, so a plain
    ``import create_style_file`` fails there even though it works under a
    legacy ``python setup.py`` invocation.
    """
    spec = importlib.util.spec_from_file_location(
        '_sphinx_docx_create_style_file',
        os.path.join(HERE, 'create_style_file.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.create_style_file()


class BuildPyWithStyleFile(build_py):
    def run(self):
        _create_style_file()
        return super().run()


setup(cmdclass={'build_py': BuildPyWithStyleFile})
