import subprocess, os
import util

def call2to3(path, rewrite = False, path2to3 = r"C:\Program Files (x86)\Python 3.5\Tools\scripts\2to3.py"):
    
    command = \
        ["python", path2to3, "-w", path] if rewrite \
        else ["python", path2to3, path]

    subprocess.call(command)



def main(*, root = ".", rewrite = False):
    for filepath in util.findfile(root):
        if filepath[-len(".py"):] == ".py":
            call2to3(filepath, rewrite = rewrite)