Document properties
===================

sphinx-docx embeds document properties into the generated document. They can
be referenced from the cover page, through Insert > Quick Parts > Field in
Office Word.

The properties are the *docproperties* item of the ``docx_documents``
configuration: a dictionary from property name to value. Some names are
treated as the properties OOXML defines.

A ``DOCPROPERTY`` field in the style file shows the value in Office Word once
Word recalculates the field. For every other reader, the value is baked into
the document by ``docx_bake_property_fields``, which is on by default.

The names below are written as Core Properties [ECMA376]_.

.. hlist::
   :columns: 3

   - title
   - creator
   - language
   - category
   - contentStatus
   - description
   - identifier
   - lastModifiedBy
   - lastPrinted
   - revision
   - subject
   - version
   - keywords
   - created
   - modified

The value of "created" or "modified" must be a ``date`` or ``datetime``
object, or a string in one of these formats.

.. hlist::
   :columns: 3

   - ``YYYY``
   - ``YYYY-MM``
   - ``YYYY-MM-DD``
   - ``YYYY-MM-DDThh``
   - ``YYYY-MM-DDThh:mm``
   - ``YYYY-MM-DDThh:mm:ss``
   - ``YYYY-MM-DDThh:mm:ss.s``

The value of "lastPrinted" must be a ``date`` or ``datetime`` object, or a
string in the ``YYYY-MM-DDThh:mm:ss`` format. Times given as strings are read
as system local time.

The value of "keywords" must be a string or a list of strings. Every other
core property must be a string.

The names below are written as Extended Properties [ECMA376]_.

.. hlist::
   :columns: 3

   * company
   * manager

The names below are written as Cover Page Properties [MSOE376]_.

.. hlist::
   :columns: 3

   * abstract
   * companyAddress
   * companyEmail
   * companyFax
   * companyPhone
   * publishDate

The value of "publishDate" must be a ``date`` or ``datetime`` object, or a
string in one of the formats above.

Every other key becomes a custom property. Its value must be an integer,
float, string, bool, or ``datetime`` object.

.. rubric:: Citations

.. [ECMA376] Standard ECMA-376,
   https://www.ecma-international.org/publications/standards/Ecma-376.htm
.. [MSOE376] [MS-OE376]: Office Implementation Information for ECMA-376 Standards Support,
   https://docs.microsoft.com/en-us/openspecs/office_standards/ms-oe376/db9b9b72-b10b-4e7e-844c-09f88c972219

