
"""
import os

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module
"""

import os
import glob
import importlib
try:
    __games_dir = os.path.basename(os.path.normpath(os.path.dirname(os.path.realpath(__file__))))
except:
    __games_dir = "games"
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
games_list = [ importlib.import_module(__games_dir + "." + os.path.basename(f)[:-3]) for f in modules if os.path.isfile(f) and not f.endswith('__init__.py')]


