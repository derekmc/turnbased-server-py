
import sys, os

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")

if __name__ == "__main__":
    from app import app
    import settings
    app.run(debug=True, port=8000, server='waitress')
    #app.run(debug=False)
