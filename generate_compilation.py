import os
import glob
import subprocess

def main():
    audit_dir = "/home/randy/Workspace/META/NREGX/audits/a10"
    os.makedirs(audit_dir, exist_ok=True)
    
    compilation_file = os.path.join(audit_dir, "compilation.md")
    src_dir = "/home/randy/Workspace/REPOS/nregx/src"
    
    with open(compilation_file, "w") as out:
        out.write("# NREGX Source Compilation\n\n")
        
        # Write all npk files
        for root, _, files in os.walk(src_dir):
            for file in sorted(files):
                if file.endswith(".npk"):
                    filepath = os.path.join(root, file)
                    relpath = os.path.relpath(filepath, src_dir)
                    out.write(f"## File: {relpath}\n\n")
                    out.write("```nitpick\n")
                    with open(filepath, "r") as f:
                        out.write(f.read())
                    if not out.tell() == 0:
                        out.write("\n")
                    out.write("```\n\n")
                    
        # Run tests and capture output
        out.write("## Build Output\n\n")
        out.write("```\n")
        res = subprocess.run(["npkc", "src/test_features.npk"], cwd="/home/randy/Workspace/REPOS/nregx", capture_output=True, text=True)
        if res.returncode == 0:
            res_run = subprocess.run(["./a.out"], cwd="/home/randy/Workspace/REPOS/nregx", capture_output=True, text=True)
            out.write(f"Compilation: SUCCESS\n")
            out.write(f"Test Execution Code: {res_run.returncode}\n")
        else:
            out.write("Compilation: FAILED\n")
            out.write(res.stderr)
        out.write("```\n")

if __name__ == "__main__":
    main()
