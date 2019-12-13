<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/basic.css">
  </head>
  <body>
    {{! nav_header }}
    <h1> List Games </h1>
    <div id="main">
      <ul>
        <li><a href="/mygames"> My Games </a></li>
        <li><a href="/opengames"> Open Games </a></li>
        <li><a href="/activegames"> Active Games </a></li>
        <li><a href="/finishedgames"> Finished Games </a></li>
      </ul>

     <h3> {{!list_title.title()}} Games </h3>
     <table class="listtable">
      %for game_info in game_list:
        <tr>
          %play_state = game_info['play_state']
          %if play_state == "Active" or play_state == "Finished":
            <td><a href='/game/{{game_info['id']}}/textplay'>{{game_info['id']}}</a></td>
          %else:
            <td><a href='/game/{{game_info['id']}}/lobby'>{{game_info['id']}}</a></td>
          %end
          <td>{{game_info['paradigm']}}</td>
          <td>{{game_info['play_state']}}</td>
       </tr>
      %end
      %if len(game_list) == 0:
        No {{list_title}} games.
      %end
     </table>
    </div>
  </body>
</html>
