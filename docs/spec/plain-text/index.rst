==========
Plain text
==========

Details
=======

.. note:: Characters inside literal blocks are not escaped.

These characters are escaped anywhere.

- :literal:`#`: number sign [#]_

  .. [#] ``#`` starts scripting and function call expressions in Typst (e.g., ``#set``, ``#let``, ``#func()``).
- :literal:`$`: dollar sign [#]_

  .. [#] ``$`` is the math mode delimiter in Typst; a bare ``$`` opens or closes an inline math expression.
- :literal:`*`: asterisk [#]_

  .. [#] ``*`` marks strong (bold) text in Typst (``*bold*``).
- :literal:`<`: less-than sign [#]_

  .. [#] ``<`` opens a label definition in Typst (e.g., ``<my-label>``),
     so a bare ``<`` would start an unintended label.
- :literal:`>`: greater-than sign [#]_

  .. [#] ``>`` closes a label definition in Typst (e.g., ``<my-label>``),
     so a bare ``>`` would end an unintended label.
- :literal:`\\`: backslash [#]_

  .. [#] ``\`` is the escape character in Typst and also produces a forced line break when used alone.
- :literal:`_`: underscore [#]_

  .. [#] ``_`` marks emphasized (italic) text in Typst (``_italic_``).
- :literal:`\``: backtick [#]_

  .. [#] A backtick opens raw (code) text in Typst
     (e.g., :literal:`\`code\`` or :literal:`\`\`\`lang ... \`\`\``).
- :literal:`~`: tilde [#]_

  .. [#] ``~`` represents a non-breaking space in Typst.

These characters are escaped if they are at the start of line.

- :literal:`+`: plus sign [#]_

  .. [#] ``+`` is the numbered-list item marker in Typst when placed at the start of a line.
- :literal:`-`: hyphen-minus [#]_

  .. [#] ``-`` is the unordered-list item marker in Typst when placed at the start of a line.
- :literal:`=`: equals sign [#]_

  .. [#] ``=`` is the heading marker in Typst
     when placed at the start of a line (``=`` for level 1, ``==`` for level 2, etc.).

Examples
========

Standard escape characters
--------------------------

.. tab-set-code::

   .. literalinclude:: standard-escape-characters.rst.txt
      :language: rst

   .. literalinclude:: standard-escape-characters.typ.txt
      :language: typst

Head-only escape characters
---------------------------

.. tab-set-code::

   .. literalinclude:: head-only-escape-characters.rst.txt
      :language: rst

   .. literalinclude:: head-only-escape-characters.typ.txt
      :language: typst
