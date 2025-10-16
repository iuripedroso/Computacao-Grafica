from camera import abrir_camera
from camera_tempo_real import camera_interativa
from imagens_tempo_real import interacao_tempo_real
from rastreamento import rastreamento_objeto    

# (opcional futuramente)
# from operacoes_imagens import menu_operacoes_imagens
# from rastreamento_video import rastrear_video

def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Abrir câmera (normal)")
        print("2 - Câmera interativa em tempo real")
        print("3 - Interação em tempo real com imagem carregada")
        print("4 - Rastrear objetos em video")
        # print("5 - Rastreamento de objeto em vídeo")
        print("q - Sair")


        opcao = input("Escolha uma opção: ").lower().strip()

        if opcao == '1':
            abrir_camera()
        elif opcao == '2':
            camera_interativa()
        elif opcao == '3':
            interacao_tempo_real()
        elif opcao == '4':
            rastreamento_objeto()
        # elif opcao == '5':
        #     rastrear_video()
        elif opcao == 'q':
            print("Encerrando o programa...")
            break
        else:
            print("⚠️  Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
