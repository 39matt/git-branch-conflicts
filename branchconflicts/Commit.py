class Commit:
    def __init__(self, message:str, sha:str, commit_parents:list) -> None:
        self.message = message
        self.sha = sha
        self.parents_sha = commit_parents

    def __str__(self) -> str:
        return f"Commit: {self.sha}\nMessage: {self.message}\nParent count: {len(self.parents_sha)}\n==================\n"