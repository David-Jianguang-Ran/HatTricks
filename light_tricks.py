#! /usr/bin/python3 -i
# Hey this script is meant to be used in a interactive session.
# dran 04/19

import time
import random
import numpy as np
import sense_hat
import constants as C


class MyOwnHat(sense_hat.SenseHat):
  
  def clear_display(self):
    # this is obviously a little slow but it is less typing :p
    self.set_pixels(C.BLANK)
    
  def random_lights(self,duration):
    
    def _individual_light(hat):
      x = random.randint(0, 7)
      y = random.randint(0, 7)
      hat.set_pixel(x, y, random.choice(C.C_LIST))
      
    start_time = time.time()
    while time.time() - start_time <= duration:
      _individual_light(self)
      time.sleep(0.05)
      
    self.clear_display()

if __name__ == "__main__":
  hat = MyOwnHat()
  hat.random_lights(10)


  

