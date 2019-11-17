<!doctype html>

<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    %if not my_turn:
       <!-- <meta http-equiv="refresh" content="15; url=/game/{{game_id}}/textplay" />-->
    %end
    <link rel="stylesheet" type="text/css" href="/static/basic.css">
    <style>
     body{ margin: 0; padding: 1em 2em; font-family: sans-serif;}

     * { }
    </style>
    %if status["is_started"] and not my_turn and not status["is_finished"]:
      <script src="/static/auto_refresh.js"></script>
      <script>
        REFRESH_TIME = 7.5*1000;
      </script>
    %end
    <script>
        function squareClick(square_name){
            var move_text_input = document.getElementById("move_text_input");
            var square_elem = document.getElementById("square_" + square_name);
            if(move_text_input.value.length){
                move_text_input.value += "-"; }
            move_text_input.value += square_name;
            square_elem.classList.add('clicked');
        }
        function clearMove(){
            var move_text_input = document.getElementById("move_text_input");
            move_text_input.value = "";
            var clicked_squares = document.getElementsByClassName('clicked');
            // removing the class removes the item from 
            // the datastructure, so always use index 0
            while(clicked_squares.length){
                clicked_squares[0].classList.remove('clicked'); }
        }
    </script>
  </head>

  <body>
    {{! nav_header }}
    <div class="overlay" onclick="window.location = window.location.pathname;">
      <h2> Page Idle </h2>
      <h3> Click to Refresh </h3>
    </div>
    <div class="main">
      <br>
      <h1> {{ game_name.strip() }} Text Play </h1>
      %if len(info.get('version', '')):
        <h3> Version {{info['version']}}</h3>
      %end

      %if not status["is_started"]: # required attribute should be present.
        Game has not started (how are you even here?)
      %elif not status["is_finished"]:
        <!-- TODO handle seat scores and seat ranks -->
        <b>{{!"Your Move" if my_turn else "Player " + str(turn_index) + "'s Turn."}}</b>
        <br><br>
        %if my_turn:
          %if move_list:
            %for move in move_list:
              <form method="POST">
                <input type="hidden" name="move_text" value="{{move}}">
                <input type="submit" value="{{move}}"/>
              </form>
            %end
          %else:
            <form method="POST">
              <input id="move_text_input" name="move_text" type="text" title="(example: (example_move goes here))">
              <input type="submit" value="Submit"/>
            </form>
            <button onclick="clearMove()">Clear</button>
          %end
        %end
      %else:
        Game finished.
        %if score:
          %if "winners" in score:
            %for winner in score["winners"]:
              %if winner == my_seat:
                You won!
              %else:
                Player {{winner}} won.
              %end
            %end
          %end
          %if "losers" in score:
            %for loser in score["losers"]:
              %if loser == my_seat:
                You lost.
              %else:
                Player {{loser}} lost.
              %end
            %end
          %end
        %end
      %end

      <div style="font-size: 160%; font-family: monospace;">
        <div style="text-align: center">{{! game_text.replace('\n','<br>') }}</pre>
      </div>
      %if status['is_started'] and not status['is_finished'] and not my_turn:
        <a href="./textplay">Refresh</a>
      %end
      <hr>
      <span style="font-size: 10pt;">
        <p>This is a text-based interface for turnbased games.
           If it's your turn, there will be a box above to enter your move,
           otherwise, refresh the page until it's your turn.
        </p>
      </span>
    </div>
  </body>
</html>
