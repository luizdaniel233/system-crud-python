import mysql.connector
from mysql.connector import Error
import os
import json
con = mysql.connector.connect(host='localhost',database='agenda',user='root',password='21092001')
os.system("clear")
if con.is_connected():
    db_info = con.get_server_info()
    print("Conectado ao servidor MySQL versão ",db_info)
    cursor = con.cursor()
    print("1-Consulta")
    print("2-Register")
    print("3-Delete")
    print("4-Edit")
    print("5-Importar Dados em Massa(Json)")
    print("6-Exit")
    firstc = int(input("Type command:"))
    while(firstc != 6):#sentinela para sair do loop     print("5-Exit")
        if firstc == 1:
            command = input("Type your search:")
            cursor.execute(command)
            linha = cursor.fetchall()
            print("Número total de registros retornados: ", cursor.rowcount)
            for row in linha:
                print("Dados Disponíveis = (%s, %s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
        else:
            if firstc == 2:
                try:
                    rg = int(input("Rg_paciente:"))
                    name = input("name:").upper().replace(".","")
                    adress = input("adress:").upper()
                    sexo = input("sexo:").upper()
                    cursor.execute(f'INSERT INTO paciente(Rg_Paciente,nome,endereço,sexo) VALUES ("{rg}","{name}","{adress}","{sexo}")')
                    con.commit()
                    print("Inserted",cursor.rowcount,"row(s) of data.")
                except Error as e:
                    print("Primary Key Error", e)
            else:
                if firstc == 3:
                    delete = 0
                    while(delete != 1):
                        cursor.execute("SELECT * FROM paciente")
                        linha = cursor.fetchall()
                        print("Número total de registros retornados: ", cursor.rowcount)
                        for row in linha:
                            print("Dados = (%s, %s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
                        id_delete = int(input("Qual o id que voce deseja apagar?\n"))
                        cursor.execute(f'SELECT * FROM paciente WHERE Rg_Paciente = {id_delete}')
                        linha = cursor.fetchall()
                        for row in linha:
                            print("Dados que deseja Apagar = (%s, %s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
                        conf = input("Confirma?")
                        if conf == 'N' or conf == 'n' or conf == "nao" or conf == "NAO" or conf == "Não" or conf == "NÂO":
                            delete = 0
                            menu = input("Voltar p/ menu?")
                        else:
                            cursor.execute(f'DELETE FROM paciente WHERE Rg_Paciente = {id_delete}')
                            delete = 1
                            break
                        if menu == 's' or menu == 'S' or menu == "Sim" or menu == "SIM":
                            break    
                else:
                    if firstc == 4:
                        cursor.execute("SELECT * FROM paciente")
                        linha = cursor.fetchall()
                        print("Número total de registros retornados: ", cursor.rowcount)
                        for row in linha:
                            print("Data row = (%s, %s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
                        id_edit = int(input("Qual o id que voce deseja editar?\n"))
                        print("1-nome,2-endereço,3-sexo")
                        command_edit = int(input("command:\n"))
                        if command_edit == 1:
                            name = input("Nome que vai setar:")
                            cursor.execute(f'UPDATE paciente SET nome = "{name}" WHERE Rg_Paciente = {id_edit}')
                            cursor.execute(f'SELECT * FROM paciente WHERE Rg_Paciente = {id_edit}')
                            linha = cursor.fetchall()
                            for row in linha:
                                print("Data Edited = (%s, %s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
                        else:
                            if command_edit == 2:
                                adress = input("Endereço que vai ser setar:")
                                cursor.execute(f'UPDATE paciente SET endereço = "{adress}" WHERE Rg_Paciente = {id_edit}')
                                linha = cursor.fetchall()
                                for row in linha:
                                    print("Data Edited = (%s, %s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
                            else:
                                if command_edit == 3:
                                    sexo = input("Sexo que vai ser setar:")
                                    cursor.execute(f'UPDATE paciente SET sexo = "{sexo}" WHERE Rg_Paciente = {id_edit}')
                                    linha = cursor.fetchall()
                                    for row in linha:
                                        print("Data Edited = (%s, %s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
                    else:
                        if firstc == 5:
                            print("Format the json:[{'Rg_Paciente':'xxxxx','nome':'xxxxx','endereço':'xxxxx','sexo':'x',...}]")
                            name_archive = input("name of arquive json,not write '.json':\n")
                            if ".json" not in name_archive:
                                name_archive += ".json"
                            with open(name_archive, 'r',encoding='UTF8') as f:
                                archive =  json.load(f)
                            for i in range(len(archive)):
                                #archive[i]
                                #cursor.execute(f'INSERT INTO paciente(Rg_Paciente,nome,endereço,sexo) VALUES ("{rg}","{name}","{adress}","{sexo}")'
                                rg = int(archive[i]["Rg_Paciente"])
                                name = archive[i]["nome"]
                                adress = archive[i]["endereço"]
                                sexo = archive[i]["sexo"]
                                query = f'INSERT INTO paciente(Rg_Paciente,nome,endereço,sexo) VALUES ("{rg}","{name}","{adress}","{sexo}")'
                                cursor.execute(query)
                                con.commit()
                                db_info = con.get_server_info()
                                print(f"Inserted your info,in the database,V:{db_info}")
                                linha = cursor.fetchall()

                                #print(query)
                        else:
                            if firstc > 6:
                                print("---COMMAND NOT FOUND!!!---")
        print("\n")
        print("1-Consulta")
        print("2-Register")
        print("3-Delete")
        print("4-Edit")
        print("5-Importar Dados em Massa(Json)")
        print("6-Exit")
        firstc = int(input("Type command:\n"))
        
'''
firstc = int(input("Type command:"))
    #print("Conectado ao banco de dados ",linha)
if con.is_connected():
    cursor.close()
    con.close()
    print("Conexão ao MySQL foi encerrada")
'''