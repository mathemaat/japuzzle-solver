from Grid import Grid

class Puzzle(object):

  def __init__(self, width, height):
    self.width = width
    self.height = height

    self.Grid = Grid(width, height)

    self.rowMatrix    = [None] * self.height
    self.columnMatrix = [None] * self.width

  def setRowMatrix(self, values):
    if len(values) != self.height:
      raise Exception('Incorrect number of rows')

    for i in xrange(self.height):
      length = len(values[i])
      if length == 0:
        raise Exception('Row %d doesn\'t contain any values' % i)

      total = sum(values[i])
      if total == 0:
        self.rowMatrix[i] = [0]
      elif total + length - 1 > self.width:
        raise Exception('Values of row %d sum up to %d (max is %d)' % (i, total, self.width))
      else:
        self.rowMatrix[i] = values[i]
    
    maxLength = self.getMaxRowLength(self.rowMatrix)
    for i in xrange(len(self.rowMatrix)):
      while len(self.rowMatrix[i]) < maxLength:
        self.rowMatrix[i].insert(0, None)

  def setColumnMatrix(self, values):
    if len(values) != self.width:
      raise Exception('Incorrect number of columns')

    for i in xrange(self.width):
      length = len(values[i])
      if length == 0:
        raise Exception('Column %d doesn\'t contain any values' % i)

      total = sum(values[i])
      if total == 0:
        self.columnMatrix[i] = [0]
      elif total + length - 1 > self.height:
        raise Exception('Values of column %d sum up to %d (max is %d)' % (i, total, self.height))
      else:
        self.columnMatrix[i] = values[i]
    
    maxLength = self.getMaxRowLength(self.columnMatrix)
    for i in xrange(len(self.columnMatrix)):
      while len(self.columnMatrix[i]) < maxLength:
        self.columnMatrix[i].insert(0, None)

  @staticmethod
  def getMaxRowLength(matrix):
    maxLength = 0
    for row in matrix:
      length = len(row)
      if length > maxLength:
        maxLength = length
    return maxLength

  def view(self, cellWidth, cellHeight):
    rowMatrix    = self.rowMatrix
    columnMatrix = Grid.transpose(self.columnMatrix)

    lineFormat   = '%s|%s|'
    borderFormat = '%s+%s+'

    offset = cellWidth * len(rowMatrix[0])
    for row in columnMatrix:
      line = ''
      for entry in row:
        if entry == None:
          line += ' ' * cellWidth
        else:
          line += (' ' * cellWidth + str(entry))[-cellWidth:]
      line = lineFormat % (' ' * offset, line)
      print line

    border = borderFormat % ('-' * offset, '-' * cellWidth * self.width)
    print border

    for i, row in enumerate(rowMatrix):
      line1 = ''
      for entry in row:
        if entry == None:
          line1 += ' ' * cellWidth
        else:
          line1 += (' ' * cellWidth + str(entry))[-cellWidth:]
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

