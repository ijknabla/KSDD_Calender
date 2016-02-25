import os

def findfile(root = os.curdir, *, filter_func = lambda path : True):
    result = []
    for target in os.listdir(root):
        path = os.path.join(root, target)
        if os.path.isdir(path):
            result.extend(findfile(path))
        else:
            if filter_func(path):
                result.append(path)
    return result