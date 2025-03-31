import os
import sys
from datetime import datetime
import re

def parse_args():
    args = sys.argv
    
    if len(args) < 3:
        print("ERROR: Invalid number of arguments. Must be: start=%m/%Y end=%m/%Y")
        exit(1)
    
    start = datetime.strptime("01/" + args[1].split("=")[-1], "%d/%m/%Y")
    end = datetime.strptime("01/" + args[2].split("=")[-1], "%d/%m/%Y")
    
    return start, end

def is_unnecessary_line(row):
    return (row == "A ISTOÉ PUBLICAÇÕES LTDA é um portal digital independente e sem vinculação editorial e societária com a EDITORA TRES COMÉRCIO DE PUBLICACÕES LTDA (recuperação judicial). Informamos também que não realizamos cobranças e que também não oferecemos cancelamento do contrato de assinatura da revista impressa de nome ISTOÉ, tampouco autorizamos terceiros a fazê-lo, nos responsabilizamos apenas pelo conteúdo digital “https://istoe.com.br” e seus respectivos sites."
            or row == "A ISTOE GERAL é uma editoria independente sem vinculação editorial e societária com A ISTOÉ PUBLICAÇÕES LTDA."
            or row == "Em"
            or row == "Atualizado em"
            or row == "Brasil"
            or row == "Política de Privacidade"
            or row == "Newsletter"
            or row == "Da Redação"
            or row == "Notícias"
            or row == "Opinião"
            or row == "Mundo"
            or row == "Esportes"
            or bool(re.fullmatch(r"\d{2}/\d{2}/\d{2,4} - \d{2}h\d{2}min", row)))

def main():
    start_date, end_date = parse_args()
    
    # --
    # Defining all directors paths
    # --
    final_news_dir = os.path.join("data", "final-news")
    news_dir = os.path.join("data", "news")

    files = os.listdir(news_dir)

    os.makedirs(final_news_dir, exist_ok=True)

    # --
    # Cleaning each line for each file
    # We will turn all letters into lower case and mantain the brazilian portuguese vocabulary letters
    # --
    new_lines = []

    for file in files:
        month_title = file.split(".")[0].split("-")[1]
        
        with open(os.path.join(news_dir, file), 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            if is_unnecessary_line(line.strip()):
                if line.strip() == "Em":
                    new_lines.append('\n')
                continue
            
            l = line.strip()
            l = l.lower()
            l = re.sub(r'[^a-zA-Z0-9áàâãéêíóôõúçüêè ]', ' ', l)
            l = l.strip()
            
            new_lines.append(l)
        
        with open(os.path.join(final_news_dir, f"fnews-{month_title}.txt"), 'w') as f:
            f.write('\n'.join(new_lines))
        
        new_lines.clear()


if __name__ == "__main__":
    main()