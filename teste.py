import cv2
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, filedialog


def selecionar_imagem():
    """Abre um seletor de arquivos e retorna o caminho da imagem escolhida."""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    caminho = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    root.destroy()
    return caminho


def calcular_area_perimetro_diametro(binaria):
    """Calcula área, perímetro e diâmetro de objetos em imagem binária."""
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print(f"🔍 {len(contornos)} objeto(s) detectado(s):\n")

    for i, contorno in enumerate(contornos):
        area = cv2.contourArea(contorno)
        perimetro = cv2.arcLength(contorno, True)
        (x, y), raio = cv2.minEnclosingCircle(contorno)
        diametro = 2 * raio

        # print(f"Objeto {i+1}:")
        # print(f"  📏 Área: {area:.2f} px²")
        # print(f"  🔹 Perímetro: {perimetro:.2f} px")
        # print(f"  ⚪ Diâmetro aproximado: {diametro:.2f} px\n")

    # Mostrar contornos
    img_contornos = cv2.cvtColor(binaria, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(img_contornos, contornos, -1, (0, 0, 255), 2)
    cv2.imshow("Contornos detectados", img_contornos)
    cv2.waitKey(0)

    if cv2.getWindowProperty("Contornos detectados", cv2.WND_PROP_VISIBLE) >= 1:
        cv2.destroyWindow("Contornos detectados") #tratamento de excessao



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
h - Exibir histograma de cores (BGR)
d - Calcular área, perímetro e diâmetro (em binário)
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
        elif key == ord('h'):
            colors = ('b', 'g', 'r')
            plt.figure(figsize=(8,4))
            plt.title("Histograma de Cores (BGR)")
            plt.xlabel("Intensidade (0 - 255)")
            plt.ylabel("Número de Pixels")

            for i, color in enumerate(colors):
                hist = cv2.calcHist([img_atual], [i], None, [256], [0, 256])
                plt.plot(hist, color=color)

            plt.xlim([0, 256])
            plt.show()
            print("📊 Histograma exibido")
        elif key == ord('d'):
            if len(img_atual.shape) == 3:
                gray = cv2.cvtColor(img_atual, cv2.COLOR_BGR2GRAY)
            else:
                gray = img_atual.copy()

            _, binaria = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            calcular_area_perimetro_diametro(binaria)

    cv2.destroyAllWindows()
    print("✅ Fechado")

if __name__ == "__main__":
    interacao_tempo_real()