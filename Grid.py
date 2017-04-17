
class Grid(object):

  def __init__(self, width, height):
    self.width = width
    self.height = height

    self.grid = []
    for i in xrange(self.height):
      self.grid.append([None] * self.width)

  def getCell(self, i, j):
    return self.grid[i][j]

  def setCell(self, i, j, value):
    self.grid[i][j] = value

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

