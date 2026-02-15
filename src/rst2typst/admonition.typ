/**
 * Admonition color and icon theme set.
 */
#let admonition-themes = (
  attention: (
    stroke: orange.darken(30%),
    background: yellow.lighten(95%),
    icon: "❗",
  ),
  caution: (
      stroke: orange.darken(20%),
      background: yellow.lighten(90%),
      icon: "🔶",
  ),
  danger: (
      stroke: red.darken(10%),
      background: red.lighten(90%),
      icon: "❌",
  ),
  error: (
      stroke: red.darken(10%),
      background: red.lighten(95%),
      icon: "🚫",
  ),
  hint: (
      stroke: green.darken(10%),
      background: green.lighten(95%),
      icon: "🔍",
  ),
  important: (
      stroke: purple.darken(10%),
      background: purple.lighten(95%),
      icon: "❕",
  ),
  note: (
      stroke: blue.darken(20%),
      background: blue.lighten(95%),
      icon: "ℹ️",
  ),
  tip: (
      stroke: green.darken(20%),
      background: green.lighten(95%),
      icon: "💡",
  ),
  warning: (
      stroke: orange.darken(10%),
      background: orange.lighten(90%),
      icon: "⚠️",
  ),
)

/**
 * Retrieve admonition block of reStructuredText directives.
 */
#let admonition-callout(
  class,
  title,
  content,
) = {
  let theme = admonition-themes.at(class, default: admonition-themes.note)
  pad(
    left: 5%,
    block(
      width: 90%,
      stroke: (left: 4pt + theme.stroke, rest: 0.75pt + gray),
      inset: 0pt,
      radius: 4pt,
      clip: true,
      [
        #block(
          width: 100%,
          inset: (x: 10pt, y: 6pt),
          fill: theme.background,
          grid(
            columns: (auto, 1fr),
            column-gutter: 6pt,
            align: (horizon, horizon),
            theme.icon,
            text(size: 0.9em, weight: "bold")[#title],
          )
        )
        #block(
          width: 100%,
          inset: (x: 14pt, y: 6pt),
          text(size: 0.85em)[#content]
        )
      ]
    )
  )
}
