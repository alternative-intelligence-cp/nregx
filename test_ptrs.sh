sed -i 's/int64:idx = 0i64;/int64:idx = 0i64;\nif (clist_ah == work_ah) { pass MatchResult{matched: 123i32, start_idx: 0i32, end_idx: 0i32}; }\n/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
