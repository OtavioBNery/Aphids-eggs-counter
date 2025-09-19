import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from ultralytics import YOLO

class ContadorOvosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Ovos 🥚")
        self.imagens = []
        self.canvas_imagens = []
        self.labels_info = [] 
        self.model = YOLO(r"best.pt")
        self.criar_widgets()

    def criar_widgets(self):
        # Frame de botões
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Selecionar Imagens", command=self.selecionar_imagens).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Contar Ovos", command=self.contar_todas).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Remover Selecionada", command=self.remover_imagem).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Limpar Tudo", command=self.limpar).pack(side=tk.LEFT, padx=5)

        # Lista de imagens selecionadas
        self.lista = tk.Listbox(self.root, width=80)
        self.lista.pack(pady=10)

        # Área rolável para miniaturas
        frame_scroll = tk.Frame(self.root)
        frame_scroll.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(frame_scroll, height=400)
        self.scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def selecionar_imagens(self):
        caminhos = filedialog.askopenfilenames(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
        if not caminhos:
            return

        self.imagens = list(caminhos)
        self.lista.delete(0, tk.END)

        # Limpa thumbnails anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.canvas_imagens.clear()
        self.labels_info.clear()

        for i, caminho in enumerate(self.imagens):
            nome_arquivo = os.path.basename(caminho)
            self.lista.insert(tk.END, f"{nome_arquivo} - aguardando contagem")

            # Mostrar miniatura
            imagem = Image.open(caminho)
            imagem.thumbnail((200, 200))
            imagem_tk = ImageTk.PhotoImage(imagem)

            frame_img = tk.Frame(self.scrollable_frame)
            frame_img.grid(row=i // 2, column=i % 2, padx=10, pady=10)  # Mosaico 2 colunas

            lbl_img = tk.Label(frame_img, image=imagem_tk)
            lbl_img.image = imagem_tk
            lbl_img.pack()

            lbl_txt = tk.Label(frame_img, text=f"{nome_arquivo}\nAguardando...")
            lbl_txt.pack()

            self.canvas_imagens.append(imagem_tk)
            self.labels_info.append(lbl_txt)

    def contar_todas(self):
        """Atualiza a contagem de todas as imagens carregadas"""
        self.lista.delete(0, tk.END)
        for i, caminho in enumerate(self.imagens):
            NOvos = self.contar_ovos(caminho)
            nome_arquivo = os.path.basename(caminho)

            # Atualiza lista
            self.lista.insert(tk.END, f"{nome_arquivo} - {NOvos} ovos contabilizados")

            # Atualiza label no mosaico
            self.labels_info[i].config(text=f"{nome_arquivo}\n{NOvos} ovos")

    def remover_imagem(self):
        """Remove a imagem selecionada na lista e no mosaico"""
        selecao = self.lista.curselection()
        if not selecao:
            return

        idx = selecao[0]

        # Remove dos arrays
        del self.imagens[idx]
        del self.canvas_imagens[idx]
        lbl = self.labels_info.pop(idx)

        # Remove o frame pai do label (contém a imagem + texto)
        lbl.master.destroy()

        # Atualiza a lista
        self.lista.delete(idx)

    def contar_ovos(self, caminho):
        results = self.model(caminho, imgsz=640, conf=0.25)
        total_ovos = 0
        for r in results:
            total_ovos += len(r.boxes)
        return total_ovos

    def limpar(self):
        self.imagens = []
        self.lista.delete(0, tk.END)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.canvas_imagens.clear()
        self.labels_info.clear()


if __name__ == "__main__":
    root = tk.Tk()
    app = ContadorOvosApp(root)
    root.mainloop()
