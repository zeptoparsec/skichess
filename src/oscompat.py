import os
from itertools import chain

def escapeFilePaths(path, file=True):
    if os.name == 'nt':
        ch = "\\"
    else:
        ch = "/"

    xs = [ch]

    for i in path:
        xs.append(i)
        xs.append(ch)

    if file:
        xs.pop()

    return ''.join(list(chain.from_iterable(xs)))
