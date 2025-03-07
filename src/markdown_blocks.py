def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    sections = markdown.split("\n\n")
    for section in sections:
        if section == "":
            continue
        blocks.append(section.strip())
    return blocks
