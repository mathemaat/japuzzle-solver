from Grid import Grid

class Puzzle(object):

  def __init__(self, rowEntries, columnEntries):
    self.width = len(columnEntries)
    self.height = len(rowEntries)

    self.Grid = Grid(self.width, self.height)

    self.rowEntries    = rowEntries
    self.columnEntries = columnEntries

    self.validate()

  def validate(self):
    self.validateRowEntries()
    self.validateColumnEntries()

  def validateRowEntries(self):
    for i in xrange(self.height):
      length = len(self.rowEntries[i])
      if length == 0:
        raise Exception('Row %d doesn\'t contain any values' % i)

      total = sum(self.rowEntries[i])
      if total > 0:
        span = total + length - 1
        if span > self.width:
          raise Exception('Span of row %d is %d (max is %d)' % (i, span, self.width))

  def validateColumnEntries(self):
    for i in xrange(self.width):
      length = len(self.columnEntries[i])
      if length == 0:
        raise Exception('Column %d doesn\'t contain any values' % i)

      total = sum(self.columnEntries[i])
      if total >= 0:
        span = total + length - 1
        if span > self.height:
          raise Exception('Span of column %d is %d (max is %d)' % (i, span, self.height))

  def getRowMatrix(self):
    rowMatrix = [None] * self.height
    for i in xrange(self.height):
      total = sum(self.rowEntries[i])
      if total == 0:
        rowMatrix[i] = [0]
      else:
        rowMatrix[i] = self.rowEntries[i]
    
    maxLength = self.getMaxRowLength(rowMatrix)
    for i in xrange(len(rowMatrix)):
      while len(rowMatrix[i]) < maxLength:
        rowMatrix[i].insert(0, None)

    return rowMatrix

  def getColumnMatrix(self):
    columnMatrix = [None] * self.width
    for i in xrange(self.width):
      total = sum(self.columnEntries[i])
      if total == 0:
        columnMatrix[i] = [0]
      else:
        columnMatrix[i] = self.columnEntries[i]
    
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

