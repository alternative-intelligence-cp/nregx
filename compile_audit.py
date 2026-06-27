import os
import subprocess
from pathlib import Path

repo_dir = "/home/randy/Workspace/REPOS/nregx"
audit_dir = "/home/randy/Workspace/META/NREGX/audits/a9"

os.makedirs(audit_dir, exist_ok=True)
compilation_file = os.path.join(audit_dir, "compilation.md")

src_dir = os.path.join(repo_dir, "src")
files_to_compile = []

for root, _, files in os.walk(src_dir):
    for f in files:
        if f.endswith('.npk') and not f.startswith('test') and not f.startswith('mini_test'):
            files_to_compile.append(os.path.join(root, f))

with open(compilation_file, 'w') as out:
    out.write("# NREGX Source Compilation\n\n")
    for fpath in files_to_compile:
        rel_path = os.path.relpath(fpath, repo_dir)
        out.write(f"## {rel_path}\n")
        out.write("```nitpick\n")
        with open(fpath, 'r') as f:
            out.write(f.read())
        out.write("\n```\n\n")

    out.write("## build output\n")
    out.write("```\n")
    
    # Run build
    result = subprocess.run(["npkc", "src/test.npk"], cwd=repo_dir, capture_output=True, text=True)
    out.write(result.stdout)
    out.write(result.stderr)
    if result.returncode == 0:
        run_res = subprocess.run(["./a.out"], cwd=repo_dir, capture_output=True, text=True)
        out.write(run_res.stdout)
        out.write(run_res.stderr)
    out.write("\n```\n")

print(f"Created {compilation_file}")
