class Branch:
    def __init__(self, name:str, commit_sha:str) -> None:
        self.name = name
        self.commit_sha = commit_sha

    def __str__(self) -> str:
        return f"Branch: {self.name}\nLatest commit: {self.commit_sha}\n==================\n"