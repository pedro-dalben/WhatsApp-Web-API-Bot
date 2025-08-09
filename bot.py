import os
import time
import requests
import tempfile
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


app = Flask(__name__)

# Configura o Chrome para persistir a sessão (não será necessário reautenticar a cada reinício)
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=./user_data")
# Caso queira executar sem abrir a janela do navegador, descomente:
# chrome_options.add_argument("--headless")
service = Service('./chromedriver')
driver = webdriver.Chrome(service=service,options=chrome_options)
wait = WebDriverWait(driver, 30)

def open_chat(phone):
    """
    Abre o chat no WhatsApp Web usando a URL de click-to-chat.
    """
    url = f"https://web.whatsapp.com/send?phone={phone}"
    driver.get(url)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
    ))
    time.sleep(1)

def send_text_message(phone, message, open=True):
    """
    Envia uma mensagem de texto para o número informado.
    """
    try:
        if open:
            open_chat(phone)
        input_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
        ))
        input_box.click()
        input_box.send_keys(message + Keys.ENTER)
        time.sleep(0.2)
        return True
    except Exception as e:
        print("Erro ao enviar mensagem de texto:", e)
        return False

def send_image_message(phone, message, image_path):
    """
    Envia uma imagem (com legenda opcional) para o número informado.
    Utiliza os XPaths atualizados para clicar no botão de anexo, enviar o arquivo,
    inserir a legenda e clicar no botão de enviar.
    """
    try:
        open_chat(phone)

        # Clica no botão de anexo
        attach_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div/button')
        ))
        attach_btn.click()
        time.sleep(0.5)

        # Localiza o input de arquivo (invisível por padrão) e o torna visível
        image_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
        ))
        driver.execute_script("arguments[0].style.display = 'block';", image_input)
        time.sleep(1)
        image_input.send_keys(image_path)
        time.sleep(2)  # aguarda o carregamento da pré-visualização da imagem


        # Clica no botão de enviar utilizando o XPath atualizado
        send_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div')
        ))
        send_btn.click()
        time.sleep(3)
        send_text_message(phone, message, False)
        return True
    except Exception as e:
        print("Erro ao enviar mensagem com imagem:", e)
        return False

def download_image(image_url):
    """
    Faz o download da imagem a partir da URL informada e salva em um arquivo temporário.
    Retorna o caminho do arquivo ou None em caso de erro.
    """
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        suffix = os.path.splitext(image_url)[-1]
        if not suffix or len(suffix) > 5:
            suffix = '.jpg'
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        with open(temp_file.name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return temp_file.name
    except Exception as e:
        print("Erro ao baixar a imagem:", e)
        return None

@app.route('/send_message', methods=['POST'])
def api_send_message():
    data = request.get_json()
    print("Dados recebidos:", data)  # Log para debug

    phone = data.get('phone')
    message = data.get('message', '')
    image_url = data.get('image_url')

    if not phone:
        return jsonify({'error': 'O parâmetro "phone" é obrigatório.'}), 400

    if image_url:
        image_path = download_image(image_url)
        if not image_path:
            return jsonify({'error': 'Falha ao baixar a imagem.'}), 500
        success = send_image_message(phone, message, image_path)
        os.remove(image_path)
    else:
        if not message:
            return jsonify({'error': 'Para mensagem sem imagem, o parâmetro "message" é obrigatório.'}), 400
        success = send_text_message(phone, message)

    if success:
        return jsonify({'status': 'Mensagem enviada com sucesso.'}), 200
    else:
        return jsonify({'error': 'Falha ao enviar a mensagem.'}), 500


if __name__ == '__main__':
    driver.get("https://web.whatsapp.com")
    print("Aguardando autenticação no WhatsApp Web (escaneie o QR Code se necessário)...")
    time.sleep(5)
    app.run(host='0.0.0.0', port=5000)
