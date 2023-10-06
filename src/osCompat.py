from os import name
from itertools import chain

def escapeFilePaths(path, file=True):
    if name == 'nt':
        ch = "\\"
    else:
        ch = "/"

    xs = [ch]

    for i in path[0:-1]:
        xs.append(i)
        xs.append(ch)

    xs.append(path[-1].lower())
    xs.append(ch)

    if file:
        xs.pop()

    return ''.join(list(chain.from_iterable(xs)))

