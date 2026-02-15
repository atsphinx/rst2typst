#pad(
  left: 5%,
  block(
    stroke: (left: 4pt + red.darken(10%)),
    fill: red.lighten(90%),
    width: 90%,
    inset: (x: 1em, y: 0.8em),
    radius: 1pt,
    breakable: true,
    [
      ❌#h(0.5em)#text(
        weight: "extrabold",
        [Danger],
      )
      #v(0.4em)
      #text(
        size: 0.9em,
      )[Beware killer rabbits!]
    ]
  )
)

#pad(
  left: 5%,
  block(
    stroke: (left: 4pt + gray.darken(50%)),
    fill: gray.lighten(90%),
    width: 90%,
    inset: (x: 1em, y: 0.8em),
    radius: 1pt,
    breakable: true,
    [
      ℹ️#h(0.5em)#text(
        weight: "extrabold",
        [And, by the way...],
      )
      #v(0.4em)
      #text(
        size: 0.9em,
      )[You can make up your own admonition too.]
    ]
  )
)
