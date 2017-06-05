
class Entry(object):

  def __init__(self, Slice, value):
    self.Slice = Slice
    self.value = value

    # its position is bounded by minStart and maxEnd
    self.minStart = None
    self.maxEnd   = None

  def setBoundaries(self, minStart, maxEnd):
    self.minStart = minStart
    self.maxEnd   = maxEnd

  def __repr__(self):
    if self.minStart == None:
      return str(self.value)
    else:
      return '%d [%2d - %2d]' % (self.value, self.minStart, self.maxEnd)

