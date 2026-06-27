with open('tests/test_basic.npk', 'r') as f:
    content = f.read()
content = content.replace('drop(assert_match(pattern, plen, "ab", 2i64, 1i32));', 'drop(assert_match(pattern, plen, string_to_cstr("ab"), 2i64, 1i32));')
content = content.replace('drop(assert_match(pattern, plen, "ac", 2i64, 1i32));', 'drop(assert_match(pattern, plen, string_to_cstr("ac"), 2i64, 1i32));')
content = content.replace('drop(assert_match(pattern, plen, "abc", 3i64, 1i32));', 'drop(assert_match(pattern, plen, string_to_cstr("abc"), 3i64, 1i32));')
content = content.replace('drop(assert_match(pattern, plen, "abcd", 4i64, 1i32));', 'drop(assert_match(pattern, plen, string_to_cstr("abcd"), 4i64, 1i32));')
content = content.replace('drop(assert_match(pattern, plen, "ad", 2i64, 0i32));', 'drop(assert_match(pattern, plen, string_to_cstr("ad"), 2i64, 0i32));')
content = content.replace('drop(assert_match(pattern, plen, "a", 1i64, 0i32));', 'drop(assert_match(pattern, plen, string_to_cstr("a"), 1i64, 0i32));')
content = content.replace('drop(assert_match(pattern, plen, "acbccd", 6i64, 1i32));', 'drop(assert_match(pattern, plen, string_to_cstr("acbccd"), 6i64, 1i32));')
content = content.replace('exit(1i32);', 'npk_sys_exit(1i32);')
content = content.replace('exit(0i32);', 'npk_sys_exit(0i32);')
with open('tests/test_basic.npk', 'w') as f:
    f.write(content)
