import subprocess, os

GIT_LINK_URL = "https://github.com/{owner}/{repo}/blob/{sha}/{relpath}#L{line_number}"


def get_git_revision_hash(filepath: str):
    return (
        subprocess.check_output(
            ["git", "describe", "--always"],
            cwd=os.path.dirname(os.path.abspath(filepath)),
        )
        .strip()
        .decode("utf-8")
    )


def gitlinker(
    owner: str, repo: str, filepath: str, relpath: str, line_number: int
) -> str:
    """
    https://github.com/qkzk/todo_markers/blob/f68173c0e7d985e97af2beffe9dcbe2cdc154f9a/src/main.py#L1
    """
    sha = get_git_revision_hash(filepath)
    return GIT_LINK_URL.format(
        owner=owner, repo=repo, sha=sha, relpath=relpath, line_number=line_number
    )
