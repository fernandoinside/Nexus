#!/bin/bash

# =====================================================
# Script de Auxílio ao Desenvolvimento
# Propósito: Gerenciar a aplicação local, testes e Docker
# =====================================================

menu() {
    clear
    echo "=========================================================="
    echo "Iniciar - Auxiliar no Desenvolvimento"
    echo "=========================================================="
    echo "1. Criar ambiente virtual"
    echo "2. Ativar ambiente virtual e rodar a aplicação"
    echo "3. Executar todos os testes dentro do ambiente virtual"
    echo "4. Executar um teste específico dentro do ambiente virtual"
    echo "5. Subir contêineres Docker (Desenvolvimento)"
    echo "6. Derrubar contêineres Docker"
    echo "7. Mostrar status dos contêineres Docker"
    echo "8. Sair"
    echo "=========================================================="
    read -p "Escolha uma opção (1-8): " escolha

    case $escolha in
        1) criar_venv ;;
        2) rodar_venv_app ;;
        3) rodar_venv_todos_testes ;;
        4) rodar_venv_teste_especifico ;;
        5) subir_docker ;;
        6) derrubar_docker ;;
        7) status_docker ;;
        8) sair ;;
        *) echo "Opção inválida"; sleep 2; menu ;;
    esac
}

criar_venv() {
    clear
    echo "Criando o ambiente virtual..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "Ambiente virtual criado com sucesso!"
        echo "Instale as dependências com 'pip install -r requirements.txt'"
    else
        echo "Erro ao criar o ambiente virtual!"
    fi
    read -p "Pressione ENTER para continuar..."
    menu
}

rodar_venv_app() {
    clear
    echo "Ativando o ambiente virtual..."
    source venv/bin/activate
    if [ $? -eq 0 ]; then
        echo "Ambiente virtual ativado."
        echo "Rodando a aplicação..."
        python app/app.py
        deactivate
    else
        echo "Erro ao ativar o ambiente virtual!"
    fi
    read -p "Pressione ENTER para continuar..."
    menu
}

rodar_venv_todos_testes() {
    clear
    echo "Ativando o ambiente virtual..."
    source venv/bin/activate
    if [ $? -eq 0 ]; then
        echo "Ambiente virtual ativado."
        echo "Executando todos os testes..."
        for teste in app/src/test/test_*.py; do
            echo "Rodando $teste..."
            python "$teste"
            echo
        done
        deactivate
    else
        echo "Erro ao ativar o ambiente virtual!"
    fi
    read -p "Pressione ENTER para continuar..."
    menu
}

rodar_venv_teste_especifico() {
    clear
    echo "Escolha um teste para executar:"
    mapfile -t testes < <(find app/src/test -name "test_*.py")
    for i in "${!testes[@]}"; do
        echo "$((i+1)). ${testes[$i]}"
    done
    read -p "Digite o número do teste: " escolha_teste
    if [ -n "${testes[$((escolha_teste-1))]}" ]; then
        source venv/bin/activate
        python "${testes[$((escolha_teste-1))]}"
        deactivate
    else
        echo "Opção inválida!"
    fi
    read -p "Pressione ENTER para continuar..."
    menu
}

subir_docker() {
    clear
    echo "Subindo contêineres Docker para desenvolvimento..."
    docker-compose -f docker-compose.yml up --build -d
    read -p "Pressione ENTER para continuar..."
    menu
}

derrubar_docker() {
    clear
    echo "Derrubando contêineres Docker..."
    docker-compose down
    read -p "Pressione ENTER para continuar..."
    menu
}

status_docker() {
    clear
    echo "Status dos contêineres Docker:"
    docker ps -a
    read -p "Pressione ENTER para continuar..."
    menu
}

sair() {
    echo "Saindo... Até logo!"
    exit 0
}

# Inicia o script
menu
