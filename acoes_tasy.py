import pyautogui
import time
import os

# Função auxiliar para localizar e clicar em botões isolados
def clicar_no_botao(nome_arquivo_botao, confiança=0.8):
    # Monta o caminho para a pasta de botões
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_botao = os.path.join(diretorio_atual, 'assets', 'botoes', nome_arquivo_botao)
    
    try:
        # Localiza o centro da imagem na tela
        ponto_clique = pyautogui.locateCenterOnScreen(caminho_botao, confidence=confiança)
        
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
    print("Logica: Selecionando Servidor de Produção...")
    
    # Em vez de 'press p', tentamos clicar no botão específico
    # Certifique-se de que o arquivo 'botao_producao.png' existe na pasta
    sucesso = clicar_no_botao('botao_producao.png')
    
    if sucesso:
        time.sleep(0.5)
        pyautogui.press('enter')
        print("Sucesso: Botão de servidor clicado.")
    else:
        # Fallback caso o clique por imagem falhe (opcional)
        pyautogui.press('p')
        pyautogui.press('enter')

def tratar_fase_login():
    print("Logica: Realizando Login...")
    
    # Aqui mantivemos sua lógica de escrita, que é mais segura que cliques se o campo já ganha foco
    pyautogui.write('automacao', interval=0.4)
    pyautogui.press('tab')
    pyautogui.write('12345678z', interval=0.4)
    pyautogui.press('enter')
    print("Sucesso: Credenciais enviadas.")