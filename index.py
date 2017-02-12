from Puzzle import Puzzle

width = 15
height = 20

rowMatrix = [
  [6],
  [3, 4],
  [2, 2],
  [2, 2],
  [1, 2],
  [2, 3, 3, 2],
  [1, 5, 1, 2],
  [1, 8, 2],
  [1, 9, 2],
  [1, 7, 2],
  [1, 3, 2, 1],
  [3, 2, 2],
  [2, 2],
  [3, 3],
  [5, 4],
  [1, 3, 2],
  [4],
  [2, 1, 3, 2],
  [9, 4],
  [4, 2, 5]
]

columnMatrix = [
  [6, 2, 1, 1],
  [3, 4, 3],
  [2, 6, 2],
  [2, 1, 5, 3, 3],
  [1, 6, 2, 1],
  [2, 5, 1, 2],
  [1, 4, 1, 1, 3],
  [1, 7, 1, 3],
  [2, 6, 1, 1],
  [2, 1, 2, 2, 3],
  [2, 3, 1, 2, 1],
  [2, 1, 2, 2, 2],
  [3, 2, 2, 2],
  [9, 1, 2],
  [5, 1]
]

puzzle = Puzzle(width, height)
puzzle.setRowMatrix(rowMatrix)
puzzle.setColumnMatrix(columnMatrix)
puzzle.view()
