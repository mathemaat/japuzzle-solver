
class Puzzle(object):

  def __init__(self, width, height):
    self.width = width
    self.height = height

    self.grid = []
    for i in xrange(self.height):
      self.grid.append([None] * self.width)

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

  def view(self):
    rowMatrix    = self.rowMatrix
    columnMatrix = self.transpose(self.columnMatrix)

    offset = 3 * len(rowMatrix[0])
    for row in columnMatrix:
      line = (' ' * offset) + '|'
      for entry in row:
        if entry == None:
          line += '   '
        else:
          line += ('   ' + str(entry))[-3:]
      line += '|'
      print line
    border = ('-' * offset) + '+' + ('-' * 3 * self.width) + '+'
    print border
    for row in rowMatrix:
      line = ''
      for entry in row:
        if entry == None:
          line += '   '
        else:
          line += ('   ' + str(entry))[-3:]
      line += '|'
#        if self.grid[i][j] == 1:
#          line += 'x'
#        elif self.grid[i][j] == 0:
#          line += '.'
#        else:
#          line += ' '
      line += '|'
      print line
    print border

  @staticmethod
  def transpose(matrix):
    newWidth = len(matrix)
    newHeight = len(matrix[0])
    transposed = [None] * newHeight
    for i in xrange(newHeight):
      transposed[i] = [None] * newWidth
      for j in xrange(newWidth):
        transposed[i][j] = matrix[j][i]
    return transposed

