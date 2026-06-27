import os
import subprocess

out_file = "/home/randy/Workspace/META/NREGX/audits/a6/compilation.md"

src_files = [
    "src/ast_types.npk",
    "src/regex_types.npk",
    "src/util/str_view.npk",
    "src/util/mem_primitives.npk",
    "src/util/error_codes.npk",
    "src/regex_compiler.npk",
    "src/nfa_compiler.npk",
    "src/regex_arena.npk",
    "src/regex_cache.npk",
    "src/regex_vm.npk",
    "src/prefix_extractor.npk",
    "src/nregx.npk"
]

with open(out_file, "w") as f:
    for src in src_files:
        f.write(f"### {src}\n```nitpick\n")
        with open(src, "r") as src_f:
            f.write(src_f.read())
        f.write("\n```\n\n")

    f.write("### build output\n```\n")
    try:
        res = subprocess.run(["npkc", "-I", "src", "tests/test_basic.npk", "-o", "test_bin"], capture_output=True, text=True)
        f.write(res.stdout)
        f.write(res.stderr)
        
        # also run it
        if res.returncode == 0:
            res_run = subprocess.run(["./test_bin"], capture_output=True, text=True)
            f.write(res_run.stdout)
            f.write(res_run.stderr)
            
    except Exception as e:
        f.write(str(e))
    f.write("\n```\n")
