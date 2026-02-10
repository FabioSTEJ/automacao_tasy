import pyautogui
import config
import os

def testar_reconhecimento():
    caminho = config.IMAGENS["TELA_SERVIDOR"]
    
    if not os.path.exists(caminho):
        print(f"❌ ERRO: O arquivo {caminho} não existe!")
        return

    print(f"🔍 Analisando imagem: {os.path.basename(caminho)}")
    print("Tentando diferentes níveis de confiança...")

    # Testa de 90% até 40% de semelhança
    for nivel in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4]:
        try:
            pos = pyautogui.locateOnScreen(caminho, confidence=nivel, grayscale=True)
            if pos:
                print(f"✅ ENCONTRADO com {int(nivel*100)}% de confiança!")
                print(f"📍 Coordenadas: {pos}")
                return
            else:
                print(f"--- {int(nivel*100)}%: Não encontrado")
        except Exception as e:
            print(f"⚠️ Erro no nível {nivel}: {e}")

    print("\n❌ CONCLUSÃO: O Python não reconhece a imagem nem com 40% de semelhança.")
    print("DICA: Tire um novo print usando a ferramenta 'Captura e Esboço' do Windows (Win + Shift + S)")

if __name__ == "__main__":
    testar_reconhecimento()