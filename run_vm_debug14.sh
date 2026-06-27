sed -i 's/if (ast_root == 0i64) {/if (ast_root == 0i64) {\npass MatchResult{matched: 125i32, start_idx: 0i32, end_idx: 0i32};\n}/g' src/nregx.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/nregx.npk
