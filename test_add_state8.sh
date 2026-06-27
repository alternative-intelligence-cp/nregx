sed -i 's/pass MatchResult{matched: ret => int32, start_idx: 0i32, end_idx: 0i32};/int64:start_state_idx = (start_state - arena_data) \/ 64i64;\npass MatchResult{matched: start_state_idx => int32, start_idx: 0i32, end_idx: 0i32};/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
