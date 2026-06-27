sed -i 's/if (lex_res == 0i32) {/if (lex_res == 0i32) { exit 11i32; } if (0i32 == 1i32) {/g' src/nregx.npk
sed -i 's/if (ast_root == 0i64) {/if (ast_root == 0i64) { exit 12i32; } if (0i32 == 1i32) {/g' src/nregx.npk
sed -i 's/if (arena_ptr == 0i64) {/if (arena_ptr == 0i64) { exit 13i32; } if (0i32 == 1i32) {/g' src/nregx.npk
sed -i 's/if (start_state == 0i64) {/if (start_state == 0i64) { exit 14i32; } if (0i32 == 1i32) {/g' src/nregx.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/nregx.npk
