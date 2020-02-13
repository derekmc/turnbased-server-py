<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/basic.css">
    <!-- <meta http-equiv="refresh" content="20; url=/game/{{game_id}}/lobby" /> -->
    <script src="/static/auto_refresh.js"></script>
    <script>
      var game_id = "{{ game_id }}"
      var is_seated = "{{!"true" if is_seated else "false"}}"

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
  <body class="hide">
    % include('nav.tpl')
    <div class="overlay" onclick="window.location = window.location.pathname;">
      <h2> Page Idle </h2>
      <h3> Click to Refresh </h3>
    </div>
    <div class="main">
      <h1> Game Lobby "{{ game_id }}"</h1>
      Game - <b><i>{{info['paradigm']}}</i></b> <br><br>
      <table class="listtable" style="min-width: 240px;">
        <tr><th> Seat </th> <th> Player </th></tr>
        %multi_sit = info.get('multi_sit', False)
        %choose_seats = info.get('choose_seats', True)
        %for i in range(int(info['max_players'])):
          %seat = seats[i] if i < len(seats) else ""
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
              %if seat == "me":
                  %if allow_seating:
                    <form method="POST" action="./sit">
                      <input id="seat_index" name="seat_index" type="hidden" value="{{-(i+1)}}"/>
                      <input type="submit" value="Stand"> </input>
                    </form>
                  %else:
                    Seated
                  %end
              %elif seat != "":
                Player {{seat}}
              %elif (not is_seated or multi_sit) and choose_seats:
                %if allow_seating:
                  <form method="POST" action="./sit">
                    <input id="seat_index" name="seat_index" type="hidden" value="{{i+1}}"/>
                    <input type="submit" value="Sit"> </input>
                  </form>
                %else:
                  -
                %end
              %else:
                -
              %end
            </td>
          </tr>
        %end
        %if not info.get('choose_seats',True) and (info.get('multi_sit', True) or not is_seated):
          <td colspan=2>
            <form method="POST" action="./sit">
              <input id="seat_index" name="seat_index" type="hidden" value="0"/>
              <input type="submit" value="Take Next Seat"> </input>
            </form>
          </td>
        %end
        <tr>
          <td colspan=2>
            %if not is_seated:
              <button disabled>
                {{!"Enter" if status["is_started"] else "Start"}} Game
              </button>
              %if status["is_started"]:
                <a target="_blank" href="./textplay"><button> Spectate Game </button></a>
              %else:
                <button disabled> Spectate Game </button>
              %end
            %else:
              %if status["is_started"]:
                <a target="_blank" href="./textplay"><button>
                  Enter Game
                </button></a>
              %elif can_start:
                <a target="_blank" href="./textplay"><button>
                  Start Game
                </button></a>
              %else:
                <button disabled> Start Game </button>
              %end
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
      <a href="./lobby">Refresh</a>
    </div>
  </body>
</html>
