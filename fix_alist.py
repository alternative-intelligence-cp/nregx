import re

# 1. Update nfa_compiler.npk to use alist
with open('src/nfa_compiler.npk', 'r') as f:
    nfa = f.read()

nfa = nfa.replace('int64:trav_stack = npk_core_alloc(16384i64);', 'int64:trav_stack = alist();')
nfa = nfa.replace('int64:frag_stack = npk_core_alloc(8192i64);', 'int64:frag_stack = alist();')
nfa = nfa.replace('defer { drop npk_core_dalloc(trav_stack); drop npk_core_dalloc(frag_stack); } // 4096 * 2 * 8 bytes', '')

# Replace frag_stack push
def repl_frag_push(m):
    indent = m.group(1)
    s = m.group(2)
    e = m.group(3)
    # The original also increments frag_stack_size, we just replace the writes.
    return f"{indent}drop alpush(frag_stack, {s});\n{indent}drop alpush(frag_stack, {e});"
nfa = re.sub(r'([ \t]+)int64:idx[a-zA-Z0-9_]*\s*=\s*\(frag_stack_size.*?;\n\1drop npk_mem_write_int64\(frag_stack,\s*[^,]+,\s*([^)]+)\);\n\1drop npk_mem_write_int64\(frag_stack,\s*[^,]+,\s*([^)]+)\);', repl_frag_push, nfa)

# Replace frag_stack pop
def repl_frag_pop(m):
    indent = m.group(1)
    pop_count = m.group(2) # e.g. "1" or "2"
    # We need to manually rewrite the pops because the regex might be brittle.
    pass

# It's better to replace the specific blocks manually.
# Let's do it using simple string replacement for the pop blocks.
pop1 = """                int64:idx1 = ((frag_stack_size - 1i32) => int64) * 16i64;
                int64:f1_s = npk_mem_read_int64(frag_stack, idx1);
                int64:f1_e = npk_mem_read_int64(frag_stack, idx1 + 8i64);
                frag_stack_size = frag_stack_size - 1i32;"""
pop1_rep = """                int64:f1_e = alpop(frag_stack);
                int64:f1_s = alpop(frag_stack);
                frag_stack_size = frag_stack_size - 1i32;"""
nfa = nfa.replace(pop1, pop1_rep)

pop2 = """                int64:idx2 = ((frag_stack_size - 1i32) => int64) * 16i64;
                int64:f2_s = npk_mem_read_int64(frag_stack, idx2);
                int64:f2_e = npk_mem_read_int64(frag_stack, idx2 + 8i64);
                int64:idx1 = ((frag_stack_size - 2i32) => int64) * 16i64;
                int64:f1_s = npk_mem_read_int64(frag_stack, idx1);
                int64:f1_e = npk_mem_read_int64(frag_stack, idx1 + 8i64);
                frag_stack_size = frag_stack_size - 2i32;"""
pop2_rep = """                int64:f2_e = alpop(frag_stack);
                int64:f2_s = alpop(frag_stack);
                int64:f1_e = alpop(frag_stack);
                int64:f1_s = alpop(frag_stack);
                frag_stack_size = frag_stack_size - 2i32;"""
nfa = nfa.replace(pop2, pop2_rep)

pop_final = """    int64:idx_final = 0i64;
    int64:final_s = npk_mem_read_int64(frag_stack, idx_final);
    int64:final_e = npk_mem_read_int64(frag_stack, idx_final + 8i64);"""
pop_final_rep = """    int64:final_e = alpop(frag_stack);
    int64:final_s = alpop(frag_stack);"""
nfa = nfa.replace(pop_final, pop_final_rep)

pop_save = """                int64:idx = ((frag_stack_size - 1i32) => int64) * 16i64;
                int64:f_s = npk_mem_read_int64(frag_stack, idx);
                int64:f_e = npk_mem_read_int64(frag_stack, idx + 8i64);
                frag_stack_size = frag_stack_size - 1i32;"""
pop_save_rep = """                int64:f_e = alpop(frag_stack);
                int64:f_s = alpop(frag_stack);
                frag_stack_size = frag_stack_size - 1i32;"""
nfa = nfa.replace(pop_save, pop_save_rep)

# trav_stack
nfa = nfa.replace("drop(npk_mem_write_int64(trav_stack, (trav_stack_size => int64) * 8i64, ast_root));", "drop alpush(trav_stack, ast_root);")
nfa = nfa.replace("drop(npk_mem_write_int64(trav_stack, ((trav_stack_size + 1i32) => int64) * 8i64, 0i64));", "drop alpush(trav_stack, 0i64);")

nfa = nfa.replace("drop(npk_mem_write_int64(trav_stack, (trav_stack_size => int64) * 8i64, node));", "drop alpush(trav_stack, node);")
nfa = nfa.replace("drop(npk_mem_write_int64(trav_stack, ((trav_stack_size + 1i32) => int64) * 8i64, 1i64));", "drop alpush(trav_stack, 1i64);")
nfa = nfa.replace("drop(npk_mem_write_int64(trav_stack, ((trav_stack_size + 1i32) => int64) * 8i64, 2i64));", "drop alpush(trav_stack, 2i64);")

nfa = nfa.replace("drop(npk_mem_write_int64(trav_stack, (trav_stack_size => int64) * 8i64, left));", "drop alpush(trav_stack, left);")
nfa = nfa.replace("drop(npk_mem_write_int64(trav_stack, (trav_stack_size => int64) * 8i64, right));", "drop alpush(trav_stack, right);")

trav_pop = """        int64:state = npk_mem_read_int64(trav_stack, ((trav_stack_size - 1i32) => int64) * 8i64);
        int64:node = npk_mem_read_int64(trav_stack, ((trav_stack_size - 2i32) => int64) * 8i64);"""
trav_pop_rep = """        int64:state = alpop(trav_stack);
        int64:node = alpop(trav_stack);"""
nfa = nfa.replace(trav_pop, trav_pop_rep)

with open('src/nfa_compiler.npk', 'w') as f:
    f.write(nfa)


# 2. prefix_extractor.npk
with open('src/prefix_extractor.npk', 'r') as f:
    pref = f.read()

pref = pref.replace('int64:trav_stack = npk_core_alloc(8192i64);', 'int64:trav_stack = alist();')
pref = pref.replace('defer { drop npk_core_dalloc(trav_stack); }', '')
pref = pref.replace('drop(npk_mem_write_int64(trav_stack, (stack_size => int64) * 8i64, curr));', 'drop alpush(trav_stack, curr);')

pref = pref.replace('curr = npk_mem_read_int64(trav_stack, ((stack_size - 1i32) => int64) * 8i64);', 'curr = alpop(trav_stack);')

with open('src/prefix_extractor.npk', 'w') as f:
    f.write(pref)

# 3. Finish regex_compiler.npk
with open('src/regex_compiler.npk', 'r') as f:
    regc = f.read()

regc = regc.replace('new_ptr->left = ast_clone(l, arena_ptr);', 'int64:ll = ast_clone(l, arena_ptr);\n        if (ll == 0i64) { fail ERR_REGEX_PARSE; }\n        new_ptr->left = ll;')
regc = regc.replace('new_ptr->right = ast_clone(r, arena_ptr);', 'int64:rr = ast_clone(r, arena_ptr);\n        if (rr == 0i64) { fail ERR_REGEX_PARSE; }\n        new_ptr->right = rr;')

def repl_clone_if(m):
    indent = m.group(1)
    cond = m.group(2)
    var = m.group(3)
    base = m.group(4)
    return f"{indent}if ({cond}) {{\n{indent}    {var} = ast_clone({base}, arena_ptr);\n{indent}    if ({var} == 0i64) {{ fail ERR_REGEX_PARSE; }}\n{indent}}}"

regc = re.sub(r'([ \t]+)if \((.*?)\) \{ ([a-zA-Z0-9_]+) = ast_clone\((.*?)\); \}', repl_clone_if, regc)

with open('src/regex_compiler.npk', 'w') as f:
    f.write(regc)

