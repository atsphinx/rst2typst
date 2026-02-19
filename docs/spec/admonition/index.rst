===========
Admonitions
===========

Details
=======

Translator generates block code of Typst to render "admonition" layout when it finds admonition directives.

This layout is complex, so it defines custom function to express simply.
In default, ``rst2typst`` inserts definition code of ``#admonition-callout`` function.

Examples
========

Danger admonition
-----------------

.. tab-set-code::

   .. literalinclude:: danger.rst.txt
      :language: rst

   .. literalinclude:: danger.typ.txt
      :language: typst

Generic admonition
------------------

.. tab-set-code::

   .. literalinclude:: generic.rst.txt
      :language: rst

   .. literalinclude:: generic.typ.txt
      :language: typst

References
==========

Docutils:

* https://www.docutils.org/docs/ref/rst/directives.html#specific-admonitions
* https://www.docutils.org/docs/ref/rst/directives.html#admonition
* https://www.docutils.org/docs/ref/doctree.html#admonition

Typst:

* https://typst.app/docs/reference/foundations/function/#defining-functions
