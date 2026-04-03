#set page(width: 1000pt, height: 1000pt, margin: 0pt, fill: rgb("#F8F9FA"))
#set text(font: "Arial", size: 22pt, fill: rgb("#212529"))

#let labels = (
  "R", "b2", "2", "b3", "3", "4",
  "b5", "5", "#5", "6", "b7", "7",
)

#let active = ({{ACTIVE_INDICES}})
#let edges = ({{EDGE_PAIRS}})
#let bass = {{BASS_INDEX}}
#let title = "{{TITLE}}"
#let subtitle = "{{SUBTITLE}}"

#let p0 = (500pt, 170pt)
#let p1 = (665pt, 214pt)
#let p2 = (786pt, 335pt)
#let p3 = (830pt, 500pt)
#let p4 = (786pt, 665pt)
#let p5 = (665pt, 786pt)
#let p6 = (500pt, 830pt)
#let p7 = (335pt, 786pt)
#let p8 = (214pt, 665pt)
#let p9 = (170pt, 500pt)
#let p10 = (214pt, 335pt)
#let p11 = (335pt, 214pt)
#let points = (p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11)

#let lp0 = (500pt, 92pt)
#let lp1 = (724pt, 152pt)
#let lp2 = (848pt, 276pt)
#let lp3 = (910pt, 500pt)
#let lp4 = (848pt, 724pt)
#let lp5 = (724pt, 848pt)
#let lp6 = (500pt, 910pt)
#let lp7 = (276pt, 848pt)
#let lp8 = (152pt, 724pt)
#let lp9 = (92pt, 500pt)
#let lp10 = (152pt, 276pt)
#let lp11 = (276pt, 152pt)
#let label_points = (lp0, lp1, lp2, lp3, lp4, lp5, lp6, lp7, lp8, lp9, lp10, lp11)

#place(top + left, dx: 170pt, dy: 170pt)[
  #circle(radius: 330pt, stroke: 3pt + rgb("#ADB5BD"))
]

#for edge in edges {
  let from = points.at(edge.at(0))
  let to = points.at(edge.at(1))
  place(top + left, dx: 0pt, dy: 0pt)[
    #line(start: from, end: to, stroke: 5pt + rgb("#0B7285"))
  ]
}

#for i in range(12) {
  let point = points.at(i)
  let label_point = label_points.at(i)
  let on = active.contains(i)
  let fill = if i == 0 {
    rgb("#E8590C")
  } else if i == bass {
    rgb("#5F3DC4")
  } else if on {
    rgb("#0B7285")
  } else {
    rgb("#F1F3F5")
  }
  let stroke = if i == 0 or i == bass or on {
    2.2pt + rgb("#495057")
  } else {
    1.5pt + rgb("#868E96")
  }
  place(top + left, dx: point.at(0) - 30pt, dy: point.at(1) - 30pt)[
    #circle(radius: 34pt, fill: fill, stroke: stroke)
  ]
  place(top + left, dx: label_point.at(0) - 110pt, dy: label_point.at(1) - 16pt)[
    #block(width: 220pt, align(center)[#text(size: 23pt, fill: rgb("#212529"))[#labels.at(i)]])
  ]
}

#place(top + left, dx: 230pt, dy: 420pt)[
  #block(width: 540pt, align(center)[
    #text(size: 27pt, weight: "bold", fill: rgb("#343A40"))[#title]
    \
    #text(size: 21pt, fill: rgb("#495057"))[#subtitle]
  ])
]
