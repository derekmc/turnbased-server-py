
index_src = """
<!doctype html>
<html>
  <head>
    <style>
      body{ font-family: sans-serif; }
      a:visited{ color: blue; }
    </style>
  </head>
  <body>
    <hr>
    <h1> Turnbased Game Server </h1>
    <a href="/new"> New Game </a> -
    <a href="/list"> List Games </a> -
    <a href="/docs"> Documentation </a>
    <hr>
  </body>
</html>
"""


doc_src = """
<!doctype html>
<html>
  <head>
  </head>
  <body>
    <h1> Documentation Page </h1>
    What the workflow will look like:
    <ol>
     <li> Automatic Session (with cookies)</li>
     <li> Make a game or Join a Game
       <ol>
         <li> Make a game
           <ul><li>item</li></ul></li>
         <li> Join a game
           <ul><li>item</li></ul></li>
       </ol>
     </li>
     <li> Join as Developer </li>
    </ol>
  </body>
</html>
"""


