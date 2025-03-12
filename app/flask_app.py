from flask import Flask, render_template, request, jsonify
import random
from src.agent.agent import Agent
from src.assistent.chat.chatbot import Chatbot
from src.assistent.recognition.recognition import Recognition
from src.assistent.speech.speech import Speech
from src.cache.cache_manager import CacheManager
from src.database.neo4j_client import Neo4jClient
from src.nlp.embedding_manager import EmbeddingManager
from src.utils.config import CACHE_CONFIG, DB_CONFIG

# Inicializa o app Flask
app = Flask(__name__)

# Inicializa componentes reutilizáveis
chatbot = Chatbot()
cache = CacheManager(**CACHE_CONFIG)
neo4j = Neo4jClient(**DB_CONFIG)
embedder = EmbeddingManager()
recognition = Recognition()
speech = Speech()

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Teste do Agent
@app.route('/test_agent', methods=['POST'])
def test_agent():
    agent = Agent()
    agent.start_listening()
    return jsonify({'status': 'Agent iniciado com sucesso'})

# Teste do Chatbot
@app.route('/test_chatbot', methods=['POST'])
def test_chatbot():
    prompt = request.form.get('prompt')
    try:
        response = chatbot.chat(prompt)
        return jsonify({'prompt': prompt, 'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})

# Teste do CacheManager e Neo4j
@app.route('/test_cache_neo4j', methods=['POST'])
def test_cache_neo4j():
    question = request.form.get('question')
    answer = request.form.get('answer')

    try:
        # Testa o CacheManager
        cache_key = cache.generate_cache_key(question)
        cache.set(cache_key, answer)
        cached_result = cache.get(cache_key)

        # Testa o Neo4j
        embedding = embedder.get_embedding(answer)
        neo4j.add_document(text=answer, embedding=embedding, metadata={"language": "pt", "category": "test"})
        results = neo4j.query_similarity(embedding)

        return jsonify({
            'cache_status': 'Cache OK' if cached_result == answer else 'Cache Falhou',
            'neo4j_result': results[0] if results else 'Nenhum resultado encontrado'
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# Teste do Reconhecimento de Voz
@app.route('/test_recognition', methods=['POST'])
def test_recognition():
    try:
        voice_input = recognition.listen()
        return jsonify({'voice_input': voice_input})
    except Exception as e:
        return jsonify({'error': str(e)})

# Teste do Speech
@app.route('/test_speech', methods=['POST'])
def test_speech():
    text = request.form.get('text')
    try:
        speech.speak(text)
        return jsonify({'status': f'Texto falado: {text}'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Executa o Flask
if __name__ == "__main__":
    app.run(debug=True)
