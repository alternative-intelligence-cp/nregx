import re

with open('src/regex_cache.npk', 'r') as f:
    cache = f.read()

# 1. Spinlock Increments (CONC-RACE-001)
inc1 = """                atomic<int32>:_ref = curr_ptr->ref_count;
                drop _ref.fetch_add(1i32);
                curr_ptr->ref_count = _ref;"""
inc1_rep = "                drop curr_ptr->ref_count.fetch_add(1i32);"
cache = cache.replace(inc1, inc1_rep)

dec1 = """    atomic<int32>:_ref = entry_ptr->ref_count;
    int32:prev = _ref.fetch_sub(1i32);
    entry_ptr->ref_count = _ref;"""
dec1_rep = """    int32:prev = entry_ptr->ref_count.fetch_sub(1i32);"""
cache = cache.replace(dec1, dec1_rep)

dec2 = """            atomic<int32>:_ref = t_ptr->ref_count;
            int32:prev_ref = _ref.fetch_sub(1i32);
            t_ptr->ref_count = _ref;"""
dec2_rep = """            int32:prev_ref = t_ptr->ref_count.fetch_sub(1i32);"""
cache = cache.replace(dec2, dec2_rep)

hit1 = """    atomic<int32>:_hc = entry_ptr->hit_counter;
    drop _hc.fetch_add(1i32);
    entry_ptr->hit_counter = _hc;"""
hit1_rep = """    drop entry_ptr->hit_counter.fetch_add(1i32);"""
cache = cache.replace(hit1, hit1_rep)

# 2. Timeout Cleanup (CONC-LEAK-002) & O(N) String Comparison (PERF-SPIN-003)
# We will rewrite strings_equal
strings_eq_orig = """func:strings_equal = int32(int64:str1, int64:len1, int64:str2, int64:len2) {
    if (len1 != len2) { pass 0i32; }
    int64:i = 0i64;
    int32:match = 1i32;
    when (i < len1) {
        int64:c1 = npk_mem_read_byte(str1, i);
        int64:c2 = npk_mem_read_byte(str2, i);
        if (c1 != c2) {
            match = 0i32;
            i = len1; // break
        } else {
            i = i + 1i64;
        }
    }
    pass match;
};"""
strings_eq_rep = """func:strings_equal = int32(int64:str1, int64:len1, int64:str2, int64:len2) {
    if (len1 != len2) { pass 0i32; }
    if (len1 == 0i64) { pass 1i32; }
    int64:cmp = npk_mem_compare(str1, str2, len1);
    if (cmp == 0i64) { pass 1i32; }
    pass 0i32;
};"""
cache = cache.replace(strings_eq_orig, strings_eq_rep)

# Move string allocation in regex_cache_insert
insert_orig = """    // Acquire lock
    int64:lock = cache->lock;
    int32:locked = 0i32;
    int32:spins = 0i32;
    when (locked == 0i32) {
        spins = spins + 1i32;
        if (spins > 1000i32) {
            pass 0i64; // Sentinel for spinlock in insert
        } else {
            int32:old = npk_atomic_int32_exchange(lock, 1i32, 5i32);
            if (old == 0i32) { locked = 1i32; }
        }
    }
    
    int64:sz = cache->size;
    int64:entry = npk_core_alloc(80i64);
    if (entry == 0i64) { 
        drop npk_atomic_int32_exchange(lock, 0i32, 5i32);
        pass 0i64; 
    }
    
    // Copy the string
    int64:p_copy = npk_core_alloc(pattern_len);
    if (p_copy == 0i64) { 
        drop npk_core_dalloc(entry);
        drop npk_atomic_int32_exchange(lock, 0i32, 5i32);
        pass 0i64; 
    }
    
    int64:i = 0i64;
    when (i < pattern_len) {
        int64:c = npk_mem_read_byte(pattern, i);
        drop npk_mem_write_byte(p_copy, i, c);
        i = i + 1i64;
    }"""
    
insert_rep = """    // Copy the string
    int64:p_copy = 0i64;
    if (pattern_len > 0i64) {
        p_copy = npk_core_alloc(pattern_len);
        if (p_copy == 0i64) { 
            if (arena_ptr != 0i64) { drop regex_arena_destroy(arena_ptr); }
            if (prefix_ptr != 0i64) { drop npk_core_dalloc(prefix_ptr); }
            pass 0i64; 
        }
        int64:i = 0i64;
        when (i < pattern_len) {
            int64:c = npk_mem_read_byte(pattern, i);
            drop npk_mem_write_byte(p_copy, i, c);
            i = i + 1i64;
        }
    }
    
    // Acquire lock
    int64:lock = cache->lock;
    int32:locked = 0i32;
    int32:spins = 0i32;
    when (locked == 0i32) {
        spins = spins + 1i32;
        if (spins > 1000i32) {
            if (p_copy != 0i64) { drop npk_core_dalloc(p_copy); }
            if (arena_ptr != 0i64) { drop regex_arena_destroy(arena_ptr); }
            if (prefix_ptr != 0i64) { drop npk_core_dalloc(prefix_ptr); }
            pass 0i64; // Sentinel for spinlock in insert
        } else {
            int32:old = npk_atomic_int32_exchange(lock, 1i32, 5i32);
            if (old == 0i32) { locked = 1i32; }
        }
    }
    
    int64:sz = cache->size;
    int64:entry = npk_core_alloc(80i64);
    if (entry == 0i64) { 
        drop npk_atomic_int32_exchange(lock, 0i32, 5i32);
        if (p_copy != 0i64) { drop npk_core_dalloc(p_copy); }
        if (arena_ptr != 0i64) { drop regex_arena_destroy(arena_ptr); }
        if (prefix_ptr != 0i64) { drop npk_core_dalloc(prefix_ptr); }
        pass 0i64; 
    }"""
cache = cache.replace(insert_orig, insert_rep)

with open('src/regex_cache.npk', 'w') as f:
    f.write(cache)

