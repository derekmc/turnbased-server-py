
import sys, os

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")

if __name__ == "__main__":
    from turnbased.app import app
    from turnbased import settings, data
    from turnbased.settings import ACCOUNTS_FILE as accts_file
    #import accounts
    #import util

    ## TODO prompt for admin user name and password if none exists
    # if not os.path.exists(accts_file):
    #     admin_name = input("Admin Login Name: ")
    #     admin_password = input("Admin Password:" )
    #     # datastructure for processing user creation, not saved directly.
    #     user_creds = {
    #         "LoginName" : admin_name,
    #         "Password" : admin_password,
    #     }
    #     login_id = accounts.new_user(accts_file, user_creds)
    #     user_id = util.genToken(settings.USER_ID_LEN, taken=data.user_ids, tries=settings.GEN_ID_TRIES)
    #     data.login_ids[admin_name] = user_id
    #     user_info = data.user_info[user_id] = {}
    #     user_info["is_admin"] = True
    #     user_info["user_name"] = login_name
    #     user_info["login_id"] = login_id

    
    data.load()
    # the server bottle should use.  This one seems to work well with minimal requirements
    # see bottle.server_names variable for list of available servers.
    app.run(debug=True, port=8000, server='waitress')

    #app.run(debug=False)
