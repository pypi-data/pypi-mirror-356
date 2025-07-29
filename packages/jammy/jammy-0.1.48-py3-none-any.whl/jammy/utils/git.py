import os
import os.path as osp

import git

from jammy.logging import get_logger

logger = get_logger()

__all__ = ["is_git", "git_rootdir", "git_hash"]


def is_git(path):
    try:
        _ = git.Repo(path, search_parent_directories=True).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


def git_rootdir(path=""):
    if is_git(os.getcwd()):
        _git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
        root = _git_repo.git.rev_parse("--show-toplevel")
        return osp.join(root, path)
    logger.warning("not a git repo")
    return osp.join(os.getcwd(), path)


def git_hash(path):
    if is_git(path):
        _git_repo = git.Repo(path, search_parent_directories=True)
        return _git_repo.head.object.hexsha
    logger.warning("not a git repo")
    return None


def git_repo(path):
    if is_git(path):
        _git_repo = git.Repo(path, search_parent_directories=True)
        return _git_repo
    logger.warning("not a git repo")
    return None


def log_repo(path):
    repo = git_repo(path)
    if repo:
        return repo.head.object.hexsha, repo.git.diff()
    # if not repo, return None sha, empty diff
    return None, ""
