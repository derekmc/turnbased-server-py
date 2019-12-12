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
        function submitMove(){
            document.move_input_form.submit();
        }
        function squareClick(square_name){
            var move_text_input = document.getElementById("move_text_input");
            var square_elem = document.getElementById("square_" + square_name);
            var move_text = move_text_input.value;
            //if(move_text.length){
            var squares = move_text.split('-');
            %if multi_move: # mixing template conditionals and client conditionals, lol.
                last_square = squares[squares.length - 1];
                if(last_square == square_name){
                    submitMove();
                    return; }
                if(move_text.length) move_text_input.value += "-";
                move_text_input.value += square_name;
            %elif single_move: # one square move
                move_text_input.value += square_name;
                submitMove()
                return;
            %else: # two square move
                var move_started = move_text.length > 0;
                if(move_started){
                    move_text_input.value += "-" + square_name;
                    submitMove();
                    return; }
                else{
                    move_text_input.value += square_name; }
            %end
           
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
      <h1> {{ game_name.strip() }}
        %if len(info.get('version', '')):
          ({{info['version']}})
        %end
      </h1>

      %if not status["is_started"]: # required attribute should be present.
        Game has not started (how are you even here?)
      %elif not status["is_finished"]:
        %if illegal_move:
          <p class="error_message"> Player {{! str(seat_number)}}  Illegal move: {{illegal_move}} </p>
        %else:
          <!-- TODO handle seat scores and seat ranks -->

          <p class="banner_message">{{!move_prompt}}</p>
        %end
      %else:
        Game finished.
        {{!end_game_message}}
      %end
      <div id="text_play_main" >
        <div style="text-align: center">{{! game_text.replace('\n','<br>') }}</div>
      </div>
      %if status['is_started'] and not status['is_finished']:
        %if not my_turn:
          <a href="./textplay">Refresh</a>
        %else:
          %if move_list:
            %for move in move_list:
              <form method="POST" name="move_input_form">
                <input type="hidden" name="move_text" value="{{move}}">
                <input type="submit" value="{{move}}"/>
              </form>
            %end
          %else:
            <form method="POST" name="move_input_form">
              <input id="move_text_input" name="move_text" type="text" title="(example: (example_move goes here))">
              <input type="submit" value="Submit"/>
            </form>
            <button onclick="clearMove()">Clear</button>
          %end
        %end

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
