from os import chdir, makedirs
from os.path import dirname
from file_manipulation import get_git_root
from markdown_blocks import markdown_to_html_node
from markdown_manipulation import extract_markdown_title


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """Generate a page using an incoming file, template, and destination path.

    All paths are expected to point to files, and not directories.
    All paths must not be empty (e.g. == "" or " ")

    Args:
        from_path:
            File path to get the Markdown-formatted text from.
        template_path;
            File path to get the HTML template text from.
        dest_path:
            File path to write the HTML file to.

    Returns: None.

    Raises:
        FileNotFoundError: If files it's trying to read from don't exist.
        IOError: If it fails to write to files.
    """
    chdir(get_git_root())

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        from_file = open(from_path, "r")
        md: str = from_file.read()
        from_file.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"Cannot find file: {from_path}")
    try:
        template_file = open(template_path, "r")
        template_html: str = template_file.read()
        template_file.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"Cannot find file: {template_path}")

    content_html: str = markdown_to_html_node(md).to_html()
    title: str = extract_markdown_title(md)
    placeholders: dict[str, str] = {"{{ Title }}": title, "{{ Content }}": content_html}
    html: str = template_html

    for placeholder, replacement in placeholders.items():
        print(html)
        html = html.replace(placeholder, replacement)

    dest_dir = dirname(dest_path)
    makedirs(dest_dir, exist_ok=True)

    try:
        with open(dest_path, "w") as f:
            _ = f.write(html)
    except IOError:
        raise IOError(f"Error writing to {dest_path}")
