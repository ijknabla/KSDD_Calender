import subprocess, util

def callgit_add(path):
    subprocess.call(["git", "add", path])

def callgit_rm(path):
    subprocess.call(["git", "rm", path])

def autogit_add(filter_func):
    for filepath in util.findfile(
        filter_func = lambda path : (
            ".git" not in path and
            ".bak" not in path
            )
        ):
        print(filepath)