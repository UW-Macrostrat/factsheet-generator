def remove_newlines(text: str):
    text = text.replace("\n", " ")
    text = text.replace("\\n", " ")
    text = text.replace("  ", " ")
    text = text.replace("  ", " ")
    text = text.replace("..", "")
    return text


def split_by_sentence(text: str) -> list[str]:
    return text.split(". ")


def remove_short_sentences(sentences: list[str], length_cutoff: int = 5) -> list[str]:
    return list(filter(lambda x: len(x.split(" ")) <= length_cutoff, sentences))
