sed -i '/extern "nitpick_libc_sys" { func:npk_core_alloc/d' src/nfa_compiler.npk
sed -i 's/int64:frag_stack = npk_core_alloc(8192i64);/int64:frag_stack = npk_core_alloc(8192i64);\n    defer { drop npk_core_dalloc(trav_stack); drop npk_core_dalloc(frag_stack); }/g' src/nfa_compiler.npk
