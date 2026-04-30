===========
Line blocks
===========

Details
=======

Line blocks are a reStructuredText syntax used to explicitly indicate
that line breaks should be treated as hard breaks.

rst2typst converts reST line blocks into ``\`` (markup of line breaks) in Typst,
as Typst lacks a built-in feature identical to reST's line blocks.

Examples
========

Simple usage
------------

.. tab-set-code::

   .. literalinclude:: simple-line-block.rst.txt
      :language: rst

   .. literalinclude:: simple-line-block.typ.txt
      :language: typst

References
==========

Docutils:

* https://www.docutils.org/docs/ref/rst/restructuredtext.html#line-blocks
* https://www.docutils.org/docs/ref/doctree.html#line-block

Typst:

* https://typst.app/docs/reference/model/link/
