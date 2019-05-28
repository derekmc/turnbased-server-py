
from textwrap import dedent


index_html = dedent("""
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
        <a href="/games/new"> New Game </a> -
        <a href="/games/list"> List Games </a> -
        <a href="/docs"> Docs </a>
        <hr>
      </body>
    </html>
    """)

new_game_tmpl = dedent("""
    <!doctype html>
    <html>
      <head>
        <style>
          body{ font-family: sans-serif; }
          td{ padding: 0.25em; }
          a:visited{ color: blue; }
        </style>
        <script>
          window.addEventListener("load", init);
          function id(x){ return document.getElementById(x); }
          function int(x){ return x? parseInt(x) : 0; }
          function updateMin(){
            var min = int(id("min_players").value);
            var max = int(id("max_players").value);
            if(max < min) id("min_players").value = max;
          }
          function updateMax(){
            var min = int(id("min_players").value);
            var max = int(id("max_players").value);
            if(max < min) id("max_players").value = min;
          }
          % import json
          var paradigm_list = {{! data['paradigms']}}
          var paradigms = {};
          for(var i=0; i<paradigm_list.length; ++i){
              var paradigm = paradigm_list[i];
              paradigms[paradigm.name] = paradigm; }
          function updateParadigm(name){
             var name = id("game_paradigm").value;
             var paradigm = paradigms[name];
             if(!paradigm) return;
             var min = paradigm.min_players;
             var max = paradigm.max_players;
             id("min_players").min = min;
             id("min_players").max = max;
             id("min_players").value = min;
             id("max_players").min = min;
             id("max_players").max = max;
             id("max_players").value = max;
          }
          function init(){
             updateParadigm();
          }
        </script>
      </head>
      <body>
        <hr>
        <form method="POST">
        <h1> New Game </h1>
          <table>
            <tr>
              <td> Game Type </td>
              <td>
                <select name="game_paradigm" id="game_paradigm" onchange="updateParadigm();">
                  %for paradigm in data['paradigms']:
                    <option value="{{paradigm['name']}}"> {{paradigm['name']}} </option>
                  %end
                </select><br>
              </td>
            </tr>
            <tr>
              <td>Min Players</td>
              <td><input name="min_players" id="min_players" onchange="updateMax();"
                         type="number" min=0 max=255></input></td>
            </td>
            <tr>
              <td>Max Players</td>
              <td><input name="max_players" id="max_players" onchange="updateMin();"
                         type="number" min=0 max=255></input></td>
            </td>
            <tr>
              <td></td>
              <td><input type="submit" value="Create Game"></input></td>
            </tr>
          <table>
        </form>
        <hr>
      </body>
    </html>
    """)




docs_html = dedent("""
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
    """)



