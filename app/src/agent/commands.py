# src/agent/commands.py
import math
import re
import random
from typing import Dict, List, Optional
from src.logger.log_manager import LogManager
from src.agent.agent import Agent
from src.agent.commands_hardware import MultimediaControl

# Configurações do sistema
MIN_CONFIDENCE = 0.80  # 80% de confiança mínima

log_manager = LogManager()

# Respostas pré-definidas para diferentes cenários
RESPONSES: Dict[str, List[str]] = {
    "low_confidence": [
        "Hmm, a confiança está em {confidence}%... Quer que eu busque fontes alternativas?",
        "Não estou totalmente seguro com {confidence}%. Devo verificar novamente?",
        "Os resultados são um pouco incertos ({confidence}%). Precisa de mais detalhes?",
    ],
    "no_results": [
        "Desculpe, não encontrei nada sobre '{query}'",
        "Parece que '{query}' não está em meu conhecimento atual",
        "Preciso de mais contexto para ajudar com '{query}'",
    ],
    "system_error": [
        "Ops! Algo deu errado. Tente novamente em breve",
        "Encontrei um problema técnico. Meus engenheiros já estão verificando",
        "Erro inesperado! Por favor, repita sua solicitação",
    ],
}


def handle_information_query(
    command: str, agent: Agent, tipo: str, listen_for_command, speak
) -> str:

    # 1. Processamento inicial da query
    """Processa e classifica a consulta do usuário."""
    log_manager.log(f"Processando comando: {command}", level="info")
    # Normalizar a entrada para comparação
    query = command.lower()

    # Verificar se a operação já foi realizada e armazenada no cache
    cached_result = agent.cache.get(query)
    if cached_result:
        log_manager.log(f"Resultado recuperado do cache: {cached_result}")
        return f"O resultado (do cache) é {cached_result}"

    log_manager.log(f"Comando normalizado: {query}", level="debug")

    commando_executato = ""

    # Verificar se o comando contém qualquer uma das palavras-chave relacionadas a multimídia
    if any(keyword in query for keyword in ["música", "música", "música", "volume", "mudo"]):
        multimedia_control = MultimediaControl()
        multimedia_control.start_listener()
        if any(keyword in command for keyword in ["próxima música", "música seguinte"]):
            multimedia_control.next_music()
            commando_executato = "Próxima música"
        elif any(keyword in command for keyword in ["música anterior", "música passada"]):
            multimedia_control.previous_music()
            commando_executato = "Música anterior"
        elif any(keyword in command for keyword in ["aumentar volume", "subir volume"]):
            multimedia_control.volume_up()
            commando_executato = "Volume aumentado"
        elif any(keyword in command for keyword in ["diminuir volume", "baixar volume"]):
            multimedia_control.volume_down()
            commando_executato = "Volume diminuído"
        elif any(keyword in command for keyword in ["mute", "mudo"]):
            multimedia_control.mute()
            commando_executato = "Mudo ativado"

        return commando_executato


    # Caso contrário, realiza o cálculo    
    if any(op in query for op in ["soma", "subtração", "multiplicação", "divisão", "potência", "módulo", "raiz", "média"]):
        result = processar_calculo(query)  # Chama a função de cálculo
        if isinstance(result, str):  # Se for uma string, significa que houve um erro
            return result
        return f"O resultado é {result}"      

    # Verificar se a consulta é uma chat
    if any(keyword in query for keyword in ["chat"]):
        if query.startswith("chat"):                                
            query = query.replace("chat", "").strip()        
        chatbot_response = agent.chatbot.chat(query)    
        return chatbot_response

    # Identificar palavras-chave para busca
    if any(keyword in query for keyword in ["busca", "pesquisa", "encontrar"]):

        if query.startswith("busque:"):        
            query = query.replace("busque:", "").strip()        
        elif query.startswith("pesquise por:"):        
            query = query.replace("pesquise por:", "").strip()        
        elif query.startswith("pesquise:"):        
            query = query.replace("pesquise:", "").strip()

        # Chamar a função de busca no banco de conhecimento
        response = search_neo4j(command, agent, tipo, listen_for_command, speak, query)
        log_manager.log(f"Busca no Neo4j - Pergunta: {query} -> Resposta: {response}")
        return response
            
    # Caso não seja reconhecido
    response = "Desculpe, não entendi a sua pergunta. Vou perguntar ao meu criador."
    chatbot_response = agent.chatbot.chat(query)
    log_manager.log(f"Chatbot - Pergunta: {query} -> Resposta: {chatbot_response}")
    return chatbot_response
    
    return response


def is_math_command(query: str) -> bool:
    """Verifica se a query contém uma expressão matemática simples"""
    math_pattern = r"(\d+(\+|\-|\*|\/)\d+)"
    return bool(re.match(math_pattern, query))


def perform_calculation(query: str) -> float:
    """Executa uma operação matemática simples"""
    try:
        # Substitui as palavras para operações matemáticas e executa o cálculo
        query = (
            query.replace("soma", "+")
            .replace("menos", "-")
            .replace("vezes", "*")
            .replace("dividido", "/")
        )
        result = eval(query)  # Avalia a expressão matemática
        return result
    except Exception as e:
        return f"Erro ao calcular: {e}"


def search_neo4j(command, agent: Agent, tipo: str, listen_for_command, speak, query):
    """Processa a consulta no banco de dados Neo4j e retorna a melhor resposta encontrada"""

    query = _clean_query(query)  # Limpa a query para remoção de palavras-chave

    # 2. Busca no banco de conhecimento
    results = _perform_search(agent, query)

    # 3. Verificação se há resultados válidos
    if not results or "similaridade" not in results[0]:
        return random.choice(RESPONSES["no_results"]).format(query=command)

    # 4. Validação dos resultados
    best_result = results[0]
    confidence = best_result["similaridade"]

    # 5. Resposta conforme confiança
    if confidence < MIN_CONFIDENCE:
        log_manager.log(
            random.choice(RESPONSES["low_confidence"]).format(
                confidence=round(confidence * 100)
            )
        )
        return learn_new_info(agent, query, tipo, listen_for_command, speak)

    # 6. Resposta final formatada
    formatted = format_response(results)
    return f"{formatted} (Confiança: {confidence * 100:.0f}%)"


def learn_new_info(agent: Agent, query: str, tipo: str, listen_for_command, speak):
    if tipo == "voz":
        speak(
            f"Não encontrei uma resposta confiável para '{query}'. Quer me ensinar? Diga 'sim' ou 'não'."
        )
        user_input = listen_for_command()  # Ouve a resposta do usuário

        if user_input and "sim" in user_input.lower():
            speak(f"Ótimo! Por favor, diga a resposta para '{query}'.")
            new_answer = listen_for_command()  # Captura a resposta correta do usuário

            if new_answer:
                # Remover a chave de cache correspondente à query
                # O número 1 aqui representa o top_n, que é 1 pela configuração do comando
                cache_key = f"query:{query}:1"
                # Remover do cache diretamente
                agent.cache.client.delete(cache_key)

                # Ensinar a nova informação
                agent.add_new_knowledge(query, new_answer)
                speak("✅ Aprendi essa nova informação! Obrigado! 🙌")
            else:
                speak("Desculpe, não consegui entender a resposta. Tente novamente.")
        else:
            speak("Ok, não vou adicionar nada por enquanto.")
    else:  # Caso seja entrada de texto
        user_input = (
            input(
                f"Não encontrei uma resposta confiável para '{query}'. Quer me ensinar? (s/n): "
            )
            .strip()
            .lower()
        )
        if user_input == "s":
            new_answer = input(f"Digite a resposta para '{query}': ").strip()

            # Remover a chave de cache correspondente à query
            # O número 1 aqui representa o top_n, que é 1 pela configuração do comando
            cache_key = f"query:{query}:1"
            # Remover do cache diretamente
            agent.cache.client.delete(cache_key)

            # Ensinar a nova informação
            agent.add_new_knowledge(query, new_answer)
            log_manager.log("✅ Aprendi essa nova informação! Obrigado! 🙌")
        else:
            log_manager.log("Ok, não vou adicionar nada por enquanto.")


def _clean_query(command: str) -> str:
    """Remove palavras-chave e normaliza a query"""
    keywords = ["o que é", "quem é", "defina"]
    query = command.lower()
    for keyword in keywords:
        if keyword in query:
            return query.replace(keyword, "", 1).strip()
    return command  # Retorna o comando original se nenhuma keyword for encontrada


def _perform_search(agent: Agent, query: str) -> Optional[List[Dict]]:
    """Executa busca no banco de dados e trata erros"""
    try:
        return agent.query_information(query)
    except Exception as e:
        log_manager.log(f"Erro na busca: {str(e)}")
        return None


def format_response(results: List[Dict]) -> str:
    """Formata a resposta baseada nos resultados encontrados"""
    if len(results) > 1:
        return (
            f"Encontrei {len(results)} resultados relevantes. "
            f"O principal é: {results[0]['texto']}. "
            "Gostaria de ouvir outros resultados?"
        )
    return f"Aqui está a melhor resposta: {results[0]['texto']}"

def processar_calculo(query):
    if any(op in query for op in ["soma", "subtração", "multiplicação", "divisão", "potência", "módulo", "raiz", "média"]):
        if is_math_command(query):
            numbers = [int(num) for num in re.findall(r"\d+", query)]
            if len(numbers) < 2 and "média" not in query and "raiz" not in query:
                return "Desculpe, preciso de pelo menos dois números para realizar a operação."
            result = calcular(query, numbers)
            if isinstance(result, str):  # Caso o resultado seja uma mensagem de erro
                return result
            return f"O resultado é {result}"

def calcular(query, numbers):
    if any(op in query.lower() for op in ["soma", "somar", "quanto é"]):
        if len(numbers) == 2:
            result = numbers[0] + numbers[1]
        else:
            result = sum(numbers)

    elif "subtração" in query.lower():
        if len(numbers) == 2:
            result = numbers[0] - numbers[1]
        else:
            return "Desculpe, a subtração precisa de exatamente dois números."

    elif "multiplicação" in query.lower():
        if len(numbers) == 2:
            result = numbers[0] * numbers[1]
        else:
            return "Desculpe, a multiplicação precisa de exatamente dois números."

    elif "divisão" in query.lower():
        if len(numbers) == 2:
            if numbers[1] != 0:
                result = numbers[0] / numbers[1]
            else:
                return "Desculpe, não posso dividir por zero."
        else:
            return "Desculpe, a divisão precisa de exatamente dois números."

    elif "potência" in query.lower():
        if len(numbers) == 2:
            result = numbers[0] ** numbers[1]
        else:
            return "Desculpe, a potência precisa de exatamente dois números."

    elif "módulo" in query.lower():
        if len(numbers) == 2:
            result = numbers[0] % numbers[1]
        else:
            return "Desculpe, o módulo precisa de exatamente dois números."

    elif "raiz quadrada" in query.lower():
        if len(numbers) == 1:
            if numbers[0] >= 0:
                result = math.sqrt(numbers[0])
            else:
                return "Desculpe, não posso calcular a raiz quadrada de um número negativo."
        else:
            return "Desculpe, a raiz quadrada precisa de um único número."

    elif "média" in query.lower():
        if len(numbers) >= 2:
            result = sum(numbers) / len(numbers)
        else:
            return "Desculpe, para calcular a média preciso de pelo menos dois números."

    else:
        return "Desculpe, não entendi a operação."

    return result