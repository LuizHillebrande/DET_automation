import requests
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

API_KEY = '121212132132132131232132131231231'
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


