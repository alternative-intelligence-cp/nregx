sed -i 's/drop add_state(start_state, clist_ah, visit_gen, visited_arr, arena_data, work_ah, 0i64, text_len, 0i64);/int64:ret = raw add_state(start_state, clist_ah, visit_gen, visited_arr, arena_data, work_ah, 0i64, text_len, 0i64);\npass MatchResult{matched: ret => int32, start_idx: 0i32, end_idx: 0i32};/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
