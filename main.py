import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

# Variável global para armazenar a imagem carregada (no formato OpenCV - BGR)
loaded_image = None

def display_image(image):
    """
    Converte a imagem do OpenCV (BGR) para RGB, converte para PIL Image e exibe na interface.
    """
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb)
    photo = ImageTk.PhotoImage(pil_image)
    label_imagem.config(image=photo)
    label_imagem.image = photo  # Mantém referência para não limpar a imagem da memória

def escolher_imagem():
    global loaded_image
    file_path = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Arquivos de imagem", "*.jpg *.jpeg *.png *.gif")]
    )
    if file_path:
        try:
            # Lê a imagem com cv2 (formato BGR) e redimensiona para melhor visualização
            loaded_image = cv2.imread(file_path)
            if loaded_image is None:
                raise Exception("Erro ao ler a imagem.")
            loaded_image = cv2.resize(loaded_image, (300, 300))
            display_image(loaded_image)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir imagem:\n{e}")

def aplicar_blur():
    global loaded_image
    if loaded_image is not None:
        # Aplica o filtro Blur com cv2 (utilizando GaussianBlur)
        blurred = cv2.GaussianBlur(loaded_image, (7, 7), 0)
        loaded_image = blurred  # Atualiza a imagem carregada
        display_image(blurred)
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione uma imagem primeiro.")

def aplicar_sharpen():
    global loaded_image
    if loaded_image is not None:
        # Define um kernel para aumentar a nitidez (sharpen)
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(loaded_image, -1, kernel)
        loaded_image = sharpened
        display_image(sharpened)
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione uma imagem primeiro.")

def rotacionar_imagem():
    global loaded_image
    if loaded_image is not None:
        # Obtém as dimensões da imagem
        (h, w) = loaded_image.shape[:2]
        center = (w // 2, h // 2)
        # Calcula a matriz de rotação para 45 graus
        M = cv2.getRotationMatrix2D(center, 45, 1.0)
        # Calcula as novas dimensões para que a imagem não seja cortada (expand=True)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        # Ajusta a matriz de rotação para centralizar a imagem
        M[0, 2] += (nW / 2) - center[0]
        M[1, 2] += (nH / 2) - center[1]
        rotated = cv2.warpAffine(loaded_image, M, (nW, nH))
        loaded_image = rotated
        display_image(rotated)
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione uma imagem primeiro.")

# Cria a janela principal
root = tk.Tk()
root.title("Interface com Imagem e Filtros (cv2)")
root.geometry("500x600")

# Botão para selecionar a imagem
btn_escolher = tk.Button(root, text="Escolher Imagem", command=escolher_imagem)
btn_escolher.pack(pady=10)

# Label para exibir a imagem selecionada
label_imagem = tk.Label(root)
label_imagem.pack(pady=10)

# Botões para aplicar os filtros
btn_blur = tk.Button(root, text="Aplicar Blur", command=aplicar_blur)
btn_blur.pack(pady=10)

btn_sharpen = tk.Button(root, text="Aplicar Sharpening", command=aplicar_sharpen)
btn_sharpen.pack(pady=10)

btn_rotate = tk.Button(root, text="Rotacionar 45°", command=rotacionar_imagem)
btn_rotate.pack(pady=10)

# Inicia o loop principal da interface
root.mainloop()
