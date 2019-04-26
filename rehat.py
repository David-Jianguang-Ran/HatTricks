# This this a library for managing pixels in a sense hat
import numpy as np
import time  as t
from sense_hat import SenseHat # dont worry about his. there is simply no sense hat lib for ubuntu

# TODO figure out garbage collection rules and whether unmounted dots will leak memory
class Dot:
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
  
  def set_x_y(self,x,y):
    # please don't call this in render
    if self.board.get_dot(x,y):
      raise SpaceOccupied
    else:
      self._x = x
      self._y = y
    
  def dot_will_render(self):
    # every loop this method will be called, do your per dot logic here and modify it's own state accordingly
    pass
  
  def mount(self, board):
    self.board = board
    # if the dot already pos then they must be validated
    if self._x and self._y:
      self.set_x_y(self._x,self._y)
      
  def unmount(self):
    # util function for removing this dot from board
    self.board.dots.remove(self)
  
  def get_adjacent(self):
    return self.board.get_adjacent_dots(self.x,self.y)
  
  @property
  def render(self):
    # Override this method to return a (int , int, int) rgb colour
    # please do not change x y or call set_x_y in here
    return (0,0,0)
  
  
class Board(SenseHat):
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
  
  def get_adjacent_dots(self,x,y):
    """ This one only gets top bottom left and right, not diag, returns a list of dots"""
    target_x_y = [(x + 1 , y),(x - 1, y),
                  (x, y + 1),(x, y - 1)]
    output = []
    for some_dot in self.dots:
      x_y = (some_dot.x, some_dot.y)
      if x_y in target_x_y:
        output.append(some_dot)
    return output
  
  def get_dot(self,x,y):
    """ Returns None or dot object instance"""
    output = None
    for some_dot in self.dots:
      x_y = (some_dot.x, some_dot.y)
      if x_y == (x,y):
        output = some_dot
    return output
    
  def render(self):
    output = np.zeros((8,8,3),dtype=np.int64)
    for dot_obj in self.content:
      output[dot_obj.x,dot_obj.y,:] = dot_obj.render
    self.set_pixels(output)
    
    
class SpaceOccupied(Exception):
  """Attempting to set_x_y for a occupied space"""
  pass