
# Word Game Dictionary

A Python utility that creates a word-game dictionary by combining the [ENABLE word list](https://github.com/BartMassey/wordlists/tree/main) with English word definitions from the [Kaikki.org English Wiktionary data dump](https://kaikki.org/dictionary/English/words/index.html).

The program matches words from ENABLE against dictionary entries, extracts a suitable definition, and produces a final dictionary containing each word and its description.

## Features

* Loads words from the ENABLE word list.
* Sorts the word list for efficient binary searching.
* Loads English dictionary entries from a Kaikki.org JSONL dump.
* Extracts the first available word definition.
* Supports fallback descriptions for:

  * Inflected forms
  * Alternative forms
* Normalizes dictionary words before matching by:

  * Converting them to uppercase
  * Removing hyphens
  * Removing spaces
* Allows manually added descriptions for words that could not be matched automatically.
* Reports dictionary coverage.
* Generates a list of words that still have no description.

## How It Works

The program uses the ENABLE word list as the source of valid words.

It then processes the Kaikki.org English dictionary data and attempts to find a matching ENABLE word for each dictionary entry.

The process is:

```text
ENABLE word list
       │
       ▼
Load words into a list
       │
       ▼
Sort words
       │
       ▼
Create empty descriptions list
       │
       ▼
Process Kaikki.org JSONL dictionary
       │
       ▼
Extract word definition
       │
       ▼
Normalize dictionary word
       │
       ▼
Binary search ENABLE words
       │
       ├── Match found ──► Store description
       │
       └── No match ─────► Ignore entry
       │
       ▼
Process manually added descriptions
       │
       ▼
Generate final dictionary
```

### Word Matching

Dictionary words are normalized before matching:

```python
formatted_word = word.upper().replace('-', '').replace(' ', '')
```

For example:

```text
dictionary entry     normalized
-----------------    ----------
word                 WORD
some-word            SOMEWORD
another word         ANOTHERWORD
```

The normalized word is then searched for in the sorted ENABLE word list using binary search.

## Description Selection

For each dictionary entry, the program examines its senses and attempts to obtain a description.

The first available `glosses` entry is used:

```python
if glosses:
    desc = glosses[0]
```

If a normal gloss is unavailable, the program also supports two fallbacks.

### Inflected Forms

If the entry specifies `form_of`, the program creates a description such as:

```text
form of run
```

### Alternative Forms

If the entry specifies `alt_of`, the program creates a description such as:

```text
alternative form of color
```

## Manual Descriptions

Some ENABLE words may not have a suitable English entry in the Kaikki.org English dataset.

These words can be given descriptions manually using:

```text
orphan_words_with_added_descriptions.txt
```

Each line should contain the word followed by its description:

```text
WORD description of the word
ANOTHERWORD another description
```

For example:

```text
ABLINS perhaps; maybe
```

Manual descriptions are only applied when the word does not already have a description from Kaikki.org.

This prevents manually supplied descriptions from overwriting descriptions that were already found automatically.

## Input Files

The program expects the following files in the project directory.

### `enable2k.txt`

The ENABLE word list.

This provides the set of words that the generated dictionary should contain.

File is included in the GitHub project directory since it is in the public domain.

### `kaikki.org-dictionary-English.jsonl`

The Kaikki.org English dictionary data in JSON Lines format.

Each line contains a JSON dictionary entry containing information such as the word and its senses.

[website](https://kaikki.org/dictionary/English/words/index.html)
[download](https://kaikki.org/dictionary/English/words/kaikki.org-dictionary-English-words.jsonl)

### `orphan_words_with_added_descriptions.txt`

Optional manually supplied descriptions for words that could not be matched with a suitable definition automatically.

## Output Files

### `word_game_dictionary.txt`

The final generated dictionary.

Each line contains a word followed by its description:

```text
AA A member of Alcoholics Anonymous.
AAH Indication of amazement or surprise or enthusiasm.
AAHED simple past and past participle of aah
AAHING present participle and gerund of aah
AAHS plural of aah
...
```

Words without descriptions are still included, but their description is empty.

### `words_without_descriptions.txt`

Contains every ENABLE word that still has no description after processing both the Kaikki.org data and manually supplied descriptions.

This file can be used to identify additional words that may need descriptions.

## Configuration

The program contains two optional limits that are useful for testing.

### ENABLE Word Limit

```python
WORD_LIMIT: int | None = None
```

Set this to an integer to process only the first specified number of ENABLE words.

For example:

```python
WORD_LIMIT: int | None = 300
```

processes only the first 300 words.

Set it to:

```python
WORD_LIMIT: int | None = None
```

to process the complete word list.

### Wiktionary Description Limit

```python
WIKTIONARY_DESCRIPTION_LIMIT: int | None = None
```

This controls how many lines of the Kaikki.org JSONL file are processed.

For testing:

```python
WIKTIONARY_DESCRIPTION_LIMIT: int | None = 100
```

processes only the first 100 dictionary entries.

For the complete dictionary:

```python
WIKTIONARY_DESCRIPTION_LIMIT: int | None = None
```

## Prerequisites

- [Python](https://www.python.org/downloads/)
- [Input files](#input-files)

## Getting started

Make sure all prerequisites are installed and the required input files are in the project directory.

Run:

```bash
python main.py
```

## Coverage

At the end of execution, the program reports:

```text
ENABLE word count: ...
Description dictionary word count: ...
Words with definitions: ...
Words without definitions: ...
Coverage: ... %
```

Coverage is calculated as:

```text
words with descriptions
──────────────────────── × 100
     ENABLE words
```

For example, if 168,084 out of 173,528 ENABLE words have descriptions:

```text
168084 / 173528 × 100 ≈ 96.86%
```

## Dependencies

The project currently uses only the Python standard library.

Main modules used:

* `json`
* `bisect`
* `typing`

No third-party Python packages are required.

## Data Sources

### ENABLE

The ENABLE word list is used as the source of valid game words.

The program does **not** use the dictionary definition dataset to determine whether a word is valid. ENABLE determines the words that appear in the final dictionary.

### Kaikki.org / Wiktionary

Definitions are obtained from the Kaikki.org English dictionary data, which is generated from Wiktionary data.

The Kaikki.org dataset is used as a **definition source**, while ENABLE is used as the **word-list source**.

Check the respective projects and data licenses before redistributing the generated dictionary.

## Project Structure

A typical project directory looks like:

```
WordGameDictionary/
│
├── .gitignore                                  # Specifies files and directories that Git should ignore
├── enable2k.txt                                # ENABLE 2K word list used as the source of valid words
├── kaikki.org-dictionary-English.jsonl         # English Wiktionary data used as the source of word descriptions
├── LICENSE                                     # Contains the license information for the project
├── main.py                                     # Main Python script used to generate the word game dictionary
├── orphan_words_with_added_descriptions.txt    # Manually added descriptions for words without descriptions
├── README.md                                   # Project documentation
├── word_game_dictionary.txt                    # Generated dictionary containing words and their descriptions
└── words_without_descriptions.txt              # Generated list of words that still do not have descriptions
```

## Notes

Not every ENABLE word necessarily has an English entry in the Kaikki.org English dataset. For example, a word may exist on Wiktionary under another language or may not have a suitable English definition in the downloaded dataset.

Consequently, some words may remain without descriptions even after processing the complete dictionary.

The project therefore supports manually adding descriptions for remaining words through the orphan-description file.
