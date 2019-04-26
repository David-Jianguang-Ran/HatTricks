# Hat Tricks

Fun things to do with the Sense Hat

so far we got:

####rehat.py
This is a react.js inspired pixel object model library. 
Tips:

- Inherent from Dot class for your pixel level object representation. (each object MUST be 1*1 pixel)
- Override Dot.dot_will_render to implement pixel level logic
- Override Dot.render to return a (int,int,int) rgb color
- Override Board.board_will_render to implement global logic
- call Board.mount_dots([array of Dot instances]) to add dots to board instance

Please see doc string in source for more.


DRan 04/19