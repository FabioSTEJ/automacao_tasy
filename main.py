import identificador_fase
import acoes_tasy
import time

def rodar_robo():
    print("Iniciando monitoramento do Tasy...")
    ultima_fase = None

    while True:
        # 1. O Identificador diz qual é a tela atual
        fase = identificador_fase.identificar_fase_atual()
        
        # 2. Se a fase mudou, executamos a ação correspondente
        if fase != "DESCONHECIDO" and fase != ultima_fase:
            print(f"--- Entrando na fase: {fase} ---")
            
            if fase == "SERVIDOR":
                acoes_tasy.tratar_fase_servidor()
                ultima_fase = fase
                
            elif fase == "LOGIN":
                acoes_tasy.tratar_fase_login()
                ultima_fase = fase

        time.sleep(1)

if __name__ == "__main__":
    rodar_robo()