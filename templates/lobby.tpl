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
      /*
      function sit(seat){
        var sit_index_input = document.getElementById('sit_index');
        sit_index_input.value = seat;
      }
      function stand(){
        var sit_index_input = document.getElementById('sit_index');
        sit_index_input.value = -1;
      }
      */

    </script>
  </head>
  <body>
    {{! nav_header }}
    <h1> Game Lobby "{{ game_id }}"</h1>
    Game - <b><i>{{info['paradigm']}}</i></b> <br><br>
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
                <form method="POST" action="./sit">
                  <input id="seat_index" name="seat_index" type="hidden" value="-1"/>
                  <input type="submit" value="Stand"> </input>
                </form>
              %elif i < len(seats) and seats[i] != "":
                Player {{i+1}}
              %elif my_seat == 0 and info.get('choose_seats',True):
                <form method="POST" action="./sit">
                  <input id="seat_index" name="seat_index" type="hidden" value="{{i+1}}"/>
                  <input type="submit" value="Sit"> </input>
                </form>
              %else:
                -
              %end
            </td>
          </tr>
        %end
        %if not info.get('choose_seats',True) and my_seat == 0:
          <td colspan=2>
            <form method="POST" action="./sit">
              <input id="seat_index" name="seat_index" type="hidden" value="0"/>
              <input type="submit" value="Take Next Seat"> </input>
            </form>
          </td>
        %end
        <tr>
          <td colspan=2>
            %if my_seat == 0:
              <button disabled> Enter Game </button>
              <a href="./textplay"><button> Spectate Game </button></a>
            %else:
              <a href="./textplay"><button> Enter Game </button></a>
              <button disabled> Spectate Game </button>
            %end
          </td>
        </tr>
        <!--Seats: {{seats}}-->
        <!--
        <tr><td> 1 </td> <td> Player 1 </td></tr>
        <tr><td> 2 </td> <td><button disabled > Sit </button></td></tr>
        <tr><td> 3 </td> <td> - </td></tr>
        <tr><td> 4 </td> <td><button> Stand </button></td></tr>
        <tr><td colspan=2><button> Take Next Seat </button> <button> Enter Game</button></td></tr-->
      </table>
      <br>
  </body>
</html>
