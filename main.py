"""
RGM DOS ALUNOS:
8113385780
8129958741
8129949041
"""



import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

class AplicacaoFiltros:
    def __init__(self):
        # Cria a janela principal internamente
        self.root = tk.Tk()
        self.root.title("Interface de Imagem e Filtros (OpenCV)")
        self.root.geometry("500x600")

        self.base_image = None    # imagem original sem rotacao
        self.rotation_angle = 0   # angulo acumulado

        # Botão para escolher a imagem
        btn_escolher = tk.Button(
            self.root, text="Escolher Imagem", command=self.escolher_imagem
        )
        btn_escolher.pack(pady=10)

        # Label para exibir a imagem
        self.label_imagem = tk.Label(self.root)
        self.label_imagem.pack(pady=10)

        # Botão Blur
        btn_blur = tk.Button(
            self.root, text="Aplicar Blur", command=self.aplicar_blur
        )
        btn_blur.pack(pady=10)

        # Botão Sharpen
        btn_sharpen = tk.Button(
            self.root, text="Aplicar Sharpening", command=self.aplicar_sharpen
        )
        btn_sharpen.pack(pady=10)

        # Botão Rotacionar
        btn_rotate = tk.Button(
            self.root, text="Rotacionar 45°", command=self.rotacionar_imagem
        )
        btn_rotate.pack(pady=10)

        # Inicia o loop de eventos do Tkinter
        self.root.mainloop()

    def escolher_imagem(self):
        file_path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.jpg *.jpeg *.png *.gif")]
        )
        if file_path:
            try:
                img = cv2.imread(file_path)  # BGR
                if img is None:
                    raise ValueError("Não foi possível ler a imagem.")
                # Redimensiona para 300×300
                img = cv2.resize(img, (300, 300))
                self.base_image = img
                self.rotation_angle = 0
                self._atualizar_exibicao()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir imagem:\n{e}")

    def aplicar_blur(self):
        if self.base_image is None:
            messagebox.showwarning("Aviso", "Selecione uma imagem primeiro.")
            return
        self.base_image = cv2.GaussianBlur(self.base_image, (7, 7), 0)
        self._atualizar_exibicao()

    def aplicar_sharpen(self):
        if self.base_image is None:
            messagebox.showwarning("Aviso", "Selecione uma imagem primeiro.")
            return
        kernel = np.array([
            [ 0, -1,  0],
            [-1,  5, -1],
            [ 0, -1,  0]
        ], dtype=np.int32)
        self.base_image = cv2.filter2D(self.base_image, -1, kernel)
        self._atualizar_exibicao()

    def rotacionar_imagem(self):
        if self.base_image is None:
            messagebox.showwarning("Aviso", "Selecione uma imagem primeiro.")
            return
        self.rotation_angle = (self.rotation_angle + 45) % 360
        self._atualizar_exibicao()

    def _atualizar_exibicao(self):
        if self.base_image is None:
            return

        h, w = self.base_image.shape[:2]
        centro = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(centro, self.rotation_angle, 1.0)
        rotated = cv2.warpAffine(self.base_image, M, (w, h))

        # Converte para RGB e exibe
        rotated_rgb = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rotated_rgb)
        tk_img = ImageTk.PhotoImage(image=pil_img)

        self.label_imagem.config(image=tk_img)
        self.label_imagem.image = tk_img  # manter referência

# Instancia a aplicação
AplicacaoFiltros()
