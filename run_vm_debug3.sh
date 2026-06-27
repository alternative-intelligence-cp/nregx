sed -i 's/int64:out1 = npk_mem_read_int64(state, 8i64);/int64:out1 = npk_mem_read_int64(state, 8i64);\npass MatchResult{matched: 111i32, start_idx: 0i32, end_idx: 0i32};/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
