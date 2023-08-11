import re
import subprocess
import os
import sys
import fcntl

MYREPO = sys.argv[1]
MYFILE = sys.argv[2]

if not os.path.exists(MYFILE):
    raise FileNotFoundError(f"Version file not found at path: {MYFILE}")

def get_bump_type_from_commit():
    commit_message = subprocess.check_output(["git", "-C", MYREPO, "log", "-1", "--pretty=%B"]).decode("utf-8").lower()
    
    if "major" in commit_message:
        return "major"
    elif "minor" in commit_message:
        return "minor"
    else:  # Default to patch if no specific keyword is found.
        return "patch"

def get_version_for_branch(branch):
    with open(MYFILE, 'r') as version_file:
        content = version_file.read()

    branch_match = re.search(f"{branch}='(v\d+\.\d+\.\d+)'", content)
    if branch_match:
        branch_version = branch_match.group(1)
        return branch_version
    else:
        raise ValueError(f"Couldn't find version pattern for branch: {branch} in the file")

def increment_version(version, bump_type="patch"):
    major, minor, patch = map(int, version[1:].split('.'))
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")
    
    return f"v{major}.{minor}.{patch}"

def update_version_file(branch):
    bump_type = get_bump_type_from_commit()
    branch_version = get_version_for_branch(branch)
    new_branch_version = increment_version(branch_version, bump_type)
    update_version_file_for_branch(new_branch_version, branch)

def update_version_file_for_branch(new_version, branch):
    with open(MYFILE, 'r+') as version_file:
        # Lock the file
        fcntl.flock(version_file, fcntl.LOCK_EX)

        content = version_file.read()
        content = re.sub(f"{branch}='v\d+\.\d+\.\d+'", f"{branch}='{new_version}'", content)

        # Move the pointer to the beginning of the file
        version_file.seek(0)
        version_file.write(content)

        # Ensure the file is truncated to the size of our data
        version_file.truncate()

        # Unlock the file
        fcntl.flock(version_file, fcntl.LOCK_UN)

def main():
    current_branch = subprocess.check_output(["git", "-C", MYREPO, "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
    update_version_file(current_branch)

if __name__ == "__main__":
    main()