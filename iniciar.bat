@echo off
:: =====================================================
:: Script de Gerenciamento de Contêineres Docker
:: Propósito: Facilitar ações de desenvolvimento e publicação
:: Autor: Fernando
:: Data: 2025-03-12
:: =====================================================

:menu
cls
echo ==========================================================
echo Gerenciamento de Contêineres Docker - Menu Principal
echo ==========================================================
echo 0. TESTAR APP (Ambiente de Desenvolvimento)
echo 1. Subir Contêineres (Ambiente de Desenvolvimento)
echo 1. Subir Contêineres (Ambiente de Desenvolvimento)
echo 2. Subir Contêineres (Produção)
echo 3. Derrubar Contêineres (Parar e Remover)
echo 4. [ATENÇÃO] Derrubar Contêineres e Excluir Volumes [IMPORTANTE! APAGA SEUS DADOS DO NEO4J!]
echo 5. Reconstruir Contêineres (Após Atualizar requirements.txt)
echo 6. Mostrar Status dos Contêineres
echo 7. Mostrar Logs
echo 8. Sair
echo ==========================================================
set /p escolha=Escolha uma opção (1-8): 

if "%escolha%" == "0" goto subir
if "%escolha%" == "1" goto subir_dev
if "%escolha%" == "2" goto subir_prod
if "%escolha%" == "3" goto derrubar
if "%escolha%" == "4" goto limpar_volumes
if "%escolha%" == "5" goto reconstruir
if "%escolha%" == "6" goto status
if "%escolha%" == "7" goto logs
if "%escolha%" == "8" goto sair
echo Opção inválida. Tente novamente.
pause
goto menu

:: =====================================================
:: Subir os Contêineres
:subir
echo Subir os contêineres...
docker-compose up -d
pause
goto menu

:: =====================================================
:: Subir Contêineres (Desenvolvimento)
:subir_dev
echo Subindo contêineres para desenvolvimento...
docker-compose -f docker-compose.yml up --build
pause
goto menu

:: =====================================================
:: Subir Contêineres (Produção)
:subir_prod
echo Subindo contêineres para produção...
docker-compose -f docker-compose.prod.yml up --build -d
pause
goto menu

:: =====================================================
:: Derrubar Contêineres
:derrubar
echo Derrubando contêineres...
docker-compose down
pause
goto menu

:: =====================================================
:: [ATENÇÃO] Derrubar Contêineres e Excluir Volumes
:limpar_volumes
cls
echo ==========================================================
echo [IMPORTANTE] Você está prestes a excluir os volumes!
echo Isso irá REMOVER TODOS OS DADOS armazenados no Neo4j.
echo Certifique-se de que você realmente deseja prosseguir.
echo ==========================================================
set /p confirm=Tem certeza que deseja continuar? (s/n): 

if /i "%confirm%" NEQ "s" (
    echo Operação cancelada.
    pause
    goto menu
)

echo Derrubando contêineres e EXCLUINDO volumes...
docker-compose down --volumes
pause
goto menu

:: =====================================================
:: Reconstruir Contêineres (Atualizar requirements.txt)
:reconstruir
echo Reconstruindo contêineres (incluindo dependências)...
docker-compose down
docker-compose build
docker-compose up --build
pause
goto menu

:: =====================================================
:: Mostrar Status dos Contêineres
:status
echo Mostrando o status dos contêineres...
docker ps -a
pause
goto menu

:: =====================================================
:: Mostrar Logs dos Contêineres
:logs
echo Exibindo logs dos contêineres em execução...
docker-compose logs -f
pause
goto menu

:: =====================================================
:: Sair do Script
:sair
echo Saindo... Obrigado por usar o Gerenciador!
exit
