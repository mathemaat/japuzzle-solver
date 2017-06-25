
class Entry(object):

  def __init__(self, Slice, index, value):
    self.Slice = Slice
    self.index = index
    self.value = value

    # its position is bounded by minStart and maxEnd
    self.initialMinStart = None
    self.initialMaxEnd   = None
    self.minStart        = None
    self.maxEnd          = None

    self.isSolved = False

  def __repr__(self):
    if self.minStart == None:
      return str(self.value)
    else:
      return '%d [%2d - %2d]' % (self.value, self.minStart, self.maxEnd)

  def initialiseBoundaries(self, minStart, maxEnd):
    self.initialMinStart = minStart
    self.initialMaxEnd   = maxEnd
    self.minStart        = minStart
    self.maxEnd          = maxEnd

  def getIsSolved(self):
    return self.isSolved

  def checkIfSolved(self):
    self.isSolved = self.maxEnd - self.minStart + 1 == self.value

  def solve(self):
    self.narrow()
    self.colorCells()

  def narrow(self):
    self.checkIfSolved()
    if not self.getIsSolved():
      self.narrowIfEdgeCase()
    self.checkIfSolved()
    if not self.getIsSolved():
      self.narrowIfNearbyZeroes()
    self.checkIfSolved()
    if not self.getIsSolved():
      self.extendNearbyOnes()

  def narrowIfEdgeCase(self):
    if self.canIgnorePrevious():
      if self.Slice.representation[self.minStart] == 1:
        self.maxEnd = self.minStart + self.value - 1
        return
      elif self.Slice.representation[self.minStart + self.value] == 1:
        self.minStart += 1
    if self.canIgnoreNext():
      if self.Slice.representation[self.maxEnd] == 1:
        self.minStart = self.maxEnd - self.value + 1
        return
      elif self.Slice.representation[self.maxEnd - self.value] == 1:
        self.maxEnd -= 1

  def narrowIfNearbyZeroes(self):
    while True:
      representationAtStart = self.Slice.representation[self.minStart:self.minStart+self.value]
      if 0 not in representationAtStart:
        break
      lastIndex = self.lastIndex(representationAtStart, 0)
      self.minStart += lastIndex + 1

    while True:
      representationAtEnd = self.Slice.representation[self.maxEnd-self.value+1:self.maxEnd+1]
      if 0 not in representationAtEnd:
        break
      firstIndex = self.firstIndex(representationAtEnd, 0)
      self.maxEnd -= self.value - firstIndex

  def extendNearbyOnes(self):
    if self.canIgnorePrevious():
      representationAtStart = self.Slice.representation[self.minStart:self.minStart+self.value]
      if 1 in representationAtStart:
        firstIndex = self.firstIndex(representationAtStart, 1)
        self.maxEnd = min(self.minStart + firstIndex + self.value - 1, self.maxEnd)
    if self.canIgnoreNext():
      representationAtEnd = self.Slice.representation[self.maxEnd-self.value+1:self.maxEnd+1]
      if 1 in representationAtEnd:
        lastIndex = self.firstIndex(representationAtEnd[::-1], 1)
        self.minStart = max(self.maxEnd - lastIndex - self.value + 1, self.minStart)

  def canIgnorePrevious(self):
    if self.index == 0:
      return True
    previousEntry = self.Slice.entries[self.index - 1]
    return previousEntry.getIsSolved() and previousEntry.maxEnd < self.minStart

  def canIgnoreNext(self):
    if self.index == len(self.Slice.entries) - 1:
      return True
    nextEntry = self.Slice.entries[self.index + 1]
    return nextEntry.getIsSolved() and nextEntry.minStart > self.maxEnd

  @staticmethod
  def firstIndex(l, value):
    return l.index(value)

  @staticmethod
  def lastIndex(l, value):
    return len(l) - 1 - l[::-1].index(value)

  def colorCells(self):
    width = self.maxEnd - self.minStart + 1
    if width < 2 * self.value:
      overlap = 2 * self.value - width
      start = self.minStart + self.value - overlap
      end   = start + overlap - 1
      self.Slice.setRange(start, end, 1)
    if self.getIsSolved():
      if self.minStart > 0:
        self.Slice.setCell(self.minStart - 1, 0)
      if self.maxEnd < self.Slice.length - 1:
        self.Slice.setCell(self.maxEnd + 1, 0)

