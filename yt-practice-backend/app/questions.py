import random


def generate_mcq(noun, all_translations):
    correct = noun["translation"]

    wrong_answers = [
        n["translation"]
        for n in all_translations
        if n["translation"] != correct
    ]

    options = random.sample(wrong_answers, min(3, len(wrong_answers)))
    options.append(correct)
    random.shuffle(options)

    return {
        "question_text": f'What does "{noun["source"]}" mean?',
        "correct_answer": correct,
        "options": options
    }