===============
Getting started
===============

Installation
============

This is published on PyPI.
You can install it by using pip or your package manager.

.. tab-set::

   .. tab-item:: pip

      .. code-block:: console

         pip install rst2typst

   .. tab-item:: uv

      .. code-block:: console

         uv add rst2typst

If you want to install latest sources that is not published,
please get from GitHub.

Write your document
===================

Please write reStructuredText into local file.
(e.g. The file name is ``document.rst`` in this page)

.. grid:: 2

    .. grid-item::
       :columns: 9

       .. literalinclude:: _examples/index.rst.txt
          :language: rst

    .. grid-item::
       :columns: 3

       .. note::

          This document has title, sections, paragraph, and list.

.. important::

   This is library for docutils, not Sphinx.
   So it can't work for directives only for Sphinx even if you want to use.
   (e.g. :rst:dir:`seealso` directive)

Convert to Typst code
=====================

Run installed command ``rst2typst`` with arguments that is your document.
In default, it generates Typst code into STDOUT.

.. grid:: 2

    .. grid-item::
       :columns: 9

       .. code-block:: console

          $ rst2typst document.rst

       .. literalinclude:: _examples/index.typ.txt
          :language: rst

    .. grid-item::
       :columns: 3

       .. note::

          This code is formatted for example.
          Actually, it is not cleared Typst code.

If you want to save into filesystem,
append positional argument.

.. code-block:: console

   $ rst2typst document.rst document.typ

Generate PDF (optional)
=======================

Generated Typst code is valid Typst code.
You can generate PDF by ``typst`` command.

.. tip:: Please install typst CLI by your hands.

.. code-block:: console

   $ typst document.typ
