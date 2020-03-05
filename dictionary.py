""" Reads and returns Nanomine Unit Dictionary.
    more to go here
"""

def read_dictionary(filename):
    d = {}
    with open(filename) as f:
        for line in f:
            items = line.strip().split('=')
            if len(items) >= 2:
                d[items[0]] = items[1:]
    return d
