sed -i 's/int64:ext = raw extract_literal_prefix(ast_root);/int64:ext = raw extract_literal_prefix(ast_root);\npass MatchResult{matched: 101i32, start_idx: (ext => int32), end_idx: 0i32};/g' src/nregx.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/nregx.npk
