====
Math
====

Details
=======

docutils supports LaTeX math syntax, but Typst does not support it natively.
Then, translator uses the `mitex` package provides a way to include LaTeX math in Typst documents.

When documment uses math roles or directives, translator append code to import packages automatically.
``#import`` expression are put on first of output.

Examples
========

Simple block
------------

.. tab-set-code::

   .. literalinclude:: simple-block.rst.txt
      :language: rst

   .. literalinclude:: simple-block.typ.txt
      :language: typst

Inline role
-----------

.. tab-set-code::

   .. literalinclude:: inline-role.rst.txt
      :language: rst

   .. literalinclude:: inline-role.typ.txt
      :language: typst

References
==========

Docutils:

* https://www.docutils.org/docs/ref/rst/mathematics.html
* https://docutils.sourceforge.io/docs/ref/rst/roles.html#math
* https://www.docutils.org/docs/ref/rst/directives.html#math

Typst:

* https://typst.app/universe/package/mitex/
