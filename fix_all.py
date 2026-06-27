import re

# 1. Result<T> fixes
files_res = ['src/regex_compiler.npk', 'src/nfa_compiler.npk', 'src/prefix_extractor.npk']
for filepath in files_res:
    with open(filepath, 'r') as f:
        content = f.read()
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'pass 0i64;' in line and 'lex_pattern' not in line:
            lines[i] = line.replace('pass 0i64;', 'fail ERR_REGEX_PARSE;')
        line = lines[i]
        line = re.sub(r'(int64:\w+\s*=\s*)(raw\s+)?(parse_alt|parse_concat|parse_rep|parse_atom|parse_regex_ast|compile_nfa|extract_literal_prefix)\(', r'\1\3(', line)
        line = re.sub(r'(\s*)(raw\s+)?(parse_alt|parse_concat|parse_rep|parse_atom|parse_regex_ast|compile_nfa|extract_literal_prefix)\((.*?)\)', r'\1\3(\4) ? 0i64', line)
        lines[i] = line
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))

with open('src/nregx.npk', 'r') as f:
    content = f.read()
    content = re.sub(r'raw compile_and_cache', r'compile_and_cache', content)
    content = re.sub(r'compile_and_cache\((.*?)\)', r'compile_and_cache(\1) ? 0i64', content)
    with open('src/nregx.npk', 'w') as f:
        f.write(content)

# 2. Pointer accesses and Cache
files_ptr = ['src/regex_cache.npk', 'src/regex_compiler.npk', 'src/nfa_compiler.npk', 'src/prefix_extractor.npk', 'src/regex_vm.npk']
for filepath in files_ptr:
    with open(filepath, 'r') as f:
        content = f.read()
        
    content = re.sub(r'(\b\w+_ptr)\.(\w+\b)', r'\1->\2', content)

    if 'regex_cache.npk' in filepath:
        content = re.sub(r'    func:npk_shim_atomic_int32_fetch_add = int32\(int64:ptr, int32:val, int32:memorder\);\n', '', content)
        content = re.sub(r'    func:npk_shim_atomic_int32_fetch_sub = int32\(int64:ptr, int32:val, int32:memorder\);\n', '', content)
        content = re.sub(r'([A-Za-z0-9_]+)\s*=>\s*Handle<CacheEntry>', r'@cast_unchecked<CacheEntry->>(\1)', content)
        content = re.sub(r'Handle<CacheEntry>:next', 'CacheEntry->:next', content)
        content = re.sub(r'([A-Za-z0-9_]+->next)\s*=>\s*int64', r'@cast_unchecked<int64>(\1)', content)

        # In regex_cache_insert:
        content = content.replace('''    // hit_counter
    int64:hit_ptr = npk_core_alloc(8i64);
    drop npk_mem_write_int32(hit_ptr, 0i64, 0i32);
    entry_ptr->hit_counter = @cast_unchecked<atomic<int32>->>(hit_ptr);''', '''    // hit_counter
    entry_ptr->hit_counter = atomic_new(0i32);''')

        content = content.replace('''    // ref_count
    int64:ref_ptr = npk_core_alloc(8i64);
    drop npk_mem_write_int32(ref_ptr, 0i64, 2i32); // 1 for cache, 1 for caller
    entry_ptr->ref_count = @cast_unchecked<atomic<int32>->>(ref_ptr);''', '''    // ref_count
    entry_ptr->ref_count = atomic_new(2i32); // 1 for cache, 1 for caller''')

        # Cache get
        content = content.replace('''                atomic<int32>->:ref_count_ptr = curr_ptr->ref_count;
                drop npk_shim_atomic_int32_fetch_add(@cast_unchecked<int64>(ref_count_ptr), 1i32, 0i32);''', '''                atomic<int32>:_rc = curr_ptr->ref_count;
                drop _rc.fetch_add(1i32);
                curr_ptr->ref_count = _rc;''')

        # Cache insert cleanup
        content = content.replace('''            atomic<int32>->:ref_count_ptr = curr_ptr->ref_count;
            int32:refs = npk_shim_atomic_int32_fetch_sub(@cast_unchecked<int64>(ref_count_ptr), 1i32, 0i32);''', '''            atomic<int32>:_rc = curr_ptr->ref_count;
            int32:refs = _rc.fetch_sub(1i32);
            curr_ptr->ref_count = _rc;''')

        content = content.replace('''                atomic<int32>->:hit_ptr = curr_ptr->hit_counter;
                drop npk_core_dalloc(@cast_unchecked<int64>(hit_ptr));
                drop npk_core_dalloc(@cast_unchecked<int64>(ref_count_ptr));
                drop npk_core_dalloc(curr);''', '''                drop npk_core_dalloc(curr);''')

        # Cache increment hit
        content = content.replace('''    atomic<int32>->:hit_ptr = entry_ptr->hit_counter;
    drop npk_shim_atomic_int32_fetch_add(@cast_unchecked<int64>(hit_ptr), 1i32, 0i32);''', '''    atomic<int32>:_hc = entry_ptr->hit_counter;
    drop _hc.fetch_add(1i32);
    entry_ptr->hit_counter = _hc;''')

        # Execute
        content = content.replace('''    atomic<int32>->:ref_count_ptr = entry_ptr->ref_count;
    int32:old_ref = npk_shim_atomic_int32_fetch_sub(@cast_unchecked<int64>(ref_count_ptr), 1i32, 0i32);''', '''    atomic<int32>:_rc = entry_ptr->ref_count;
    int32:old_ref = _rc.fetch_sub(1i32);
    entry_ptr->ref_count = _rc;''')

        content = content.replace('''        atomic<int32>->:hit_ptr = entry_ptr->hit_counter;
        drop npk_core_dalloc(@cast_unchecked<int64>(hit_ptr));
        drop npk_core_dalloc(@cast_unchecked<int64>(ref_count_ptr));
        drop npk_core_dalloc(entry);''', '''        drop npk_core_dalloc(entry);''')

    with open(filepath, 'w') as f:
        f.write(content)

