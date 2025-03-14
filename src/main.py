from os import getcwd

from file_manipulation import overwrite_directory_files
from generate_files import generate_page, generate_pages_recursive
from markdown_manipulation import extract_markdown_links


def main():
    overwrite_directory_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    _ = main()
