from os import chdir, getcwd, listdir, mkdir, path
from shutil import copy, rmtree
import subprocess


def get_git_root():
    return subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    ).stdout.strip()


def overwrite_directory_files(source: str, destination: str) -> None:
    # git_root = get_git_root()
    # chdir(git_root)
    print(f"Current working directory: {getcwd()}")
    if path.exists(destination):
        rmtree(destination)
        mkdir(destination)
    else:
        mkdir(destination)
    copy_files(source, destination)


def copy_files(source: str, destination: str) -> None:
    dir_items = listdir(source)
    for item in dir_items:
        source_path = path.join(source, item)
        dest_path = path.join(destination, item)
        if path.isfile(source_path):  # File
            copy(source_path, dest_path)
            print(f"Copying {source_path} to {dest_path}")
        else:  # Directory
            mkdir(dest_path)
            copy_files(source_path, dest_path)
