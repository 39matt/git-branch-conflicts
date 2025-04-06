def find_conflicts(repo_owner: str, repo_name: str, access_token: str, local_repo_path: str, branch_a: str, branch_b: str) -> list:
    try:
        conflicted_files = []

        return conflicted_files
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    github_username = "39matt"
    repository_name = "jetbrains-test-repo"
    access_token = ""
    local_repo_path = "/home/matija/D/JetBrains/jetbrains-test-repo"
    branch_a = "branchA"
    branch_b = "branchB"

    find_conflicts(github_username,repository_name,access_token,local_repo_path,branch_a,branch_b)