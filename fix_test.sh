sed -i 's/int64:pattern = "a(b|c)+d?";/string:pattern_str = "a(b|c)+d?";\n    int64:pattern = string_to_cstr(pattern_str);/g' tests/test_basic.npk
sed -i 's/int32:res = nregx_match/MatchResult:res_struct = raw nregx_match/g' tests/test_basic.npk
sed -i 's/if (res != expect)/int32:res = res_struct.matched;\n    if (res != expect)/g' tests/test_basic.npk
