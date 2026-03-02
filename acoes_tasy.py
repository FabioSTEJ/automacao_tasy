import pyautogui
import time
import os


# Função auxiliar para localizar e clicar em botões isolados
def clicar_no_botao(nome_arquivo_botao, confiança=0.8):
    # Monta o caminho para a pasta de botões
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_botao = os.path.join(
        diretorio_atual, "assets", "botoes", nome_arquivo_botao
    )

    try:
        # Localiza o centro da imagem na tela
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
    
    # 1. Espera o sistema carregar visualmente
    time.sleep(2) 

    # 2. Tenta clicar no campo de usuário para ganhar o foco
    # Procure tirar um print apenas da caixa branca ou do rótulo "Usuário"
    clicou_campo = clicar_no_botao("botao_usuario.png", confiança=0.8)

    if not clicou_campo:
        print("Aviso: Não encontrei o campo de usuário pelo clique. Tentando focar com TAB...")
        pyautogui.press("tab") # Plano B: Tenta alternar o foco caso o clique falhe
    
    time.sleep(0.5)

    # 3. Limpeza Total (Garante que o campo está vazio)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    time.sleep(0.3)

    # 4. Digitação com Cadência (Intervalo de 0.15s entre as letras)
    print("Digitando credenciais...")
    pyautogui.write("automacao", interval=0.15) 
    pyautogui.press("tab")
    
    time.sleep(0.5) # Pausa entre campos
    
    # Limpa o campo de senha também (por segurança)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    
    pyautogui.write("12345678z", interval=0.15)
    pyautogui.press("enter")
    
    print("Sucesso: Credenciais enviadas. Aguardando transição de tela...")
    time.sleep(4) # Tempo para o servidor processar e a tela mudar
def tratar_fase_gerenciamento_senha():
    print("Iniciando fluxo no Gerenciador de Senha...")

    # PASSO 1: Clicar na Aba Cadastro com verificação
    aba_clicada = False
    for i in range(3):
        print(f"Tentativa {i+1} de clicar na Aba Cadastro...")
        if clicar_no_botao("botao_aba_cadastro.png", confiança=0.85):
            aba_clicada = True
            break
        time.sleep(1.5) # Espera o sistema carregar a interface

    if not aba_clicada:
        print("Erro: Não foi possível abrir a aba Cadastro.")
        return

    # PASSO 2: Aguardar o botão Autoatendimento aparecer (Espera Ativa)
    print("Aba clicada. Aguardando botão Autoatendimento aparecer...")
    
    timeout = 10 # segundos
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if clicar_no_botao("botao_autoatendimento.png", confiança=0.85):
            print("Sucesso: Botão Autoatendimento clicado!")
            return
        time.sleep(0.5) # Checa a cada meio segundo
        
    print("Erro: O botão Autoatendimento não apareceu a tempo.")



def tratar_fase_auto_atendimento():
    print(">>> MODO VIGILÂNCIA ATIVO: Tasy operando em Autoatendimento.")
    # Aqui o robô fica "quieto". 
    # Ele só saiu do loop do main porque detectou essa fase.
    # O controle volta para o main.py que continuará vigiando a tela.
    pass

        
def tratar_fase_login_prosseguir():
    print("Detectada sessão ativa. Clicando em OK para prosseguir...")
    # Tenta clicar no OK até 3 vezes com intervalo, pois popups as vezes demoram a aceitar o clique
    for _ in range(3):
        if clicar_no_botao("botao_ok.png", confiança=0.8):
            print("Sucesso: Botão OK clicado.")
            return True
        time.sleep(1)
    print("Erro: Botão OK não foi encontrado ou clicado.")
    return False

def tratar_fase_funcao():
    botao_funcao = clicar_no_botao("botao_funcao.png", confiança=0.8)

    if botao_funcao:
        print("Sucesso: Botão Função clicado.")
    else:
        print("Erro: Botão Função não foi clicado.")

def tratar_instabilidade_tasy():
    print("⚠️ Alerta: Instabilidade detectada! Tentando recuperar...")
    # Exemplo: Dar um refresh na tela
    pyautogui.hotkey('ctrl', 'shift', 'r')
    time.sleep(5) # Espera o Tasy respirar