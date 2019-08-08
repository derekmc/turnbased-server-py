<!doctype html>

<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!--<meta http-equiv="refresh" content="10; url=/game/{{game_id}}/textplay" />-->
    <style>
     body{ max-width: 480px; margin: 0; padding: 1em 2em; font-family: sans-serif;}

     * { }
    </style>
  </head>

  <body>
    {{! nav_header }}

    <!-- START-SECTION: html -->
      <h2> Turnbased Game Test </h2>
      <table>
      Paradigm: {{info['paradigm']}} <br>
      Version: {{info.get('version','')}} <br>
      Turn: <br>
      
      <pre>{{ game_text }}</pre>
      <form>
        <!--input name="move_text" type="text" title="(example: e2 e4)">
        <input type="submit" value="Submit"/-->
      </form>
      
      <p>This is a text-based testing interface for turnbased games.
         If it's your turn, there will be a box above to enter your move,
         otherwise, the page will automatically refresh until it's your turn.
      </p>
      
      <p> Example move: <b></b></p>
    <!-- END-SECTION: html -->
  </body>
</html>

