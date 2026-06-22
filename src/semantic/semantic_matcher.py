from sentence_transformers import SentenceTransformer, util


class SemanticMatcher:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.cache = {}

    def get_embedding(self, text):

        text = text.lower().strip()

        if text not in self.cache:

            self.cache[text] = self.model.encode(
                text,
                convert_to_tensor=True,
            )

        return self.cache[text]

    def similarity(self, text1, text2):

        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)

        score = util.cos_sim(
            emb1,
            emb2,
        )

        return float(score)