# This this a library for managing pixels in a sense hat
import numpy as np
import time  as t
import inspect
from sense_hat import SenseHat # dont worry about this. there is simply no sense hat lib for my desktop env


# TODO figure out garbage collection rules and whether unmounted dots will leak memory
class Dot:
  """
  This class is basically react.Component
  Instance this and mount them to the board (react-dom) with board.mount_dots
  """
  def __init__(self, x=None, y=None):
    # the real x y is kep here, don't set this directly use set_x_y
    self._x = x
    self._y = y
    
    self.board = None
    
  @property
  def x(self):
    return self._x
  
  @property
  def y(self):
    return self._y
  
  @property
  def pos(self):
    position = (self._x, self._y)
    return position
  
  def set_x_y(self,x,y):
    # checking if render is in the call stack, if so feak out
    if "render" in [frame[3] for frame in inspect.stack()]:
      raise LifeCycleError
    
    valid = list(range(0,8))
    if (not x in valid) or (not y in valid):
      raise ValueError
    
    try:
      if self.board.get_dot(x,y):
        raise SpaceOccupied
    except AttributeError:
      # if there is no board then we allow x y to be set to what ever
      pass
    
    self._x = x
    self._y = y
    
  def dot_will_render(self):
    # TODO I think there is a potential race condition here with mulitple dot instances that also depend on other dots
    # every loop this method will be called, all dot location changes must happen here
    pass
  
  def mount(self, board):
    self.board = board
    # if the dot already pos then they must be validated
    if self._x and self._y:
      self.set_x_y(self._x,self._y)
      
  def unmount(self):
    # util function for removing this dot from board
    self.board.dots.remove(self)
  
  def get_adjacent_dots(self):
    try:
      return self.board.get_adjacent(self.x, self.y)
    except AttributeError:
      raise BoardDoesNotExist
    
  def get_adjacent_space(self):
    x = self.x
    y = self.y
    
    try:
      adj_dots = self.board.get_adjacent(x,y)
    except AttributeError:
      raise BoardDoesNotExist
    
    # make a list of valid position around me
    valid_space = find_valid_adjacent_space(x,y)
    
    for dot in adj_dots:
      valid_space.remove(dot.pos)
    
    return valid_space
  
  @property
  def render(self):
    # Override this method to return a (int , int, int) rgb colour
    # dot level logic that involves changing states here
    # please do not change x y or call set_x_y in here
    return (0,0,0)
  
  
class Board(SenseHat):
  """
  This is essentially react-dom.
  This object holds dots (components), turns main event loops and renders new led visuals
  """
  def __init__(self):
    super().__init__()
    self.dots = []
  
  def main(self, duration):
    """ Call this function with a set number of seconds to run the main loop for"""
    start_time = t.time()
    while t.time() - start_time <= duration:
      # here is the main loop
      # first we call board level logic
      self.board_will_render()
      
      # then we call the dot level logic in each component
      for each_dot in self.dots:
        each_dot.dot_will_render()
        
      # then we call render to show board state for this loop
      self.render()
      
      # finally we sleep for a little so the loops don't go too fast
      t.sleep(0.05)
  
  def board_will_render(self):
    # override this method to implement main logic
    pass
  
  def mount_dots(self,dots):
    for some_dot in dots:
      self.dots.append(some_dot)
      some_dot.mount(self)
  
  def get_adjacent(self, x, y):
    """ now this function gets all 3x3 area neighbours"""
    target_x_y = find_valid_adjacent_space(x,y)

    return [dot for dot in self.dots if dot.pos in target_x_y]
  
  def get_dot(self,x,y):
    """ Returns None or dot object instance"""
    output = None
    for some_dot in self.dots:
      if some_dot.pos == (x,y):
        output = some_dot
    return output
    
  def render(self):
    output = np.zeros((8,8,3),dtype=np.int64)
    for dot_obj in self.content:
      output[dot_obj.x,dot_obj.y,:] = dot_obj.render
    self.set_pixels(output)
    
##
# Errors and Exceptions

class SpaceOccupied(Exception):
  """Attempting to set_x_y for a occupied space"""
  pass


class BoardDoesNotExist(Exception):
  """Attempting to access board when Dot is unmounted"""
  pass

class LifeCycleError(Exception):
  """Attempting to call set_x_y inside render. Please only change location of dots inside dot_will_render"""
  pass

##
# Util functions
def find_valid_adjacent_space(x,y):
  """
  make a list of valid position around a pos
  :param x:
  :param y:
  :return: [(x,y), ...] list of x y pos tuple
  """
  valid_space = []
  for x_int in range(x - 1, x + 2):
    if not x_int in list(range(0, 8)):
      continue
    else:
      for y_int in range(y - 1, y + 2):
        if not y_int in list(range(0, 8)):
          continue
        else:
          valid_space.append((x_int, y_int))
  return valid_space

