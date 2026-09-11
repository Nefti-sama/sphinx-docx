Cooperation with third party extensions
=======================================

sphinx-docx supports any third party extension which produces a well-formed
`docutils document tree`_.

Some extensions add docutils nodes of their own instead. Those nodes are
unknown to the builder and are skipped, so their contents do not reach the
document. To include them, define a visit function for the node in
``conf.py``.

The example below handles the ``plantuml`` node.

.. code-block:: python
   :caption: Example to define a method for third party extension

   # in conf.py
   def setup(app):
       # Visit method for the plantuml node of sphinxcontrib.plantuml
       # https://pypi.org/project/sphinxcontrib-plantuml/
       def docx_visit_plantuml(self, node):
           def get_filepath(self, node):
               from sphinxcontrib import plantuml
               _, filepath = plantuml.render_plantuml(self, node, 'png')
               return filepath
           alt = node.get('alt', (node['uml'], None))
           # The translator provides helpers for this. See the API reference.
           self.visit_image_node(node, alt, get_filepath)
       # Attach the visit method to the docx translator
       import sphinx_docx
       translator = sphinx_docx.DocxBuilder.default_translator_class
       setattr(translator, 'visit_plantuml', docx_visit_plantuml)

.. _`docutils document tree`: https://docutils.sourceforge.io/docs/ref/doctree.html

