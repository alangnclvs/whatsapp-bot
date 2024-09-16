import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Nome do contato a ser utilizado
CONTACT_NAME = 'Le'

# Função para pré-processar o texto
def preprocess_text(text):
    # Remove caracteres não alfabéticos, mas mantém números e espaços
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()
    return text

# Função para determinar a intenção da mensagem
def get_intent(message):
    message = preprocess_text(message)
    print(f"Mensagem processada: {message}")
    if 's3' in message:
        return "O Amazon S3 é um serviço de armazenamento de objetos na nuvem."
    elif 'ec2' in message:
        return "O Amazon EC2 é um serviço de computação em nuvem que fornece instâncias virtuais."
    elif 'rds' in message:
        return "O Amazon RDS é um serviço de banco de dados gerenciado na nuvem."
    elif 'vpc' in message:
        return "O Amazon VPC permite criar uma rede isolada na nuvem da AWS."
    elif 'cloudfront' in message:
        return "O Amazon CloudFront é um serviço de CDN (Content Delivery Network) da AWS."
    else:
        return "Desculpe, não entendi sua pergunta. Pode reformular?"

# Navega até o WhatsApp Web
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://web.whatsapp.com/")
driver.maximize_window()
print("Por favor, escaneie o QR Code e pressione Enter para continuar...")
input()

def find_and_message_contact(contact_name):
    try:
        contato = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, f"//span[@title='{contact_name}']"))
        )
        return contato
    except Exception as e:
        print(f"Erro ao encontrar o contato: {e}")
        return []

def check_unread_messages():
    try:
        unread_messages = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@aria-label, 'unread')]"))
        )
        return len(unread_messages) > 0
    except Exception as e:
        print(f"Erro ao verificar mensagens não lidas: {e}")
        return False

def get_last_message():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div._akbu"))
        )
        mensagens = driver.find_elements(By.CSS_SELECTOR, "div._akbu")
        
        if mensagens:
            ultima_mensagem = mensagens[-1].text
            print(f"Mensagem recebida: {ultima_mensagem}")
            return ultima_mensagem
        else:
            print("Nenhuma mensagem encontrada.")
            return ""
    except Exception as e:
        print(f"Erro ao capturar a última mensagem: {e}")
        return ""

# Variáveis para armazenar o texto da última mensagem processada e última resposta enviada
last_processed_message = ""
last_bot_response = ""

while True:
    print("Verificando mensagens não lidas...")
    time.sleep(5)

    try:
        if check_unread_messages():
            print("Há mensagens não lidas.")

            contato = find_and_message_contact(CONTACT_NAME)

            if contato:
                print(f"Contato '{CONTACT_NAME}' encontrado!")

                for contato in contato:
                    contato.click()
                    time.sleep(2)

                    ultima_mensagem = get_last_message()

                    # Verifica se a última mensagem não é a resposta do bot e se é diferente da mensagem processada anteriormente
                    if ultima_mensagem and ultima_mensagem != last_processed_message and ultima_mensagem != last_bot_response:
                        resposta = get_intent(ultima_mensagem)
                        if resposta:
                            campos_mensagem = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
                            if len(campos_mensagem) > 1:
                                campo_mensagem = campos_mensagem[1]
                                campo_mensagem.click()
                                time.sleep(2)

                                campo_mensagem.send_keys(resposta)
                                time.sleep(2)

                                campo_mensagem.send_keys(Keys.ENTER)
                                print(f"Mensagem enviada para '{CONTACT_NAME}': {resposta}")
                                time.sleep(2)

                                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                                time.sleep(5)
                                
                                # Atualiza as mensagens processadas e resposta do bot
                                last_processed_message = ultima_mensagem
                                last_bot_response = resposta
                            else:
                                print("Campo de mensagem não encontrado.")
            else:
                print(f"Contato '{CONTACT_NAME}' não encontrado.")
        else:
            print("Nenhuma mensagem não lida encontrada.")

    except Exception as e:
        print(f"Erro encontrado: {e}")
        time.sleep(5)
