import requests

API_KEY = "62a06978600e98d3cbf430ffe18ea254"

def obter_saldo():
    url = f"http://2captcha.com/getBalance?key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        saldo = response.text.strip()
        if saldo.isdigit():
            print(f"Seu saldo é: {saldo} créditos")
            return saldo
        else:
            print(f"Erro ao obter saldo: {response.text}")
            return None
    else:
        print("Erro ao conectar com a API")
        return None

# Exemplo de uso
obter_saldo()
