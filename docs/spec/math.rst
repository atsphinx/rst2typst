====
Math
====

docutils supports LaTeX math syntax, but Typst does not support it natively.
Then, translator uses the `mitex` package provides a way to include LaTeX math in Typst documents.

When documment uses math roles or directives, translator append code to import packages automatically.
``#import`` expression are put on first of output.

Examples
========

Simple block
------------

From:

.. code-block:: rst

   .. math::

      x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}

To:

.. code-block:: typst

   #mitex(`
     x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
   `)

Inline role
-----------

From:

.. code-block:: rst

   The area of a circle is :math:`A_\text{c} = (\pi/4) d^2`.

To:

.. code-block:: typst

   The area of a circle is #mi(`A_\text{c} = (\pi/4) d^2`).

References
==========

Docutils:

* https://www.docutils.org/docs/ref/rst/mathematics.html
* https://docutils.sourceforge.io/docs/ref/rst/roles.html#math
* https://www.docutils.org/docs/ref/rst/directives.html#math

Typst:

* https://typst.app/universe/package/mitex/
