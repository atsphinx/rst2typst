Home
====

.. raw:: html

   <style>
   h1 {
       display: none;
   }
   </style>

**Hello document writers!!**

rst2typst is Python project to provide features that convert reStructuredText to Typst code.
You can shorten build cycle to generate PDF your reStructuredText based document.

.. todo:: Write benchmark

.. grid:: 2
    :outline:

    .. grid-item::

        Input (reStructuredText):

        .. literalinclude:: _examples/index.rst.txt
           :language: rst

    .. grid-item::

        Output (Typst): [#]_

        .. [#] This is formatted code. writer do output unclearly.

        .. literalinclude:: _examples/index.typ.txt
           :language: typst

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   getting-started
   cli
   spec

.. toctree::
   :hidden:
   :caption: Reference:

   api
