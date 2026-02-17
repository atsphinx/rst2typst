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

From:

.. code-block:: rst

   .. danger::
      Beware killer rabbits!

To:

.. code-block:: typst

   #admonition-callout(
     "danger", "Danger",
     [Beware killer rabbits!],
   )

Generic admonition
------------------

From:

.. code-block:: rst

   .. admonition:: And, by the way...

      You can make up your own admonition too.

To:

.. code-block:: typst

   #admonition-callout(
     "admonition", "And, by the way...",
     [You can make up your own admonition too.],
   )

References
==========

Docutils:

* https://www.docutils.org/docs/ref/rst/directives.html#specific-admonitions
* https://www.docutils.org/docs/ref/rst/directives.html#admonition
* https://www.docutils.org/docs/ref/doctree.html#admonition

Typst:

* https://typst.app/docs/reference/foundations/function/#defining-functions
