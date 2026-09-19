
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

def main():

    WORD_LIMIT: int | None = None

    enable_word_count: int = 0

    words: list[str] = []
    descriptions: list[str] = []

    print()
    print("Loading enable word list into dictionary")
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

    descriptions = [ '' ] * enable_word_count

    print("Loading dictionary descriptions into descriptions")
    print()

    WIKITIONARY_DESCRIPTION_LIMIT: int | None = None

    description_dictionary_word_count: int = 0
    words_with_definitions: int = 0

    with open(
        file="kaikki.org-dictionary-English.jsonl",
        mode="r",
        newline='',
        encoding="utf-8"
    ) as kaikki_org_dictionary_english_jsonl_file:

        for i, line in enumerate(kaikki_org_dictionary_english_jsonl_file):
            if WIKITIONARY_DESCRIPTION_LIMIT is not None and i >= WIKITIONARY_DESCRIPTION_LIMIT:
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
            if formatted_word == "ABLINS":
                print("FOUND ABLINS ENTRY IN WIKTIONARY:\n\n", entry, "\n\n")
            formatted_word_index: int = binary_search(words, formatted_word)
            if formatted_word_index != -1 and descriptions[formatted_word_index] == '':
                descriptions[formatted_word_index] = desc
                words_with_definitions += 1

    print("Writing dictionary to word_game_dictionary.txt")
    print()

    with open(
        file="word_game_dictionary.txt",
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
            if description == '':
                words_without_descriptions_txt_file.write(f"{word}\n")

    print("ENABLE word count: ", enable_word_count)
    print("Description dictionary word count: ", description_dictionary_word_count)
    print("Words with definitions: ", words_with_definitions)
    print("Words without definitions: ", enable_word_count - words_with_definitions)
    print("Coverage: ", words_with_definitions / enable_word_count * 100, '%')

    print("binary search ABLINS index: ", binary_search(words, "ABLINS"))
    print("Is 'ABLINS' in words: ", "ABLINS" in words)
    print("result index: ", words[binary_search(words, "ABLINS")])

if __name__ == "__main__":
    main()
