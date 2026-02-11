#image(
  "./figure-sample.png",
  alt: "Sample image",
  width: 50%,
)

#figure([
  #image(
    "./figure-sample.png",
  )],
  caption: [Title],
)

#figure([
  #link("https://example.com")[
    #image(
      "./figure-sample.png",
    )]],
  caption: [Next Title],
)
