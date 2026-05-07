import spacy
from collections import Counter


nlp = spacy.load("nl_core_news_sm")

def extract_nouns(text: str, top_n: int = 100):
    
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


def extract_verbs(text: str, top_n: int = 100):
    
    doc = nlp(text)
    verbs = [
    token.lemma_.lower()
    for token in doc
    if token.pos_ in {"VERB", "VBG"}
    and token.is_alpha
    and not token.is_stop
]

    freq = Counter(verbs)

    return freq.most_common(top_n)



def extract_topics(text: str):
    doc = nlp(text)
    topics = []

    for token in doc:
        if token.pos_ == "NOUN":
            modifiers = [
                child.text
                for child in token.children
                if child.pos_ in {"ADJ", "VERB"}  # include participles
            ]

            for mod in modifiers:
                topics.append(f"{mod} {token.text}".lower())

    return topics



