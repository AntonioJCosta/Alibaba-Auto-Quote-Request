import requests
from bs4 import BeautifulSoup
import pandas as pd
import pyautogui, time
import PySimpleGUI as sg
import pyperclip
import random as rd

lista_fornecedores = []

lista_de_temas = sg.theme_list()
sg.theme(rd.choice(lista_de_temas))

layout = [
    [sg.Text('Digite o nome do produto e a descrição para o fornecedor:')],
    [sg.Text('Nome do produto', size=(30,1)), sg.InputText(key='nome_produto01')],
    [sg.Text('Mensagem para o vendedor', size=(30,1)), sg.InputText(key='mensagem_vendedor01')],
    [sg.Text('Número de fornecedores', size=(30,1)), sg.Spin([i for i in range(0,40)], initial_value=0, key='numero_repeticoes01')],
    [sg.Text("Selecione a pasta destino: "), sg.FolderBrowse(button_text='Procurar',key="salvar")],
    [sg.Text('Digite o nome de seu navegador', size=(25,1)), sg.InputText (key='nome_navegador')],[
    [sg.Text('Contato automático?', size=(15,1))],
                sg.Radio('Sim - Processo automático.', "RADIO",  key='sim_automatico', enable_events = True),
                sg.Radio('Não - Dados em uma planilha.',"RADIO")],
    [sg.Submit(button_text= 'Iniciar', key = 'Submit'), sg.Button('Limpar'), sg.Exit(button_text = 'Sair', key = 'Exit')]
]
window = sg.Window(' Busca de fornecedores - Alibaba',  layout, size = (500,300))

def Limpar_input():
    for key in values:
        window[key]('')
    return None

def Anexar_arquivo():
    
    alt_anx = rd.uniform(1,2)
    
    anexar = pyautogui.locateOnScreen("media/anexar.PNG", confidence=0.7)
    pyautogui.click(anexar)
    time.sleep(alt_anx)
    
    pyautogui.click(x =374, y = 132)
    time.sleep(1)
    
    abrir = pyautogui.locateOnScreen("media/abrir.png", confidence=0.7)
    pyautogui.click(abrir)
    time.sleep(alt_anx)

def contato_automatico():
        
    url_base = 'https://www.alibaba.com/corporations/'
    nome_produto = values['nome_produto01']
    mensagem_vendedor = values['mensagem_vendedor01']
    numero_repeticoes = values['numero_repeticoes01']
    
    response_site_fornecedor = requests.get(url_base + nome_produto + ".html") 
    content_site_fornecedor = response_site_fornecedor.content
    site_produto = BeautifulSoup(content_site_fornecedor, 'html.parser')
    dados_fornecedores = site_produto.findAll('div', attrs={'class': 'item-main'})
    
    alt_01 = rd.uniform(0.5, 1.5)
    alt_02 = rd.uniform(5, 6)
    alt_mvr = rd.uniform(200, 600)
    
    #abrir navegador
    pyautogui.press('winleft')
    time.sleep(1)
    
    pyautogui.write(values['nome_navegador'])
    time.sleep(0.5)
    
    pyautogui.press('enter')
    time.sleep(1)
        
    for index, dados_fornecedor in zip(range(int(numero_repeticoes)), dados_fornecedores):
        
        nome_empresa = dados_fornecedor.find('a', attrs = {'target' : '_blank' })
        principais_produtos = dados_fornecedor.find('div', attrs = {'class' : 'value ellipsis ph'})
        contato_direto = dados_fornecedor.find('a', attrs = {'class' : 'button csp'})
        
        if (contato_direto):
            
            lista_fornecedores.append([nome_empresa.text, principais_produtos.text, nome_empresa['href'], contato_direto['href']])
            time.sleep(alt_01)
            
            #abrir nova aba
            
            pyautogui.hotkey('ctrl','t')
            time.sleep(alt_01)
            
            #Concertando bug da biblioteca PyautoGUI
            pyperclip.copy(contato_direto['href'])
            
            #escrever endereco para contato direto com fornecedor
            
            pyautogui.hotkey('ctrl','v')
            time.sleep(alt_01)
            #carregar endereco web
            
            pyautogui.press('enter')
            time.sleep(alt_02)
            
            #selecionar caixa de texto
            
            pyautogui.press('tab', presses = 2)
            
            #escrever a mensagem padrao
            
            pyautogui.write(mensagem_vendedor)
            time.sleep(alt_01)
            
            #Anexar_arquivo()
            
            #enviar pedido de cotação
            enviar_cotacao = pyautogui.locateOnScreen('media/send_inquiry.png', confidence=0.8)
            pyautogui.click(enviar_cotacao)
            pyautogui.moveTo(alt_mvr, alt_mvr, duration = alt_01)
            
        else:
            lista_fornecedores.append([nome_empresa.text, principais_produtos.text, nome_empresa['href'], ''])
                        
    coleta_de_dados()
    
def apenas_coleta():
    
    url_base = 'https://www.alibaba.com/corporations/'
    nome_produto = values['nome_produto01']
    mensagem_vendedor = values['mensagem_vendedor01']
    numero_repeticoes = values['numero_repeticoes01']
    
    response_site_fornecedor = requests.get(url_base + nome_produto + ".html") 
    content_site_fornecedor = response_site_fornecedor.content
    site_produto = BeautifulSoup(content_site_fornecedor, 'html.parser')
    dados_fornecedores = site_produto.findAll('div', attrs={'class': 'item-main'})
        
        
    for index, dados_fornecedor in zip(range(int(numero_repeticoes)), dados_fornecedores):
        
        nome_empresa = dados_fornecedor.find('a', attrs = {'target' : '_blank' })
        principais_produtos = dados_fornecedor.find('div', attrs = {'class' : 'value ellipsis ph'})
        contato_direto = dados_fornecedor.find('a', attrs = {'class' : 'button csp'})
        
        if (contato_direto):
            
            lista_fornecedores.append([nome_empresa.text, principais_produtos.text, nome_empresa['href'], contato_direto['href']])
            
        else:
            lista_fornecedores.append([nome_empresa.text, principais_produtos.text, nome_empresa['href'], ''])
            
    coleta_de_dados()
    
    
def coleta_de_dados():
    
    salvar_arquivo = values['salvar']
    nome_produto = values['nome_produto01']         
    dados_coletados = pd.DataFrame(lista_fornecedores, columns=['Nome da empresa', 'Principais produtos', 'site', 'Contato Direto'])
    dados_coletados.to_excel(salvar_arquivo + "\\" + "fornecedores_de_"+ str(nome_produto) + ".xlsx", index = False)
    
while True:
    try:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Limpar':
            Limpar_input()
        if event == 'Submit':
            sg.popup('A busca esta sendo realizada.')
            Limpar_input()
            while True:
                if  values['sim_automatico']:
                    inicio = time.time() 
                    contato_automatico()
                    fim = time.time()
                    sg.popup(f'Fornecedores contatados com sucesso!\n\nTempo de execução: {fim - inicio} Segundos')
                    break
                else:
                    inicio = time.time()
                    apenas_coleta()
                    fim = time.time()
                    sg.popup(f'Coleta realizada com sucesso!\n\nTempo de execução: {fim - inicio} Segundos')
                    break
    except ValueError:
        sg.popup('Ocorreu algo errado. Tente novamente.')
window.close()

