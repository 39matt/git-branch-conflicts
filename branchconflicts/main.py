import os
import requests
import subprocess

from branchconflicts.Branch import Branch
from branchconflicts.Commit import Commit


def find_conflicts(repo_owner: str, repo_name: str, access_token: str, local_repo_path: str, branch_a: str, branch_b: str) -> list:

    api = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    conflicted_files = []
    modified_files_local = []


    remote_branch = find_branch_by_name_remote(api, branch_a)
    local_branch = find_branch_by_name_local(local_repo_path, branch_b)
    # if remote_branch and local_branch:
    #     print(remote_branch, local_branch)

    merge_base_sha = find_merge_base(remote_branch, local_branch, repo_owner, repo_name, local_repo_path)
    #print(merge_base)

    latest_commit_local = get_latest_commit_local(local_branch, local_repo_path)
    modified_files_local = find_modified_files_local(latest_commit_local.sha, merge_base_sha, local_repo_path)
    #print(modified_files_local)

    latest_commit_remote = get_latest_commit_remote(remote_branch,repo_owner,repo_name)
    modified_files_remote = find_modified_files_remote(api, latest_commit_remote.sha, merge_base_sha)
    #print(modified_files_remote)

    for local_file in modified_files_local and modified_files_remote:
        conflicted_files.append(local_file)

    return conflicted_files


def find_branch_by_name_remote(api:str, branch_name:str) -> Branch:
    remote_branches_list = requests.get(api + "/branches").json()
    branch = next((branch for branch in remote_branches_list if branch['name'] == branch_name),None)

    if not branch:
        raise Exception(f"Branch '{branch_name}' not found")

    return Branch(branch['name'], branch['commit']['sha'])

def find_branch_by_name_local(local_repo_path:str, branch_name:str) -> Branch:
    local_branch_list = os.listdir(local_repo_path + "/.git/logs/refs/heads")
    branch_name = next((branch for branch in local_branch_list if branch == branch_name),None)

    if not branch_name:
        raise Exception(f"Local branch '{branch_name}' not found")

    with open(local_repo_path + "/.git/logs/refs/heads/" + branch_name, "r") as branch_file:
        for line in branch_file:
            pass
        last_line = line


    return Branch(branch_name, last_line.split(" ")[1])

def get_latest_commit_remote(branch: Branch, owner:str, repo:str) -> Commit:
    api_call = f"https://api.github.com/repos/{owner}/{repo}/commits/" + branch.commit_sha
    response = requests.get(api_call).json()
    commit = Commit(response["commit"]["message"], response["sha"], [])
    for parent in response["parents"]:
        commit.parents_sha.append(parent["sha"])

    return commit

def get_latest_commit_local(branch: Branch, local_repo_path:str) -> Commit:
    commit = Commit("","",[])
    with open(local_repo_path + "/.git/logs/refs/heads/" + branch.name, "r") as branch_file:
        branch_file.readline()
        for line in branch_file:
            fields = line.split(" ")
            commit.parents_sha.append(fields[0])
        commit.sha = fields[1]
        commit.message = ' '.join(fields[6:])

    return commit

def find_merge_base(branch_a: Branch, branch_b: Branch, repo_owner:str, repo_name:str, local_repo_path:str) -> str | None:
    latest_commit_remote = get_latest_commit_remote(branch_a, repo_owner, repo_name)
    latest_commit_local = get_latest_commit_local(branch_b, local_repo_path)
    #print(latest_commit_remote, latest_commit_local)

    for sha in latest_commit_remote.parents_sha:
        if sha in latest_commit_local.parents_sha:
            return sha
    return None

def find_modified_files_local(latest_commit_sha: str, merge_base_sha: str, local_repo_path:str) -> list[str]:
    wd = os.getcwd()
    os.chdir(local_repo_path)
    modified_files =  subprocess.run(["git", "diff-tree", "--no-commit-id", "--name-only", latest_commit_sha, merge_base_sha, "-r"], capture_output=True, text=True).stdout.strip().split("\n")
    os.chdir(wd)
    return modified_files

def find_modified_files_remote(api:str, latest_commit_sha: str, merge_base_sha:str) -> list[str]:
    response = requests.get(f"{api}/compare/{latest_commit_sha}...{merge_base_sha}").json()
    modified_files = [x["filename"] for x in response["files"]]
    return modified_files


if __name__ == "__main__":
    github_username = "39matt"
    repository_name = "jetbrains-test-repo"
    access_token = ""
    local_repo_path = "/home/matija/D/JetBrains/jetbrains-test-repo"
    branch_a = "branchA"
    branch_b = "branchB"

    conflicted_files = find_conflicts(github_username,repository_name,access_token,local_repo_path,branch_a,branch_b)
    if len(conflicted_files) > 0:
        print(f"Conflicted files in both remote and local branch:")
        for file in conflicted_files:
            print(file)
    else:
        print(f"No conflicted files in both remote and local branch")
