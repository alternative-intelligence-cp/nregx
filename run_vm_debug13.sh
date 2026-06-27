sed -i 's/if (start_state == 0i64) {/if (start_state == 0i64) {\npass MatchResult{matched: 124i32, start_idx: 0i32, end_idx: 0i32};\n}/g' src/nregx.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/nregx.npk
