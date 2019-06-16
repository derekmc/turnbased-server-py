<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="static/basic.css">
    <script>
      var game_id = "{{ game_id }}"
      function init(){
      }
    </script>
  </head>
  <body>
    {{! nav_header }}
    <hr>
    <h1> Game Lobby "{{ game_id }}" </h1>
    <form>
      <table style="min-width: 240px;">
        <tr><th> Seat </th> <th> Join </th></tr>
        <tr><td> 1 </td> <td> Filled </tr>
        <tr><td> 2 </td> <td><button> Sit </button><td></tr>
        <tr><td> 3 </td> <td> Empty </td></tr>
        <!--tr><td colspan=2><button> Take Next Seat </button> <button> Enter Game</button></td></tr-->
      </table>
      <br>
      <button> Take Next Seat </button>
      <button> Enter Game </button>
      <hr>
    </form>
    
  </body>
</html>
