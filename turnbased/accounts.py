
# comma separated values LoginName, Salt, Hash, LoginID, MustChange
# MustChange is if you merge two different services, then 
__header_line = "LoginName, Salt, Hash, LoginID, MustChange, Locked"
__login_name_index = 0
__salt_index = 1
__hash_index = 2
__login_id_index = 3
__must_change_index = 4
__locked_index = 5


Account = {
    "LoginName" : "",
    "Salt" : "",
    "Hash" : "",
    "LoginID" : 0,
    # MustChange is set if you merge two different sets of accounts, and there is a conflict in login names 
    "$MustChange" : False,
    # In the rare case there is a conflict in both login names and passwords upon a merge, lock both accounts, and require manual resolution.
    "$Locked" : False,
}
Accounts = {
    "list": [Account],
    "names": {"": 0} # maps name to the list index
    "ids": {0: 0}, # maps login id to the list index
}
def load_accounts(accounts_file):
    result = T(Accounts, {list: [], ids: set()})

    with open(accounts_file) as f:
        for i, line in enumerate(f.readlines()):
            if i == 0: # header
                continue
            account_row = [entry.strip() for entry in line.split(",")]
            account = {}
            login_name = account["LoginName"] = account_row[__login_name_index]
            account["Salt"] = account_row[__salt_index]
            account["Hash"] = account_row[__hash_index]
            login_id = account["LoginID"] = int(account_row[__login_id_index])
            if len(account_row) > __must_change_index:
                account["MustChange"] = account_row[__must_change_index]
            if len(account_row) > __locked_index:
                account["Locked"] = account_row[__locked_index]
            result["list"].append(account)
            index = len(result.list) - 1
            result["names"][login_name] = index
            result["ids"][login_id] = index
    
    return result

def save_accounts(accounts_file, accounts):
    T(Accounts, accounts)

    with open(accoun)
    pass

def is_user(accounts_file, login_name):
   
    return False


def new_user(accounts_file, login_name, password, is_admin=False):
    if is_user(accounts_file, login_name):
        return False
    save_user

def remove_user(accounts_file, login_name, password):



def update_user(accounts_file, login_name, old_password, new_password, is_admin=False):
    if not check_user(accounts_file, login_name, old_password):
        return False
    
    
    
    updated_file_lines = []
    with open(accounts_file) as f:
        for i, line in enumerate(f.readlines())
            if i == 0:
                update_file_lines.append(line)
            account_info = [entry.strip() for entry in line.split(",")]
            



def save_user(accounts_file, login_name, password, is_admin=False):
    salt = gen_token(settings.SALT_LEN)
    hash_value = hashlib.sha256((salt + password).encode()).hexdigest()

    

    add_headers = not os.path.exists(accounts_file)
    with open(accounts_file, "a") as file:
        if add_headers:
            file.append(__header_line + "\n")
        file.append()


# TODO if user has valid credentials, but login name and password already exist on this server, force a name change. 
def check_user(accounts_file, login_name, password):
    with open(accounts_file) as f:


