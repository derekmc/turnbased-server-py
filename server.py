
from bottle import Bottle, SimpleTemplate
import NimHandler as handler

import string
import pickledb
import random

app = Bottle()

def gen_randomstring(n):
    return ''.join(random.choice(string.ascii_letters) for x in range(n))
def gen_cookie():
    return gen_randomstring(COOKIE_LEN)


index_src = """
<!doctype html>
<html>
  <head>
  </head>
  <body>
    <h1> Index Page </h1>
    What the workflow will look like:
    <ul>
     <li></li>
    </ul>
  </body>
</html>
"""


@app.route('/')
def index():
    return index_src
    

if __name__ == "__main__":
    app.run(debug=False)


