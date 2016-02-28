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
    for dir_ in all_dir(root):
        for target in os.listdir(dir_):
            target = os.path.join(dir_, target)
            if os.path.isfile(target):
                yield target


def find_2to3():
    pythonpath = sys.path[1]
    if not os.path.isdir(pythonpath):
        pythonpath = os.path.dirname(pythonpath)

    for file in all_file(pythonpath):
        if file.split(os.sep)[-1] == "2to3.py":
            return os.path.abspath(file)

def get_2to3():
    try:
        with open("path2to3.txt", "r") as pathfile:
            path2to3 = pathfile.read()
            if os.path.isfile(path2to3):
                return path2to3
            else:
                raise ValueError
    except:
        with open("path2to3.txt", "w") as pathfile:
            path2to3 = find_2to3()
            pathfile.write(path2to3)
            return path2to3

if __name__ == "__main__":
    import subprocess
    subprocess.call(["python", get_2to3()])
    input("press any key")
