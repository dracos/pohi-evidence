import glob
import json
import os
import subprocess

os.chdir('evidence/process')

def process_evidence():
    for file in sorted(glob.glob('*.pdf')):
        if file == 'POL00174423.pdf': continue  # corrupt

        file_base = file.replace(".pdf", "")
        file_txt = file_base + ".txt"

        if not os.path.exists(file_base + '-1.png') and not os.path.exists(file_base + '-01.png') and not os.path.exists(file_base + '-001.png'):
            print(f"Running pdftocairo on {file}")
            subprocess.run(['pdftocairo', '-png', file])

    for file in sorted(glob.glob('*.png')):
        file_base = file.replace(".png", "")
        file_txt = file_base + ".txt"
        if not os.path.exists(file_txt):
            print(f'parsing {file} with tesseract')
            subprocess.run(['tesseract', file, file_base])

    for file in sorted(glob.glob('*.pdf')):
        file_base = file.replace(".pdf", "")
        file_txt = '../' + file_base + ".txt"
        if not os.path.exists(file_txt) and (os.path.exists(file_base + '-1.txt') or os.path.exists(file_base + '-01.txt') or os.path.exists(file_base + '-001.txt')):
            l = sorted(glob.glob(file_base + '-*.txt'))
            with open(file_txt, "w") as outfile:
                subprocess.run(['cat'] + l, stdout=outfile)
            file_rst = file_txt.replace(".txt", ".rst")
            with open(file_rst, 'w') as out:
                url, title = META[file]
                out.write(title + '\n' + '=' * len(title) + '\n\n')
                out.write(f'.. literalinclude:: {file_base}.txt\n')

    for file in sorted(glob.glob('*.pdf')):
        if file == 'POL00174423.pdf': continue  # corrupt

        file_base = file.replace(".pdf", "")
        file_txt = '../' + file_base + ".txt"
        file_rst = '../' + file_base + ".rst"
        if os.path.exists(file_txt) and os.path.exists(file_rst):
            print("PDF has txt and rst")
        elif os.path.exists(file_rst):
            print("PDF has rst")
        elif os.path.exists(file_txt):
            print("PDF has txt")
        else:
            print("PDF has neither")

META = json.load(open('../../data/evidence-pdf-metadata.json'))
process_evidence()
