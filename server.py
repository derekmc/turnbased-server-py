
from bottle import Bottle, SimpleTemplate, request, response
import NimHandler as handler

import string
import pickledb
import random
import sys


DB_FILE = sys.argv[1] if len(sys.argv) > 1 else "turnbased_server.db"
COOKIE = "SESSION_ID"
COOKIE_KEY = "cookie|"
COOKIE_LEN = 8 

db = pickledb.load(DB_FILE, False)
app = Bottle()


def gen_randomstring(n):
    return ''.join(random.choice(string.ascii_letters) for x in range(n))
def gen_cookie():
    return gen_randomstring(COOKIE_LEN)


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

def session():
    cookie = request.get_cookie(COOKIE)
    if cookie:
        if db.get(COOKIE_KEY + cookie):
            return cookie
        else:
            cookie = None
        
    cookie = gen_cookie()
    response.set_cookie(COOKIE, cookie, path='/')
    db.set(COOKIE_KEY + cookie, cookie)
    db.dump()

    return cookie


@app.route('/')
def index():
    cookie = session()
    return index_src
    
@app.route('/docs')
def docs():
    return doc_src


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=False)


