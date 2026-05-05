from deep_translator import GoogleTranslator


def translate_nouns(nouns):
    translated = []

    for word, freq in nouns:
        try:
            eng = GoogleTranslator(source="nl", target="en").translate(word)
            # print(f"word: {word}")
            # print(f"eng: {eng}")

        except Exception:
            eng = word

        translated.append({
            "source": word,
            "translation": eng,
            "frequency": freq
        })
    # print(f"translated list: {translated}")
    return translated