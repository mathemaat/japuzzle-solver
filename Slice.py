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
    self.entries = [Entry(self, i, hint) for i, hint in enumerate(self.hints)]

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
      self.entries[n].initialiseBoundaries(minStartPositions[n], maxEndPositions[n])

  def updateRepresentation(self):
    if self.orientation == 'h':
      self.representation = self.Puzzle.Grid.getRow(self.index)
    else:
      self.representation = self.Puzzle.Grid.getColumn(self.index)

  def updateGrid(self):
    if self.orientation == 'h':
      for i, cell in enumerate(self.representation):
        if cell != None:
          self.Puzzle.Grid.setCell(self.index, i, cell)
    else:
      for i, cell in enumerate(self.representation):
        if cell != None:
          self.Puzzle.Grid.setCell(i, self.index, cell)

  def solve(self):
    self.solveEntries()
    self.cascadeTranslations()
    self.updateGrid()

  def solveEntries(self):
    for Entry in self.entries:
      if not Entry.getIsSolved():
        Entry.solve()

  def cascadeTranslations(self):
    offset = 0
    for Entry in self.entries:
      offset = max(Entry.minStart - Entry.initialMinStart, offset)
      if not Entry.getIsSolved():
        Entry.minStart += offset - (Entry.minStart - Entry.initialMinStart)
    offset = 0
    for Entry in self.entries[::-1]:
      offset = max(Entry.initialMaxEnd - Entry.maxEnd, offset)
      if not Entry.getIsSolved():
        Entry.maxEnd -= offset - (Entry.initialMaxEnd - Entry.maxEnd)

  def setCell(self, index, value):
    self.setRange(index, index, value)

  def setRange(self, start, end, value):
    i = start
    while i <= end:
      self.representation[i] = value
      i += 1

