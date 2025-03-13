from os import getcwd

from file_manipulation import overwrite_directory_files


def main():
    overwrite_directory_files("static", "public")


if __name__ == "__main__":
    _ = main()
