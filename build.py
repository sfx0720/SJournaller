"""Build script — clean + compile + verify."""
import subprocess
import shutil
import os
import sys

def main():
    root = os.path.dirname(os.path.abspath(__file__))

    # 1. Wipe old build artifacts
    for d in ("build", "dist"):
        path = os.path.join(root, d)
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Removed {path}/")

    # 2. Build
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "sjournaller.spec",
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=root)

    if result.returncode != 0:
        print("Build failed!", file=sys.stderr)
        sys.exit(1)

    # 3. Verify output exists
    exe = os.path.join(root, "dist", "SJournaller.exe")
    if os.path.isfile(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"Success: {exe} ({size_mb:.1f} MB)")
    else:
        print("ERROR: exe not found in dist/", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()