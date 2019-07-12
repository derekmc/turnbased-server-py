<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/basic.css">
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
      var paradigms = {{! json.dumps(data['paradigms'])}}
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
    {{! nav_header }}
    <form method="POST">
    <h1> New Game </h1>
      <table>
        <tr>
          <td> Game Type </td>
          <td>
            <select name="game_paradigm" id="game_paradigm" onchange="updateParadigm();">
              %for name in data['paradigms']:
                <option value="{{name}}"> {{name}} </option>
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
          <td colspan=2>
            <label for="choose_seats">Choose Seats</label>
            <input type="checkbox" name="choose_seats" id="choose_seats"></input>
          </td>
        </tr>
        <tr>
          <td colspan=2><input type="submit" value="Create Game"></input></td>
        </tr>
      <table>
    </form>
  </body>
</html>
