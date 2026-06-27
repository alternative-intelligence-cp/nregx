sed -i 's/int64:entry = raw compile_and_cache(pattern, pattern_len);/int64:entry = raw compile_and_cache(pattern, pattern_len);\nif (entry == 0i64) { pass MatchResult{matched: 122i32, start_idx: 0i32, end_idx: 0i32}; }/g' src/nregx.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/nregx.npk
