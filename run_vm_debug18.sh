sed -i 's/if (matched == 1i32) {/pass MatchResult{matched: 133i32, start_idx: 0i32, end_idx: 0i32};\nif (matched == 1i32) {/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
