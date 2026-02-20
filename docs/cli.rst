=================
Command line tool
=================

``rst2typst`` is a command-line entrypoint of rst2typst.

Usage
=====

This generates Typst code from reStructuredText.

.. important::

   This does not have feature to generate PDF.
   If you want to generate PDF, you should install Typst and use ``typst`` command.

Options
=======

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

.. note:: Require Typst executable.

.. code:: console

   $ rst2typst input.rst | typst compile - output.pdf
