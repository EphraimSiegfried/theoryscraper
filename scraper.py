
import os
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import re


def get_theory(page_layout, searchterm, delimiters, encountered_content):
    theory_list = []
    recording = False
    current_theory = {'name': '', 'content': ''}

    for element in page_layout:
        if isinstance(element, LTTextContainer):
            for text_line in element:
                line = text_line.get_text().strip()
                if line.startswith(searchterm):
                    recording = True
                    match = re.match(r'{}\s*\((.*?)\)'.format(searchterm), line)
                    if match:
                        name = match.group(1)
                        current_theory['name'] = name
                        current_theory['content'] = line[match.end():] + '\n'
                elif recording:
                    if line == '' or any([line.startswith(delimiter) for delimiter in delimiters]):
                        recording = False
                        if current_theory['content'] not in encountered_content:
                            encountered_content.add(current_theory['content'])
                            theory_list.append(current_theory)
                        current_theory = {'name': '', 'content': ''}
                    else:
                        current_theory['content'] += line + '\n'

    if recording:
        if current_theory['content'] not in encountered_content:
            theory_list.append(current_theory)

    return theory_list

def extract_theory_from_pdf_files(folder_path, search_terms):
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.pdf')])
    all_theory = {}
    encountered_content = set()

    for search_term in search_terms:
        all_theory[search_term] = []
        for pdf_file in pdf_files:
            for page_layout in extract_pages(os.path.join(folder_path, pdf_file)):
                theory = get_theory(page_layout, search_term, search_terms[search_term],encountered_content)
                all_theory[search_term].extend(theory)

    return all_theory

folder_path = input("Folder with slides: " )
search_terms = {"Definition":["Gabriele", "Proof", "Theorem"], "Theorem":["Proof", "Example","Gabriele","Question"]}
theory = extract_theory_from_pdf_files(folder_path, search_terms)
print(theory)
with open('theory.json', 'w') as f:
    json.dump(theory, f,indent=4)
