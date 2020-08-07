from os import listdir, getcwd, path
import sys


sys.path.append(getcwd() + '/modules')
modules_list = []

path_mods = getcwd() + '/modules'
for item in listdir(path_mods):
    temp_tuple = path.splitext(item)
    if temp_tuple[1] == ".py":
        modules_list.append(temp_tuple)

print(modules_list)

for module in modules_list:
    if "".join(module) != __file__:
        exec(f"import {module[0]}")
        print(f"imported {''.join(module)}")
