# src/test/test_chatbot.py
import random
from src.assistent.chat.chatbot import Chatbot

def main():
    # Inicializa o objeto Chatbot
    chatbot = Chatbot()

    # Lista de perguntas para testar
    test_prompts = [
        "pesquisar sobre inteligência artificial",  # Contexto de pesquisa geral
        "o que é machine learning",  # Contexto de definição
        "como funciona uma rede neural",  # Explicação técnica
        "história da robótica",  # Histórico
        "quem desenvolveu o primeiro computador quântico",  # Informação biográfica
        "comparar carros elétricos e combustíveis fósseis",  # Comparação
        "desafios da energia solar",  # Análise de desafios
        "dados sobre o mercado de smartphones",  # Estatísticas
        "previsões para a economia em 2030",  # Previsões futuras
        "exemplos de aplicações de blockchain",  # Casos práticos
        "vantagens e desvantagens da inteligência artificial",  # Prós e contras
        "como surgiu o conceito de programação orientada a objetos",  # Origem
        "quem criou o protocolo HTTP",  # Informações históricas
        "tendências tecnológicas para 2025",  # Tendências
        "explicar a diferença entre IA e aprendizado de máquina",  # Explicações comparativas
        "problemas enfrentados pela indústria automotiva",  # Problemas e soluções
        "estatísticas sobre mudanças climáticas",  # Estatísticas e dados
        "listar tecnologias emergentes em medicina",  # Lista de tecnologias
        "previsões sobre robótica nos próximos anos",  # Previsões
        "como localizar informações sobre cibersegurança",  # Consulta genérica de pesquisa
        "quem inventou a inteligência artificial",  # Histórico com autoria
        "como surgiu o metaverso",  # Histórico e origem
        "descrever aplicações práticas do metaverso",  # Aplicações práticas
        "listar benefícios do uso de energias renováveis",  # Benefícios
        "Encontre frameworks para construir APIs com Python.",
        "O que é o OWASP e como funciona?",
        "Explique como funciona o protocolo HTTPS.",
        "Qual é a história do Linux e como ele evoluiu?",
        "Compare a criptografia RSA com AES, incluindo vantagens e desvantagens.",
        "Estatísticas sobre o uso de Python no mercado de tecnologia.",
        "Quais são as tendências futuras para automação de segurança?",
        "Quais são os principais desafios em proteger sistemas contra ataques DDoS?",
        "Dê exemplos de exploits usados para ataques em sistemas web.",
        "Como criar um firewall básico usando iptables no Linux.",
    ]

    # Seleciona 5 perguntas aleatoriamente da lista
    random_prompts = random.sample(test_prompts, 5)

    # Testa cada pergunta escolhida aleatoriamente
    for prompt in random_prompts:
        print(f"\nPergunta: {prompt}")
        try:
            # Obtém a resposta do chatbot
            response = chatbot.chat(prompt)
            print(f"Resposta: {response}")
        except Exception as e:
            print(f"Erro ao processar a pergunta: {e}")

if __name__ == "__main__":
    main()
