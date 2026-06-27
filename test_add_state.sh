sed -i 's/drop(apush_list(list_ah, state, state_start_idx));/drop(apush_list(list_ah, state, state_start_idx));\nexit 77i32;/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
