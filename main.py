from googletrans import LANGUAGES
from table_print import table_print
from sub_translator import run_translation

def language_input(language_type):
    while True:
        language = input(f"Enter the {language_type} language: ")
        if language in LANGUAGES.values():
            break
        else:
            print(f"Language {language} not found...")
    return language

def langkey_fetch(lang):
    for key, value in LANGUAGES.items():
        if lang == value:
            return key

def main():
    langs = [LANGUAGES.get(lang) for lang in LANGUAGES]

    print("Choose the languages in the table below for the origin and the destination languages\n")

    table_print(langs)

    origin_language = langkey_fetch(language_input("origin"))
    destination_language = langkey_fetch(language_input("destination"))

    run_translation(origin_language, destination_language)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interruped by the user, exiting..")
