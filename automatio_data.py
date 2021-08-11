import json
import pandas as pd
#{"Rg_Paciente":x,"nome":nome,"endereço":adress,"sexo":sexo}
#fazer uma automação para montar o json
def escrever_json(dados):
    with open('dados_banco.json', 'w') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4, separators=(',', ':'))
def ler_json(arq_json):
    with open(arq_json, 'r', encoding='utf8') as f:
        return json.load(f)
dados = pd.read_excel('/home/luiz/Desktop/git/codepy/nomes.xlsx',sheet_name='Folha1')
ditt = {}
ditt_list = []
for i in range(0,40):
    Rg_Paciente = str(dados["Rg_Paciente"][i])
    nome = dados["nome"][i]
    endereço = dados["endereço"][i]
    sexo = dados["sexo"][i]
    ditt = {"Rg_Paciente":Rg_Paciente,
            "nome":nome,"endereço":endereço,
            "sexo":sexo}
    ditt_list.append(ditt)
escrever_json(ditt_list)