import re

files = ['src/regex_compiler.npk', 'src/nfa_compiler.npk', 'src/prefix_extractor.npk', 'src/nregx.npk']

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # We replace `raw func(...)` with `func(...) ? 0i64`
        # But only for functions returning Result that we changed
        line = lines[i]
        line = re.sub(r'raw\s+(parse_alt|parse_concat|parse_rep|parse_atom|parse_regex_ast|compile_nfa|extract_literal_prefix)\((.*?)\)', r'\1(\2) ? 0i64', line)
        lines[i] = line
        
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))

