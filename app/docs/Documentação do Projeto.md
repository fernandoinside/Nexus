**Documentação do Projeto**

### 1. Objetivo do Projeto
Construir um sistema inteligente que combina reconhecimento de voz, processamento de linguagem natural (NLP) e consultas semânticas para responder a perguntas dos usuários. Ele integra:
- **Cache (Redis)** para otimizar consultas frequentes.
- **Banco de dados gráfico (Neo4j)** para consultas baseadas em embeddings.
- **Chatbot (GPT/Ollama)** para respostas a perguntas novas.

---

### 2. Tecnologias e Ferramentas Utilizadas
- **Linguagem principal:** Python.
- **Bibliotecas e ferramentas adicionais:**  
  - Redis (cache), Neo4j (banco de dados gráfico), Vosk (reconhecimento de voz offline), PyAudio, dotenv, Sentence Transformers, PyTorch.

---

### 3. Arquitetura do Sistema
O sistema segue uma arquitetura modular com os seguintes componentes:

#### 3.1 **Agent**
- Orquestra o fluxo geral entre os módulos (reconhecimento de voz, cache, banco de dados e fallback com Chatbot).
  
#### 3.2 **CacheManager**
- Usa Redis para armazenar respostas a perguntas frequentes.

#### 3.3 **Neo4jClient**
- Interface para o banco de dados gráfico, permitindo consultas baseadas em embeddings semânticos.

#### 3.4 **Chatbot**
- Usa mecanismos como GPT e Ollama para responder perguntas não encontradas no cache ou banco.

#### 3.5 **Recognition**
- Reconhece comandos de voz usando Vosk.

#### 3.6 **EmbeddingManager**
- Gera representações vetoriais (embeddings) usando Sentence Transformers.

---

### 4. Fluxo do Sistema
1. **Inicialização**
   - O **Agent** configura componentes e entra em modo de escuta.
2. **Processamento**
   - O reconhecimento de voz converte o comando em texto.
   - O texto é analisado para identificar intenção.
3. **Busca de Resposta**
   - O sistema verifica se a resposta está no cache, banco ou passa ao Chatbot.
4. **Resposta ao Usuário**
   - A resposta é falada ao usuário em partes curtas.

---

### 5. Funcionalidades Implementadas
#### 5.1 Sistema de Cache (Redis)
- Salva respostas com chaves únicas.  
**Exemplo de chave única:** `cache:{hash(question)}`.

#### 5.2 Banco de Dados (Neo4j)
- Criação de índice vetorial para consultas semânticas.
```cypher
CREATE VECTOR INDEX document_embedding
FOR (n:Document) ON (n.embedding)
OPTIONS {
    indexConfig: {
        `vector.dimensions`: 384,
        `vector.similarity_function`: 'cosine'
    }
}
```

#### 5.3 Chatbot
- Identifica o contexto das perguntas através de um arquivo JSON de mapeamento.  
**Exemplo:**  
```json
{
    "ask": [
        {
            "context": "Sobre IA: {palavra}",
            "work": ["inteligência artificial", "aprendizado de máquina"]
        }
    ]
}
```

---

### 6. Testes Realizados
#### Teste do Cache
```python
def test_cache_manager():
    cache = CacheManager(**CACHE_CONFIG)
    question = "O que é Python?"
    answer = "Uma linguagem de programação."
    key = cache.generate_cache_key(question)

    cache.set(key, answer)
    assert cache.get(key) == answer
```
#### Teste do Banco Neo4j
```python
def test_neo4j_client():
    neo4j = Neo4jClient(**DB_CONFIG)
    embedder = EmbeddingManager()
    question = "O que é IA?"
    embedding = embedder.get_embedding("Simulação da inteligência humana.")

    neo4j.add_document("Simulação da inteligência humana.", embedding, {"category": "test"})
    results = neo4j.query_similarity(embedding)
    assert results[0]["text"] == "Simulação da inteligência humana."
```

---

### 7. Logs e Depuração
#### Logs de Sucesso
- `[2025-03-12 04:00:00] INFO - Agente inicializado com sucesso.`
#### Logs de Erros
- `[2025-03-12 04:07:00] ERROR - Nenhum contexto encontrado para o prompt.`

---

### 8. Resultados
- **Integração Completa:** Cache, banco de dados e fallback de Chatbot.
- **Respostas:** Rápidas e relevantes, conforme esperado.
- **Manutenção:** Facilidade por logs e arquitetura modular.

---
