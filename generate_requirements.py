import os
import ast
import sys
import subprocess

def get_installed_packages():
    """Return a dict mapping package names to their installed versions."""
    installed = {}
    try:
        output = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
        for line in output.splitlines():
            if "==" in line:
                pkg, ver = line.split("==", 1)
                installed[pkg.lower()] = ver
    except Exception as e:
        print(f"Warning: Could not get installed packages: {e}")
    return installed

def scan_imports(project_path):
    """Scan all .py files and return a set of imported top-level modules."""
    imported_modules = set()
    for root, _, files in os.walk(project_path):
        for filename in files:
            if filename.endswith(".py"):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        node = ast.parse(f.read(), filename=file_path)
                        for n in ast.walk(node):
                            if isinstance(n, ast.Import):
                                for alias in n.names:
                                    imported_modules.add(alias.name.split(".")[0])
                            elif isinstance(n, ast.ImportFrom):
                                if n.module:
                                    imported_modules.add(n.module.split(".")[0])
                except Exception:
                    pass  # skip files that can't be parsed
    return imported_modules

def filter_third_party(modules):
    """Remove standard library modules based on sys.stdlib_module_names (Python 3.10+)."""
    std_libs = set()
    if hasattr(sys, "stdlib_module_names"):  # Python 3.10+
        std_libs = sys.stdlib_module_names
    else:
        # fallback: load from known list
        std_libs = {"os", "sys", "math", "json", "re", "datetime", "time", "typing", "pathlib", "subprocess"}
    return {m for m in modules if m not in std_libs}

if __name__ == "__main__":
    project_dir = os.path.abspath(".")
    print(f"Scanning project folder: {project_dir}\n")

    imported = scan_imports(project_dir)
    third_party = filter_third_party(imported)

    installed_pkgs = get_installed_packages()

    requirements = []
    for pkg in sorted(third_party):
        version = installed_pkgs.get(pkg.lower())
        if version:
            requirements.append(f"{pkg}=={version}")
        else:
            requirements.append(pkg)  # package not installed, version unknown

    # Save to requirements.txt
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(requirements))

    print("Found dependencies:")
    for r in requirements:
        print(f"  {r}")
    print("\nSaved to requirements.txt")
