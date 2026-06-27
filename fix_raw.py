import re

files = ['src/nfa_compiler.npk', 'src/prefix_extractor.npk']
for fpath in files:
    with open(fpath, 'r') as f:
        c = f.read()
    c = c.replace('alist()', 'raw alist()')
    c = c.replace('alpush(', 'raw alpush(')
    c = c.replace('alpop(', 'raw alpop(')
    with open(fpath, 'w') as f:
        f.write(c)
