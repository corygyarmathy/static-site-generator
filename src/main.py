from os import getcwd

from file_manipulation import overwrite_directory_files
from generate_files import generate_page, generate_pages_recursive
from markdown_manipulation import extract_markdown_links
import sys


def main():
    base_path = "/"
    if sys.argv.__len__() > 1:
        if sys.argv[1] != "":
            base_path = sys.argv[1]
    overwrite_directory_files("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", base_path)


if __name__ == "__main__":
    _ = main()
