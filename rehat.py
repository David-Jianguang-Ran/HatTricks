# This this a library for managing pixels in a sense hat

import numpy as np
import time  as t
from sense_hat import SenseHat

class Dot:
  def __init__(self,x=0,y=0):
    self.x = x
    self.y = y
    self.board = None
    
  @property
  def render(self):
    # Override this method to return a (int , int, int) rgb colour
    return (0,0,0)
  
  def set_state(self):
    # every loop this method will be called, do your per dot logic here and modify it's own state accordingly
    pass
    
  def mount(self, board):
    self.board = board
  
  def get_adjacent(self):
    self.board.get_adjacent_dots(self.x,self.y)
    pass
  
  
class Board(SenseHat):
  def __init__(self):
    super().__init__()
    self.dots = []
  
  def main(self, duration):
    start_time = t.time()
    while t.time() - start_time <= duration:
      # here is the main loop
      # first we call board level logic
      self.top_level_logic()
      
      # then we call the set_state logic in each components
      for each_dot in self.dots:
        each_dot.set_state()
        
      # then we call render to show board state for this loop
      self.render()
      
      # finally we sleep for a little so the loops don't go too fast
      t.sleep(0.05)
  
  def top_level_logic(self):
    # override this method to implement main logic
    pass
  
  def mount_dots(self,dots):
    for some_dot in dots:
      self.dots.append(some_dot)
      some_dot.mount(self)
  
  def get_adjacent_dots(self,x,y):
    target_x_y = [(x + 1 , y),(x - 1, y),
                  (x, y + 1),(x, y - 1)]
    output = []
    for some_dot in self.dots:
      x_y = (some_dot.x, some_dot.y)
      if x_y in target_x_y:
        output.append(some_dot)
    return output
  
  def get_dot(self,x,y):
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
    
  
    
    
    