<!doctype html>

<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    %if not my_turn:
       <!-- <meta http-equiv="refresh" content="15; url=/game/{{game_id}}/textplay" />-->
    %end
    <link rel="stylesheet" type="text/css" href="/static/basic.css">
    <style>
     body{ max-width: 480px; margin: 0; padding: 1em 2em; font-family: sans-serif;}

     * { }
    </style>
    %if not my_turn:
      <script src="/static/auto_refresh.js"></script>
      <script>
        REFRESH_TIME = 7.5*1000;
      </script>
    %end
  </head>

  <body>
    {{! nav_header }}
    <div class="overlay" onclick="window.location = window.location.pathname;">
      <h2> Page Idle </h2>
      <h3> Click to Refresh </h3>
    </div>
    <div class="main">
      <br>
      <h1> {{ game_name }} Text Play </h1>
      %if len(info.get('version', '')):
        <h3> Version {{info['version']}}</h3>
      %end

      <b>{{!"Your Move" if my_turn else "Player " + str(turn_index) + "'s Turn."}}</b>
      <br><br>

      %if not my_turn:
        <a href="./textplay">Refresh</a>
      %end

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
            <input name="move_text" type="text" title="(example: (example_move goes here))">
            <input type="submit" value="Submit"/>
          </form>
        %end
      %end
      <span style="font-size: 160%; font-family: monospace;">
        <pre>{{ game_text }}</pre>
      </span>

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
