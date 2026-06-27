import os, glob

for fpath in glob.glob('tests/*.npk'):
    with open(fpath, 'r') as f:
        c = f.read()
    if 'func:failsafe' not in c:
        c += "\n\npub func:failsafe = int32(tbb32:err) {\n    drop err;\n    exit 1i32;\n};\n"
        with open(fpath, 'w') as f:
            f.write(c)
