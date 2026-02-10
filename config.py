import os
import ctypes

# Garante a precisão dos pixels no Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# Caminhos de Pastas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Credenciais (Substitua pelos seus dados reais)
USUARIO = "automacao"
SENHA = "12345678a"

# Dicionário de Imagens (Âncoras e Alvos)
IMAGENS = {
    "TELA_SERVIDOR":  os.path.join(ASSETS_DIR, 'tela_servidor.png'),
    "CLICK_SERVIDOR": os.path.join(ASSETS_DIR, 'click_servidor.png'),
    "USUARIO_LOGIN":  os.path.join(ASSETS_DIR, 'usuario_login.png')
}

