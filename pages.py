
index_src = """
<!doctype html>
<html>
  <head>
    <style>
      body{ font-family: sans-serif; }
      a:visited{ color: blue; }
    </style>
  </head>
  <body>
    <hr>
    <h1> Turnbased Game Server </h1>
    <a href="/new"> New Game </a> -
    <a href="/list"> List Games </a> -
    <a href="/docs"> Documentation </a>
    <hr>
  </body>
</html>
"""


doc_src = """
<!doctype html>
<html>
  <head>
  </head>
  <body>
<pre>
Documentation Page
=========================

What the workflow will look like:

 - Automatic Session (with cookies)

 - Make a game or Join a Game
    Make a game
    Join a game

 - Developer Info

 - Paradigm Info
    min_players
    max_players
    sequenced_turns --
      Enforce turn sequence.
      If turns are sequenced, then time limits are based on the current turn.
      Otherwise, time limits are based on the player's last turn.
      Once time runs out, a "null" move is sent.
    elo: boolean

 - Game Info
    min_players
    max_players
    turn_time --
      time allocated for each move, including first.
      after turn time expires, your total time starts draining.
    extra_turn_time --
      time allocated to the total time pool after each completed move.
    total_time --
      time allocated per player for entire game.
      once the turn time has been used, the total time starts draining.
    public_list -- list the game so anyone can view or join.
    public_view -- spectators may join, and game is listed after it is started.

    TODO: update elo based on score.
    Elo Stuff
      unranked -- dont compute elo
      min_elo
      max_elo
</pre>
  </body>
</html>
"""


