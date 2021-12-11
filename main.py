from googletrans import LANGUAGES, Translator
from configparser import ConfigParser
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

# Function to write the last number of line in a configuration file
def write_config(line_number):
    parser.set('filenames', subtitle_file, str(line_number))
    with open(config_file, "w") as conf:
        parser.write(conf)

# Function to extract file name from full file path
def get_filename_from_path(path):
    last_index = len(path) - 1
    filename = ""
    for index in range(last_index, -1, -1):
        if path[index] == '\\' or path[index] == '/':  # Supporting both Linux and Windows
            break
        filename += path[index]
    return filename[::-1]


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

output_file_path = os.getcwd() + '/output-' + get_filename_from_path(subtitle_file)
config_file = os.getcwd() + "/output.conf"

parser = ConfigParser()

translation_resumable = False
last_translated_line = 0
if os.path.isfile(config_file):
    parser.read(config_file)
    if subtitle_file in parser['filenames']:
        translation_resumable = True
        print("Resuming translation......")
        if parser['filenames'][subtitle_file] != 'completed':
            last_translated_line = int(parser['filenames'][subtitle_file])
        else:
            print("Translation for the file completed")
            exit()
else:
    parser['filenames'] = {subtitle_file: '0'}
    with open(config_file, "w") as config:
        parser.write(config)

# Choosing to read from the output file or the input file depending on resumable state
if translation_resumable:
    with open(output_file_path, "r") as file:
        lines = file.readlines()
else:
    with open(subtitle_file, "r") as file:
        lines = file.readlines()

translator = Translator()

total_lines = len(lines)

for index, line in enumerate(lines):
    current_line_number = index + 1  # Added one since natural counting starts at that number
    percentage_progress = (current_line_number / total_lines) * 100
    
    if index < last_translated_line:
        continue
    
    print(f"Percentage completion: {percentage_progress}%")

    current_line = Line(line)

    if current_line.is_content():
        translated_line = ""
        try:
            translated_line = translator.translate(line, dest=get_lang_code(destination_language)).text
        except:
            sys.stderr.write("Something went wrong!, Try checking your internet connection.\n")
            write_config(index)
            exit(1)

        if "\n" not in translated_line:
            translated_line += "\n"
        if translated_line == line:
            sys.stderr.write("Google translate API failure, try again after a few minutes.\n")
            write_config(index)
            exit(1)

        lines[index] = translated_line

    update_output(output_file_path, lines)

print(f"Done, file saved in the path: {output_file_path}")
write_config("completed")
