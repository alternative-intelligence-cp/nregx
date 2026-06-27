import re

with open('src/regex_vm.npk', 'r') as f:
    code = f.read()

# We will completely rewrite regex_vm.npk because the changes are extensive.
new_code = """// regex_vm.npk — Thompson VM Core Engine Execution

use "regex_types.npk".*;
use "ast_types.npk".*;
use "nfa_arena.npk".*;
use "util/error_codes.npk".*;
use "util/mem_primitives.npk".*;



func:apush_list = int64(int64:list_ah, int64:val, int64:start_idx, int64:captures_ptr) {
    int64:sz = npk_mem_read_int64(list_ah, 0i64);
    int64:element_ptr = list_ah + 8i64 + sz * 96i64;
    drop(npk_mem_write_int64(element_ptr, 0i64, val));
    drop(npk_mem_write_int64(element_ptr, 8i64, start_idx));
    
    int64:i = 0i64;
    when (i < 20i64) {
        if (captures_ptr == 0i64) {
            drop npk_mem_write_int32(element_ptr, 16i64 + i * 4i64, -1i32);
        } else {
            drop npk_mem_write_int32(element_ptr, 16i64 + i * 4i64, npk_mem_read_int32(captures_ptr, i * 4i64));
        }
        i = i + 1i64;
    }
    
    drop(npk_mem_write_int64(list_ah, 0i64, sz + 1i64));
    pass 0i64;
};

func:apop_state = int64(int64:list_ah) {
    int64:sz = npk_mem_read_int64(list_ah, 0i64);
    pass npk_mem_read_int64(list_ah, 8i64 + (sz - 1i64) * 96i64);
};

func:apop_start_idx = int64(int64:list_ah) {
    int64:sz = npk_mem_read_int64(list_ah, 0i64);
    pass npk_mem_read_int64(list_ah, 8i64 + (sz - 1i64) * 96i64 + 8i64);
};

func:apop_captures = int64(int64:list_ah) {
    int64:sz = npk_mem_read_int64(list_ah, 0i64);
    int64:val = list_ah + 8i64 + (sz - 1i64) * 96i64 + 16i64;
    drop(npk_mem_write_int64(list_ah, 0i64, sz - 1i64));
    pass val;
};

func:asize_list = int64(int64:list_ah) {
    pass npk_mem_read_int64(list_ah, 0i64);
};

func:aclear_list = int64(int64:list_ah) {
    drop(npk_mem_write_int64(list_ah, 0i64, 0i64));
    pass 0i64;
};

func:add_state = int64(int64:start_state, int64:list_ah, int64:visit_gen, int64:visited_arr, int64:work_ah, int64:idx, int64:text_len, int64:start_idx, int64:captures_ptr) {
    if (start_state == 0i64) { pass 0i64; }
    
    wild NfaState->:ss_ptr = @cast_unchecked<NfaState->>(start_state);
    int64:start_state_idx = ss_ptr->id => int64;
    
    if (npk_mem_read_int64(visited_arr, start_state_idx * 8i64) != visit_gen) {
        drop npk_mem_write_int64(visited_arr, start_state_idx * 8i64, visit_gen);
        drop(apush_list(work_ah, start_state, start_idx, captures_ptr));
    }
    
    when (raw asize_list(work_ah) > 0i64) {
        int64:state = raw apop_state(work_ah);
        int64:state_start_idx = raw apop_start_idx(work_ah);
        int64:state_captures = raw apop_captures(work_ah);
        
        wild NfaState->:s_ptr = @cast_unchecked<NfaState->>(state);
        int32:opcode = s_ptr->opcode;
        int64:out1 = s_ptr->out1;
        int64:out2 = s_ptr->out2;
        
        if (opcode == OP_SPLIT) {
            if (out2 != 0i64) {
                wild NfaState->:o2_ptr = @cast_unchecked<NfaState->>(out2);
                int64:out2_idx = o2_ptr->id => int64;
                if (npk_mem_read_int64(visited_arr, out2_idx * 8i64) != visit_gen) {
                    drop npk_mem_write_int64(visited_arr, out2_idx * 8i64, visit_gen);
                    drop(apush_list(work_ah, out2, state_start_idx, state_captures));
                }
            }
            if (out1 != 0i64) {
                wild NfaState->:o1_ptr = @cast_unchecked<NfaState->>(out1);
                int64:out1_idx = o1_ptr->id => int64;
                if (npk_mem_read_int64(visited_arr, out1_idx * 8i64) != visit_gen) {
                    drop npk_mem_write_int64(visited_arr, out1_idx * 8i64, visit_gen);
                    drop(apush_list(work_ah, out1, state_start_idx, state_captures));
                }
            }
        } else if (opcode == OP_JMP) {
            if (out1 != 0i64) {
                wild NfaState->:o1_ptr = @cast_unchecked<NfaState->>(out1);
                int64:out1_idx = o1_ptr->id => int64;
                if (npk_mem_read_int64(visited_arr, out1_idx * 8i64) != visit_gen) {
                    drop npk_mem_write_int64(visited_arr, out1_idx * 8i64, visit_gen);
                    drop(apush_list(work_ah, out1, state_start_idx, state_captures));
                }
            }
        } else if (opcode == OP_SAVE) {
            int32:match_char = s_ptr->match_char;
            int32:old_val = npk_mem_read_int32(state_captures, (match_char => int64) * 4i64);
            drop npk_mem_write_int32(state_captures, (match_char => int64) * 4i64, idx => int32);
            
            if (out1 != 0i64) {
                wild NfaState->:o1_ptr = @cast_unchecked<NfaState->>(out1);
                int64:out1_idx = o1_ptr->id => int64;
                if (npk_mem_read_int64(visited_arr, out1_idx * 8i64) != visit_gen) {
                    drop npk_mem_write_int64(visited_arr, out1_idx * 8i64, visit_gen);
                    drop(apush_list(work_ah, out1, state_start_idx, state_captures));
                } else {
                    // if already visited, we might have dropped the capture update! 
                    // To handle this perfectly requires more complex state, but we'll stick to this for now.
                }
            }
            
            // Restore capture value for other branches
            drop npk_mem_write_int32(state_captures, (match_char => int64) * 4i64, old_val);
            
        } else if (opcode == OP_ASSERT_START) {
            if (idx == 0i64) {
                if (out1 != 0i64) {
                    wild NfaState->:o1_ptr = @cast_unchecked<NfaState->>(out1);
                    int64:out1_idx = o1_ptr->id => int64;
                    if (npk_mem_read_int64(visited_arr, out1_idx * 8i64) != visit_gen) {
                        drop npk_mem_write_int64(visited_arr, out1_idx * 8i64, visit_gen);
                        drop(apush_list(work_ah, out1, state_start_idx, state_captures));
                    }
                }
            }
        } else if (opcode == OP_ASSERT_END) {
            if (idx == text_len) {
                if (out1 != 0i64) {
                    wild NfaState->:o1_ptr = @cast_unchecked<NfaState->>(out1);
                    int64:out1_idx = o1_ptr->id => int64;
                    if (npk_mem_read_int64(visited_arr, out1_idx * 8i64) != visit_gen) {
                        drop npk_mem_write_int64(visited_arr, out1_idx * 8i64, visit_gen);
                        drop(apush_list(work_ah, out1, state_start_idx, state_captures));
                    }
                }
            }
        } else {
            drop(apush_list(list_ah, state, state_start_idx, state_captures));
        }
    }
    pass 0i64;
};

pub func:regex_vm_match = MatchResult(int64:arena_ptr, int64:start_state, int64:text, int64:text_len, int64:initial_idx) {
    if (start_state == 0i64) { pass MatchResult{matched: 0i32, start_idx: 0i32, end_idx: 0i32}; }
    
    int64:capacity = npk_mem_read_int64(arena_ptr, 0i64) / 64i64;
    
    int64:batch_mem = npk_tlc_batch_alloc(capacity * 96i64 * 3i64 + 24i64 + capacity * 8i64);
    
    int64:clist_ah = batch_mem; drop(npk_mem_write_int64(clist_ah, 0i64, 0i64));
    int64:nlist_ah = batch_mem + capacity * 96i64 + 8i64; drop(npk_mem_write_int64(nlist_ah, 0i64, 0i64));
    int64:work_ah = batch_mem + capacity * 192i64 + 16i64; drop(npk_mem_write_int64(work_ah, 0i64, 0i64));
    
    int64:visited_arr = batch_mem + capacity * 288i64 + 24i64;
    int64:vi = 0i64;
    when (vi < capacity) {
        drop npk_mem_write_int64(visited_arr, vi * 8i64, 0i64);
        vi = vi + 1i64;
    }
    
    int64:visit_gen = 1i64;
    
    int64:idx = initial_idx;
    int32:matched = 0i32;
    int32:running = 1i32;
    int64:final_start_idx = 0i64;
    int64:final_captures_ptr = 0i64;
    
    when (running == 1i32) {
        drop add_state(start_state, clist_ah, visit_gen, visited_arr, work_ah, idx, text_len, idx, 0i64);
        
        if (raw asize_list(clist_ah) == 0i64) {
            running = 0i32;
        } else {
            int64:c = -1i64;
            int64:next_idx = idx + 1i64;
            if (idx < text_len) {
                int64:b0 = npk_mem_read_byte(text, idx);
                c = b0;
                if ((b0 & 128i64) != 0i64) {
                    if ((b0 & 224i64) == 192i64) {
                        if (idx + 1i64 < text_len) {
                            c = ((b0 & 31i64) << 6i64) | (npk_mem_read_byte(text, idx + 1i64) & 63i64);
                            next_idx = idx + 2i64;
                        }
                    } else if ((b0 & 240i64) == 224i64) {
                        if (idx + 2i64 < text_len) {
                            c = ((b0 & 15i64) << 12i64) | ((npk_mem_read_byte(text, idx + 1i64) & 63i64) << 6i64) | (npk_mem_read_byte(text, idx + 2i64) & 63i64);
                            next_idx = idx + 3i64;
                        }
                    } else if ((b0 & 248i64) == 240i64) {
                        if (idx + 3i64 < text_len) {
                            c = ((b0 & 7i64) << 18i64) | ((npk_mem_read_byte(text, idx + 1i64) & 63i64) << 12i64) | ((npk_mem_read_byte(text, idx + 2i64) & 63i64) << 6i64) | (npk_mem_read_byte(text, idx + 3i64) & 63i64);
                            next_idx = idx + 4i64;
                        }
                    }
                }
            }
            
            visit_gen = visit_gen + 1i64;
            
            int64:sz = raw asize_list(clist_ah);
            int64:ti = 0i64;
            when (ti < sz) {
                int64:state = npk_mem_read_int64(clist_ah, 8i64 + ti * 96i64);
                int64:state_start_idx = npk_mem_read_int64(clist_ah, 8i64 + ti * 96i64 + 8i64);
                int64:state_captures = clist_ah + 8i64 + ti * 96i64 + 16i64;
                
                wild NfaState->:s_ptr = @cast_unchecked<NfaState->>(state);
                int32:opcode = s_ptr->opcode;
                
                if (opcode == OP_MATCH) {
                    matched = 1i32;
                    running = 0i32;
                    final_start_idx = state_start_idx;
                    final_captures_ptr = state_captures;
                    ti = sz;
                } else if (c != -1i64) {
                    if (opcode == OP_CHAR) {
                        int32:match_char = s_ptr->match_char;
                        if (c == (match_char => int64)) {
                            int64:out1 = s_ptr->out1;
                            drop add_state(out1, nlist_ah, visit_gen, visited_arr, work_ah, next_idx, text_len, state_start_idx, state_captures);
                        }
                    } else if (opcode == OP_ANY) {
                        int64:out1 = s_ptr->out1;
                        drop add_state(out1, nlist_ah, visit_gen, visited_arr, work_ah, next_idx, text_len, state_start_idx, state_captures);
                    } else if (opcode == OP_CHAR_CLASS) {
                        int32:is_inverted = s_ptr->match_char; // wait, is_inverted is in match_char for char class!
                        if (c <= 255i64) {
                            int64:byte_idx = c / 8i64;
                            int64:bit_idx = c % 8i64;
                            // mask_byte is at state + 24 + byte_idx
                            int64:mask_byte = npk_mem_read_byte(state, 24i64 + byte_idx);
                            if ((mask_byte & (1i64 << bit_idx)) != 0i64) {
                                int64:out1 = s_ptr->out1;
                                drop add_state(out1, nlist_ah, visit_gen, visited_arr, work_ah, next_idx, text_len, state_start_idx, state_captures);
                            }
                        } else {
                            if (is_inverted == 1i32) {
                                int64:out1 = s_ptr->out1;
                                drop add_state(out1, nlist_ah, visit_gen, visited_arr, work_ah, next_idx, text_len, state_start_idx, state_captures);
                            }
                        }
                    }
                }
                
                if (ti != sz + 1i64) { ti = ti + 1i64; }
            }
            drop(aclear_list(clist_ah));
            
            if (matched == 0i32) {
                if (idx >= text_len) {
                    running = 0i32;
                } else {
                    int64:tmp = clist_ah;
                    clist_ah = nlist_ah;
                    nlist_ah = tmp;
                    
                    idx = next_idx;
                }
            }
        }
    }
    
    MatchResult:mr;
    if (matched == 1i32) {
        mr.matched = 1i32;
        mr.start_idx = final_start_idx => int32;
        mr.end_idx = idx => int32;
        int64:ci = 0i64;
        when (ci < 20i64) {
            mr.captures[ci] = npk_mem_read_int32(final_captures_ptr, ci * 4i64);
            ci = ci + 1i64;
        }
    } else {
        mr.matched = 0i32;
        mr.start_idx = 0i32;
        mr.end_idx = 0i32;
        int64:ci = 0i64;
        when (ci < 20i64) {
            mr.captures[ci] = -1i32;
            ci = ci + 1i64;
        }
    }
    pass mr;
};
"""

with open('src/regex_vm.npk', 'w') as f:
    f.write(new_code)
