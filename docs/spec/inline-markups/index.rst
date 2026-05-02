==============
Inline markups
==============

Details
=======

rst2typst supports most inline markup syntax.

Examples
========

Emphasis
--------

.. tab-set-code::

   .. literalinclude:: emphasis.rst.txt
      :language: rst

   .. literalinclude:: emphasis.typ.txt
      :language: typst

Strong emphasis
---------------

.. tab-set-code::

   .. literalinclude:: strong-emphasis.rst.txt
      :language: rst

   .. literalinclude:: strong-emphasis.typ.txt
      :language: typst

Literals
--------

.. tab-set-code::

   .. literalinclude:: literals.rst.txt
      :language: rst

   .. literalinclude:: literals.typ.txt
      :language: typst

Language roles (using "Interprepted text")
------------------------------------------

.. tab-set-code::

   .. literalinclude:: language-roles.rst.txt
      :language: rst

   .. literalinclude:: language-roles.typ.txt
      :language: typst

Title references
----------------

.. tab-set-code::

   .. literalinclude:: title-references.rst.txt
      :language: rst

   .. literalinclude:: title-references.typ.txt
      :language: typst

References
==========

Docutils:

* https://www.docutils.org/docs/ref/rst/restructuredtext.html#inline-markup

Typst:

* https://typst.app/docs/reference/model/emph/
* https://typst.app/docs/reference/model/strong/
* https://typst.app/docs/reference/text/raw/
