import random as rd
import time

import pandas as pd
import pyautogui
import pyperclip
import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup

suppliers_list = []

list_themes = sg.theme_list()
sg.theme(rd.choice(list_themes))

layout = [
    [sg.Text("Enter the product name and description for the supplier:")],
    [sg.Text("Product name", size=(30, 1)), sg.InputText(key="product_name")],
    [sg.Text("Message to seller", size=(30, 1)), sg.InputText(key="seller_message")],
    [
        sg.Text("How many suppliers?", size=(30, 1)),
        sg.Spin([i for i in range(0, 40)], initial_value=0, key="suppliers_number"),
    ],
    [sg.Text("Destination folder: "), sg.FolderBrowse(button_text="Search", key="save")],
    [sg.Text("Enter the name of your browser", size=(25, 1)), sg.InputText(key="nome_navegador")],
    [
        [sg.Text("Contato automático?", size=(15, 1))],
        sg.Radio("Sim - Processo automático.", "RADIO", key="sim_automatico", enable_events=True),
        sg.Radio("Não - Dados em uma planilha.", "RADIO"),
    ],
    [sg.Submit(button_text="Iniciar", key="Submit"), sg.Button("Limpar"), sg.Exit(button_text="Sair", key="Exit")],
]
window = sg.Window(" Busca de fornecedores - Alibaba", layout, size=(500, 300))


def Clear_input():
    for key in values:
        window[key]("")
    return None


def Attach_file():

    alt_anx = rd.uniform(1, 2)

    anexar = pyautogui.locateOnScreen("media/anexar.PNG", confidence=0.7)
    pyautogui.click(anexar)
    time.sleep(alt_anx)

    pyautogui.click(x=374, y=132)
    time.sleep(1)

    abrir = pyautogui.locateOnScreen("media/abrir.png", confidence=0.7)
    pyautogui.click(abrir)
    time.sleep(alt_anx)


def Auto_contact():

    url_base = "https://www.alibaba.com/corporations/"
    nome_produto = values["product_name"]
    mensagem_vendedor = values["seller_message"]
    numero_repeticoes = values["suppliers_number"]

    response_site_fornecedor = requests.get(url_base + nome_produto + ".html")
    content_site_fornecedor = response_site_fornecedor.content
    site_produto = BeautifulSoup(content_site_fornecedor, "html.parser")
    dados_fornecedores = site_produto.findAll("div", attrs={"class": "item-main"})

    alt_01 = rd.uniform(0.5, 1.5)
    alt_02 = rd.uniform(5, 6)
    alt_mvr = rd.uniform(200, 600)

    # abrir navegador
    pyautogui.press("winleft")
    time.sleep(1)

    pyautogui.write(values["nome_navegador"])
    time.sleep(0.5)

    pyautogui.press("enter")
    time.sleep(1)

    for index, dados_fornecedor in zip(range(int(numero_repeticoes)), dados_fornecedores):

        nome_empresa = dados_fornecedor.find("a", attrs={"target": "_blank"})
        principais_produtos = dados_fornecedor.find("div", attrs={"class": "value ellipsis ph"})
        contato_direto = dados_fornecedor.find("a", attrs={"class": "button csp"})

        if contato_direto:

            suppliers_list.append(
                [nome_empresa.text, principais_produtos.text, nome_empresa["href"], contato_direto["href"]]
            )
            time.sleep(alt_01)

            # abrir nova aba

            pyautogui.hotkey("ctrl", "t")
            time.sleep(alt_01)

            # Concertando bug da biblioteca PyautoGUI
            pyperclip.copy(contato_direto["href"])

            # escrever endereco para contato direto com fornecedor

            pyautogui.hotkey("ctrl", "v")
            time.sleep(alt_01)
            # carregar endereco web

            pyautogui.press("enter")
            time.sleep(alt_02)

            # selecionar caixa de texto

            pyautogui.press("tab", presses=2)

            # escrever a mensagem padrao

            pyautogui.write(mensagem_vendedor)
            time.sleep(alt_01)

            # Attach_file()

            # enviar pedido de cotação
            enviar_cotacao = pyautogui.locateOnScreen("media/send_inquiry.png", confidence=0.8)
            pyautogui.click(enviar_cotacao)
            pyautogui.moveTo(alt_mvr, alt_mvr, duration=alt_01)

        else:
            suppliers_list.append([nome_empresa.text, principais_produtos.text, nome_empresa["href"], ""])

    Collect_data()


def Collect_data_only():

    url_base = "https://www.alibaba.com/corporations/"
    nome_produto = values["product_name"]
    mensagem_vendedor = values["seller_message"]
    numero_repeticoes = values["suppliers_number"]

    response_site_fornecedor = requests.get(url_base + nome_produto + ".html")
    content_site_fornecedor = response_site_fornecedor.content
    site_produto = BeautifulSoup(content_site_fornecedor, "html.parser")
    dados_fornecedores = site_produto.findAll("div", attrs={"class": "item-main"})

    for index, dados_fornecedor in zip(range(int(numero_repeticoes)), dados_fornecedores):

        nome_empresa = dados_fornecedor.find("a", attrs={"target": "_blank"})
        principais_produtos = dados_fornecedor.find("div", attrs={"class": "value ellipsis ph"})
        contato_direto = dados_fornecedor.find("a", attrs={"class": "button csp"})

        if contato_direto:

            suppliers_list.append(
                [nome_empresa.text, principais_produtos.text, nome_empresa["href"], contato_direto["href"]]
            )

        else:
            suppliers_list.append([nome_empresa.text, principais_produtos.text, nome_empresa["href"], ""])

    Collect_data()


def Collect_data():

    save_arquivo = values["save"]
    nome_produto = values["product_name"]
    dados_coletados = pd.DataFrame(
        suppliers_list, columns=["Nome da empresa", "Principais produtos", "site", "Contato Direto"]
    )
    dados_coletados.to_excel(save_arquivo + "\\" + "fornecedores_de_" + str(nome_produto) + ".xlsx", index=False)


while True:
    try:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Limpar":
            Clear_input()
        if event == "Submit":
            sg.popup("A busca esta sendo realizada.")
            Clear_input()
            while True:
                if values["sim_automatico"]:
                    inicio = time.time()
                    Auto_contact()
                    fim = time.time()
                    sg.popup(f"Fornecedores contatados com sucesso!\n\nTempo de execução: {fim - inicio} Segundos")
                    break
                else:
                    inicio = time.time()
                    Collect_data_only()
                    fim = time.time()
                    sg.popup(f"Coleta realizada com sucesso!\n\nTempo de execução: {fim - inicio} Segundos")
                    break
    except ValueError:
        sg.popup("Ocorreu algo errado. Tente novamente.")
window.close()
