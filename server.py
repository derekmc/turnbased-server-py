
import sys, os

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")

if __name__ == "__main__":
    from app import app
    import settings
    import data

    data.load()
    # the server bottle should use.  This one seems to work well with minimal requirements
    # see bottle.server_names variable for list of available servers.
    app.run(debug=True, port=8000, server='waitress')

    #app.run(debug=False)
