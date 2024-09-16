from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumUtils:
    def __init__(self, driver):
        self.driver = driver

    def find_and_message_contact(self, contact_name):
        try:
            contato = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, f"//span[@title='{contact_name}']"))
            )
            return contato
        except Exception as e:
            print(f"Erro ao encontrar o contato: {e}")
            return []

    def check_unread_messages(self):
        try:
            unread_messages = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@aria-label, 'unread')]"))
            )
            return len(unread_messages) > 0
        except Exception as e:
            print(f"Erro ao verificar mensagens não lidas: {e}")
            return False

    def get_last_message(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div._akbu"))
            )
            mensagens = self.driver.find_elements(By.CSS_SELECTOR, "div._akbu")
            
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

    def get_message_input_fields(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
