import time
from sentence_transformers import SentenceTransformer, util

# Load the model only once for the entire application
_model = None


class SemanticMatcher:

    def __init__(self):

        global _model

        if _model is None:

            print("\nLoading SentenceTransformer Model...")

            start = time.time()

            _model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

            print(
                f"✅ Semantic model loaded in "
                f"{time.time() - start:.2f} seconds\n"
            )

        self.model = _model

        self.embedding_cache = {}

    def get_embedding(self, text):

        text = text.lower().strip()

        if text not in self.embedding_cache:

            self.embedding_cache[text] = self.model.encode(
                text,
                convert_to_tensor=True,
            )

        return self.embedding_cache[text]

    def similarity(
        self,
        text1,
        text2,
    ):

        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)

        score = util.cos_sim(
            emb1,
            emb2,
        )

        return float(score.item())