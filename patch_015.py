import re

# 1. ast_types.npk
with open('src/ast_types.npk', 'r') as f:
    ast_types = f.read()
ast_types = ast_types.replace(
    'pub fixed int32:AST_SAVE    = 11i32;',
    'pub fixed int32:AST_SAVE    = 11i32;\npub fixed int32:AST_EPSILON = 12i32;'
)
with open('src/ast_types.npk', 'w') as f:
    f.write(ast_types)

# 2. regex_compiler.npk
with open('src/regex_compiler.npk', 'r') as f:
    regex_compiler = f.read()

# Capture groups limit
cap_code = """        if (is_capture == 1i32) {
            cap = npk_mem_read_int32(idx_ptr, 4i64);
            drop npk_mem_write_int32(idx_ptr, 4i64, cap + 1i32);
        }"""
new_cap_code = """        if (is_capture == 1i32) {
            cap = npk_mem_read_int32(idx_ptr, 4i64);
            if (cap >= 10i32) { fail ERR_REGEX_COMPLEXITY_EXCEEDED; }
            drop npk_mem_write_int32(idx_ptr, 4i64, cap + 1i32);
        }"""
regex_compiler = regex_compiler.replace(cap_code, new_cap_code)

# Inverted char class explicit set
inv_code = """        if (inverted == 1i32) {
            int64:b0 = npk_mem_read_int64(c_node, 24i64);"""
new_inv_code = """        if (inverted == 1i32) {
            wild AstNode->:c_ptr = @cast_unchecked<AstNode->>(c_node);
            c_ptr->val = 1i32;
            int64:b0 = npk_mem_read_int64(c_node, 24i64);"""
regex_compiler = regex_compiler.replace(inv_code, new_inv_code)

# Empty repetition (EPSILON)
eps_code = """                if (m == 0i32 && n == 0i32) {
                    // Match empty string
                    node = raw ast_arena_alloc_node(arena_ptr,AST_LITERAL, 0i32); // actually we can just pass empty but let's do this
                }"""
new_eps_code = """                if (m == 0i32 && n == 0i32) {
                    // Match empty string
                    node = raw ast_arena_alloc_node(arena_ptr,AST_EPSILON, 0i32);
                }"""
regex_compiler = regex_compiler.replace(eps_code, new_eps_code)

with open('src/regex_compiler.npk', 'w') as f:
    f.write(regex_compiler)

# 3. nfa_compiler.npk
with open('src/nfa_compiler.npk', 'r') as f:
    nfa_compiler = f.read()

nfa_eps = """            } else if (type == AST_ANY) {"""
new_nfa_eps = """            } else if (type == AST_EPSILON) {
                int64:s = raw regex_arena_alloc(arena_ptr, OP_JMP, 0i32);
                if (s == 0i64) { fail ERR_REGEX_PARSE; }
                int64:e = raw regex_arena_alloc(arena_ptr, OP_MATCH, 0i32);
                if (e == 0i64) { fail ERR_REGEX_PARSE; }
                wild NfaState->:s_ptr = @cast_unchecked<NfaState->>(s);
                s_ptr->out1 = e;
                drop alpush(frag_stack, s);
                drop alpush(frag_stack, e);
                frag_stack_size = frag_stack_size + 1i32;
            } else if (type == AST_ANY) {"""
nfa_compiler = nfa_compiler.replace(nfa_eps, new_nfa_eps)
with open('src/nfa_compiler.npk', 'w') as f:
    f.write(nfa_compiler)

# 4. regex_cache.npk
with open('src/regex_cache.npk', 'r') as f:
    regex_cache = f.read()

cache_insert_code = """    when (locked == 0i32) {
        
        int64:new_entry = npk_core_alloc(80i64);
        if (new_entry == 0i64) {
            // Drop lock
            drop npk_atomic_int32_set(global_cache_lock, 0i32);
            pass 0i64;
        }
        
        int64:ref_count_ptr = npk_atomic_int32_create(1i32);
        if (ref_count_ptr == 0i64) {
            drop npk_core_dalloc(new_entry);
            drop npk_atomic_int32_set(global_cache_lock, 0i32);
            pass 0i64;
        }"""
new_cache_insert_code = """    int64:new_entry = npk_core_alloc(80i64);
    if (new_entry == 0i64) { pass 0i64; }
    int64:ref_count_ptr = npk_atomic_int32_create(1i32);
    if (ref_count_ptr == 0i64) {
        drop npk_core_dalloc(new_entry);
        pass 0i64;
    }
    
    when (locked == 0i32) {
        """
regex_cache = regex_cache.replace(cache_insert_code, new_cache_insert_code)

timeout_code = """        if (spin_count > 100000i32) {
            // Spinlock timeout
            pass 0i64;
        }"""
new_timeout_code = """        if (spin_count > 100000i32) {
            // Spinlock timeout
            drop npk_core_dalloc(new_entry);
            drop npk_core_dalloc(ref_count_ptr); // assuming create uses alloc
            pass 0i64;
        }"""
regex_cache = regex_cache.replace(timeout_code, new_timeout_code)

with open('src/regex_cache.npk', 'w') as f:
    f.write(regex_cache)

# 5. prefix_extractor.npk
with open('src/prefix_extractor.npk', 'r') as f:
    prefix_ext = f.read()

prefix_code = """    int64:ext = npk_core_alloc(24i64);
    defer { drop npk_core_dalloc(ext); }
    
    int64:str_buf = npk_core_alloc(100i64);"""
new_prefix_code = """    int64:ext = npk_core_alloc(24i64);
    if (ext == 0i64) { pass 0i64; }
    defer { drop npk_core_dalloc(ext); }
    
    int64:str_buf = npk_core_alloc(100i64);
    if (str_buf == 0i64) { pass 0i64; }"""
prefix_ext = prefix_ext.replace(prefix_code, new_prefix_code)

with open('src/prefix_extractor.npk', 'w') as f:
    f.write(prefix_ext)

print("Patching complete.")
