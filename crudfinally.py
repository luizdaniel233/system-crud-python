#!/usr/bin/python3.6

import PySimpleGUI as sg
import mysql.connector
from mysql.connector import Error
import os
import json
import qrcode
#-----conexão BD -----
con = mysql.connector.connect(host='xxxxx',database='xxx',user='xxxxx',password='xxxxx')
os.system("clear")
if con.is_connected():
    db_info = con.get_server_info()
    print("Conectado ao servidor MySQL versão ",db_info)
    cursor = con.cursor()
def tela_cadastro():
    sg.change_look_and_feel('Reddit')
    #layout 
    layout = [
                [sg.Text('Rg do Paciente:',size=(50,0)),sg.Input(size=(70,0),key ='rg')],
                [sg.Text('Nome:',size=(50,0)),sg.Input(size=(70,0),key ='nome')],
                [sg.Text('Endereço:',size=(50,0)),sg.Input(size=(70,0),key ='endereço')],
                [sg.Text('Sexo:',size=(50,0)),sg.Input(size=(70,0),key ='sexo')],
                [sg.Button("Export QR Code")],
                [sg.Button('Voltar')],[sg.Button('Enviar Dados')]
                ]
    #janela
    return sg.Window("Dados do Usuário",layout = layout,finalize=True)

def tela_consulta():
    sg.theme('Reddit')
    #layout 
    
    layout = [[sg.Text("Digite o RG:")],
              [sg.Text(),sg.Input(size=(70,0),key ='rg')],
              [sg.Button("Voltar")],[sg.Button("Go")],
              
             ]
    return sg.Window("Consulta",layout = layout,finalize = True)
def tela_consulta_bd(line):
    sg.theme('Reddit')
    #layout 
    cursor.execute(f'SELECT * FROM paciente WHERE Rg_Paciente = {line}')
    linha = cursor.fetchall()
    for row in linha:
        dados = row
    layout = [[sg.Text(f'Rg:{dados[0]}')],
              [sg.Text(f'Nome:{dados[1]}')],
              [sg.Text(f'Endereço:{dados[2]}')],
              [sg.Text(f'Sexo:{dados[3]}')],
              #[sg.Button("Export QR Code")],
              [sg.Button("Voltar")]
             ]
    
    return sg.Window("Consulta",layout = layout,finalize = True)
def tela_consulta_edit(Rg_Paciente):
    sg.theme('Reddit')
    valor = int(Rg_Paciente)
    cursor.execute(f'SELECT * FROM paciente WHERE Rg_Paciente = {valor}')
    linha = cursor.fetchall()
    for row in linha:
        dados = row
    layout = [[sg.Text(f'Rg:{dados[0]}',key ='Rg_Paciente')],
              [sg.Text(f'Nome:{dados[1]}'),sg.Input(size=(40,0),key ='nome')],
              [sg.Text(f'Endereço:{dados[2]}'),sg.Input(size=(40,0),key ='endereço')],
              [sg.Text(f'Sexo:{dados[3]}'),sg.Input(size=(40,0),key ='sexo')],
              [sg.Checkbox('Nome', default=False, key="nome_check")],
              [sg.Checkbox('Endereço', default=False, key="adress_check")],
              [sg.Checkbox('Sexo', default=False, key="sexo_check")],
              [sg.Button("Voltar")],[sg.Button("Edit")],[sg.Button("Menu")],
              [sg.Button("Export QR Code")],
             ]
    return sg.Window("Consulta",layout = layout,finalize = True)

def tela_edit():
    sg.theme('Reddit')
    #layout 
    layout = [[sg.Text("Digite o Rg que deseja editar")],
              [sg.Text(),sg.Input(size=(70,0),key ='Rg_Paciente')],
              [sg.Button("Voltar")],[sg.Button("Consulta")],
              
             ]
    return sg.Window("Editar",layout = layout,finalize = True)

def tela_delete():
    sg.theme('Reddit')
    #layout 
    layout = [[sg.Text("Digite o Rg que deseja Deletar")],
              [sg.Text(),sg.Input(size=(70,0),key ='deletado')],
              [sg.Button("Export QR Code")],
              [sg.Button("Voltar")],[sg.Button("Delete")]
             ]
    return sg.Window("Deletar",layout = layout,finalize = True)

def tela_sair():
    sg.theme('Reddit')
    #layout 
    layout = [[sg.Text("Saindo...")]]      
    return sg.Window("Sair",layout = layout,finalize = True)

def tela_main():
    sg.theme('Reddit')
    layout = [[sg.Button('Consultar',size=(60,2))],
                [sg.Button('Registrar',size=(60,2))],
                [sg.Button('Deletar',size=(60,2))],
                [sg.Button('Editar',size=(60,2))],
                [sg.Button('Sair',size=(60,2))]
                ]
    
    return sg.Window("Hospital",layout = layout,finalize = True)

janela1,janela2 = tela_main(),None

while True:
    window,event,values = sg.read_all_windows()
    if window == janela1  and event == sg.WIN_CLOSED:
        break

    if window == janela1  and event == "Sair":
        break

    if window == janela1 and event == 'Registrar':
        janela2 = tela_cadastro()
        janela1.hide()

    if window == janela1 and event == 'Consultar':
        janela2 = tela_consulta()
        janela1.hide()
        
    if window == janela1 and event == 'Editar':
        janela2 = tela_edit()
        janela1.hide()

    if window == janela1 and event == 'Deletar':
        janela2 = tela_delete()
        janela1.hide()

    if window == janela2 and event == 'Voltar':
        janela2.hide()
        janela1.un_hide()
    
    if window == janela2 and event == 'Export QR Code':
        url = values
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit = True)

        img = qr.make_image(fill_color="black", back_color="white")
        #img.save('myqrlink.png')
        img.show()
        

    if window == janela2 and event == 'Enviar Dados':
        rg = values['rg']
        name = values['nome'].upper().replace(".","")
        adress = values['endereço'].upper()
        sexo = values['sexo'][0].upper()
        cursor.execute(f'INSERT INTO paciente(Rg_Paciente,nome,endereço,sexo) VALUES ("{rg}","{name}","{adress}","{sexo}")')
        con.commit()
        janela2.hide()
        janela1.un_hide()
        #print("Inserted",cursor.rowcount,"row(s) of data.")
    if window == janela2 and event == 'Go':
        line_command = values['rg']
        janela2 = tela_consulta_bd(line_command)

    if window == janela2 and event == 'Delete':
        id_delete = values['deletado']
        cursor.execute(f'DELETE FROM paciente WHERE Rg_Paciente = {id_delete}')
        con.commit()
        janela2.hide()
        janela1.un_hide()

    if window == janela2 and event == 'Consulta':
        id_consult = values['Rg_Paciente']
        janela2 = tela_consulta_edit(id_consult)
        
    if window == janela2 and event == 'Edit':
        #print(id_edit)
        nome_edit = values['nome']
        adress_edit = values['endereço']
        sexo_edit = values['sexo']
        if values['nome_check'] == True:
            cursor.execute(f'UPDATE paciente SET nome = "{nome_edit}" WHERE Rg_Paciente = {id_consult}')
            con.commit()
        else:
            if values['sexo_check'] == True:
                cursor.execute(f'UPDATE paciente SET sexo = "{sexo_edit}" WHERE Rg_Paciente = {id_consult}')
                con.commit()
            else:
                if values['endereço_check'] == True:
                    cursor.execute(f'UPDATE paciente SET endereço = "{adress_edit}" WHERE Rg_Paciente = {id_consult}')
                    con.commit()
    if window == janela2 and event == 'Menu':     
        janela2.hide()
        janela1.un_hide()


