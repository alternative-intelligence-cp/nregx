import re

files = [
    'src/regex_compiler.npk',
    'src/nfa_compiler.npk'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Variables with _ptr somewhere in the name
    content = re.sub(r'(\b\w*_ptr\w*)\.(\w+\b)', r'\1->\2', content)

    with open(filepath, 'w') as f:
        f.write(content)

