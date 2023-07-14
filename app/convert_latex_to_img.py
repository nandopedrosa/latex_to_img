import csv
import re
import os
from sympy import preview
from unidecode import unidecode

REGEX_LATEX = r"\\\((.+?)\\\)"
DOCS_PATH = os.path.join(os.getcwd(), "app", "docs")
IMG_PATH = os.path.join(os.getcwd(), "app", "images")
PREFIX_LATEX = r"\("
SUFFIX_LATEX = r"\)"


# NOTA: EXECUTAR O PROGRAMA DO DIRETÓRIO RAIZ
# PARA EXECUTAR: python app/convert.py
def converter_do_csv():
    filepath_csv_anki = os.path.join(DOCS_PATH, "Anki_Export.csv")
    with open(filepath_csv_anki, encoding="utf-8") as arquivo_csv_anki:
        csv_reader = csv.reader(arquivo_csv_anki, delimiter=",")
        line_count = 1
        total_images = 0
        for row in csv_reader:
            if line_count > 1:  # ignore header
                # Pergunta/Resposta estão sempre na primeira coluna
                col = strip_tags(row[0])
                # Procuramos pela fórmula
                matches = re.findall(REGEX_LATEX, col)
                match_number = 1
                for match in matches:
                    formula = unidecode(PREFIX_LATEX + match + SUFFIX_LATEX)
                    print(
                        f"Tentando extrair imagem da linha {line_count}... fórmula: {formula}\n"
                    )
                    preview(
                        formula,
                        viewer="file",
                        filename=os.path.join(
                            IMG_PATH, f"{line_count}_{match_number}.png"
                        ),
                        dvioptions=["-D", "300"],
                    )
                    match_number += 1
                    total_images += 1
            line_count += 1
    print(
        f"Processamento realizado com sucesso. Foram extraídas {total_images} imagens."
    )


# -- Conversor de HTML tags ---
from io import StringIO
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


if __name__ == "__main__":
    converter_do_csv()
