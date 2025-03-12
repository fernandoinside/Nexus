2. Estrutura do Projeto

meu_projeto/
│
├── app/                    # Código da sua aplicação
│   ├── Dockerfile          # Configuração do contêiner da aplicação
│   ├── main.py             # Aplicação principal (exemplo em Python)
│   └── requirements.txt    # Dependências da aplicação (se for Python)
│
├── docker-compose.yml      # Arquivo de configuração do Docker Compose
└── .env                    # Variáveis de ambiente (opcional e recomendado)


Testando o Projeto
    docker-compose up --build

    docker exec -it minha_aplicacao sh

    python app/main.py


Parar os contêineres:
    docker-compose down

Parar e Limpar os contêineres, redes e volumes:
    docker-compose down --volumes



