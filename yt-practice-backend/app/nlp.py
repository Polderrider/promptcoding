import spacy
from collections import Counter


nlp = spacy.load("nl_core_news_sm")

def extract_nouns(text: str, top_n: int = 20):
    
    doc = nlp(text)
    nouns = [
    token.lemma_.lower()
    for token in doc
    if token.pos_ in {"NOUN", "PROPN"}
    and token.is_alpha
    and not token.is_stop
]

    freq = Counter(nouns)

    return freq.most_common(top_n)