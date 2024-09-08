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
    return [random.randint(1, 7) for _ in range(13)]

def generate_situacao_futura():
    return [random.randint(5, 10) for _ in range(4)]

def generate_opinioes():
    opinioes = [
        "A LITTERACI ajudaria minha Unidade de Informação a se manter atual e ativa",
        "A minha Unidade de Informação precisa dessa solução para aprimorar a sua forma de atendimento ao usuário",
        "Eu e/ou a minha Unidade de Informação estaria disposto(a) a conhecer com mais detalhes a LITTERACI",
        "Eu e/ou a minha Unidade de Informação estaria disposto(s) a adquirir a solução LITTERACI"
    ]
    return ";".join(random.sample(opinioes, k=random.randint(1, 4)))

def generate_data(num_entries, ui_type):
    data = []
    for i in range(num_entries):
        entry = {
            "TimeStamp": generate_timestamp().strftime("%Y-%m-%d %H:%M:%S"),
            "Origin": f"user{i+1}",
            "Tipo de UI": ui_type,
            "Situacao Atual UI": ";".join(map(str, generate_situacao_atual())),
            "Situacao Futura UI": ";".join(map(str, generate_situacao_futura())),
            "Opinioes UI": generate_opinioes(),
            "Dados Contato": f"user{i+1}@example.com"
        }
        data.append(entry)
    return data

# Gerar dados
data = []
data.extend(generate_data(500, "Biblioteca (setor público)"))
data.extend(generate_data(500, "Biblioteca (setor privado)"))
data.extend(generate_data(100, "Arquivo (setor público)"))
data.extend(generate_data(100, "Arquivo (setor privado)"))
data.extend(generate_data(100, "Museu (setor público)"))
data.extend(generate_data(100, "Museu (setor privado)"))
data.extend(generate_data(100, "Outro tipo de Unidade de Informação"))

# Embaralhar os dados
random.shuffle(data)

# Escrever dados em um arquivo CSV
with open("dados_teste_litteraci.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["TimeStamp", "Origin", "Tipo de UI", "Situacao Atual UI", "Situacao Futura UI", "Opinioes UI", "Dados Contato"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("Arquivo 'dados_teste_litteraci.csv' gerado com sucesso!")