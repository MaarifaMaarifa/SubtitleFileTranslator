from googletrans import Translator
import sys
import os

# Class for a line in the subtitle text file
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


def run_translation(origin_language, destination_language):
    subtitle_file = input("Enter the full path to the subtitle file: ")

    if not os.path.isfile(subtitle_file):
        sys.stderr.write("Subtitle file not found.\n")
        exit(1)

    with open(subtitle_file, "r") as file:
            lines = file.readlines()

    output_path = input("Enter the path to save the output: ")
    
    if not os.path.isdir(output_path):
        sys.stderr.write("Path for output file not found.\n")
        exit(1)

    lines_indices = {}     # A dictionary to keep index of where the content line where taken from the original file.
    content_lines = []     # A container for lines with the actual contents.

    # Extracting the lines with the actual contents.
    for index, line in enumerate(lines):
        current_line = Line(line)

        if current_line.is_content():
            lines_indices[index] = line
            content_lines.append(line)
            
    translator = Translator()

    print("Translating........")

    results = []
    translation_fails = 0
    for index, line in enumerate(content_lines):
        percent_translation = (index+1)/len(content_lines) * 100
        print(f"{percent_translation}% complete: ", end="")

        result = translator.translate(line, src=origin_language, dest=destination_language)
        results.append(result)

        if result.text == line:
            print("Failure!")
            translation_fails += 1
    print()
    
    if translation_fails > 0:
        sys.stderr.write(f"Failed to translate the file due to bad API response: {(translation_fails/len(content_lines)) * 100}% failure\n")
        exit(1)

    # Replacing the original contents with the translated contents.
    for index, line in enumerate(lines_indices):
        lines_indices[line] = results[index].text
    
    for index, line in enumerate(lines):
        if index in lines_indices:
            lines[index] = lines_indices[index] 

    # Saving the new subtitle file with the translations.
    with open(output_path + "output.srt", "w") as file:
        for line in lines:
            file.write(line)

    print("Done")
