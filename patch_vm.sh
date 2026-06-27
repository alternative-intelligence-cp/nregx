sed -i 's/int64:capacity = npk_mem_read_int64(arena_ptr, 8i64);/int64:capacity = npk_mem_read_int64(arena_ptr, 8i64);\n    int64:batch_mem = npk_core_alloc(capacity * 16i64 * 3i64 + 24i64 + capacity * 8i64);\n    defer { drop npk_core_dalloc(batch_mem); };/g' src/regex_vm.npk
sed -i 's/int64:clist_ah = npk_tlc_batch_alloc(capacity \* 16i64 + 8i64);/int64:clist_ah = batch_mem;/g' src/regex_vm.npk
sed -i 's/int64:nlist_ah = npk_tlc_batch_alloc(capacity \* 16i64 + 8i64);/int64:nlist_ah = batch_mem + capacity * 16i64 + 8i64;/g' src/regex_vm.npk
sed -i 's/int64:work_ah = npk_tlc_batch_alloc(capacity \* 16i64 + 8i64);/int64:work_ah = batch_mem + capacity * 32i64 + 16i64;/g' src/regex_vm.npk
sed -i 's/int64:visited_arr = npk_tlc_batch_alloc(capacity \* 8i64);/int64:visited_arr = batch_mem + capacity * 48i64 + 24i64;/g' src/regex_vm.npk
