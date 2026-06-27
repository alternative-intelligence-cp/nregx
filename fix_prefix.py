with open('src/prefix_extractor.npk', 'r') as f:
    code = f.read()

pass1_orig = """                if (type == AST_LITERAL) {
                    literal_count = literal_count + 1i32;
                } else if ((type == AST_CONCAT) || (type == AST_SAVE) || (type == AST_ASSERT_START)) {"""
pass1_new = """                if (type == AST_LITERAL) {
                    int32:val = npk_mem_read_int32(curr, 4i64);
                    int64:v = val => int64;
                    if (v <= 127i64) {
                        literal_count = literal_count + 1i32;
                    } else if (v <= 2047i64) {
                        literal_count = literal_count + 2i32;
                    } else if (v <= 65535i64) {
                        literal_count = literal_count + 3i32;
                    } else {
                        literal_count = literal_count + 4i32;
                    }
                } else if ((type == AST_CONCAT) || (type == AST_SAVE) || (type == AST_ASSERT_START)) {"""

pass2_orig = """                    if (type == AST_LITERAL) {
                        int32:val = npk_mem_read_int32(curr, 4i64);
                        drop npk_mem_write_byte(str_buf, c_idx, val => int64);
                        c_idx = c_idx + 1i64;
                    } else if ((type == AST_CONCAT) || (type == AST_SAVE) || (type == AST_ASSERT_START)) {"""
pass2_new = """                    if (type == AST_LITERAL) {
                        int32:val = npk_mem_read_int32(curr, 4i64);
                        int64:v = val => int64;
                        if (v <= 127i64) {
                            drop npk_mem_write_byte(str_buf, c_idx, v);
                            c_idx = c_idx + 1i64;
                        } else if (v <= 2047i64) {
                            drop npk_mem_write_byte(str_buf, c_idx, (192i64 | ((v >> 6i64) & 31i64)));
                            drop npk_mem_write_byte(str_buf, c_idx + 1i64, (128i64 | (v & 63i64)));
                            c_idx = c_idx + 2i64;
                        } else if (v <= 65535i64) {
                            drop npk_mem_write_byte(str_buf, c_idx, (224i64 | ((v >> 12i64) & 15i64)));
                            drop npk_mem_write_byte(str_buf, c_idx + 1i64, (128i64 | ((v >> 6i64) & 63i64)));
                            drop npk_mem_write_byte(str_buf, c_idx + 2i64, (128i64 | (v & 63i64)));
                            c_idx = c_idx + 3i64;
                        } else {
                            drop npk_mem_write_byte(str_buf, c_idx, (240i64 | ((v >> 18i64) & 7i64)));
                            drop npk_mem_write_byte(str_buf, c_idx + 1i64, (128i64 | ((v >> 12i64) & 63i64)));
                            drop npk_mem_write_byte(str_buf, c_idx + 2i64, (128i64 | ((v >> 6i64) & 63i64)));
                            drop npk_mem_write_byte(str_buf, c_idx + 3i64, (128i64 | (v & 63i64)));
                            c_idx = c_idx + 4i64;
                        }
                    } else if ((type == AST_CONCAT) || (type == AST_SAVE) || (type == AST_ASSERT_START)) {"""

code = code.replace(pass1_orig, pass1_new)
code = code.replace(pass2_orig, pass2_new)

with open('src/prefix_extractor.npk', 'w') as f:
    f.write(code)

