import os, sys

def all_dir(root = os.curdir):
    if not os.path.isdir(root):
        root = os.path.dirname(root)

    for target in os.listdir(root):
        target = os.path.join(root, target)
        if os.path.isdir(target):
            yield target
            yield from all_dir(target)

def all_file(root = os.curdir):
    for dir in all_dir(root):
        print(dir)
        yield from filter(
            os.path.isfile,
            os.listdir(dir)
            )


def find_2to3():
    pythonpath = sys.path[1]
    if not os.path.isdir(pythonpath):
        pythonpath = os.path.dirname(pythonpath)
    print(pythonpath)

    for i in all_file(pythonpath):
        print(i)
    return [os.path.abspath(file) for file in all_file(pythonpath) if "2to3.py" in file]
