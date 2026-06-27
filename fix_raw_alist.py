import re
with open('src/alist.npk', 'r') as f:
    c = f.read()
c = c.replace('npk_core_alloc(', 'raw npk_core_alloc(')
c = c.replace('npk_mem_write_int64(', 'raw npk_mem_write_int64(')
c = c.replace('npk_mem_read_int64(', 'raw npk_mem_read_int64(')
with open('src/alist.npk', 'w') as f:
    f.write(c)
