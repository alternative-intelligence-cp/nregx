import re

# 1. Fix regex_compiler.npk (AST Null Dereference + ReDoS)
with open('src/regex_compiler.npk', 'r') as f:
    code = f.read()

# Fix ReDoS: m > 1000 check
parse_rep_target = """if (valid == 1i32) {
                drop npk_mem_write_int32(idx_ptr, 0i64, i);"""
parse_rep_replace = """if (valid == 1i32) {
                if (m > 1000i32 || n > 1000i32) { fail ERR_REGEX_COMPLEXITY_EXCEEDED; }
                drop npk_mem_write_int32(idx_ptr, 0i64, i);"""
code = code.replace(parse_rep_target, parse_rep_replace)

# Fix AST Null Dereference
# Replace pass raw ast_arena_alloc_node(...)
def repl_pass(m):
    args = m.group(1)
    return f"int64:n = raw ast_arena_alloc_node({args});\n            if (n == 0i64) {{ fail ERR_REGEX_PARSE; }}\n            pass n;"
code = re.sub(r'pass raw ast_arena_alloc_node\((.*?)\);', repl_pass, code)

# Replace assignment: int64:var = raw ast_arena_alloc_node(...)
def repl_assign(m):
    indent = m.group(1)
    var = m.group(2)
    args = m.group(3)
    return f"{indent}int64:{var} = raw ast_arena_alloc_node({args});\n{indent}if ({var} == 0i64) {{ fail ERR_REGEX_PARSE; }}"
code = re.sub(r'([ \t]+)int64:([a-zA-Z0-9_]+)\s*=\s*raw ast_arena_alloc_node\((.*?)\);', repl_assign, code)

# Fix ast_clone internal allocation
clone_target = """    int64:new_node = raw ast_arena_alloc_node(arena_ptr, old_ptr->type, old_ptr->val);
    if (new_node == 0i64) { fail ERR_REGEX_PARSE; }"""
clone_replace = """    int64:new_node = raw ast_arena_alloc_node(arena_ptr, old_ptr->type, old_ptr->val);
    if (new_node == 0i64) { pass 0i64; }"""
code = code.replace(clone_target, clone_replace) # Fix ast_clone to return 0 instead of fail since it doesn't fail natively unless modified, wait, ast_clone implicitly returns Result if we add fail.
# Actually, ast_clone returning 0i64 on fail is better.

# Let's check ast_clone assignments:
def repl_clone(m):
    indent = m.group(1)
    var = m.group(2)
    args = m.group(3)
    return f"{indent}int64:{var} = ast_clone({args});\n{indent}if ({var} == 0i64) {{ fail ERR_REGEX_PARSE; }}"
# We have `new_ptr->left = ast_clone(l, arena_ptr);` -> need to be careful.
# Let's just do it manually for ast_clone calls.

with open('src/regex_compiler.npk', 'w') as f:
    f.write(code)

# 2. Fix nregx.npk (Crash on invalid regex)
with open('src/nregx.npk', 'r') as f:
    nregx = f.read()

nregx = nregx.replace('int64:start_state = raw compile_nfa(arena_ptr, ast_root);', 
                      'int64:start_state = compile_nfa(arena_ptr, ast_root) ? 0i64;\n    if (start_state == 0i64) {\n        drop regex_arena_destroy(arena_ptr);\n        fail ERR_REGEX_PARSE;\n    }')
with open('src/nregx.npk', 'w') as f:
    f.write(nregx)

