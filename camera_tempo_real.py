import cv2

def camera_interativa():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Erro: não foi possível acessar a câmera.")
        return

    print("""
📷 Câmera interativa aberta!
Comandos em tempo real:
g - Cinza
n - Negativo
b - Binário Otsu
m - Suavização média
d - Suavização mediana
c - Canny
e - Erosão
l - Dilatação
o - Abertura
f - Fechamento
r - Reset
q - Fechar
""")

    efeito_atual = None  # variável para reset
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame.")
            break

        frame = cv2.flip(frame, 1)
        
        # Aplicar efeito se houver
        img = frame.copy()
        if efeito_atual == 'g':
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif efeito_atual == 'n':
            img = cv2.bitwise_not(frame)
        elif efeito_atual == 'b':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif efeito_atual == 'm':
            img = cv2.blur(frame, (5,5))
        elif efeito_atual == 'd':
            img = cv2.medianBlur(frame, 5)
        elif efeito_atual == 'c':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.Canny(gray, 100, 200)
        elif efeito_atual == 'e':  # erosão
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            img = cv2.erode(frame, kernel, iterations=1)
        elif efeito_atual == 'l':  # dilatação
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            img = cv2.dilate(frame, kernel, iterations=1)
        elif efeito_atual == 'o':  # abertura
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            img = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        elif efeito_atual == 'f':  # fechamento
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            img = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

        cv2.imshow("Câmera Interativa", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            efeito_atual = None
            print("🔄 Reset para original")
        elif key in [ord('g'), ord('n'), ord('b'), ord('m'), ord('d'), ord('c'),
                     ord('e'), ord('l'), ord('o'), ord('f')]:
            efeito_atual = chr(key)
            print(f"🎨 Efeito aplicado: {efeito_atual}")

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Câmera fechada")

if __name__ == "__main__":
    camera_interativa()
