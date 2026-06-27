import re

# 1. Update regex_types.npk
with open('src/regex_types.npk', 'r') as f:
    types = f.read()

types = types.replace('atomic<int32>: hit_counter;', 'int64: hit_counter;')
types = types.replace('atomic<int32>: ref_count;', 'int64: ref_count;')

with open('src/regex_types.npk', 'w') as f:
    f.write(types)

# 2. Update regex_cache.npk
with open('src/regex_cache.npk', 'r') as f:
    cache = f.read()

cache = cache.replace('extern func:npk_atomic_int32_exchange = int32(int64:ptr, int32:val, int32:order);',
                      'extern func:npk_atomic_int32_exchange = int32(int64:ptr, int32:val, int32:order);\nextern func:npk_atomic_int32_fetch_add = int32(int64:ptr, int32:val, int32:order);\nextern func:npk_atomic_int32_fetch_sub = int32(int64:ptr, int32:val, int32:order);')

# In regex_cache_get
cache = cache.replace('drop curr_ptr->ref_count.fetch_add(1i32);',
                      'drop npk_atomic_int32_fetch_add(curr_ptr->ref_count, 1i32, 5i32);')

# In regex_cache_free_entry
free_rep = """    int64:hc = entry_ptr->hit_counter;
    if (hc != 0i64) { drop npk_core_dalloc(hc); }
    int64:rc = entry_ptr->ref_count;
    if (rc != 0i64) { drop npk_core_dalloc(rc); }
    drop npk_core_dalloc(entry);"""
cache = cache.replace('drop npk_core_dalloc(entry);', free_rep)

# In regex_cache_decrement_ref
cache = cache.replace('int32:prev = entry_ptr->ref_count.fetch_sub(1i32);',
                      'int32:prev = npk_atomic_int32_fetch_sub(entry_ptr->ref_count, 1i32, 5i32);')

# In regex_cache_insert initialization
cache = cache.replace('entry_ptr->hit_counter = atomic_new(0i32);',
                      'entry_ptr->hit_counter = npk_atomic_int32_create(0i32);')
cache = cache.replace('entry_ptr->ref_count = atomic_new(2i32); // 1 for cache, 1 for caller',
                      'entry_ptr->ref_count = npk_atomic_int32_create(2i32); // 1 for cache, 1 for caller')

# In regex_cache_insert eviction
cache = cache.replace('int32:prev_ref = t_ptr->ref_count.fetch_sub(1i32);',
                      'int32:prev_ref = npk_atomic_int32_fetch_sub(t_ptr->ref_count, 1i32, 5i32);')

# In regex_cache_increment_hit
cache = cache.replace('drop entry_ptr->hit_counter.fetch_add(1i32);',
                      'drop npk_atomic_int32_fetch_add(entry_ptr->hit_counter, 1i32, 5i32);')

with open('src/regex_cache.npk', 'w') as f:
    f.write(cache)

