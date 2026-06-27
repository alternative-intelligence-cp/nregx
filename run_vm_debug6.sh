sed -i 's/pass match_res;/pass MatchResult{matched: 123i32, start_idx: 0i32, end_idx: 0i32};/g' src/nregx.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/nregx.npk
