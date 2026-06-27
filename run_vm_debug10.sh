sed -i 's/int32:match_char = npk_mem_read_int32(state, 4i64);/int32:match_char = npk_mem_read_int32(state, 4i64);\npass MatchResult{matched: (c => int32), start_idx: 0i32, end_idx: 0i32};/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
