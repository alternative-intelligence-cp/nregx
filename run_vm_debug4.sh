sed -i 's/if (c == (match_char => int64)) {/if (c == (match_char => int64)) {\nmatched = 111i32;\nrunning = 0i32;\nbreak;/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
