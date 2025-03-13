@echo off
:: =====================================================
:: Script de Auxílio ao Desenvolvimento
:: Propósito: Gerenciar a aplicação local, testes e Docker
:: Autor: Fernando
:: Data: 2025-03-12
:: =====================================================

:menu
cls
echo ==========================================================
echo Iniciar - Auxiliar no Desenvolvimento
echo ==========================================================
echo 1. Criar ambiente virtual
echo 2. Ativar ambiente virtual e rodar a aplicação
echo 3. Executar todos os testes dentro do ambiente virtual
echo 4. Executar um teste específico dentro do ambiente virtual
echo 5. Subir contêineres Docker (Desenvolvimento)
echo 6. Derrubar contêineres Docker
echo 7. Mostrar status dos contêineres Docker
echo 8. Sair
echo ==========================================================
set /p escolha=Escolha uma opção (1-8): 

if "%escolha%" == "1" goto criar_venv
if "%escolha%" == "2" goto rodar_venv_app
if "%escolha%" == "3" goto rodar_venv_todos_testes
if "%escolha%" == "4" goto rodar_venv_teste_especifico
if "%escolha%" == "5" goto subir_docker
if "%escolha%" == "6" goto derrubar_docker
if "%escolha%" == "7" goto status_docker
if "%escolha%" == "8" goto sair
echo Opção inválida. Tente novamente.
pause
goto menu

:: =====================================================
:: Criar ambiente virtual
:criar_venv
cls
echo Criando o ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo Erro ao criar o ambiente virtual!
    pause
    goto menu
)
echo Ambiente virtual criado com sucesso!
echo Instale as dependências com "pip install -r requirements.txt".
pause
goto menu

:: =====================================================
:: Ativar ambiente virtual e rodar a aplicação
:rodar_venv_app
cls
echo Ativando o ambiente virtual...
call venv\Scripts\activate
if errorlevel 1 (
    echo Erro ao ativar o ambiente virtual!
    pause
    goto menu
)
echo Ambiente virtual ativado.
echo Rodando a aplicação...
python app\app.py
deactivate
pause
goto menu

:: =====================================================
:: Executar todos os testes dentro do ambiente virtual
:rodar_venv_todos_testes
cls
echo Ativando o ambiente virtual...
call venv\Scripts\activate
if errorlevel 1 (
    echo Erro ao ativar o ambiente virtual!
    pause
    goto menu
)
echo Ambiente virtual ativado.
echo Executando todos os testes...
for %%f in (app\src\test\test_*.py) do (
    echo Rodando %%f...
    python %%f
    echo.
)
deactivate
pause
goto menu

:: =====================================================
:: Executar um teste específico dentro do ambiente virtual
:rodar_venv_teste_especifico
cls
echo Escolha um teste para executar:
setlocal enabledelayedexpansion
set i=0
for %%f in (app\src\test\test_*.py) do (
    set /a i+=1
    echo !i!. %%f
    set "testes[!i!]=%%f"
)
set /p escolha_teste=Digite o número do teste: 
if defined testes[%escolha_teste%] (
    set teste_selecionado=!testes[%escolha_teste%]!
    echo Ativando o ambiente virtual...
    call venv\Scripts\activate
    if errorlevel 1 (
        echo Erro ao ativar o ambiente virtual!
        pause
        goto menu
    )
    echo Ambiente virtual ativado.
    echo Rodando !teste_selecionado!...
    python !teste_selecionado!
    deactivate
) else (
    echo Opção inválida!
)
pause
goto menu

:: =====================================================
:: Subir contêineres Docker (Desenvolvimento)
:subir_docker
cls
echo Subindo contêineres Docker para desenvolvimento...
docker-compose -f docker-compose.yml up --build -d
pause
goto menu

:: =====================================================
:: Derrubar contêineres Docker
:derrubar_docker
cls
echo Derrubando contêineres Docker...
docker-compose down
pause
goto menu

:: =====================================================
:: Mostrar status dos contêineres Docker
:status_docker
cls
echo Status dos contêineres Docker:
docker ps -a
pause
goto menu

:: =====================================================
:: Sair do Script
:sair
echo Saindo... Até logo!
exit
