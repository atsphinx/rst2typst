Spec of translator
==================

:py:class:`TypstTranslator <rst2typst.writer.TypstTranslator>` is a core class for convert from DocTree to Typst code.
These are list of translate specs that what convert from each docutils' nodes.

.. note::

   These are not all spec for nodes of docutils yet.
   Currently, please see `e2e test directory <https://github.com/atsphinx/rst2typst/tree/dev/e2e/cases-cli>`_  to know all behaviors of translator.

.. toctree::
   :maxdepth: 1
   :caption: List of translate specs:
   :glob:

   spec/*/index
