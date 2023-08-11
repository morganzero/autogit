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
    main_match = re.search(r"main='(v\d+\.\d+\.\d+)'", content)
    beta_match = re.search(r"beta='(v\d+\.\d+\.\d+)'", content)

    if latest_match and develop_match and main_match and beta_match:
        latest_version = latest_match.group(1)
        develop_version = develop_match.group(1)
        main_version = main_match.group(1)
        beta_version = beta_match.group(1)
        return latest_version, develop_version, main_version, beta_version
    else:
        raise ValueError("Couldn't find version patterns in the file")

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
    if branch == "latest":
        update_version_file_in_branch(new_version, "latest")
    elif branch == "develop":
        update_version_file_in_branch(new_version, "develop")
    elif branch == "main":
        update_version_file_in_branch(new_version, "main")
    elif branch == "beta":
        update_version_file_in_branch(new_version, "beta")
    else:
        print("Unknown branch:", branch)

def update_version_file_in_branch(new_version, branch):
    with open(MYFILE, 'r') as version_file:
        content = version_file.read()
    
    content = re.sub(f"{branch}='(v\d+\.\d+\.\d+)'", f"{branch}='{new_version}'", content)

    with open(MYFILE, 'w') as version_file:
        version_file.write(content)

def rollback_version(new_version):
    update_version_file_in_branch(new_version, "latest")
    update_version_file_in_branch(new_version, "develop")
    update_version_file_in_branch(new_version, "main")
    update_version_file_in_branch(new_version, "beta")

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
        
        new_version = increment_version(get_current_versions()[0], level)
        update_version_file(current_branch, new_version)

if __name__ == "__main__":
    main()
