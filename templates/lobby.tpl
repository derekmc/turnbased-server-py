<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/basic.css">
    <script>
      var game_id = "{{ game_id }}"
      function init(){
      }
    </script>
  </head>
  <body>
    {{! nav_header }}
    <h1> Game Lobby "{{ game_id }}"</h1>
    Game Type - <i>{{info['paradigm']}}</i> <br><br>
    <form>
      <table style="min-width: 240px;">
        <tr><th> Seat </th> <th> Player </th></tr>
        <tr><td> 1 </td> <td> Player 1 </td></tr>
        <tr><td> 2 </td> <td><button disabled > Sit </button></td></tr>
        <tr><td> 3 </td> <td> - </td></tr>
        <tr><td> 4 </td> <td><button> Stand </button></td></tr>
        <!--tr><td colspan=2><button> Take Next Seat </button> <button> Enter Game</button></td></tr-->
      </table>
      <br>
      <button> Take Next Seat </button>
      <button> Enter Game </button>
      <button disabled> Spectate Game </button>
    </form>
    
  </body>
</html>
