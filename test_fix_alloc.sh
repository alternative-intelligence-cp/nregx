sed -i 's/npk_tlc_batch_alloc/npk_core_alloc/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
