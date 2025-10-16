import cv2
from tkinter import Tk, filedialog
import numpy as np
import pygame
import threading  # Para tocar o som sem travar o vídeo

# --- Caminho do seu áudio ---
CAMINHO_AUDIO = r"c:\Users\iurip\Downloads\WhatsApp-Video-2025-10-16-at-00.47.00.mp3"

# --- Função para tocar som em thread separada ---
def tocar_som():
    def play():
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(CAMINHO_AUDIO)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"⚠️ Erro ao tocar áudio: {e}")
    threading.Thread(target=play, daemon=True).start()

# --- Funções Auxiliares ---
def selecionar_video():
    root = Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo de vídeo",
        filetypes=[("Arquivos de Vídeo", "*.mp4 *.avi *.mov *.mkv")]
    )
    return caminho_arquivo

def criar_tracker(tipo='KCF'):
    if hasattr(cv2, "legacy"):
        TrackerKCF = cv2.legacy.TrackerKCF_create
        TrackerTLD = cv2.legacy.TrackerTLD_create
    else:
        TrackerKCF = getattr(cv2, "TrackerKCF_create", None)
        TrackerTLD = getattr(cv2, "TrackerTLD_create", None)

    if tipo == 'KCF' and TrackerKCF:
        print("⚡ Usando Tracker KCF.")
        return TrackerKCF()
    elif tipo == 'TLD' and TrackerTLD:
        print("🧠 Usando Tracker TLD.")
        return TrackerTLD()
    else:
        raise Exception(f"Tracker '{tipo}' não disponível neste OpenCV.")

# --- Rastreamento com Recuperação ---
def rastreamento_objeto():
    print("""
🎯 Rastreamento de Objeto com Recuperação
-----------------------------------
- Pressione 'g' para SELECIONAR o objeto (ENTER/ESPAÇO para confirmar).
- Pressione 'q' para encerrar.
-----------------------------------
""")

    TRACKER_TYPE = 'KCF'
    caminho = selecionar_video()
    if not caminho:
        print("❌ Nenhum arquivo selecionado.")
        return

    cap = cv2.VideoCapture(caminho)
    if not cap.isOpened():
        print("❌ Erro ao abrir o vídeo.")
        return

    tracker = None
    template = None
    bbox = None
    objeto_presente = False  # Controle para não repetir som

    while True:
        ret, frame = cap.read()
        if not ret:
            print("🎬 Fim do vídeo.")
            break

        key = cv2.waitKey(30) & 0xFF

        # Pressionar 'g' para selecionar o objeto
        if key == ord('g'):
            bbox = cv2.selectROI("Seleção do Objeto", frame, False)
            cv2.destroyWindow("Seleção do Objeto")
            if bbox[2] <= 0 or bbox[3] <= 0:
                print("❌ Seleção inválida. Tente novamente.")
                continue

            x, y, w, h = [int(v) for v in bbox]
            template = frame[y:y+h, x:x+w]
            tracker = criar_tracker(TRACKER_TYPE)
            tracker.init(frame, bbox)
            print("✅ Objeto selecionado e rastreamento iniciado!")

        if tracker is None:
            cv2.putText(frame, "Aperte 'g' para selecionar o objeto", (20, 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if tracker:
            success, box = tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "Objeto Detectado!", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # 🔊 Toca o som apenas uma vez quando o objeto aparecer
                if not objeto_presente:
                    tocar_som()
                    objeto_presente = True
            else:
                objeto_presente = False
                res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                if max_val > 0.7:
                    x, y = max_loc
                    w, h = template.shape[1], template.shape[0]
                    bbox = (x, y, w, h)
                    tracker = criar_tracker(TRACKER_TYPE)
                    tracker.init(frame, bbox)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.putText(frame, "Objeto Reencontrado!", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                else:
                    cv2.putText(frame, "Perdido...", (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Rastreamento de Objeto", frame)

        if key == ord('q'):
            print("🛑 Rastreamento encerrado pelo usuário.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    rastreamento_objeto()
