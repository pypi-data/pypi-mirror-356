"""Debug helper code for Jupyter Lab.

This module provides utilities for dumping debug information and
reproducing experiments in Jupyter notebooks.
"""

import os
from typing import Dict, Optional
import datetime

import jammy.io as jio
import jammy.utils.git as git
import ipynbname

# Constants
IMPORTANT_FILE_EXT = [".py", ".yaml", ".secret", ".yml", ".json"]


def dump_git_codebase(git_root: str, target_dir: str) -> None:
    """Dump git repository information and tracked files.

    Args:
        git_root: Path to the git repository root.
        target_dir: Directory to store the dumped information.
    """
    jio.mkdir(target_dir)

    # Create a directory for storing git repo info
    git_info_dir = os.path.join(target_dir, "git")
    jio.mkdir(git_info_dir)

    # Dump git repo info
    proj_sha, proj_diff = git.log_repo(git_root)
    with open(
        os.path.join(git_info_dir, "proj_diff.patch"), "w", encoding="utf-8"
    ) as f:
        f.write(proj_diff)
    jio.dump(proj_sha, os.path.join(git_info_dir, "sha.txt"))

    repo = git.git_repo(git_root)

    # Copy untracked files with important extensions
    for item in repo.untracked_files:
        if any(item.endswith(ext) for ext in IMPORTANT_FILE_EXT):
            jio.cp(os.path.join(git_root, item), os.path.join(target_dir, item))

    # Copy tracked files
    for item in repo.tree():
        if item.type == "blob":  # 'blob' means file in git terminology
            source_file_path = os.path.join(git_root, item.path)
            target_file_path = os.path.join(target_dir, item.path)
            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
            jio.cp(source_file_path, target_file_path)


def generate_dump_name(name: Optional[str] = None) -> str:
    """Generate a name for the dump directory.

    Args:
        name: Optional custom name for the dump.

    Returns:
        A string name for the dump directory.
    """
    if name is None:
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return name


def get_target_folder(
    nb_name: str, proj_dir: str, exp_name: Optional[str] = None
) -> str:
    """Get the target folder for dumping results.

    Args:
        nb_name: Name of the Jupyter notebook.
        proj_dir: Project directory.
        exp_name: Optional experiment name.

    Returns:
        Path to the target folder.
    """
    target_root = os.path.join(proj_dir, nb_name.replace(".ipynb", ""))
    jio.mkdir(target_root)
    if exp_name is None:
        exp_name = generate_dump_name()
    return os.path.join(target_root, exp_name)


def get_notebook_path():
    """
    Get the current Jupyter notebook name and project directory.

    Returns:
        tuple: A tuple containing (notebook_name, project_directory).
               Returns (None, None) if not in a Jupyter environment.
    """
    try:
        # Get the full path of the current notebook
        notebook_path = ipynbname.path()

        if notebook_path:
            # Extract the notebook name
            notebook_name = notebook_path.name

            # Get the project directory (parent of the notebook)
            project_directory = str(notebook_path.parent)

            return notebook_name, project_directory
        else:
            print("Warning: Not running in a Jupyter notebook environment.")
            return None, None
    except Exception as e:
        print(f"Error getting notebook info: {e}")
        return None, None


def dump_jlab(
    result_dict: Optional[Dict] = None, exp_name: Optional[str] = None
) -> str:
    """Dump Jupyter Lab experiment results and codebase.

    This function is intended to be used within a Jupyter notebook.

    Args:
        result_dict: Optional dictionary of results to dump.
        exp_name: Optional experiment name.

    Returns:
        Path to the target folder where results were dumped.

    Raises:
        NotImplementedError: If unable to determine notebook name or project directory.
    """
    # TODO: Implement a way to get the current Jupyter notebook name and project directory
    # TODO: (qsh 2024-09-11) verify it!
    nb_name, proj_dir = get_notebook_path()

    if nb_name is None or proj_dir is None:
        raise NotImplementedError(
            "Unable to determine notebook name or project directory."
        )

    target_fp = get_target_folder(nb_name, proj_dir, exp_name)
    dump_git_codebase(proj_dir, os.path.join(target_fp, "codebase"))

    # Dump results
    if result_dict:
        for k, v in result_dict.items():
            jio.dump(v, os.path.join(target_fp, k))

    return target_fp
