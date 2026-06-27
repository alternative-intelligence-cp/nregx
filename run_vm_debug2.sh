sed -i 's/int64:byte_idx = c \/ 8i64;/int64:byte_idx = c \/ 8i64;\npass MatchResult{matched: 111i32, start_idx: 0i32, end_idx: 0i32};/g' src/regex_vm.npk
npkc -I src src/test.npk -o test_bin && ./test_bin; echo $?
git restore src/regex_vm.npk
