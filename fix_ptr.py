import re

files = [
    'src/regex_cache.npk',
    'src/regex_compiler.npk',
    'src/nfa_compiler.npk',
    'src/prefix_extractor.npk',
    'src/regex_vm.npk'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Change .fetch_add to .add, etc.
    content = content.replace('.fetch_add(', '.add(')
    content = content.replace('.fetch_sub(', '.sub(')
    
    # Change Handle<CacheEntry> casts
    content = content.replace('=> Handle<CacheEntry>', '=> CacheEntry->')
    content = content.replace('Handle<CacheEntry>:next', 'CacheEntry->:next')
    
    # Change all .field on pointers to ->field
    # This matches \w+_ptr.field
    content = re.sub(r'(\b\w+_ptr)\.(\w+\b)', r'\1->\2', content)

    with open(filepath, 'w') as f:
        f.write(content)

