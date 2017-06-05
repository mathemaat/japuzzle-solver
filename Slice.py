from Entry import Entry

class Slice(object):

  def __init__(self, Puzzle, orientation, hints):
    self.Puzzle = Puzzle
    self.orientation = orientation
    self.hints = hints

    self.determineLength()
    self.initialiseEntries()

  def determineLength(self):
    if self.orientation == 'h':
      self.length = self.Puzzle.width
    else:
      self.length = self.Puzzle.height

  def initialiseEntries(self):
    self.entries = [Entry(hint) for hint in self.hints]

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

