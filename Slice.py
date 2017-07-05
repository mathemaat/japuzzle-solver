from Entry import Entry

class Slice(object):

  def __init__(self, Puzzle, orientation, index):
    self.Puzzle = Puzzle
    self.orientation = orientation
    self.index = index

    self.determineLength()
    self.initialiseEntries()

    self.updateRepresentation()

  def determineLength(self):
    if self.orientation == 'h':
      self.length = self.Puzzle.width
    else:
      self.length = self.Puzzle.height

  def initialiseEntries(self):
    if self.orientation == 'h':
      entryValues = self.Puzzle.rows[self.index]
    else:
      entryValues = self.Puzzle.columns[self.index]

    self.entries = [Entry(self, i, value) for i, value in enumerate(entryValues)]
    self.numberOfEntries = len(self.entries)

    minStartPositions = []
    maxEndPositions = []
    for n in xrange(self.numberOfEntries):
      if n == 0:
        minStartPositions.append(0)
        maxEndPositions.insert(0, self.length - 1)
      else:
        minStartPositions.append(minStartPositions[n-1] + entryValues[n-1] + 1)
        maxEndPositions.insert(0, maxEndPositions[0] - entryValues[self.numberOfEntries-n] - 1)
    for n in xrange(self.numberOfEntries):
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
    self.locateIslands()
    self.locateGaps()
    self.updateGrid()

  def solveEntries(self):
    for Entry in self.entries:
      Entry.solve()

  def cascadeTranslations(self):
    offset = 0
    for Entry in self.entries:
      offset = max(Entry.minStart - Entry.initialMinStart, offset)
      if not Entry.getIsSolved():
        Entry.minStart = Entry.initialMinStart + offset
    offset = 0
    for Entry in self.entries[::-1]:
      offset = max(Entry.initialMaxEnd - Entry.maxEnd, offset)
      if not Entry.getIsSolved():
        Entry.maxEnd = Entry.initialMaxEnd - offset

  def locateIslands(self):
    i = -1
    while i < self.length - 1 and self.representation[i+1] == 0:
      i += 1
    if i < self.length - 1:
      for Entry in self.entries:
        if Entry.getIsSolved():
          i = Entry.maxEnd + 1
        else:
          representation = self.representation[i+1:]
          if 1 in representation:
            firstIndex = Entry.firstIndex(representation, 1)
            Entry.maxEnd = min(Entry.maxEnd, i + firstIndex + Entry.value)
            i += firstIndex + Entry.value
            while i < self.length - 1 and self.representation[i+1] == 1:
              i += 1
          else:
            i = self.length - 1
        if i >= self.length - 1:
          break
    i = self.length
    while i > 0 and self.representation[i-1] == 0:
      i -= 1
    if i > 0:
      for Entry in self.entries[::-1]:
        if Entry.getIsSolved():
          i = Entry.minStart - 1
        else:
          representation = self.representation[:i]
          if 1 in representation:
            firstIndex = Entry.firstIndex(representation[::-1], 1)
            Entry.minStart = max(Entry.minStart, i - firstIndex - Entry.value)
            i -= firstIndex + Entry.value
            while i > 0 and self.representation[i-1] == 1:
              i -= 1
          else:
            i = 0
        if i <= 0:
          break

  def locateGaps(self):
    previousEnd = -1
    for Entry in self.entries:
      self.setRange(previousEnd + 1, Entry.minStart - 1, 0)
      previousEnd = Entry.maxEnd
    if previousEnd < self.length - 1:
      self.setRange(previousEnd + 1, self.length - 1, 0)

  def setCell(self, index, value):
    self.setRange(index, index, value)

  def setRange(self, start, end, value):
    i = start
    while i <= end:
      self.representation[i] = value
      i += 1

