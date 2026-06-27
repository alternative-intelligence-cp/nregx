sed -i 's/exit 1i32;/npk_sys_exit(1i32);/g' tests/test_basic.npk
sed -i 's/pub func:failsafe = int32(tbb32:err) {/pub func:failsafe = int32(tbb32:err) {\n    drop err;\n    exit 1i32;\n}/g' tests/test_basic.npk
# Wait, let me just regenerate tests/test_basic.npk
cat << 'TEST' > tests/test_basic.npk
use "../src/nregx.npk".*;

extern "nitpick_libc_sys" {
    func:npk_sys_exit = void(int32:code);
}

func:assert_match = int32(int64:pattern, int64:plen, int64:text, int64:tlen, int32:expect) {
    MatchResult:res_struct = raw nregx_match(pattern, plen, text, tlen);
    int32:res = res_struct.matched;
    if (res != expect) {
        npk_sys_exit(1i32);
    }
    pass(0i32);
};

pub func:main = int32() {
    drop(nregx_init());

    // Pattern: a(b|c)+d?
    string:pattern_str = "a(b|c)+d?";
    int64:pattern = string_to_cstr(pattern_str);
    int64:plen = 9i64;

    drop(assert_match(pattern, plen, string_to_cstr("ab"), 2i64, 1i32));
    drop(assert_match(pattern, plen, string_to_cstr("ac"), 2i64, 1i32));
    drop(assert_match(pattern, plen, string_to_cstr("abc"), 3i64, 1i32));
    drop(assert_match(pattern, plen, string_to_cstr("abcd"), 4i64, 1i32));
    drop(assert_match(pattern, plen, string_to_cstr("ad"), 2i64, 0i32)); // + requires at least one b or c
    drop(assert_match(pattern, plen, string_to_cstr("a"), 1i64, 0i32));
    drop(assert_match(pattern, plen, string_to_cstr("acbccd"), 6i64, 1i32));

    exit 0i32;
};

pub func:failsafe = int32(tbb32:err) {
    drop err;
    exit 1i32;
};
TEST
