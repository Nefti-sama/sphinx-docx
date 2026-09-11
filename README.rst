###########
sphinx-docx
###########

sphinx-docx is a Sphinx extension to build docx formatted documents. The
distribution is ``sphinx-docx``; the module you import and name in
``extensions`` is ``sphinx_docx``.

.. note::

   This extension butchered the `original docxbuilder <https://github.com/amedama41/docxbuilder>`_ to add some functionality.

Added:

* SVG images: the vector is embedded for Word 2016+, with a png fallback
* Multiple cover pages (`<https://github.com/amedama41/docxbuilder/pull/12>`_)
* Directives the original ignored: ``autosummary``, ``inheritance-diagram``,
  ``productionlist``, ``acks``, and PEP 695 type parameters in signatures
* Per-admonition styles, so ``.. note::`` and ``.. warning::`` can look different
* Sphinx 9 / docutils 0.22 compatibility (``findall``, ``FileOutput``)
* Common color names for the highlight of ``:emphasize-lines:``


************
Requirements
************

:Python: 3.12 or later (developed and tested on 3.14)
:Sphinx: 9.x or later

*******
Install
*******

::

   pip install sphinx-docx

For ``.. math::`` and the math role, which are rendered as OMML::

   pip install "sphinx-docx[math]"

Then add it to **conf.py**::

   extensions = [
       "sphinx_docx",
   ]

and build with::

   sphinx-build -b docx source build/docx

The development version::

   pip install "sphinx-docx @ git+https://github.com/Nefti-sama/sphinx-docx.git"

***********
Development
***********

The default style file ``sphinx_docx/docx/style.docx`` is generated, not
committed: ``create_style_file.py`` zips ``style_file/docx/`` into it, and
``.gitignore`` excludes the result. ``setup.py`` hooks that into ``build_py``,
which both a wheel build and a PEP 660 editable install run, so
``pip install -e .`` produces it.

Working straight from a clone without installing, regenerate it by hand after
``git clean -xdf`` or ``make clean``::

   python create_style_file.py

Without it, any build which does not set ``docx_style`` in **conf.py** aborts
with::

   FileNotFoundError: [Errno 2] No such file or directory: '.../sphinx_docx/docx/style.docx'

Edit the default style under ``style_file/docx/``, not ``style.docx`` itself;
the latter is overwritten on the next regeneration. ``make update_style_file``
does the full round trip, rebuilding ``style_file/docx/`` from the Sphinx
project in ``style_file/`` first; note that it calls
``./create_style_file.py``, which needs the executable bit and a ``python``
on PATH.

*****
Usage
*****

Add 'sphinx_docx' to ``extensions`` configuration of **conf.py**:

.. code:: python

   extensions = ['sphinx_docx']

and build your documents::

   make docx

You can control the generated document by adding configurations into ``conf.py``:

.. code:: python

   docx_documents = [
       ('index', 'sphinx_docx.docx', {
            'title': project,
            'creator': author,
            'subject': 'A manual of sphinx_docx',
        }, True),
   ]
   docx_style = 'path/to/custom_style.docx'
   docx_pagebreak_before_section = 1

For more details, see `the (original) documentation <https://docxbuilder.readthedocs.io/en/latest/>`_.

SVG images
==========

Use ``.. image::`` or ``.. figure::`` with an ``.svg`` file, as with any other
image::

   .. image:: diagram.svg
      :width: 12cm

Each SVG is embedded twice: the vector original, which Word 2016 and later
draw sharp at any zoom, and a png rendered with cairosvg for older clients.

Sizing follows the SVG's own ``width`` and ``height`` in any absolute unit
(``px``, ``pt``, ``pc``, ``in``, ``cm``, ``mm``), falling back to the
``viewBox`` when they are missing or relative. ``:width:`` and ``:height:``
override that as usual.

``cairosvg`` is installed as a dependency. Without it the build still
succeeds; every SVG is skipped with a warning instead of aborting.

Images an SVG pulls in with an ``href`` (another svg, a bitmap) are inlined as
data URIs, so they survive the move into the docx. References made through CSS
``url()`` are not, and draw empty (#TODO).

CSS custom properties are substituted before either renderer sees the file,
because neither cairosvg nor Word implements them. ``var(--bg, #ffffff)``
becomes ``#ffffff``; a ``var()`` with no fallback takes the value declared for
it elsewhere in the file, and one with neither becomes ``none``. Drawio 
emit these constantly -- a recent draw.io SVG is full of them -- and
without the substitution cairosvg fails the whole image with ``invalid literal
for int() with base 16``.

Directives
==========

Beyond what the original builder handles:

.. list-table::
   :header-rows: 1

   * - Directive
     - Rendered as
   * - ``.. autosummary::``
     - the summary table, and with ``:toctree:`` the generated stub pages
   * - ``.. inheritance-diagram::``
     - a graphviz image, through the same path as ``.. graphviz::``
   * - ``.. productionlist::``
     - a borderless two-column table, styled ``Production List``
   * - ``.. acks::``
     - the contained bullet list
   * - ``.. py:class:: Widget[T]``
     - PEP 695 type parameters, in square brackets

Admonitions take one table style per type, not a shared one: ``.. note::``
uses ``Admonition Note``, ``.. warning::`` uses ``Admonition Warning``, and a
``.. admonition:: My Title`` uses ``Admonition My Title``. Define the style in
your style file to change how that one type looks. Types you do not define get
a style created from ``Based Admonition``, so nothing breaks if it is missing.

Code highlighting
=================

``:emphasize-lines:`` highlights a line with the ``highlight_color`` of the
Pygments style, which is normally a hex string. A common color name is
accepted too:

.. code:: python

   # in conf.py, or a style module on sys.path
   from pygments.styles.default import DefaultStyle

   class MyStyle(DefaultStyle):
       highlight_color = 'lightgreen'

   pygments_style = 'mystyle.MyStyle'

Word does not take a color here: its ``w:highlight`` accepts only the fifteen
names of the OOXML ``ST_HighlightColor`` list, and a file using any other name
is invalid. So the requested color is snapped to the nearest name Word does
have, matching hue before brightness. ``lightgreen`` and ``lime`` highlight
green, ``orange`` and ``gold`` yellow, ``navy`` dark blue.


Style file
==========

Generated docx file's design is customized by a style file
(The default style is ``sphinx_docx/docx/style.docx``).
The style file is a docx file, which defines some paragraph,
character, and table styles.

The below lists shows typical styles.

Character styles:

* Emphasis
* Strong
* Literal
* Hyperlink
* Footnote Reference

Paragraph styles:

* Body Text
* Footnote Text
* Definition Term
* Literal Block
* Image Caption, Table Caution, Literal Caption
* Heading 1, Heading 2, ..., Heading *N*
* TOC Heading
* toc 1, toc 2, ..., toc *N*
* List Bullet
* List Number

Table styles:

* Table
* Field List
* Production List
* Admonition, Admonition Note, Admonition Warning, ...

****
TODO
****

- Support URL path for images.
- Follow CSS ``url()`` references inside SVG images.

*******
Licence
*******

MIT Licence

