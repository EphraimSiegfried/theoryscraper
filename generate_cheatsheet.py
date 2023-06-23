
import json

def generate_html_cheatsheet(theory, filename):
    with open(filename, 'w') as f:
        f.write('<html><head>\n')
        f.write('<style>\n')
        f.write('body { font-size: 10px; }\n')
        f.write('.columns { column-count: 3; }\n')
        f.write('@media print { @page { size: A4; } }\n')
        f.write('</style>\n')
        f.write('</head><body>\n')

        for searchterm, definitions in theory.items():
            f.write('<h1>{}s</h1>\n'.format(searchterm))
            f.write('<div class="columns">\n')
            for definition in definitions:
                name, body = definition['name'], definition['content']
                f.write('<p><b>{}</b>{}</p>\n'.format(name, body))
            f.write('</div>\n')

        f.write('</body></html>\n')

# Load theory from JSON file
with open('theory.json', 'r') as f:
    theory = json.load(f)

generate_html_cheatsheet(theory, 'cheatsheet.html')
