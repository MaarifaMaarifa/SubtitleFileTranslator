from googletrans import LANGUAGES, Translator
from print_table import print_table
import sys
import os

# A blueprint for the line in the subtitle file
class Line:
    def __init__(self, line):
        self.line = line
        
    def is_content_number(self):
        try:
            int(self.line)
            return True
        except ValueError:
            return False

    def is_content(self):
        if self.line != "\n" and not self.is_content_number() and "-->" not in self.line:
            return True
        else:
            return False

# Function to get the language code
def get_lang_code(lang):
    for langcode, language in LANGUAGES.items():
        if lang == language:
            return langcode

# Function to update the output file when obtaining the translations back
def update_output(file_name, input_file_lines):
    with open(file_name, "w") as file:
        for line in input_file_lines:
            file.write(line)

# Function to handle reading the files and detecting the need to resume translation
def file_loader(subtitle_file, output_file):
    resumable = False
    output_file_lines = []          # Initialized the list as the output file might not be present
    if os.path.isfile(output_file):
        print("Previous output file detected. Resuming translation..")
        with open(output_file, "r") as file:
            output_file_lines = file.readlines()
        resumable = True

    with open(subtitle_file, "r") as file:
        input_file_lines = file.readlines()
    

    return input_file_lines, output_file_lines, resumable

# Getting the list for all of the available languages
langs = [LANGUAGES.get(lang) for lang in LANGUAGES]

print("Choose one of the language from the table for the destination language")

print_table(langs)

while True:
    destination_language = input(f"Enter the destination language: ")
    if destination_language in LANGUAGES.values():
        break
    else:
        sys.stderr.write(f"Language {destination_language} not found, input again.\n")

while True:
    subtitle_file = input("Enter the full path to the subtitle file: ")
    if os.path.isfile(subtitle_file):
        break
    else:
        sys.stderr.write("Subtitle file not found, Input again.\n")


output_file_path = os.getcwd() + "/output.srt"

input_file_lines, output_file_lines, resumable = file_loader(subtitle_file, output_file_path)

translator = Translator()

if resumable:
    lines = output_file_lines
else:
    lines = input_file_lines

total_lines = len(lines)

for index, line in enumerate(lines):
    current_line_number = index + 1               # Added one since natural counting starts at that number
    percentage_progress = (current_line_number/total_lines) * 100

    if resumable:
        for index, line in enumerate(output_file_lines):
            if line != input_file_lines[index]:   # Inequality suggests that lines are translated
                continue
    resumable = False

    current_line = Line(line)

    print(f"Percentage completion: {percentage_progress}%")

    if current_line.is_content():
        try:
            translated_line = translator.translate(line, dest=get_lang_code(destination_language)).text
        except:
            sys.stderr.write("Something went wrong!, Try checking your internet connection.")
            exit(1)

        if "\n" not in translated_line:
            translated_line += "\n"
        if translated_line == line:
            sys.stderr.write("Google translate API failure, exiting..\n")
            exit(1)

        lines[index] = translated_line

    update_output(output_file_path, lines)

print(f"Done, file saved in the path: {output_file_path}")
