import logging
from src.cache.cache_manager import CacheManager
from src.database.neo4j_client import Neo4jClient
from src.nlp.embedding_manager import EmbeddingManager
from src.utils.config import CACHE_CONFIG, DB_CONFIG

# Configuração do log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)

def test_cache_manager(cache, question, answer):
    """
    Testa as funcionalidades do CacheManager.
    """
    logging.info("Testando o CacheManager...")

    # Gera uma chave para o cache
    cache_key = cache.generate_cache_key(question)

    # Adiciona uma resposta ao cache
    cache.set(cache_key, answer)

    # Recupera a resposta armazenada
    cached_result = cache.get(cache_key)

    # Valida a resposta armazenada
    if cached_result == answer:
        logging.info("CacheManager: Teste bem-sucedido!")
    else:
        logging.error("CacheManager: Teste falhou! Resposta no cache incorreta.")

def test_neo4j_client(neo4j, embedder, question, answer):
    """
    Testa as funcionalidades do Neo4jClient.
    """
    logging.info("Testando o Neo4jClient...")

    try:
        # Gera um embedding para a pergunta
        embedding = embedder.get_embedding(answer)

        # Insere o documento no banco
        neo4j.add_document(
            text=answer,
            embedding=embedding,
            metadata={"language": "pt", "category": "test"}
        )
        logging.info("Neo4jClient: Documento inserido com sucesso!")

        # Consulta por similaridade
        results = neo4j.query_similarity(embedding)

        # Valida o resultado
        if results and results[0]["text"] == answer:
            logging.info("Neo4jClient: Consulta por similaridade bem-sucedida!")
        else:
            logging.error("Neo4jClient: Falha na consulta por similaridade!")
    except Exception as e:
        logging.error(f"Erro ao testar o Neo4jClient: {e}")

def main():
    """
    Executa os testes para CacheManager e Neo4jClient.
    """
    logging.info("Iniciando os testes de cache e Neo4j...")

    # Inicializa os componentes
    cache = CacheManager(**CACHE_CONFIG)
    neo4j = Neo4jClient(**DB_CONFIG)
    embedder = EmbeddingManager()

    # Dados de teste
    question = "O que é Python?"
    answer = "Python é uma linguagem de programação de alto nível, interpretada, de propósito geral e orientada a objetos."

    # Testa os componentes
    test_cache_manager(cache, question, answer)
    test_neo4j_client(neo4j, embedder, question, answer)

if __name__ == "__main__":
    main()
