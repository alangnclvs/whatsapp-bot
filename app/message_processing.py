import json
import os
import re
import spacy

# Carregar o modelo de NLP do spaCy
nlp = spacy.load('pt_core_news_sm')  # Modelo em português

class MessageProcessor:
    def __init__(self):
        # Definir stop words
        self.stop_words = nlp.Defaults.stop_words
        
        # Carregar intents.json
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório atual
        intents_path = os.path.join(current_dir, 'intents.json')  # Junta com o nome do arquivo

        self.intents = self.load_intents(intents_path)  # Carrega o arquivo de intenções

    def load_intents(self, file_path):
        """Carrega as intenções a partir de um arquivo JSON."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def preprocess_text(self, text):
        """Preprocessa o texto, removendo caracteres especiais, stop words e lematizando."""
        # Remover caracteres especiais e converter para minúsculas
        text = re.sub(r'[^\w\s]', '', text).lower()
        # Processar o texto com spaCy
        doc = nlp(text)
        # Tokenização, remoção de stop words e lematização
        tokens = [token.lemma_ for token in doc if token.text.lower() not in self.stop_words and not token.is_punct]
        return ' '.join(tokens)

    def get_intent(self, message):
        """Retorna a intenção com base na mensagem processada."""
        # Preprocessar a mensagem
        processed_message = self.preprocess_text(message)
        print(f"Mensagem processada: {processed_message}")

        # Verificar se alguma palavra-chave da intenção está na mensagem processada
        for key, response in self.intents.items():
            if key in processed_message:
                return response
        
        # Resposta padrão se nenhuma intenção for encontrada
        return "Desculpe, não entendi sua pergunta. Pode reformular?"

# Exemplo de uso:
# processor = MessageProcessor()
# intent = processor.get_intent("Olá, tudo bem?")
# print(intent)
