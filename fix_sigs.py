import re

files = [
    'src/regex_compiler.npk',
    'src/nfa_compiler.npk',
    'src/prefix_extractor.npk',
    'src/nregx.npk'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
        
    for func in ['parse_alt', 'parse_concat', 'parse_rep', 'parse_atom', 'parse_regex_ast', 'compile_nfa', 'extract_literal_prefix', 'compile_and_cache']:
        # Replace `func:NAME = int64` with `func:NAME = Result<int64>`
        content = re.sub(rf'func:{func}\s*=\s*int64\(', rf'func:{func} = Result<int64>(', content)
        
    with open(filepath, 'w') as f:
        f.write(content)
