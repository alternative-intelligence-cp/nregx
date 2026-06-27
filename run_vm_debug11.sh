sed -i 's/int64:pos = raw npk_mem_find_substr(text, text_len, prefix_str, prefix_len => int64);/int64:pos = raw npk_mem_find_substr(text, text_len, prefix_str, prefix_len => int64);\npass MatchResult{matched: 199i32, start_idx: (pos => int32), end_idx: 0i32};/g' src/nregx.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/nregx.npk
