sed -i 's/int64:byte_idx = c \/ 8i64;/int64:byte_idx = c \/ 8i64;\nexit 111i32;/g' src/regex_vm.npk
npkc -I src src/test.npk -o test_bin && ./test_bin; echo $?
git restore src/regex_vm.npk
