sed -i 's/int32:running = 1i32;/int32:running = 1i32;\npass MatchResult{matched: (start_state => int32), start_idx: 0i32, end_idx: 0i32};/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
