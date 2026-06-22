from semantic.semantic_matcher import SemanticMatcher

matcher = SemanticMatcher()

pairs = [
    ("LLM", "Large Language Models"),
    ("RAG", "Retrieval Augmented Generation"),
    ("Python", "Python"),
    ("AWS", "Amazon Web Services"),
    ("ML", "Machine Learning"),
]

for a, b in pairs:
    score = matcher.similarity(a, b)
    print(f"{a:10} <-> {b:35} = {score:.3f}")