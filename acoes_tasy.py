import pyautogui
import time
import os
import socket
import identificador_fase
from config_totem import MAPA_SEQUENCIAS_TOTEM


# ---------------------------------------------------------------------------


def aguardar_elemento(nome_arquivo, confiança=0.8, subpasta="botoes", timeout=10, intervalo=0.5):

    inicio = time.time()
    while time.time() - inicio < timeout:
        if verificar_elemento_local(nome_arquivo, confiança=confiança, subpasta=subpasta):
            return True
        time.sleep(intervalo)
    print(f"[TIMEOUT] Elemento '{nome_arquivo}' não apareceu em {timeout}s.")
    return False


def aguardar_fase(fase_esperada, timeout=15, intervalo=0.5):

    inicio = time.time()
    while time.time() - inicio < timeout:
        if identificador_fase.identificar_fase_atual() == fase_esperada:
            return True
        time.sleep(intervalo)
    print(f"[TIMEOUT] Fase '{fase_esperada}' não detectada em {timeout}s.")
    return False


def verificar_elemento_local(nome_arquivo, confiança=0.8, subpasta="botoes"):

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(diretorio_atual, "assets", subpasta, nome_arquivo)
    if not os.path.exists(caminho):
        return False
    try:
        return pyautogui.locateOnScreen(caminho, confidence=confiança) is not None
    except Exception:
        return False
    

def clicar_no_botao(nome_arquivo_botao, confiança=0.8, subpasta="botoes"):
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_botao = os.path.join(
        diretorio_atual, "assets", subpasta, nome_arquivo_botao
    )

    if not os.path.exists(caminho_botao):
        return False

    try:
        if ponto_clique := pyautogui.locateCenterOnScreen(caminho_botao, confidence=confiança):
            pyautogui.click(ponto_clique)
        return True
    except Exception as e:
        print(f"Erro ao tentar clicar no botão {nome_arquivo_botao}: {e}")
        return False
    

def tratar_fase_servidor():
    print("Selecionando Servidor de Produção...")

    if sucesso := clicar_no_botao("botao_producao.png"):
        pyautogui.press("enter")
        print("Servidor selecionado.")
        return True
    else:
        print("Erro ao selecionar o servidor de produção.")
        return False
    

def tratar_fase_login():  # sourcery skip: extract-duplicate-method
    print("Iniciando processo de Login Blindado...")

    if campo_disponivel := aguardar_elemento("botao_usuario.png", confiança=0.8, timeout=10):
        clicar_no_botao("botao_usuario.png", confiança=0.8)
    else:
        print("Aviso: Campo de usuário não apareceu a tempo. Tentando focar com TAB...")
        pyautogui.press("tab")

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')

    print("Digitando credenciais...")
    pyautogui.write("automacao", interval=0.15)
    pyautogui.press("tab")

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')

    pyautogui.write("12345678z", interval=0.15)
    pyautogui.press("enter")

    print("Credenciais enviadas. Aguardando transição de tela...")

    inicio = time.time()
    while time.time() - inicio < 15:
        if identificador_fase.identificar_fase_atual() != "LOGIN":
            print("Sucesso: Transição de tela detectada.")
            return True
        time.sleep(0.5)

    print("Aviso: Tela não mudou após envio de credenciais. Pode ter havido erro de login.")
    return True 


def tratar_fase_gerenciamento_senha():
    print("Iniciando fluxo no Gerenciador de Senha...")

    print("[FLUXO] Verificando se o cadastro de computador aparece...")
    inicio = time.time()
    while time.time() - inicio < 5:
        fase_atual = identificador_fase.identificar_fase_atual()
        if fase_atual == "CADASTRO_COMPUTADOR":
            print("[FLUXO] Tela de Cadastro de Computador detectada. Transferindo controle...")
            return True
        if fase_atual != "GERENCIADOR_SENHA":
            break  
        time.sleep(0.5)

    print("[FLUXO] Cadastro de computador não é necessário. Prosseguindo para o autoatendimento...")

    aba_clicada = False
    for i in range(3):
        print(f"Tentativa {i+1} de clicar na Aba Cadastro...")
        if clicar_no_botao("botao_aba_cadastro.png", confiança=0.85):
            aba_clicada = True
            break

        aguardar_elemento("botao_aba_cadastro.png", confiança=0.85, timeout=3)

    if not aba_clicada:
        print("ERRO: Não foi possível clicar na aba Cadastro.")
        return False

    print("Aba clicada. Aguardando botão Autoatendimento aparecer...")

    # Polling até o botão aparecer e clicar
    if aguardar_elemento("botao_autoatendimento.png", confiança=0.85, timeout=10) and clicar_no_botao("botao_autoatendimento.png", confiança=0.85):
        print("Sucesso: Botão Autoatendimento clicado!")
        return True

    print("ERRO: O botão Autoatendimento não apareceu a tempo.")
    return False


def tratar_fase_auto_atendimento():
    print(">>> MODO VIGILÂNCIA ATIVO: Tasy operando em Autoatendimento.")
    return True


def monitorar_instabilidade_autoatendimento():
    """
    Verifica erros, alertas ou travamentos durante o Autoatendimento.
    Retorna True se alguma ação corretiva foi tomada.
    """
    # 1. Verifica e fecha popups de erro (rápido, sem espera)
    botoes_alerta = ["botao_fechar_erro.png", "botao_ok_alerta.png", "botao_tentar_novamente.png"]
    for botao in botoes_alerta:
        if clicar_no_botao(botao, confiança=0.85, subpasta="classificador"):
            print(f"[MONITOR] Alerta detectado e tratado: {botao}")
            time.sleep(1)
            return True

    if identificador_fase.verificar_elemento("icone_carregando.png", confiança=0.8, subpasta="classificador"):
        print("[MONITOR] Carregamento detectado. Iniciando cronômetro de segurança...")

        limite_espera = 40
        inicio_carregamento = time.time()

        while time.time() - inicio_carregamento < limite_espera:
            if not identificador_fase.verificar_elemento("icone_carregando.png", confiança=0.8, subpasta="classificador"):
                print("[MONITOR] Carregamento finalizado com sucesso dentro do tempo.")
                return False
            time.sleep(2)

        print("[ALERTA] Tempo limite de carregamento excedido! Tentando recuperação...")

        pyautogui.press('esc')
        time.sleep(3)

        if identificador_fase.verificar_elemento("icone_carregando.png", confiança=0.8, subpasta="classificador"):
            print("[CRÍTICO] Resetando sistema via Refresh...")
            tratar_instabilidade_tasy()
            return True

    return False


def tratar_fase_login_prosseguir():
    print("Detectada sessão ativa. Clicando em OK para prosseguir...")

    if aguardar_elemento("botao_ok.png", confiança=0.8, timeout=5) and clicar_no_botao("botao_ok.png", confiança=0.8):
        print("Sucesso: Botão OK clicado.")
        return True

    print("Erro: Botão OK não foi encontrado ou clicado.")
    return False


def obter_sequencia_computador():
    try:
        nome_pc = socket.gethostname().upper()
        sequencia = MAPA_SEQUENCIAS_TOTEM.get(nome_pc, MAPA_SEQUENCIAS_TOTEM.get("DEFAULT", "000"))
        return nome_pc, sequencia
    except Exception as e:
        print(f"[ERRO]: Falha ao obter sequência do computador: {e}")
        return None, None


def tratar_fase_cadastro_computador():
    print("[LOG]: Iniciando validação de Cadastro do Computador...")

    if aguardar_elemento("botao_cadastro_computador.png", confiança=0.8, timeout=3):
        clicar_no_botao("botao_cadastro_computador.png", confiança=0.8)
        print("[SUCESSO]: Passo 1 detectado e clicado. Aguardando formulário abrir...")
        # Aguarda o formulário abrir dinamicamente
        aguardar_elemento("botao_ok_cadastro.png", confiança=0.8, timeout=5)
    else:
        print("[INFO]: Botão inicial não encontrado. Verificando se já estamos no Passo 2...")

    nome_pc, sequencia = obter_sequencia_computador()
    if nome_pc is None or sequencia is None:
        return False

    print(f"[AÇÃO]: Tentando digitar sequência {sequencia} para {nome_pc}...")
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(sequencia, interval=0.15)

    print("[AÇÃO]: Verificando botões de confirmação (OK)...")

    # Aguarda o botão OK aparecer e clica
    if aguardar_elemento("botao_ok_cadastro.png", confiança=0.8, timeout=5):
        clicar_no_botao("botao_ok_cadastro.png", confiança=0.8)
        print("[OK]: Primeiro OK clicado. Aguardando possível popup secundário...")

        # Aguarda e tenta o segundo OK se houver popup de confirmação
        if aguardar_elemento("botao_ok_cadastro.png", confiança=0.8, timeout=3):
            clicar_no_botao("botao_ok_cadastro.png", confiança=0.8)

        print("[SUCESSO]: Processo de cadastro finalizado.")
        return True
    else:
        print("[AVISO]: Nenhum botão de interação (Cadastro ou OK) foi encontrado.")
        return False


def tratar_fase_funcao():
    if clicar_no_botao("botao_funcao.png", confiança=0.8):
        print("Sucesso: Botão Função clicado.")
        return True
    else:
        print("Erro: Botão Função não foi clicado.")
        return False


def tratar_instabilidade_tasy():
    print("⚠️ Alerta: Instabilidade detectada! Tentando recuperar...")
    pyautogui.hotkey('ctrl', 'shift', 'r')

    inicio = time.time()
    while time.time() - inicio < 15:
        fase = identificador_fase.identificar_fase_atual()
        if fase not in ("DESCONHECIDO", "ERRO_PASTA"):
            print(f"[RECUPERAÇÃO] Sistema estabilizou na fase: {fase}")
            return True
        time.sleep(1)

    print("[RECUPERAÇÃO] Sistema não estabilizou após refresh.")
    return True


def salvar_print_erro():
    
    diretorio_logs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/logs_erros")

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