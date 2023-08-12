import re
import subprocess
import os

MYREPO = os.environ.get("GITPATH")
MYFILE = os.environ["GITFILEPATH"]

if not os.path.exists(MYFILE):
    raise FileNotFoundError(f"Version file not found at path: {MYFILE}")

BRANCHES = {
    "latest": "latest",
    "develop": "develop",
    "main": "main",
    "beta": "beta"
}

def get_current_versions():
    with open(MYFILE, 'r') as version_file:
        content = version_file.read()

    versions = {}

    for branch in BRANCHES:
        match = re.search(f"{branch}='(v\d+\.\d+\.\d+)'", content)
        if match:
            versions[branch] = match.group(1)
        else:
            raise ValueError(f"Couldn't find version pattern for branch: {branch}")

    return versions

def increment_version(version, level):
    major, minor, patch = map(int, version[1:].split('.'))
    
    if level == "major":
        major += 1
        minor = 0
        patch = 0
    elif level == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    
    return f"v{major}.{minor}.{patch}"

def update_version_file(branch, new_version):
    with open(MYFILE, 'r') as version_file:
        content = version_file.read()

    content = re.sub(f"{branch}='{get_current_versions()[branch]}'", f"{branch}='{new_version}'", content)

    with open(MYFILE, 'w') as version_file:
        version_file.write(content)

def rollback_version(new_version):
    for branch in BRANCHES:
        update_version_file(branch, new_version)

def main():
    current_branch = subprocess.check_output(["git", "-C", MYREPO, "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()

    commit_message = subprocess.check_output(["git", "-C", MYREPO, "log", "-1", "--pretty=%B"]).decode("utf-8").strip()
    
    if "rollback" in commit_message:
        match = re.search(r"rollback \[(\d+\.\d+\.\d+)\]", commit_message)
        if match:
            rollback_version(match.group(1))
    else:
        level = "patch"
        if "minor" in commit_message:
            level = "minor"
        elif "major" in commit_message:
            level = "major"
        
        new_version = increment_version(get_current_versions()[current_branch], level)
        update_version_file(current_branch, new_version)

if __name__ == "__main__":
    main()
