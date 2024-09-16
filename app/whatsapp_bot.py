import time
from selenium.webdriver.common.keys import Keys
from selenium_utils import SeleniumUtils
from message_processing import MessageProcessor
from config import CONTACT_NAME

class WhatsAppBot:
    def __init__(self, driver):
        self.driver = driver
        self.contact_name = CONTACT_NAME
        self.last_processed_message = ""
        self.last_bot_response = ""

    def start(self):
        print("Por favor, escaneie o QR Code e pressione Enter para continuar...")
        input()
        
        while True:
            print("Verificando mensagens não lidas...")
            time.sleep(5)
            self.check_and_respond()

    def check_and_respond(self):
        selenium_utils = SeleniumUtils(self.driver)
        
        if selenium_utils.check_unread_messages():
            print("Há mensagens não lidas.")
            contato = selenium_utils.find_and_message_contact(self.contact_name)

            if contato:
                print(f"Contato '{self.contact_name}' encontrado!")

                for c in contato:
                    c.click()
                    time.sleep(2)

                    ultima_mensagem = selenium_utils.get_last_message()

                    if ultima_mensagem and ultima_mensagem != self.last_processed_message and ultima_mensagem != self.last_bot_response:
                        self.respond_to_message(ultima_mensagem)
            else:
                print(f"Contato '{self.contact_name}' não encontrado.")
        else:
            print("Nenhuma mensagem não lida encontrada.")

    def respond_to_message(self, message):
        processor = MessageProcessor()
        resposta = processor.get_intent(message)

        if resposta:
            selenium_utils = SeleniumUtils(self.driver)
            campos_mensagem = selenium_utils.get_message_input_fields()

            if len(campos_mensagem) > 1:
                campo_mensagem = campos_mensagem[1]
                campo_mensagem.click()
                time.sleep(2)

                campo_mensagem.send_keys(resposta)
                time.sleep(2)
                campo_mensagem.send_keys(Keys.ENTER)
                print(f"Mensagem enviada para '{self.contact_name}': {resposta}")

                self.last_processed_message = message
                self.last_bot_response = resposta
            else:
                print("Campo de mensagem não encontrado.")
