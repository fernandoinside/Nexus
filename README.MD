# 🚀 Projeto Inteligente: Reconhecimento de Voz + NLP + Consultas Semânticas

Bem-vindo ao **[nome do projeto]**, um sistema inteligente que combina **reconhecimento de voz**, **processamento de linguagem natural (NLP)** e **consultas baseadas em similaridade semântica**. Este repositório fornece um pipeline robusto para interação com usuários, utilizando diversas tecnologias de ponta!

---

## 🎯 Objetivo do Projeto

Este projeto foi criado para **responder perguntas de maneira inteligente e eficiente**, integrando:
- 🎙️ **Reconhecimento de Voz** para capturar comandos do usuário.
- 🧠 **Processamento de Linguagem Natural (NLP)** para compreender intenções.
- 📊 **Banco de Dados Gráfico Neo4j** para consultas rápidas e baseadas em contexto.
- 🤖 **Chatbot Avançado (GPT ou Ollama)** como fallback para perguntas novas.

### 🌟 Exemplos de Aplicação
Este projeto é ideal para:
- **Assistentes Virtuais**: Automação de interações com clientes.
- **Soluções de FAQ Inteligentes**: Fornecimento de respostas personalizadas em empresas.
- **Educação e Suporte**: Resolução de dúvidas em contextos educacionais.
- **Controle por Voz**: Sistemas onde a interação sem uso das mãos é essencial.

---

## ⚙️ Tecnologias Utilizadas

O sistema foi desenvolvido com foco em modularidade e eficiência, utilizando:

- **Python** 🐍: Linguagem principal para o desenvolvimento do backend.
- **Redis** 🛠️: Sistema de cache in-memory para melhorar a performance.
- **Neo4j** 📈: Banco de dados gráfico para buscas semânticas avançadas.
- **Vosk** 🎧: Reconhecimento de voz offline rápido e confiável.
- **Sentence Transformers** ✍️: Criação de embeddings vetoriais para análise semântica.
- **dotenv** 🔑: Gerenciamento de configurações sensíveis.
- **PyTorch** 🚀: Base para modelos de aprendizado de máquina.

---

## 🛠️ Como Configurar e Usar

### 1️⃣ Pré-requisitos
Certifique-se de ter instalado:
- **Python 3.8+**
- **Docker** e **Docker Compose** (opcional, para simplificar a execução)

### 2️⃣ Como Instalar
Clone o repositório e instale as dependências:
```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
pip install -r requirements.txt
```

### 3️⃣ Executando o Sistema
**Via Docker:**
1. Configure as variáveis de ambiente no arquivo `.env`.
2. Execute o comando:
   ```bash
   docker-compose up
   ```

**Localmente:**
1. Inicie os serviços Redis e Neo4j.
2. Rode o script principal:
   ```bash
   python app/main.py
   ```

---

## 🗂️ Estrutura do Projeto

```plaintext
📂 C:.
│   📄 .env                       # Configurações de ambiente (credenciais e variáveis)
│   📄 .gitignore                 # Arquivos e pastas a serem ignorados no Git
│   📄 docker-compose.yml         # Configuração de orquestração do Docker
│   📄 iniciar.bat                # Script de inicialização para Windows
│   📄 README.MD                  # Documentação geral do projeto
│   
└───📂 app
    │   📄 Dockerfile             # Configuração para criação do container Docker
    │   📄 main.py                # Script principal do sistema
    │   📄 flask_app.py           # Arquivo principal para inicializar o     
    │   📄 requirements.txt       # Dependências do Python
    │   
    ├───📂 docs 📘                # Documentações e guias do projeto
    │       📄 Documentação do Projeto.md   # Detalhamento completo do projeto
    │       
    └───📂 src 🔧                 # Código-fonte principal
        ├───📂 agent 🕹️           # Orquestrador do sistema e módulos
        │       📄 agent.py                # Orquestrador principal dos módulos
        │       📄 commands.py             # Gerenciador de comandos do sistema
        │       📄 nlp.py                  # Funções relacionadas a NLP
        │       
        ├───📂 assistent 🤖        # Módulo assistente que inclui chatbot
        │   │   📄 __init__.py             # Inicializador do módulo assistent
        │   │   
        │   ├───📂 chat 💬          # Gerencia o Chatbot e comunicação com usuários
        │   │   │   📄 chatbot.py          # Configuração do chatbot
        │   │   │   📄 chatbot_base.py     # Classe base para chatbots
        │   │   │   📄 chatbot_gpt.py      # Implementação com GPT
        │   │   │   📄 chatbot_ollama.py   # Implementação com Ollama
        │   │   │   📄 __init__.py         # Inicializador do submódulo
        │   │   └───📂 prompts ✍️         # Modelos de contexto para perguntas
        │   │           📄 context_pesquisa.json # Contextos para perguntas
        │   │
        │   ├───📂 recognition 🎙️  # Focado no reconhecimento de voz
        │   │       📄 recognition.py                  # Reconhecimento de comandos de voz
        │   │       📄 recognition_base.py             # Classe base para reconhecimento
        │   │       📄 recognition_speech_recognition.py # Reconhecimento usando SpeechRecognition
        │   │       📄 recognition_vosk.py             # Reconhecimento usando Vosk
        │   │       📄 __init__.py                     # Inicializador do submódulo
        │   │
        │   └───📂 speech 🗣️        # Responsável pela síntese e manipulação de voz
        │           📄 speech.py                       # Funções gerais de síntese de voz
        │           📄 speech_azure.py                 # Implementação com Azure
        │           📄 speech_base.py                  # Classe base de síntese
        │           📄 speech_coqui.py                 # Implementação com Coqui
        │           📄 speech_google.py                # Implementação com Google
        │           📄 speech_pyttsx.py                # Implementação com Pyttsx
        │           📄 __init__.py                     # Inicializador do submódulo
        │
        ├───📂 cache 🔄            # Gestão de cache e respostas rápidas
        │       📄 cache_manager.py        # Gerenciador do sistema de cache Redis
        │       📄 __init__.py             # Inicializador do módulo
        │
        ├───📂 database 📊         # Banco de dados e gerenciador de consultas
        │       📄 neo4j_client.py         # Interface para interação com Neo4j
        │       📄 query_manager.py        # Gerenciador de consultas
        │       📄 __init__.py             # Inicializador do módulo
        │
        ├───📂 models 🧠           # Modelos para reconhecimento de voz e embeddings
        │   └───📂 vosk 🔉         # Arquivos do modelo de reconhecimento de voz
        │       └───📂 vosk-model-small-pt-0.3
        │           📄 disambig_tid.int    # Dados de desambiguação
        │           📄 final.mdl           # Modelo treinado final
        │           📄 Gr.fst              # Arquivo de gramática
        │           📄 HCLr.fst            # Arquivo de transições acústicas
        │           📄 mfcc.conf           # Configuração de MFCC
        │           📄 phones.txt          # Definição dos fonemas
        │           📄 README              # Documentação do modelo
        │           📄 word_boundary.int   # Arquivo de delimitação de palavras
        │           📂 ivector
        │               📄 final.dubm      # Modelo de i-vector para clustering
        │               📄 final.ie        # Estimador de i-vector
        │               📄 final.mat       # Matrizes finais
        │               📄 global_cmvn.stats # Estatísticas globais
        │               📄 online_cmvn.conf  # Configurações de normalização online
        │               📄 splice.conf       # Configuração de Splicing
        │
        ├───📂 nlp 📚              # Processamento de Linguagem Natural (NLP)
        │       📄 embedding_manager.py    # Gerador de embeddings para textos
        │       📄 nlp_processor.py        # Processador de linguagem natural
        │       📄 text_preprocessor.py    # Pré-processador de texto
        │       📄 __init__.py             # Inicializador do módulo
        │
        ├───📂 test 🧪             # Testes automatizados do sistema
        │       📄 test_agent.py           # Testes para o módulo agent
        │       📄 test_chatbot.py         # Testes para chatbots
        │       📄 test_neo4j_and_cache.py # Testes para Neo4j e Redis
        │       📄 test_recognition.py     # Testes para reconhecimento de voz
        │       📄 test_speech.py          # Testes para síntese de voz
        │
        └───📂 utils 🛠️            # Utilitários e configurações gerais
                📄 config.py               # Configurações gerais do projeto
                📄 logger.py               # Sistema de logs do projeto
```

---

## 🎨 Funcionalidades Principais

- **🔍 Busca por Similaridade**: Utiliza embeddings para respostas contextuais.
- **💾 Sistema de Cache**: Melhora a performance com respostas já processadas.
- **🤖 Chatbot Fallback**: Garante respostas para perguntas inéditas.
- **🎤 Comandos de Voz**: Captura e processa interações com precisão.

---

## 🚀 Utilizar o Flask

### Configuração do Flask no Dockerfile
Se o Flask for o ponto de entrada da aplicação, atualize o **Dockerfile** para refletir isso:

1. **Atualizar o comando de inicialização:**
   Substitua o comando para iniciar diretamente o Flask:
   ```dockerfile
   CMD ["python", "flask_app.py"]
   ```

2. **Definir o Flask como servidor principal (opcional):**
   Utilize o comando `flask run` no Dockerfile:
   ```dockerfile
   ENV FLASK_APP=flask_app.py
   CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
   ```

3. **Certifique-se de expor a porta correta (5000 no caso do Flask):**
   ```dockerfile
   ENV APP_PORT=5000
   EXPOSE ${APP_PORT}
   ```

---

## 📚 Documentação

- [Documentação do Projeto](https://github.com/seu-usuario/seu-repositorio/blob/main/docs/documentacao.md)

- [Fluxograma](https://github.com/seu-usuario/seu-repositorio/blob/main/docs/fluxograma.md)

---

## 📈 Futuras Melhorias
- 🔮 **Integração com serviços de IA na nuvem**.
- 🛡️ **Autenticação e segurança avançada**.
- 🌍 **Suporte a múltiplos idiomas**.

---

## 🤝 Contribuições

Sinta-se à vontade para contribuir com sugestões, melhorias ou correções!  
Basta abrir uma **issue** ou enviar um **pull request**. Adoraremos ter você como parte da comunidade. ❤️

---

## 📜 Licença
Este projeto é licenciado sob a [MIT License](LICENSE).

---