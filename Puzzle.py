from Grid import Grid
from Slice import Slice

class Puzzle(object):

  def __init__(self, rows, columns):
    self.width = len(columns)
    self.height = len(rows)

    self.Grid = Grid(self.width, self.height)

    self.rows    = rows
    self.columns = columns

    self.validate()

    self.slices = []
    self.slices += [Slice(self, 'h', i) for i, row in enumerate(rows)]
    self.slices += [Slice(self, 'v', i) for i, column in enumerate(columns)]

    self.iteration = 0

  def validate(self):
    self.validateRows()
    self.validateColumns()

  def validateRows(self):
    for i in xrange(self.height):
      length = len(self.rows[i])
      if length == 0:
        raise Exception('Row %d doesn\'t contain any values' % i)

      total = sum(self.rows[i])
      if total > 0:
        span = total + length - 1
        if span > self.width:
          raise Exception('Span of row %d is %d (max is %d)' % (i, span, self.width))

  def validateColumns(self):
    for i in xrange(self.width):
      length = len(self.columns[i])
      if length == 0:
        raise Exception('Column %d doesn\'t contain any values' % i)

      total = sum(self.columns[i])
      if total >= 0:
        span = total + length - 1
        if span > self.height:
          raise Exception('Span of column %d is %d (max is %d)' % (i, span, self.height))

  def getRowMatrix(self):
    rowMatrix = [None] * self.height
    for i in xrange(self.height):
      total = sum(self.rows[i])
      if total == 0:
        rowMatrix[i] = [0]
      else:
        rowMatrix[i] = list(self.rows[i])

    maxLength = self.getMaxRowLength(rowMatrix)
    for i in xrange(len(rowMatrix)):
      while len(rowMatrix[i]) < maxLength:
        rowMatrix[i].insert(0, None)

    return rowMatrix

  def getColumnMatrix(self):
    columnMatrix = [None] * self.width
    for i in xrange(self.width):
      total = sum(self.columns[i])
      if total == 0:
        columnMatrix[i] = [0]
      else:
        columnMatrix[i] = list(self.columns[i])

    maxLength = self.getMaxRowLength(columnMatrix)
    for i in xrange(len(columnMatrix)):
      while len(columnMatrix[i]) < maxLength:
        columnMatrix[i].insert(0, None)

    return columnMatrix

  @staticmethod
  def getMaxRowLength(matrix):
    maxLength = 0
    for row in matrix:
      length = len(row)
      if length > maxLength:
        maxLength = length
    return maxLength

  def view(self, cellWidth, cellHeight):
    rowMatrix    = self.getRowMatrix()
    columnMatrix = Grid.transpose(self.getColumnMatrix())

    lineFormat   = '%s|%s|'
    borderFormat = '%s+%s+'

    offset = cellWidth * len(rowMatrix[0])
    for row in columnMatrix:
      line = ''
      for hint in row:
        if hint == None:
          line += ' ' * cellWidth
        else:
          line += (' ' * cellWidth + str(hint))[-cellWidth:]
      line = lineFormat % (' ' * offset, line)
      print line

    border = borderFormat % ('-' * offset, '-' * cellWidth * self.width)
    print border

    for i, row in enumerate(rowMatrix):
      line1 = ''
      for hint in row:
        if hint == None:
          line1 += ' ' * cellWidth
        else:
          line1 += (' ' * cellWidth + str(hint))[-cellWidth:]
      line2 = ' ' * offset

      fill = ''
      for j in range(self.width):
        value = self.Grid.getCell(i, j)
        if value == 1:
          fill += 'X' * cellWidth
        elif value == 0:
          fill += '.' * cellWidth
        else:
          fill += ' ' * cellWidth
      line1 = lineFormat % (line1, fill)
      line2 = lineFormat % (line2, fill)
      print line1
      if cellHeight >= 2:
        extraLines = cellHeight - 1
        while extraLines >= 1:
          print line2
          extraLines -= 1
    print border

  def solve(self):
    self.iteration = 1
    while self.iteration < 100:
      for Slice in self.slices:
        Slice.solve()
      # don't update representation of slices until all slices are evaluated
      for Slice in self.slices:
        Slice.updateRepresentation()
      self.iteration += 1

