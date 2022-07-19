import subprocess


def get_user_repo() -> tuple[str, str]:
    output = subprocess.check_output(["git", "remote", "-v"]).decode("utf-8")
    for line in output.splitlines():
        if line.startswith("origin"):
            words = line.split("/")
            owner = words[3]
            domain = words[4]
            repo = domain.split(".")[0]
            return owner, repo
    else:
        raise FileNotFoundError(
            "Couldn't parse `git remote -v` correctly. Is this a git repository ?"
        )
