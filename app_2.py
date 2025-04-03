from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyautogui
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import pdfplumber
import pandas as pd
import customtkinter as ctk
import json
from time import sleep
import zipfile
import os
import shutil
from thefuzz import process 
from selenium.webdriver.common.by import By
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyautogui
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import pdfplumber
import pandas as pd
import customtkinter as ctk
import json
from time import sleep
import zipfile
import os
import shutil
from thefuzz import process 
import undetected_chromedriver as uc
import openpyxl as opx
from openpyxl import Workbook, load_workbook
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import tkinter as tk
import threading


#CAPTCHA
API_KEY = "62a06978600e98d3cbf430ffe18ea254"
def enviar_captcha(caminho_imagem):
    url = "http://2captcha.com/in.php"
    files = {'file': open(caminho_imagem, 'rb')}
    data = {
        'key': API_KEY,
        'method': 'post',  
        'json': 1,
        'coordinatescaptcha': 1  # Isso ativa a detecção de coordenadas
    }
    
    response = requests.post(url, files=files, data=data)
    result = response.json()
    
    if result.get("status") == 1:
        return result["request"]  # ID do CAPTCHA para buscar a resposta
    return None

# Passo 2: Buscar a resposta com as coordenadas
def obter_resposta_captcha(captcha_id):
    url = f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1"
    
    for _ in range(30):  # Espera até 30 segundos pela resposta
        response = requests.get(url)
        result = response.json()
        
        if result.get("status") == 1:
            return result["request"]  # Coordenadas da resposta
        
        elif result.get("request") == "CAPCHA_NOT_READY":
            time.sleep(5)  # Aguarda antes de tentar de novo
        
        else:
            print(f"Erro na resposta do 2Captcha: {result}")
            return None  # Sai do loop se houver erro crítico
    
    return None

# Passo 3: Clicar nas coordenadas retornadas
def clicar_nas_coordenadas(coordenadas):
    if not coordenadas:
        print("Nenhuma coordenada recebida!")
        return

    if isinstance(coordenadas, list):  # Verifica se é uma lista de dicionários
        for ponto in coordenadas:
            try:
                x, y = int(ponto['x']), int(ponto['y'])  # Extrai os valores corretamente
                print(f"Clicando no ponto: ({x}, {y})")
                pyautogui.click(x, y)
                time.sleep(1)  # Aguardar 1 segundo após o clique para evitar fechamentos inesperados
            except Exception as e:
                print(f"Erro ao clicar na coordenada {ponto}: {e}")
    else:
        print(f"Formato inesperado das coordenadas: {coordenadas}")



coordenadas_imagens = [
    (545, 286),  # 1
    (675, 289),  # 2
    (794, 284),  # 3
    (547, 413),  # 4
    (680, 414),  # 5
    (797, 415),  # 6
    (544, 542),  # 7
    (671, 549),  # 8
    (801, 560)   # 9
]



def login_det():
    try:
        mes_atual = datetime.now().strftime("%m-%Y")
        diretorio_download = os.path.join(os.getcwd(), f"DET_CONSULTA_{mes_atual}")

        chrome_options = Options()
        chrome_options.add_argument(f'--download-default-directory={diretorio_download}')

        # Inicializa o WebDriver com as configurações
        driver = uc.Chrome(options=chrome_options)
        driver.get('https://det.sit.trabalho.gov.br/login?r=%2Fcaixapostal')
        driver.maximize_window()

        entrar_com_gov = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='br-button is-primary']"))
        )
        entrar_com_gov.click()

        button_certif_digital = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='login-certificate']"))
        )
        button_certif_digital.click()

        sleep(5)

        hcaptcha_iframes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//iframe[contains(@title, 'hCaptcha')]"))
        )

        if hcaptcha_iframes:
            print("CAPTCHA detectado! Aguarde a resolução.")
            driver.switch_to.frame(hcaptcha_iframes[0])

            screenshot_path = "captcha_screenshot.png"
            pyautogui.screenshot(screenshot_path)
            print(f"Screenshot do CAPTCHA foi salva em: {screenshot_path}")

            captcha_id = enviar_captcha(screenshot_path)
            if captcha_id:
                coordenadas = obter_resposta_captcha(captcha_id)
                if coordenadas:
                    clicar_nas_coordenadas(coordenadas)
                else:
                    print("Erro ao obter a resposta do CAPTCHA.")
            else:
                print("Erro ao enviar o CAPTCHA.")

            driver.switch_to.default_content()
        
        sleep(3)
        try:
            botao_proximo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'button-submit') and contains(@class, 'button') and (contains(text(), 'Próximo') or contains(text(), 'Avançar'))]"))
            )
            driver.execute_script("arguments[0].click();", botao_proximo)
            print("Botão 'Próximo' ou 'Avançar' clicado com sucesso!")
        except Exception as e:
            print(f"Erro ao clicar no botão: {e}")


    

    except Exception as e:
        print(f"Erro inesperado: {e}")

    finally:
        print("Fechando WebDriver.")
        try:
            driver.quit()
        except Exception as e:
            print(f"Erro ao fechar o WebDriver: {e}")

login_det()




