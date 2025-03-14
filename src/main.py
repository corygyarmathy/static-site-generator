from os import getcwd

from file_manipulation import overwrite_directory_files
from generate_files import generate_page
from markdown_manipulation import extract_markdown_links


def main():
    overwrite_directory_files("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    _ = main()
