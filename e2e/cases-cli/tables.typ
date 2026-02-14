#table(
  columns: (24fr, 12fr, 10fr, 10fr),
  table.header(
    [Header row, column 1
    (header rows optional)],
    [Header 2],
    [Header 3],
    [Header 4],
  ),
  [body row 1, column 1],
  [column 2],
  [column 3],
  [column 4],
  [body row 2],
  table.cell(colspan: 3,)[Cells may span columns.],
  [body row 3],
  table.cell(rowspan: 2,)[Cells may
  span rows.],
  table.cell(rowspan: 2,colspan: 2,)[  - Table cells
  - contain
  - body elements.
],
  [body row 4],
)

#table(
  columns: (5fr, 5fr, 7fr),
  table.header(
    [A],
    [B],
    [A and B],
  ),
  [False],
  [False],
  [False],
  [True],
  [False],
  [False],
  [False],
  [True],
  [False],
  [True],
  [True],
  [True],
)

#figure([
  #table(
    columns: (15fr, 10fr, 30fr),
    table.header(
      [Treat],
      [Quantity],
      [Description],
    ),
    [Albatross],
    [2.99],
    [On a stick!],
    [Crunchy Frog],
    [1.49],
    [If we took the bones out,
    it wouldn't be crunchy, now would it?],
    [Gannet Ripple],
    [1.99],
    [On a stick!],
  )],
  caption: [Frozen Delights!],
)

#figure([
  #table(
    columns: (15fr, 10fr, 30fr),
    table.header(
      [Treat],
      [Quantity],
      [Description],
    ),
    [Albatross],
    [2.99],
    [On a stick!],
    [Crunchy Frog],
    [1.49],
    [If we took the bones out, it wouldn't be
    crunchy, now would it?],
    [Gannet Ripple],
    [1.99],
    [On a stick!],
  )],
  caption: [Frozen Delights!],
)
