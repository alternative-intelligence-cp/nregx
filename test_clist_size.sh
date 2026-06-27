sed -i 's/int64:idx = 0i64;/int64:idx = 0i64;\npass MatchResult{matched: raw asize_list(clist_ah) => int32, start_idx: 0i32, end_idx: 0i32};/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
