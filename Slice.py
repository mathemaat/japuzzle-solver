from Entry import Entry

class Slice(object):

  def __init__(self, Puzzle, orientation, index):
    self.Puzzle = Puzzle
    self.orientation = orientation
    self.index = index

    self.determineLength()
    self.determineHints()
    self.initialiseEntries()

    self.updateRepresentation()

  def determineLength(self):
    if self.orientation == 'h':
      self.length = self.Puzzle.width
    else:
      self.length = self.Puzzle.height

  def determineHints(self):
    if self.orientation == 'h':
      self.hints = self.Puzzle.rows[self.index]
    else:
      self.hints = self.Puzzle.columns[self.index]

  def initialiseEntries(self):
    self.entries = [Entry(self, hint) for hint in self.hints]

    minStartPositions = []
    maxEndPositions = []
    count = len(self.hints)
    for n in xrange(count):
      if n == 0:
        minStartPositions.append(0)
        maxEndPositions.insert(0, self.length - 1)
      else:
        minStartPositions.append(minStartPositions[n-1] + self.hints[n-1] + 1)
        maxEndPositions.insert(0, maxEndPositions[0] - self.hints[count-n] - 1)
    for n in xrange(count):
      self.entries[n].setBoundaries(minStartPositions[n], maxEndPositions[n])

  def updateRepresentation(self):
    if self.orientation == 'h':
      self.representation = self.Puzzle.Grid.getRow(self.index)
    else:
      self.representation = self.Puzzle.Grid.getColumn(self.index)

  def updateGrid(self):
    if self.orientation == 'h':
      for i, cell in enumerate(self.representation):
        self.Puzzle.Grid.setCell(self.index, i, cell)
    else:
      for i, cell in enumerate(self.representation):
        self.Puzzle.Grid.setCell(i, self.index, cell)

  def solve(self):
    for Entry in self.entries:
      Entry.solve()
    self.updateGrid()

  def fillRange(self, start, end):
    i = start
    while i <= end:
      self.representation[i] = 1
      i += 1

