sed -i 's/int32:old_ref = raw regex_cache_decrement_ref(entry);/int32:old_ref = 2i32;/g' src/nregx.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/nregx.npk
