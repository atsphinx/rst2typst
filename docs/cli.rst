==================
Command line tools
==================

This project provides two entrypoints of command line tools.

* :ref:`rst2typst <cli-rst2typst>`
* :ref:`rst2typstpdf <cli-rst2typstpdf>`

.. _cli-rst2typst:

``rst2typst`` command
=====================

This is entrypoint to generate Typst code from reStructuredText.

Usage
-----

.. code::

   rst2typst [options] [<source> [<destination>]]

``source`` is path of reStructuredText file.

``destination`` is output path of Typst file. If ``destination`` is not specified, it outputs into STDOUT.

Options
-------

--template
  Template for render code.

  :Type: path string (``<filepath>``)
  :Default: Path of built-in template

  rst2typst computes translated strings and renders them using template.
  When you want to inject custom strings into head or foot of output,
  you can specify a template file path that has them.

--page-break-level
  Section level for page-break.

  :Type: Comma separated integers (``<int>(,<int>...)``)
  :Default: empty string (it means ``[]`` )

  Many PDF files as e-book usually have page breaks at high level sections.
  This values explicit which section level should break page.

.. _cli-rst2typstpdf:

``rst2typstpdf`` command
========================

Entrypoint to generate PDF bypassing Typst code.

.. important::

   You need to install this with "pdf" extra to run this command.

Usage
-----

.. code::

   rst2typstpdf [options] [<source> [<destination>]]

``source`` is path of reStructuredText file.

``destination`` is output path of Typst file. If ``destination`` is not specified, it outputs into STDOUT.

Options
-------

These are same from options for :ref:`cli-rst2typst` command.

Examples
========

Simple generate
---------------

.. code:: console

   $ rst2typst input.rst output.typ

Break pages at top-level sections
---------------------------------

.. code:: console

   $ rst2typst --page-break-level=1 input.rst output.typ

Use custom template
-------------------

.. code:: console

   $ cat ./template.txt
   #page("a5")
   {imports}
   {includes}
   {body}
   $ rst2typst --template=./template.txt input.rst output.typ

Generate PDF
------------

.. code:: console

   $ rst2typstpdf input.rst output.pdf
