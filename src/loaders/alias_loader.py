import json


class AliasLoader:

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)