import re
import subprocess
import os

MYREPO = os.environ.get("GITPATH")
MYFILE = os.environ["GITFILEPATH"]

if not os.path.exists(MYFILE):
    raise FileNotFoundError(f"Version file not found at path: {MYFILE}")

def get_current_versions():
    with open(MYFILE, 'r') as version_file:
        content = version_file.read()

    latest_match = re.search(r"latest='(v\d+\.\d+\.\d+)'", content)
    develop_match = re.search(r"develop='(v\d+\.\d+\.\d+)'", content)

    if latest_match and develop_match:
        latest_version = latest_match.group(1)
        develop_version = develop_match.group(1)
        return latest_version, develop_version
    else:
        raise ValueError("Couldn't find version patterns in the file")

def increment_version(version, bump_type="patch"):
    major, minor, patch = map(int, version[1:].split('.'))
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"v{major}.{minor}.{patch}"

def update_version_file(branch):
    latest_version, develop_version = get_current_versions()
    
    if branch == "latest":
        new_latest_version = increment_version(latest_version)
        update_version_file_in_branch(new_latest_version, "latest")
    elif branch == "develop":
        new_develop_version = increment_version(develop_version)
        update_version_file_in_branch(new_develop_version, "develop")
    else:
        print("Unknown branch:", branch)

def update_version_file_in_branch(new_version, branch):
    with open(MYFILE, 'r') as version_file:
        content = version_file.read()
    
    content = re.sub(f"{branch}='v\d+\.\d+\.\d+'", f"{branch}='{new_version}'", content)

    with open(MYFILE, 'w') as version_file:
        version_file.write(content)

def main():
    current_branch = subprocess.check_output(["git", "-C", MYREPO, "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
    commit_msg = subprocess.check_output(["git", "-C", MYREPO, "log", "-1", "--pretty=%B"]).decode("utf-8").strip().lower()
    
    if "major" in commit_msg:
        bump_type = "major"
    elif "minor" in commit_msg:
        bump_type = "minor"
    else:
        bump_type = "patch"
    
    update_version_file(current_branch, bump_type)

if __name__ == "__main__":
    main()
