#import "./admonition.typ": admonition-callout;
#import "./docinfo.typ": docinfo-callout;

#let admonition(
  class,
  title,
  content,
) = admonition-callout(class, title, content)

#let docinfo = docinfo-callout
