#! /usr/bin/python3
"""
# Design Doc:

- Type of Dots
 - Food
    - can be "eaten" by spore
 - Waste
    - can be "moved" by spore if adj
    - if by waste, then it turns into mold
 - Mold
    - turns adj waste into mold
    - life span ? expires into food
    
 - Spore stem
    - spawns spore if it has < 1 adj stem
    - infinite life span
    - turns into spore if next to waste
 - Spore hungry
    - movement : random wander
    - can push waste away from self
 - spore fed
    - turns into stem when in contact with stem
    - has a waste counter, if counter a
    
# Feelings log?
- a little tired orz
 
"""
import spore_config as C
import rehat
import random
import time

from spore_config import DEBUG


# here are some custom dot classes
class SporeDish(rehat.Board):
  
  def _add_food(self):
    # just try to find a spot for the food untill one is found
    try:
      new_food = FoodWasteMold(x=random.randint(0, 7), y=random.randint(0, 7), type="food")
      rehat.debug_print("food spawned in pos({},{})".format(new_food.x,new_food.y))
      new_food.mount(self)

    except rehat.SpaceOccupied:
      self._add_food()
  
  def ensure_food(self,food_count):
    food_item_count = [":p" for dot in self.dots if isinstance(dot,FoodWasteMold)]
    while len(food_item_count) < food_count:
      self._add_food()
      food_item_count.append("^_^")
    
  def set_starting_board(self):
    # make starting spore
    queen_bee = Spore(x=random.randint(0,7),y=random.randint(0,7),type="stem")
    queen_bee.mount(self) # orz

    # food supply is ensured in board will render
    
  def board_will_render(self):
    self.ensure_food(C.FOOD_MIN)


class FoodWasteMold(rehat.Dot):
  def __init__(self,x=None ,y=None ,type="food"):
    super().__init__(x=x,y=y)
    
    self.type = type
    self.mold_growth = None
    
  def __str__(self):
    return str("FWM type:{} pos:{}".format(self.type,self.pos))
    
  def dot_will_render(self):
    # helper functions below
    def _make_one_mold(adj_waste):
      new_mold = random.choice(adj_waste)
      new_mold.become_mold()
    
    # waste surrounded by CONSTANT amount of waste become mold
    adj_waste = [dot for dot in self.get_adjacent_dots() if dot.type == "waste"]
    if self.type == "waste" and len(adj_waste) >= C.MOLD_SPAWN_THRESHOLD:
      _make_one_mold(adj_waste)
    elif self.type == "mold":
      _make_one_mold(adj_waste)
    
  def become_mold(self):
    self.type = "mold"
    self.mold_growth = C.MOLD_GROWTH_PERIOD
  
  def render(self):
    # if there is a mold growth counter decrement it and change to food if we are at 0
    if self.mold_growth:
      if self.mold_growth != 0:
        self.mold_growth -= 1
      else:
        self.type = "food"
        self.mold_growth = None
        
    return C.COLORS[self.type]
  

class Spore(rehat.Dot):
  def __init__(self,x=None ,y=None ,type="hungry"):
    super().__init__(x=x,y=y)
    
    self.type = type
    self.generate_waste = None
    
  def __str__(self):
    return str("Spore type:{} pos:{}".format(self.type,self.pos))
    
  def dot_will_render(self):
    valid_space = self.get_adjacent_space()
    adj_dots = self.get_adjacent_dots()

    # fed spores generate waste with counter
    if self.generate_waste:
      if self.generate_waste > 0:
        self.generate_waste -= 1
      elif len(valid_space) > 0 and self.generate_waste == 0:
        new_pos = random.choice(valid_space)
        valid_space.remove(new_pos)
    
        # make our new spore component and mount it to board
        new_spore = FoodWasteMold(x=new_pos[0], y=new_pos[1], type="waste")
        new_spore.mount(self.board)
    
        self.generate_waste = None
    
    # TODO Add a dot pushing behaviour here

    if self.type == "hungry":
      # move waste before moving
      if len(valid_space) > 0:
        adj_waste = [dot for dot in adj_dots if dot.type == "waste"]
        new_pos = random.choice(valid_space)
        if len(adj_waste) > 0:
          chosen_waste = random.choice(adj_waste)
          chosen_waste.set_x_y(new_pos)
          valid_space.remove(new_pos)
      
      # eat food
      adj_food = [dot for dot in adj_dots if dot.type == "food"]
      if len(adj_food) > 0:
        eatee = random.choice(adj_food)
        adj_dots.remove(eatee)
        eatee.unmount()
        
        self.type = "fed"
        self.generate_waste = C.SPORE_WASTE_DELAY
    
    if self.type == "stem":
      # stems spawn new spores
      adj_stem = [dot for dot in adj_dots if dot.type == "stem"]
      
      if len(adj_stem) <= C.SPORE_SPAWN_THRESHOLD and len(valid_space) > 0:
        new_pos = random.choice(valid_space)
        valid_space.remove(new_pos)
        
        # make our new spore component and mount it to board
        new_spore = Spore(x=new_pos[0], y=new_pos[1], type="hungry")
        new_spore.mount(self.board)
    else:
      if len(valid_space) > 0:
        # if this is a hungry or fed spore it just wanders
        new_pos = random.choice(valid_space)
        self.set_x_y(new_pos[0],new_pos[1])
      # if a hungry spore is totally closed in it will die
      elif self.type == "hungry":
        self.unmount()
        
  def render(self):
    adj_dots = self.get_adjacent_dots()
    
    if self.type == "stem":
      # begins to leave if next to waste
      adj_waste = [dot for dot in adj_dots if dot.type == "waste"]
      if len(adj_waste) > 0:
        self.type = "hungry"
      
      # becomes hungry if next to big crowd
      adj_stem = [dot for dot in adj_dots if dot.type == "waste"]
      if len(adj_stem) > C.STEM_CROWD_THRESHOLD:
        self.type = "hungry"
        
    elif self.type == "fed":
      adj_stem = [dot for dot in adj_dots if dot.type == "stem"]
      if len(adj_stem) > 0:
        self.type = "stem"
        
    return C.COLORS[self.type]


# main logic

if __name__ == "__main__":
  dish = SporeDish()
  dish.set_pixels(C.LOADING_SCREEN)
  time.sleep(1)

  dish.set_starting_board()
  
  dish.main(30, 0.5)
  
  time.sleep(30)
  dish.set_pixels([(0,0,0) for i in range(0,64)])
