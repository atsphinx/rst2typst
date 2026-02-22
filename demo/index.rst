=================
Demo of rst2typst
=================

:Date: 2026-02-23 Asia/Tokyo
:Author: Kazuya Takei

Preface
=======

I like docutils and Sphinx.
Because I don't only develop many Python libraries with Sphinx documentation,
but also I think that reStructuredText is good format to write structured documents.

docutils supports converting to LaTeX source code,
and Sphinx supports converting to PDF using LaTeX executable.
But it requires a large size items of LaTeX and need knowledge of LaTeX to customize.
This is important point for lifecycle of writing documentation,
because "Continuous Documentation" is affected from usage machine resources.

This document is demo and short description of rst2typst.
It is simple implementation to convert from reStructuredText to Typst source using docutils.
If you are reStructuredText users , you can experience about PDF generating from plain text rapidly.

About docutils and Typst
========================

docuitls and reStructuredText
-----------------------------

*docutils* is a Python library that provides support for
parsing and processing reStructuredText documents.
It is a powerful tool for converting reStructuredText documents
into various formats, including HTML, mandoc and LaTeX.

docutils is extensible by other users for adding new directives and roles,
supporting other text formats (e.g. Markdown) and generating at new output format.

*reStructuredText* is a lightweight markup language
that provides simple and easy-to-read syntax for creating documents.
This is default format for docutils,
and it is used in documentation of many projects: Linux Kernel, Python and more.

Typst
-----

*Typst* is a modern, expressive, and easy-to-learn programming language for creating beautiful documents.
It is designed to be a complete replacement for LaTeX, but with a simpler syntax and more powerful features. [#]_

.. [#] https://typst.app/docs/

Typst compiler is written in Rust. Then it is lightweight file size and can build documents rapidly.

For more information about Typst, please visit `the official website <https://typst.app/>`_.

Overview of rst2typst
=====================

What is rst2typst
-----------------

*rst2typst* is a Python library that provides support for translation between reStructuredText and Typst formats.
This uses docutils and provides command line interface likely docutils' CLI
(e.g. rst2html, rst2man and rst2latex).

This only has features to translate reStructuredText to Typst,
and it doesn't have feature to compile Typst to PDF.
You should install and run Typst to generate PDF.

This is developed by indivisual user.
It maybe support required syntax to write standard document
, but it is not support all syntax of reStructuredText.

Mechanism
---------

docutils runs for convert files with three steps:

1. Parse converts from reStructuredText document into a "DocTree" that is the AST presents document structure.
2. Transform metamorphosis DocTree by each transform rules.
3. Write generates from DocTree to Typst source text and save into file.

.. raw:: typst

   #figure(
     mermaid("
       graph LR
         A(Source)
         A --> B([Parser])
         B --> C([Transforms])
         C --> D([Writer])
         D --> E(Output)
     "),
     caption: [docutils's steps],
   )

rst2typst extends "Transform" and "Write" steps of docutils.

* Extend "Transform" step by adding new transform rules.
* Use "Write" step to generate Typst source text.

.. raw:: typst

   #figure(
     mermaid("
       graph LR
         A(Source)
         A --> B([Parser])
         B --> C([Transforms])
         C --> D([Writer])
         D --> E(Output)
         style C fill:#fa9
         style D fill:#f96
     "),
     caption: [docutils's steps (colored steps are extended by rst2typst)],
   )

Usage
=====

Installation
------------

rst2typst can be installed using pip:

.. code:: bash

   pip install rst2typst

If you want to build PDF in same workspace,
install Typst from PyPI or other package manager.

Write a document
----------------

You need to write a document in reStructuredText format.
rst2typst supports many syntax of reStructuredText.
Please write your document without worry.

There are examples of reStructuredText syntax supported by rst2typst and what they are converted.
To see all rules, check document [#]_ and test cases. [#]_

.. [#] https://rst2typst.attakei.dev/spec/
.. [#] https://github.com/attakei/rst2typst/tree/main/e2e

.. important::

   It has full-compatibility not all syntax, some attributes are ignored by rst2typst.

+---------------+--------------------------------+------------------------------+
| Syntax        | reStructuredText source        | Converted Typst source       |
+===============+================================+==============================+
| Empasis       | ``*Use for term*``             | ``_Use for term_``           |
+---------------+--------------------------------+------------------------------+
| Strong        | ``**Use for power sentence**`` | ``*Use for power sentence*`` |
+---------------+--------------------------------+------------------------------+
| Numbered list | .. code:: rst                  | .. code:: typst              |
|               |                                |                              |
|               |    #. Item A                   |    + Iem A                   |
|               |  #. Item B                     |  + Item B                    |
|               |  #. Item C                     |  + Item C                    |
+---------------+--------------------------------+------------------------------+
| Field list    | .. code:: rst                  | .. code:: typst              |
|               |                                |                              |
|               |    :User: Takei                |    / User: Takei             |
|               |  :Account: attakei             |  / Account: attakei          |
+---------------+--------------------------------+------------------------------+
