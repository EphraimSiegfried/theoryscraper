
import json

def generate_html_cheatsheet(definitions, filename):
    with open(filename, 'w') as f:
        f.write('<html><head>\n')
        f.write('<style>\n')
        f.write('body { font-size: 10px; }\n')
        f.write('.columns { column-count: 3; }\n')
        f.write('@media print { @page { size: A4; } }\n')
        f.write('</style>\n')
        f.write('</head><body><div class="columns">\n')
        for definition in definitions:
            name, body = definition['name'], definition['content']
            f.write('<p><b>{}</b>{}</p>\n'.format(name, body))
        f.write('</div></body></html>\n')

# Load definitions from JSON file
with open('definitions.json', 'r') as f:
    definitions = json.load(f)

generate_html_cheatsheet(definitions, 'cheatsheet.html')
