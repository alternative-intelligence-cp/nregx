import re

files = ['src/regex_compiler.npk', 'src/nfa_compiler.npk', 'src/prefix_extractor.npk']

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We DO NOT modify signatures to Result<int64>
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Change pass 0i64 to fail ERR_REGEX_PARSE
        if 'pass 0i64;' in line and 'lex_pattern' not in line:
            lines[i] = line.replace('pass 0i64;', 'fail ERR_REGEX_PARSE;')
            
        # Ensure parse calls are unwrapped using raw
        # (original code may have `int64:root = parse_alt(...)`)
        line = lines[i]
        line = re.sub(r'(int64:\w+\s*=\s*)(parse_alt|parse_concat|parse_rep|parse_atom|parse_regex_ast|compile_nfa|extract_literal_prefix)\(', r'\1raw \2(', line)
        lines[i] = line
        
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))

