
from typing import TypeVar

from bisect import bisect_left

import json

T = TypeVar('T')
def binary_search(
    arr: list[T],
    target: T
) -> int:
    index = bisect_left(arr, target)
    if index < len(arr) and arr[index] == target:
        return index
    return -1

NULL_DESCRIPTION: str = ''

def main():

    WORD_LIMIT: int | None = None

    enable_word_count: int = 0

    words: list[str] = []
    descriptions: list[str] = []


    ENABLE_WORD_LIST_FILE_NAME: str = "enable2k.txt"

    print()
    print(f"Loading enable word list from '{ENABLE_WORD_LIST_FILE_NAME}' into words list")
    print()

    with open(
        file="enable2k.txt",
        mode="r",
        encoding="utf-8",
        newline=''
    ) as enable_word_list_file:
        for i, line in enumerate(enable_word_list_file):
            if WORD_LIMIT is not None and i >= WORD_LIMIT:
                break
            word = line.strip().upper()
            words.append(word)
            enable_word_count += 1

    print("Sorting words list")
    print()

    words.sort()


    print("Reserving memory for descriptions list")
    print()

    descriptions = [ NULL_DESCRIPTION ] * enable_word_count


    WIKTIONARY_FILE_NAME: str = "kaikki.org-dictionary-English.jsonl"

    print(f"Mapping words from '{ENABLE_WORD_LIST_FILE_NAME}' to descriptions from '{WIKTIONARY_FILE_NAME}' (storing descriptions in descriptions list)")
    print()

    WIKTIONARY_DESCRIPTION_LIMIT: int | None = None

    description_dictionary_word_count: int = 0

    with open(
        file=WIKTIONARY_FILE_NAME,
        mode="r",
        newline='',
        encoding="utf-8"
    ) as kaikki_org_dictionary_english_jsonl_file:

        for i, line in enumerate(kaikki_org_dictionary_english_jsonl_file):
            if WIKTIONARY_DESCRIPTION_LIMIT is not None and i >= WIKTIONARY_DESCRIPTION_LIMIT:
                break

            entry = json.loads(line)

            word: str | None = entry.get("word")
            if word is None:
                continue

            description_dictionary_word_count += 1

            senses: list[str] = entry.get("senses", [])
            desc: str | None = None

            for sense in senses:
                glosses = sense.get("glosses")
                if glosses:
                    desc = glosses[0]
                    break
                # fallbacks for inflection / alt-form entries
                if sense.get("form_of"):
                    desc = f"form of {sense['form_of'][0]['word']}"
                    break
                if sense.get("alt_of"):
                    desc = f"alternative form of {sense['alt_of'][0]['word']}"
                    break

            if desc is None:
                continue

            formatted_word = word.upper().replace('-', '').replace(' ', '')
            formatted_word_index: int = binary_search(words, formatted_word)
            if formatted_word_index >= 0 and descriptions[formatted_word_index] == NULL_DESCRIPTION:
                descriptions[formatted_word_index] = desc


    ORPHAN_WORD_DESCRIPTIONS_FILE_NAME: str = "orphan_words_with_added_descriptions.txt"

    print(f"Filling orphan words (words with no descriptions) with word descriptions in '{ORPHAN_WORD_DESCRIPTIONS_FILE_NAME}'")
    print()

    with open(
        file=ORPHAN_WORD_DESCRIPTIONS_FILE_NAME,
        mode="r",
        encoding="utf-8",
        newline=''
    ) as orphan_word_desription_txt_file:
        for line in orphan_word_desription_txt_file:
            stripped_line = line.strip()
            word, description = stripped_line.split(' ', maxsplit=1)
            orphan_word_index: int = binary_search(words, word)
            if orphan_word_index >= 0 and descriptions[orphan_word_index] == NULL_DESCRIPTION:
                descriptions[orphan_word_index] = description


    WORD_GAME_DICTIONARY_FILE_NAME: str = "word_game_dictionary.txt"
                
    print(f"Writing dictionary to '{WORD_GAME_DICTIONARY_FILE_NAME}'")
    print()

    with open(
        file=WORD_GAME_DICTIONARY_FILE_NAME,
        mode="w",
        encoding="utf-8",
        newline=''
    ) as word_game_dictionary_txt_file:
        for word, description in zip(words, descriptions):
            word_game_dictionary_txt_file.write(f"{word} {description}\n")

    print("Writing words without descriptions to words_without_descriptions.txt")
    print()
    with open(
        file="words_without_descriptions.txt",
        mode="w",
        encoding="utf-8",
        newline=''
    ) as words_without_descriptions_txt_file:
        for word, description in zip(words, descriptions):
            if description == NULL_DESCRIPTION:
                words_without_descriptions_txt_file.write(f"{word}\n")

    words_without_descriptions: int = 0
    for description in descriptions:
        if description == NULL_DESCRIPTION:
            words_without_descriptions += 1

    words_with_descriptions: int = enable_word_count - words_without_descriptions

    print("ENABLE word count: ", enable_word_count)
    print("Description dictionary word count: ", description_dictionary_word_count)
    print("Words with definitions: ", words_with_descriptions)
    print("Words without definitions: ", words_without_descriptions)
    print("Coverage: ", words_with_descriptions / enable_word_count * 100, '%')

if __name__ == "__main__":
    main()
