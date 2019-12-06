# turnbased-demo-py

This project is to allow people to rapidly prototype turnbased games into a playable state for testing and development.

There are only 5 primary functions that must be implemented, and then the framework takes care
of all the correct server behavior:
 * init
 * verify
 * update
 * view
 * score
 
 Additionally, implementing the 'text_play' functions, allows the framework to easily
 create a standardized straightforward client interface for playing the game.
 
 To see how this works, please refer to the implemented game examples:
  * [nim.py](games/nim.py) - A very simple game where 2 players take turns removing one or two stones.  The player to take the last stone loses.
  * [chinese_checkers.py](games/chinese_checkers.py) - A movement based game where player can jump pieces to try to get all their pieces to the other side.
  
If you want to license use, please contact me.
