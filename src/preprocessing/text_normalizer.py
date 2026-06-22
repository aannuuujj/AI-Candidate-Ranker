import re


class TextNormalizer:

    @staticmethod
    def normalize(text: str):

        text = text.lower()

        text = re.sub(r"[^\w\s]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()