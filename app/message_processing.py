import json
import re
import spacy

# Carregar o modelo de NLP do spaCy
nlp = spacy.load('pt_core_news_sm')  # Modelo em português

class MessageProcessor:
    def __init__(self):
        self.stop_words = nlp.Defaults.stop_words
        self.intents = self.load_intents('intents.json')

    def load_intents(self, file_path):
        """Carrega as intenções a partir de um arquivo JSON."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def preprocess_text(self, text):
        # Remover caracteres especiais e converter para minúsculas
        text = re.sub(r'[^\w\s]', '', text).lower()
        # Processar o texto com spaCy
        doc = nlp(text)
        # Tokenização, remoção de stop words e lematização
        tokens = [token.lemma_.lower() for token in doc if token.text.lower() not in self.stop_words and not token.is_punct]
        return ' '.join(tokens)

    def get_intent(self, message):
        message = self.preprocess_text(message)
        print(f"Mensagem processada: {message}")

        # Verifica se alguma das palavras-chave está na mensagem
        for key, response in self.intents.items():
            if key in message:
                return response

        return "Desculpe, não entendi sua pergunta. Pode reformular?"
