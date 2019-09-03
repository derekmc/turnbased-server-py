<!doctype html>

<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!--<meta http-equiv="refresh" content="10; url=/game/{{game_id}}/textplay" />-->
    <link rel="stylesheet" type="text/css" href="/static/basic.css">
    <style>
     body{ max-width: 480px; margin: 0; padding: 1em 2em; font-family: sans-serif;}

     * { }
    </style>
  </head>

  <body>
    {{! nav_header }}

    <!-- START-SECTION: html -->
      <h1> Turnbased Game Test </h1>

      <table>
        <tr><th>Paradigm</th><td>{{info['paradigm']}}</td>
            <th>Version</th><td>{{info.get('version','')}}</td></tr>
        <tr><th>Current Turn</th><td>{{turn_index}}</td>
            <th>Total Turns</th><td>{{turn_count}}</td></tr>
      </table>
      <br>
      <a href="./textplay">Refresh Game</a><br>


      <hr>
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
      <pre>{{ game_text }}</pre>

      <hr>
      <small>
      <p>This is a text-based interface for turnbased games.
         If it's your turn, there will be a box above to enter your move,
         otherwise, refresh the page until it's your turn.
      </p>
    </small>

    <!-- END-SECTION: html -->
  </body>
</html>
