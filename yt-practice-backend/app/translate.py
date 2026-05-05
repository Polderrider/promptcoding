from deep_translator import GoogleTranslator


def translate_nouns(nouns):
    translated = []

    for word, freq in nouns:
        try:
            eng = GoogleTranslator(source="nl", target="en").translate(word)
            if word == eng:
                print(f"translate.py word: {word}")
                
                print(f"translate.py translated word eng: {eng}")

        except Exception:
            eng = word

        translated.append({
            "source": word,
            "translation": eng,
            "frequency": freq
        })

    return translated