=======
Roadmap
=======

My goal for this project
========================

I develop rst2typst for personal goals.

* Write e-books about my Sphinx extensions as "Tech-ZINE" by reStructuredText.
* Replace process to output PDF of Sphinx from ``latexpdf`` builder.

For purpose of this project, it is going to support all nodes of docutils.

Versioning
==========

This project uses semantic versioning.

v.0.1.0
-------

First official release for using to generate PDF.

This version provides basic features for generating PDF: transforms,
writer and translations of nodes.
But it does not support all nodes of docutils, it only has support of nodes
that I think are necessary for my first e-book.

v0.x
----

This versions provides updates that it have new features and bug fixes but it does not support full yet.

I will develop features and bug fixes when I need them.
It will be released every Friday night if it has new updates in this week.

* Up to minor version when updates include adding support of new nodes or breaking changes of behavior.
* Up to patch version when updates include bug fixes or internal changes of behavior (it does not change interfaces).

v1.0.0
------

This version provides full support of all nodes of docutils.

It will have these features:

* Support of all nodes defined in docutils (but only standard usage).
* Interface to extend custom Typst functions defined in this project.
* APIs to use from Sphinx.

v1.x.x
------

(TBD)

v2.0.0
------

This version will release if I have to change implemented interfaces of this project.
