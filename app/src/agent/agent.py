# src\agent\agent.py
import logging
from src.assistent.speech.speech import Speech
from src.assistent.recognition.recognition import Recognition
from src.assistent.chat.chatbot import Chatbot
from src.cache.cache_manager import CacheManager
from src.database.neo4j_client import Neo4jClient
from src.nlp.embedding_manager import EmbeddingManager
from src.utils.config import config

class Agent:
    def __init__(self, timeout=10):
        self.speech = Speech()
        self.recognition = Recognition()
        self.chatbot = Chatbot()
        self.cache = CacheManager(**config.CACHE_CONFIG)
        self.neo4j = Neo4jClient(**config.DB_CONFIG)
        self.embedder = EmbeddingManager()        
        self.recognition_timeout = timeout
        self.is_listening = False
        logging.info("Agente inicializado com sucesso")

    def speak(self, text):
        try:
            logging.info(f"Iniciando fala: {text[:50]}...")
            self.speech.speak(text)
        except Exception as e:
            logging.error(f"Erro na fala: {e}")

    def _check_stop_words(self, text):
        stop_words = ['pare', 'parar', 'stop', 'silencio', 'sair']
        return any(word in text.lower() for word in stop_words)

    def _get_response(self, question):
        """
        Fluxo completo de validação e resposta.
        1. Verifica o cache para uma resposta existente.
        2. Busca no banco de dados Neo4j com base na similaridade semântica.
        3. Consulta o Chatbot configurado como fallback.
        4. Salva os resultados no cache e no banco, quando aplicável.
        
        Parâmetros:
        ----------
        question : str
            A pergunta feita pelo usuário.

        Retorno:
        -------
        str
            A resposta encontrada (ou uma mensagem informando que não foi possível encontrar uma resposta).
        """
        logging.info(f"Buscando resposta para: '{question}'")

        # Etapa 1: Verificar no cache
        cache_key = self.cache.generate_cache_key(question)
        cached_response = self.cache.get(cache_key)
        if cached_response:
            logging.info("Resposta encontrada no cache.")
            return cached_response

        # Etapa 2: Gerar embedding da pergunta
        try:
            embedding = self.embedder.get_embedding(question)
        except Exception as e:
            logging.error(f"Erro ao gerar embedding para a pergunta '{question}': {e}")
            return "Houve um erro ao processar sua solicitação."

        # Etapa 3: Buscar no Neo4j por similaridade
        try:
            similar_results = self.neo4j.query_similarity(embedding)
            if similar_results:
                best_match = similar_results[0]  # Obtém o primeiro resultado
                if best_match["score"] >= 0.8:  # Verifica a pontuação mínima de similaridade
                    logging.info("Resposta encontrada no banco de dados Neo4j.")
                    self.cache.set(cache_key, best_match["text"])
                    return best_match["text"]
            logging.info(f"Nenhuma resposta relevante encontrada no banco de dados para: '{question}'.")
        except Exception as e:
            logging.error(f"Erro ao consultar o banco de dados Neo4j para a pergunta '{question}': {e}")

        # Etapa 4: Consultar o Chatbot como fallback
        logging.info("Resposta não encontrada no cache ou Neo4j. Consultando o Chatbot...")
        try:
            ask_response = self.chatbot.chat(question)
            print(f" -------------------------------- Resposta do Chatbot: {ask_response}")
            # Exemplo de resposta errada = Erro ao processar o prompt: Nenhum contexto adequado encontrado para o prompt.
            # Se for uma resposta errada, não salvar no cache e banco
            if "Erro ao processar o prompt" in ask_response:
                return "Desculpe, não consegui encontrar uma resposta."
            
            # Salvar a resposta no cache e banco
            self.cache.set(cache_key, ask_response)
            self.neo4j.add_document(
                text=ask_response,
                embedding=embedding,
                metadata={"category": "ask_generated", "language": "pt"}
            )
            logging.info("Resposta gerada pelo Chatbot e salva com sucesso.")
            return ask_response
        except Exception as e:
            logging.error(f"Erro ao consultar o Chatbot para a pergunta '{question}': {e}")

        # Resposta final caso nenhuma etapa seja bem-sucedida
        return "Desculpe, não consegui encontrar uma resposta."

    def start_listening(self):
        self.is_listening = True
        logging.info("Modo de escuta iniciado")

    def stop_listening(self):
        self.is_listening = False
        logging.info("Modo de escuta finalizado")

    def process_commands(self):
        """
        Processa os comandos do usuário, integrando reconhecimento de voz, chatbot e resposta.
        """
        if not self.is_listening:
            return False

        try:
            if not self.recognition.is_microphone_available():
                logging.error("Microfone não disponível")
                return False

            voice_input = self.recognition.listen()
            
            if voice_input:
                logging.info(f"Comando capturado: {voice_input}")
                
                # Verifica comandos de parada
                if self._check_stop_words(voice_input):
                    logging.warning("Comando de parada detectado")
                    return False
                
                # Se for um comando para o Chatbot
                #if any(word in voice_input.lower() for word in ['Alexa', 'alexa']):
                logging.info("Comando reconhecido para CHATBOT")
                
                # Obter resposta validando cache, banco ou GPT
                response = self._get_response(voice_input)
                
                # Fala a resposta de forma parcial e gerencia a continuidade
                sentences = response.split('.')
                initial_response = sentences[0]
                
                # Se a primeira sentença for muito curta, adiciona mais sentenças
                if len(initial_response) < 50:
                    for sentence in sentences[1:]:
                        if len(initial_response + sentence) <= 70:
                            initial_response += '.' + sentence
                        else:
                            break
                
                self.speak(initial_response + "... Deseja ouvir o resto da resposta?")
                
                # Aguarda confirmação do usuário
                confirmation = self.recognition.listen()
                
                if confirmation and any(word in confirmation.lower() for word in ['sim', 'yes', 'continue', 'quero']):
                    remaining_response = response[len(initial_response):]
                    self.speak(remaining_response)
                
                logging.info("Resposta do chatbot processada")
                
                return True
                
        except Exception as e:
            self.speak("Encontrei um erro, tente novamente.")
            logging.error(f"Erro no processamento: {e}")
            
        return True
