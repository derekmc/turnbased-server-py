#!/usr/bin/python3

from sys import argv
FILENAME = 'todo.txt'
DEFAULT_LIST = 5

help_msg = """
todo (task description)
  OR
todo [index:int] [list | done | now | later]
 - index is optional, command defaults to list.
 - negative indexes are allowed, -1 is the last list item.

Examples:
 > todo pick up groceries  -- add a new item
 > todo           -- list default number of items
 > todo 10        -- lists 10 items 
 > todo later     -- moves top item to bottom of list
 > todo 7 now     -- moves item #7 to top of list
 > todo 3 later   -- moves item #3 to bottom of list
 > todo done      -- removes top item from list (with confirmation prompt)
 > todo -3 done   -- removes third to last item from list
 > todo help      -- show this message

"""

def __help(index, item):
    print(help_msg)

__file = open(FILENAME, 'a+')
#__file.write("")
#__file.close()
lines = open(FILENAME, 'r').readlines()
lines = list(filter(lambda x: len(x.strip())>0, lines))

def dump():
    # __file.write("".join(lines))
    open(FILENAME, 'w').write("".join(lines))

def listitems(index, na):
    if index <= 1:
        index = DEFAULT_LIST
    to_list = min(len(lines), max(index, DEFAULT_LIST))
    i = 1
    print("==== TODO LIST (%d/%d) ====" % (to_list, len(lines)))
    for line in lines:
        print(" %d - %s" % ( i, line.rstrip() ))
        i += 1
        if i > index:
            break

def add(index, item):
    lines.insert(index-1, item)
    dump()
    to_list = max(index, DEFAULT_LIST)
    listitems(to_list, item)

def now(index, na):
    if index > 0:
        index -= 1
    else: index += len(lines)
    item = ""
    try:
        item = lines[index]
    except:
        print("-- todo: no item #%d --" % (index + 1))
        return
    del lines[index]
    lines.insert(0,item)
    dump()
    listitems(DEFAULT_LIST, na)
    
def later(index, na):
    if index > 0:
        index -= 1
    else: index += len(lines)
    item = ""
    try:
        item = lines[index]
    except:
        print("-- todo: no item #%d --" % (index + 1))
        return
    del lines[index]
    lines.append(item)
    dump()
    listitems(len(lines), na)
    
def done(index, na):
    if index > 0:
        index -= 1
    else: index += len(lines)
    item = ""
    try:
        item = lines[index]
    except:
        print("-- todo: no item #%d --" % (index + 1))
        return
    confirm = input("Remove item \"" + item.strip() + "\" (Y/n): ")
    confirm = confirm.strip().lower()
    if confirm == "" or confirm == "y" or confirm == "yes":
        del lines[index]
        dump()
        listitems(DEFAULT_LIST, na)
        print("-- item #" + str(index + 1) + " removed -- ")
    else:
        print("-- 'done' action cancelled -- ")
    


def __main__():
    command = 'list'
    index = 1
    item = ""

    commands = {
        'list' : listitems,
        'done' : done,
        'add' : add,
        'now' : now,
        'later' : later,
        'help' : __help,
    }

    if len(argv) > 1:
        arg1 = ""
        single_command_len = 2
        try:
            index = int(argv[1])
            if len(argv) > 2:
                arg1 = argv[2]
            single_command_len = 3
        except:
            arg1 = argv[1]
            item = " ".join(argv[2:]) + "\n"
            command = 'add'
        if arg1 in commands:
            if len(argv) <= single_command_len:
                command = arg1
            else:
                command = 'add'
            item = " ".join(argv[2:]) + "\n"
        else:
            if len(argv) > single_command_len - 1:
                command = 'add'
            item = " ".join(argv[1:]) + "\n"

    # print("todo " + str(index) + " " + command)
    print("- todo '" + command + "' (" + str(index) + ")" + " -")
    action = commands[command]
    action(index, item)


if __name__ == "__main__":
    __main__()
