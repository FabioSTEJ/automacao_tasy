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
        return True
    else:
        print("Erro ao selecionar o servidor de produção.")
        return False

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
    return True

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
        return False

    print("Aba clicada. Aguardando botão Autoatendimento aparecer...")
    
    timeout = 10
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if clicar_no_botao("botao_autoatendimento.png", confiança=0.85):
            print("Sucesso: Botão Autoatendimento clicado!")
            return True
        time.sleep(0.5)
        
    print("Erro: O botão Autoatendimento não apareceu a tempo.")
    return False

def tratar_fase_auto_atendimento():
    print(">>> MODO VIGILÂNCIA ATIVO: Tasy operando em Autoatendimento.")
    return True

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
    print("[LOG]: Iniciando validação de Cadastro do Computador...")
    
    # --- PASSO 1: O BOTÃO INICIAL ESTÁ LÁ? ---
    # Tentamos ver se o botão de "Cadastrar" aparece.
    if clicar_no_botao("botao_cadastro_computador.png", confiança=0.8):
        print("[SUCESSO]: Passo 1 detectado e clicado. Abrindo formulário...")
        time.sleep(1.5) # Espera o formulário abrir
    else:
        print("[INFO]: Botão inicial não encontrado. Verificando se já estamos no Passo 2...")

    # --- PASSO 2: DIGITAÇÃO DA SEQUÊNCIA ---
    # Aqui não usamos 'if not', apenas tentamos agir no campo que já deve estar aberto
    try:
        nome_pc = socket.gethostname().upper()
        sequencia = MAPA_SEQUENCIAS_TOTEM.get(nome_pc, MAPA_SEQUENCIAS_TOTEM.get("DEFAULT", "000"))
        
        # Tentativa de focar e digitar
        print(f"[AÇÃO]: Tentando digitar sequência {sequencia} para {nome_pc}...")
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        time.sleep(0.3)
        pyautogui.write(sequencia, interval=0.15)
        pyautogui.press('enter')
        time.sleep(1.0)
    except Exception as e:
        print(f"[ERRO]: Falha ao tentar digitar: {e}")
        return False

    print("[AÇÃO]: Verificando botões de confirmação (OK)...")
    
    # Tenta o primeiro OK
    primeiro_ok = clicar_no_botao("botao_ok_cadastro.png", confiança=0.8)
    
    if primeiro_ok:
        print("[OK]: Primeiro OK clicado. Aguardando possível popup secundário...")
        time.sleep(1.5)
        # Tenta o segundo OK (se houver popup de confirmação)
        clicar_no_botao("botao_ok_cadastro.png", confiança=0.8)
        print("[SUCESSO]: Processo de cadastro finalizado.")
        return True
    else:
        # Se não achou nem o botão inicial, nem o OK, então algo deu errado
        print("[AVISO]: Nenhum botão de interação (Cadastro ou OK) foi encontrado.")
        return False
def tratar_fase_funcao():
    botao_funcao = clicar_no_botao("botao_funcao.png", confiança=0.8)

    if botao_funcao:
        print("Sucesso: Botão Função clicado.")
        return True
    else:
        print("Erro: Botão Função não foi clicado.")
        return False

def tratar_instabilidade_tasy():
    print("⚠️ Alerta: Instabilidade detectada! Tentando recuperar...")
    pyautogui.hotkey('ctrl', 'shift', 'r')
    time.sleep(5)
    return True

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