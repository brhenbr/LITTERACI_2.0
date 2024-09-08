import csv
import random
from datetime import datetime, timedelta

def generate_timestamp():
    start_date = datetime(2024, 9, 8)
    end_date = datetime(2024, 9, 15)
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )

def generate_situacao_atual():
    return '"' + ";".join(str(random.randint(1, 10)) for _ in range(13)) + '"'

def generate_situacao_futura():
    return '"' + ";".join(str(random.randint(4, 10)) for _ in range(4)) + '"'

def generate_opinioes():
    opinioes = [
        "A LITTERACI ajudaria minha Unidade de Informação a se manter atual e ativa",
        "A minha Unidade de Informação precisa dessa solução para aprimorar a sua forma de atendimento ao usuário",
        "Eu e/ou a minha Unidade de Informação estaria disposto(a) a conhecer com mais detalhes a LITTERACI",
        "Eu e/ou a minha Unidade de Informação estaria disposto(s) a adquirir a solução LITTERACI"
    ]
    return ";".join(random.sample(opinioes, k=random.randint(1, 4)))

def generate_data(num_entries, ui_types):
    data = []
    for i in range(num_entries):
        ui_type = random.choice(ui_types)
        entry = [
            generate_timestamp().strftime("%Y-%m-%d %H:%M:%S"),
            f"user{i+1}",
            ui_type,
            generate_situacao_atual(),
            generate_situacao_futura(),
            generate_opinioes(),
            f"user{i+1}@example.com" if random.random() > 0.1 else ""  # 10% chance of empty email
        ]
        data.append(entry)
    return data

# Tipos de UI
ui_types = [
    "Biblioteca (setor público)",
    "Biblioteca (setor privado)",
    "Arquivo (setor público)",
    "Arquivo (setor privado)",
    "Museu (setor público)",
    "Museu (setor privado)",
    "Outro tipo de Unidade de Informação"
]

# Gerar dados
data = []
data.extend(generate_data(1000, ui_types[:2]))  # 1000 entradas para bibliotecas
for ui_type in ui_types[2:]:
    data.extend(generate_data(100, [ui_type]))  # 100 entradas para cada outro tipo de UI

# Embaralhar os dados
random.shuffle(data)

# Escrever dados em um arquivo CSV
with open("dados_teste_litteraci.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["TimeStamp", "Origin", "Tipo de UI", "Situacao Atual UI", "Situacao Futura UI", "Opinioes UI", "Dados Contato"])
    writer.writerows(data)

print("Arquivo 'dados_teste_litteraci.csv' gerado com sucesso!")