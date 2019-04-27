
DEBUG = True

# SIM RULES SETTINGS
MOLD_SPAWN_THRESHOLD = 4
MOLD_GROWTH_PERIOD = 7

SPORE_SPAWN_THRESHOLD = 3
SPORE_WASTE_DELAY = 2

FOOD_MIN = 6

STEM_CROWD_THRESHOLD = 4

# VISUAL SETTINGS

COLORS = {
  # FWM component
  "food"  : (255,0,0),
  "waste" : (125,0,125),
  "mold"  : (0,0,225),
  # spore component
  "stem"  : (255,255,0),
  "hungry": (0,255,0),
  "fed"   : (0,125,125)
}

COLORS_BASIC = {
"K" : (0,0,0),
"R" : (255,0,0),
"Y" : (125,125,0),
"G" : (0,255,0),
"C" : (0,125,125),
"B" : (0,0,225),
"P" : (125,0,125)
}

k = COLORS_BASIC['K']


LOADING_SCREEN = [
  k, k, k, k, k, k, k, k,
  (0,125,125),(0,125,125),(0,125,125),(0,125,125),(0,125,125),(0,125,125),(0,125,125),(0,125,125),
  k, k, k, k, k, k, k, k,
  (0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),
  k, k, k, k, k, k, k, k,
  k, k, k, k, k, k, k, k,
  k, k, k, k, k, k, k, k,
  k, k, k, k, k, k, k, k,
]