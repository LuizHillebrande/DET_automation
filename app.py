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

def resolver_captcha_2captcha(image_path):
    try:
        print("Enviando CAPTCHA para o 2Captcha...")
        with open(image_path, 'rb') as img_file:
            files = {'file': img_file}
            response = requests.post(
                f"http://2captcha.com/in.php?key={API_KEY}&method=post",
                files=files
            )
        
        if response.status_code != 200 or "OK" not in response.text:
            raise Exception("Erro ao enviar o CAPTCHA para o 2Captcha")
        
        captcha_id = response.text.split('|')[1]
        print(f"CAPTCHA enviado. ID: {captcha_id}")
        
        # Passo 2: Aguardar e consultar o resultado
        for _ in range(45):  # Tenta por até 30 segundos
            time.sleep(5)  # Espera 5 segundos entre consultas
            result_response = requests.get(f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}")
            if result_response.text == "CAPCHA_NOT_READY":
                print("CAPTCHA ainda não está pronto, aguardando...")
                continue
            
            if "OK" in result_response.text:
                captcha_text = result_response.text.split('|')[1]
                print(f"CAPTCHA resolvido: {captcha_text}")
                return captcha_text
            
        raise Exception("Tempo esgotado para resolver o CAPTCHA")
    except Exception as e:
        print(f"Erro ao resolver CAPTCHA com 2Captcha: {e}")
        return None
    
def verificar_captcha(janela_captcha, label_tempo, tempo_restante, driver):
    while tempo_restante > 0:
        time.sleep(1)
        tempo_restante -= 1
        label_tempo.config(text=f"Tempo restante: {tempo_restante}s")

        # Verifica se o CAPTCHA já foi resolvido
        try:
            driver.switch_to.default_content()  # Sai do iframe, se estiver dentro
            hcaptcha_iframes = driver.find_elements(By.XPATH, "//iframe[contains(@title, 'hCaptcha')]")
            if not hcaptcha_iframes:  # Se não encontrar o iframe, significa que o CAPTCHA sumiu
                print("CAPTCHA resolvido automaticamente!")
                janela_captcha.destroy()
                return
        except Exception:
            pass  # Se houver erro, continua a contagem regressiva normalmente
    
    janela_captcha.destroy()

def mostrar_aviso_captcha(driver, tempo=60):
    janela_captcha = ctk.CTkToplevel()
    janela_captcha.title("Ação necessária: Resolver CAPTCHA")
    janela_captcha.geometry("350x180")
    janela_captcha.grab_set()  # Bloqueia interação com a janela principal
    
    label_msg = tk.Label(janela_captcha, text="Resolvendo CAPTCHA... Aguarde.", font=("Arial", 12))
    label_msg.pack(pady=10)

    label_tempo = tk.Label(janela_captcha, text=f"Tempo restante: {tempo}s", font=("Arial", 12, "bold"), fg="red")
    label_tempo.pack(pady=10)

    # Botão para o usuário confirmar que resolveu o CAPTCHA manualmente
    btn_resolvi = ctk.CTkButton(janela_captcha, text="Resolvi", command=janela_captcha.destroy)
    btn_resolvi.pack(pady=10)

    # Inicia a contagem regressiva em outra thread
    threading.Thread(target=verificar_captcha, args=(janela_captcha, label_tempo, tempo, driver), daemon=True).start()

    janela_captcha.mainloop()

imagem_alvo = r"certificado_esperado.png"

# Intervalo entre os cliques de tecla
intervalo = 0.5

def localizar_imagem_na_tela(imagem, confidence=0.8):
    """
    Tenta localizar a imagem na tela.
    :param imagem: Caminho da imagem a ser localizada.
    :param confidence: Nível de confiança para correspondência da imagem.
    :return: Coordenadas da imagem encontrada ou None.
    """
    try:
        # Localiza a imagem na tela
        localizacao = pyautogui.locateOnScreen(imagem, confidence=confidence)
        
        if localizacao:
            # Move o mouse para as coordenadas do centro da imagem
            pyautogui.moveTo(pyautogui.center(localizacao))
            sleep(1)
            pyautogui.click()
            return localizacao
        else:
            print("Imagem não encontrada.")
            return None
    except Exception as e:
        print(f"Erro ao localizar imagem: {e}")
        return None


def pressionar_ate_encontrar(imagem, intervalo=0.5):
    """
    Pressiona a seta para baixo até encontrar a imagem na tela.
    :param imagem: Caminho da imagem a ser localizada.
    :param intervalo: Intervalo entre as teclas pressionadas.
    """
    while True:
        localizacao = localizar_imagem_na_tela(imagem)
        if localizacao:
            print(f"Imagem encontrada nas coordenadas: {localizacao}")
            pyautogui.press('enter')
            sleep(3)
            break
        else:
            print("Imagem não encontrada. Pressionando seta para baixo...")
            pyautogui.press('down')
            time.sleep(intervalo)

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
    mes_atual = datetime.now().strftime("%m-%Y")
    diretorio_download = os.path.join(os.getcwd(), f"DET_CONSULTA_{mes_atual}")

    chrome_options = Options()
    chrome_options.add_argument(f'--download-default-directory={diretorio_download}')

    # Inicializa o WebDriver com as configurações
    driver = uc.Chrome(options=chrome_options)
    driver.get('https://det.sit.trabalho.gov.br/login?r=%2Fcaixapostal')
    driver.maximize_window()

    entrar_com_gov = WebDriverWait(driver,5).until(
        EC.element_to_be_clickable((By.XPATH,"//button[@class='br-button is-primary']"))
    )
    entrar_com_gov.click()

    button_certif_digital = WebDriverWait(driver,5).until(
        EC.element_to_be_clickable((By.XPATH,"//button[@id='login-certificate']"))
    )
    button_certif_digital.click()

    
    sleep(5)

    hcaptcha_iframes = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//iframe[contains(@title, 'hCaptcha')]"))
    )

    try:
        if hcaptcha_iframes:
            print("CAPTCHA detectado! Aguarde a resolução.")

            # Alterna para o iframe do CAPTCHA
            driver.switch_to.frame(hcaptcha_iframes[0]) 
            action = ActionChains(driver)

            # Tirar o screenshot da tela onde o CAPTCHA está
            screenshot_path = "captcha_screenshot.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot do CAPTCHA foi salva em: {screenshot_path}")

            # Loop para tentar resolver o CAPTCHA até obter uma resposta válida
            while True:
                # Resolver o CAPTCHA com 2Captcha (usando o caminho do screenshot)
                captcha_token = resolver_captcha_2captcha(screenshot_path)

                # Verifica se a resposta contém apenas números
                if captcha_token and captcha_token.isdigit():
                    print(f"CAPTCHA resolvido: {captcha_token}")
                    for position in captcha_token:  # Supondo que `captcha_token` é uma string com os números das posições (ex: "258")
                        position = int(position)  # Converte para inteiro

                        # Verifica se a posição está dentro das coordenadas válidas
                        if 1 <= position <= len(coordenadas_imagens):
                            x, y = coordenadas_imagens[position - 1]  # Subtrai 1 porque as listas começam do 0
                            action.move_by_offset(x, y).click().perform()  # Move até a posição e clica
                            print(f"Clicando na posição {position} nas coordenadas ({x}, {y}).")
                    break  # Sai do loop após o sucesso

                else:
                    print("Resposta do CAPTCHA inválida, tentando novamente.")

            # Volta para o conteúdo principal após resolver o CAPTCHA
            driver.switch_to.default_content()

            return
    except Exception as e:
        print(f"Nenhum CAPTCHA detectado. Prosseguindo com o login. Erro: {e}")


    sleep(10)
    driver.quit()

login_det()



