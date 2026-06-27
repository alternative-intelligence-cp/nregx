import re

files = ['src/nfa_compiler.npk', 'src/prefix_extractor.npk', 'src/alist.npk']
for fpath in files:
    with open(fpath, 'r') as f:
        c = f.read()
    c = c.replace('raw alist()', 'alist()')
    c = c.replace('raw alpush(', 'alpush(')
    c = c.replace('raw alpop(', 'alpop(')
    c = c.replace('raw npk_core_alloc(', 'npk_core_alloc(')
    c = c.replace('raw npk_mem_write_int64(', 'npk_mem_write_int64(')
    c = c.replace('raw npk_mem_read_int64(', 'npk_mem_read_int64(')
    with open(fpath, 'w') as f:
        f.write(c)
