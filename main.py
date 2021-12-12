from googletrans import LANGUAGES, Translator
from configparser import ConfigParser
from print_table import print_table
import sys
import os


# A blueprint for a line in the subtitle file
class Line:
    def __init__(self, line):
        self.line = line

    def is_content(self):
        is_number_line = False
        is_timestamp_line = False
        is_empty_line = False
        is_content = False

        try:
            int(self.line)
            is_number_line = True
        except ValueError:
            pass              # Pass keyword is useful in this case and not bad coding as what it normally is

        if " --> " in self.line:
            is_timestamp_line = True
        
        if self.line == "\n":
            is_empty_line = True

        if not is_empty_line and not is_number_line and not is_timestamp_line:
            is_content = True

        return is_content


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

# Taking user inputs with exceptions for missing files handled
while True:
    destination_language = input(f"Enter the destination language: ")
    if destination_language in LANGUAGES.values():
        break
    else:
        sys.stderr.write(f"Language '{destination_language}' not found, input again.\n")

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
        subtitle_file_lines = file.readlines()
else:
    with open(subtitle_file, "r") as file:
        subtitle_file_lines = file.readlines()

translator = Translator()

total_lines = len(subtitle_file_lines)

for index, line in enumerate(subtitle_file_lines):
    current_line_number = index + 1  # Added one since natural counting starts at that number
    percentage_progress = round((current_line_number / total_lines) * 100, 2)
    
    if index < last_translated_line:
        continue
    
    print(f"Progress: {percentage_progress}%")

    if Line(line).is_content():
        try:
            translated_line = translator.translate(line, dest=get_lang_code(destination_language))
        except:
            sys.stderr.write("Something went wrong!, Try checking your internet connection.\n")
            write_config(index)
            exit(1)

        if translated_line._response.is_error:
            sys.stderr.write("Google translate API error!, try again after a few minutes.\n")
            write_config(index)
            exit(1)

        subtitle_file_lines[index] = translated_line.text + "\n"       # Appending a newline character as google API removes it 

    update_output(output_file_path, subtitle_file_lines)

print(f"Done, file saved in the path: {output_file_path}")
write_config("completed")
