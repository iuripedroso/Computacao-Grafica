import cv2
import os
from tkinter import Tk, filedialog

# --- Variáveis globais ---
imagem_atual = None
caminho_atual = None

# --- Câmera ---
def abrir_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Erro: não foi possível acessar a câmera.")
        return

    print("📷 Câmera aberta — pressione 'q' para sair.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame.")
            break

        frame = cv2.flip(frame, 1)

        cv2.imshow("Câmera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Câmera encerrada.")

def selecionar_video():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    caminho = filedialog.askopenfilename(
        title="Selecione um vídeo",
        filetypes=[("Vídeos", "*.mp4 *.avi *.mov *.mkv")]
    )
    root.destroy()
    return caminho