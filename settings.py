
COOKIE_NAME = "COOKIE"   
COOKIE_LEN = 12  
USER_ID_LEN = 12
COOKIE_TRIES = 6
GEN_ID_TRIES = 6 
GAME_ID_LEN = 4
SALT_LEN = 16
ALLOW_NAMES = True
ALLOW_CHAT = True # chat includes a maximum number of lines and characters.
MAX_CHAT_LEN = 10000
NAV_FILE = "views/nav.html.tpl"
DATA_FILE = "game_data.pickle"

# comma separated list of username, user-id, password salts, and password hashes.
# this is distinct from the game data so it can be replicated to other services
ACCOUNTS_FILE = "accounts.txt" 
VERBOSE = True
