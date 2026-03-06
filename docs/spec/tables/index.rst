======
Tables
======

Details
=======

rst2typst supports all types of tabple syntax,
but it only accepts some attributes.


Examples
========

Grid table
----------

.. tab-set-code::

   .. literalinclude:: grid-table.rst.txt
      :language: rst

   .. literalinclude:: grid-table.typ.txt
      :language: typst

Simple table
------------

.. tab-set-code::

   .. literalinclude:: simple-table.rst.txt
      :language: rst

   .. literalinclude:: simple-table.typ.txt
      :language: typst

CSV table
---------

.. tab-set-code::

   .. literalinclude:: csv-table.rst.txt
      :language: rst

   .. literalinclude:: csv-table.typ.txt
      :language: typst

List table
----------

.. tab-set-code::

   .. literalinclude:: list-table.rst.txt
      :language: rst

   .. literalinclude:: list-table.typ.txt
      :language: typst

References
==========

Docutils:

* https://www.docutils.org/docs/ref/rst/restructuredtext.html#tables
* https://www.docutils.org/docs/ref/rst/directives.html#tables

Typst:

* https://typst.app/docs/reference/model/table/
