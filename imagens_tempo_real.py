import cv2
import numpy as np
from tkinter import Tk, filedialog
import os

# Pasta para salvar as imagens
PASTA_SALVAR = r"C:\Users\iurip\OneDrive\Área de Trabalho\trabalho PDI\imgs"
os.makedirs(PASTA_SALVAR, exist_ok=True)


def selecionar_imagem():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    caminho = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    root.destroy()
    return caminho


def salvar_imagem(nome, img):
    caminho = os.path.join(PASTA_SALVAR, nome)
    cv2.imwrite(caminho, img)
    print(f"💾 Imagem salva em: {caminho}")


def gerar_bit_planes(img):
    """Gera e salva os bit planes 5-7."""
    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img.copy()

    for i in range(5, 8):
        bit_mask = 2 ** i
        plane = np.bitwise_and(img_gray, bit_mask)
        plane[plane > 0] = 255
        salvar_imagem(f"bit_plane_{i}.png", plane)


def interacao_tempo_real():
    caminho = selecionar_imagem()
    if not caminho:
        print("❌ Nenhum arquivo selecionado.")
        return

    img_original = cv2.imread(caminho)
    if img_original is None:
        print("❌ Erro ao carregar a imagem.")
        return

    img_atual = img_original.copy()
    cv2.namedWindow("Imagem Interativa")

    print("""
🎨 Comandos em tempo real:
g - Cinza
n - Negativo
b - Binário Otsu
r - Reset para original
p - Salvar Bit Planes 5-7
s - Salvar imagem atual
q - Fechar
""")

    while True:
        cv2.imshow("Imagem Interativa", img_atual)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('r'):
            img_atual = img_original.copy()
            print("🔄 Reset para imagem original")
        elif key == ord('g'):
            img_atual = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
            print("🎨 Convertido para Cinza")
        elif key == ord('n'):
            img_atual = cv2.bitwise_not(img_original)
            print("🌑 Convertido para Negativo")
        elif key == ord('b'):
            gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
            _, img_atual = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            print("⚪ Convertido para Binário (Otsu)")
        elif key == ord('p'):
            gerar_bit_planes(img_atual)
            print("📊 Bit Planes 5-7 gerados e salvos")
        elif key == ord('s'):
            salvar_imagem("imagem_atual.png", img_atual)
            print("💾 Imagem atual salva")

    cv2.destroyAllWindows()
    print("✅ Fechado")


if __name__ == "__main__":
    interacao_tempo_real()
