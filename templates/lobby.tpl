<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/basic.css">
    <script>
      var game_id = "{{ game_id }}"
      var my_seat = "{{ my_seat }}"
      window.addEventListener("load", init);
      function init(){
          
      }
      function sit(seat){
        var sit_index_input = document.getElementById('sit_index');
        sit_index_input.value = seat;
      }
      function stand(){
        var sit_index_input = document.getElementById('sit_index');
        sit_index_input.value = -1;
      }

    </script>
  </head>
  <body>
    {{! nav_header }}
    % if error_message != None:
      <span class='error_text'> {{ error_message }} </span>
    % end
    <h1> Game Lobby "{{ game_id }}"</h1>
    Game - <b><i>{{info['paradigm']}}</i></b> <br><br>
    <form method="POST">
      <input id="sit_index" name="sit_index" type="hidden" value="0"/>
      <table style="min-width: 240px;">
        <tr><th> Seat </th> <th> Player </th></tr>
        %for i in range(int(info['max_players'])):
          <tr>
            %# bold the required seats.
            <td>
              %if i < int(info['min_players']):
                <b> {{i+1}} </b>
              %else:
                {{i+1}}
              %end
            </td>
            <td>
              %if int(my_seat) == i+1:
                <input type="submit" onclick="stand()"; value="Stand"> </input>
              %elif i+1 in seats:
                Player {{i+1}}
              %elif my_seat == 0 and info.get('choose_seats',True):
                <input type="submit" onclick="sit({{i+1}})" value="Sit"> </input>
              %else:
                -
              %end
            </td>
          </tr>
        %end
        %if not info.get('choose_seats',True) and my_seat == 0:
          <tr><td colspan=2><button> Take Next Seat </button></td></tr>
        %end
        <tr>
          <td colspan=2>
            %if my_seat == 0:
              <button disabled> Enter Game </button>
              <button> Spectate Game </button>
            %else:
              <button> Enter Game </button>
              <button disabled> Spectate Game </button>
            %end
          </td>
        </tr>
        <!--
        <tr><td> 1 </td> <td> Player 1 </td></tr>
        <tr><td> 2 </td> <td><button disabled > Sit </button></td></tr>
        <tr><td> 3 </td> <td> - </td></tr>
        <tr><td> 4 </td> <td><button> Stand </button></td></tr>
        <tr><td colspan=2><button> Take Next Seat </button> <button> Enter Game</button></td></tr-->
      </table>
      <br>
    </form>
    
  </body>
</html>
