def split_by_paragraph(text: str) -> list[str]:
    return text.split("\n")


def split_by_sentence(text: str) -> list[str]:
    paragraphs = split_by_paragraph(text)
    return list(map(lambda x: x.split(". "), paragraphs))


def remove_short_paragraphs(paragraphs: list[str]) -> list[str]:
    return list(filter(lambda x: len(x.split(" ")), paragraphs))
