<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/basic.css">
  </head>
  <body>
    {{! nav_header }}
    <h1> {{list_title}} Games </h1>
    <div id="main">
     
     <table>
      %for game in game_list:
       <tr><td><a href='/game/{{game['id']}}/lobby'>{{game['id']}}</a></td>
           <td>{{game['paradigm']}}</td>
       </tr>
      %end
     </table>
    </div>
  </body>
</html>
