import os
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import re

def get_definitions(page_layout):
    definitions = []
    recording = False
    current_definition = {'name': '', 'content': ''}
    encountered_names = set()

    for element in page_layout:
        if isinstance(element, LTTextContainer):
            for text_line in element:
                line = text_line.get_text().strip()
                if line.startswith('Definition'):
                    recording = True
                    match = re.match(r'Definition\s*\((.*?)\)', line)
                    if match:
                        name = match.group(1)
                        if name not in encountered_names:
                            encountered_names.add(name)
                            current_definition['name'] = name
                            current_definition['content'] = line[match.end():] + '\n'
                        else:
                            recording = False
                elif recording:
                    if line == '' or line.startswith('Gabriele') or line.startswith('Example') or line.startswith('Theorem'):
                        recording = False
                        definitions.append(current_definition)
                        current_definition = {'name': '', 'content': ''}
                    else:
                        current_definition['content'] += line + '\n'

    if recording:
        definitions.append(current_definition)

    return definitions

def extract_definitions_from_pdf_files(folder_path):
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.pdf')])
    all_definitions = []

    for pdf_file in pdf_files:
        for page_layout in extract_pages(os.path.join(folder_path, pdf_file)):
            definitions = get_definitions(page_layout)
            all_definitions.extend(definitions)

    return all_definitions

folder_path = input("Folder with slides" )
definitions = extract_definitions_from_pdf_files(folder_path)

with open('definitions.json', 'w') as f:
    json.dump(definitions, f,indent=4)

