import pyautogui
import time
import os
import socket  # Importado para ler o nome da máquina (Hostname)
from config_totem import MAPA_SEQUENCIAS_TOTEM  # Importa o mapa do arquivo separado

def clicar_no_botao(nome_arquivo_botao, confiança=0.8):
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_botao = os.path.join(
        diretorio_atual, "assets", "botoes", nome_arquivo_botao
    )

    try:
        ponto_clique = pyautogui.locateCenterOnScreen(
            caminho_botao, confidence=confiança
        )

        if ponto_clique:
            pyautogui.click(ponto_clique)
            return True
        else:
            print(f"Aviso: Botão {nome_arquivo_botao} não visível na tela.")
            return False
    except Exception as e:
        print(f"Erro ao tentar clicar no botão {nome_arquivo_botao}: {e}")
        return False

def tratar_fase_servidor():
    print("Selecionando Servidor de Produção...")
    sucesso = clicar_no_botao("botao_producao.png")

    if sucesso:
        time.sleep(0.5)
        pyautogui.press("enter")
        print("Servidor selecionado.")
    else:
        print("Erro ao selecionar o servidor de produção.")

def tratar_fase_login():
    print("Iniciando processo de Login Blindado...")
    
    time.sleep(2) 

    clicou_campo = clicar_no_botao("botao_usuario.png", confiança=0.8)

    if not clicou_campo:
        print("Aviso: Não encontrei o campo de usuário pelo clique. Tentando focar com TAB...")
        pyautogui.press("tab") 
    
    time.sleep(0.5)
    
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    time.sleep(0.3)

    print("Digitando credenciais...")
    pyautogui.write("automacao", interval=0.15) 
    pyautogui.press("tab")
    
    time.sleep(0.5) 
    
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    
    pyautogui.write("12345678z", interval=0.15)
    pyautogui.press("enter")
    
    print("Sucesso: Credenciais enviadas. Aguardando transição de tela...")
    time.sleep(4)

def tratar_fase_gerenciamento_senha():
    print("Iniciando fluxo no Gerenciador de Senha...")
    
    aba_clicada = False
    for i in range(3):
        print(f"Tentativa {i+1} de clicar na Aba Cadastro...")
        if clicar_no_botao("botao_aba_cadastro.png", confiança=0.85):
            aba_clicada = True
            break
        time.sleep(1.5)

    if not aba_clicada:
        print("Erro: Não foi possível abrir a aba Cadastro.")
        return

    print("Aba clicada. Aguardando botão Autoatendimento aparecer...")
    
    timeout = 10
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if clicar_no_botao("botao_autoatendimento.png", confiança=0.85):
            print("Sucesso: Botão Autoatendimento clicado!")
            return
        time.sleep(0.5)
        
    print("Erro: O botão Autoatendimento não apareceu a tempo.")

def tratar_fase_auto_atendimento():
    print(">>> MODO VIGILÂNCIA ATIVO: Tasy operando em Autoatendimento.")
    pass 

def tratar_fase_login_prosseguir():
    print("Detectada sessão ativa. Clicando em OK para prosseguir...")
    for _ in range(3):
        if clicar_no_botao("botao_ok.png", confiança=0.8):
            print("Sucesso: Botão OK clicado.")
            return True
        time.sleep(1)
    print("Erro: Botão OK não foi encontrado ou clicado.")
    return False
def tratar_fase_cadastro_computador():
    print("[LOG]: Fase de cadastro do computador.")
    
    # 1. Clica na caixa (campo) que vai receber a sequência para garantir o foco
    botao_cadastro = clicar_no_botao("botao_cadastro_computador.png", confiança=0.8)
    
    if not botao_cadastro:
        print("Erro: Botão de cadastro do computador não encontrado.")
    else:
        print("Sucesso: Botão de cadastro do computador clicado. Identificando máquina...")
        time.sleep(0.8) # Tempo para o campo focar corretamente

        # 2. Identifica o nome desta máquina (Hostname) e busca a sequência
        nome_pc = socket.gethostname().upper()
        sequencia = MAPA_SEQUENCIAS_TOTEM.get(nome_pc, MAPA_SEQUENCIAS_TOTEM.get("DEFAULT", "000"))
        
        print(f"[AÇÃO]: Computador {nome_pc} identificado. Digitando sequência {sequencia}...")

        # 3. Limpeza de segurança e digitação da sequência
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        time.sleep(0.3)
        
        pyautogui.write(sequencia, interval=0.15)
        
        # 4. Sequência de Cliques no OK de Cadastro (2 tempos)
        print("[AÇÃO]: Iniciando confirmação em 2 tempos...")
        
        # Primeiro Clique (Para confirmar a digitação/fechar campo)
        if clicar_no_botao("botao_ok_cadastro.png", confiança=0.8):
            print("Primeiro OK clicado. Aguardando 1 segundo para o popup...")
            time.sleep(1.0)
            
            # Segundo Clique (Para fechar o popup de 'Máquina informada com sucesso')
            if clicar_no_botao("botao_ok_cadastro.png", confiança=0.8):
                print(f"[OK]: Cadastro da máquina {nome_pc} e popup confirmados.")
            else:
                print("[AVISO]: Segundo clique no OK não foi possível (Popup não apareceu ou já fechou).")
        else:
            print("[ERRO]: Não foi possível realizar o primeiro clique no botao_ok_cadastro.png.")
def tratar_fase_funcao():
    botao_funcao = clicar_no_botao("botao_funcao.png", confiança=0.8)

    if botao_funcao:
        print("Sucesso: Botão Função clicado.")
    else:
        print("Erro: Botão Função não foi clicado.")

def tratar_instabilidade_tasy():
    print("⚠️ Alerta: Instabilidade detectada! Tentando recuperar...")
    pyautogui.hotkey('ctrl', 'shift', 'r')
    time.sleep(5)

def salvar_print_erro():
    """Tira um print da tela e salva na pasta logs_erros para análise posterior."""
    diretorio_logs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs_erros")
    
    if not os.path.exists(diretorio_logs):
        os.makedirs(diretorio_logs)
        print(f"[SISTEMA] Pasta de logs criada: {diretorio_logs}")

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"erro_desconhecido_{timestamp}.png"
    caminho_final = os.path.join(diretorio_logs, nome_arquivo)
    try:
        pyautogui.screenshot(caminho_final)
        print(f"[CÂMERA] Evidência salva em: {caminho_final}")
    except Exception as e:
        print(f"[ERRO] Falha ao capturar print: {e}")
        #teste