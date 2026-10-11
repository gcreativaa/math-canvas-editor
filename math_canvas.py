import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import os

class MathCanvasEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("G-Creativa Math & Equation Canvas")
        self.root.geometry("900x600")
        self.root.configure(bg="#2c3e50")

        # Variables de dibujo
        self.color_pincel = "black"
        self.grosor_pincel = 3
        self.x_previo = None
        self.y_previo = None
        
        # Imagen en memoria (Pillow) para exportar con alta fidelidad
        self.imagen_memoria = Image.new("RGB", (900, 500), "white")
        self.draw_memoria = ImageDraw.Draw(self.imagen_memoria)

        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Panel Superior de Herramientas
        panel_herramientas = tk.Frame(self.root, bg="#34495e", pady=10)
        panel_herramientas.pack(fill=tk.X)

        # Botones de dibujo
        btn_lapiz = tk.Button(panel_herramientas, text="✏️ Lápiz", command=self.usar_lapiz, font=("Arial", 10, "bold"))
        btn_lapiz.pack(side=tk.LEFT, padx=5)

        btn_goma = tk.Button(panel_herramientas, text="🧽 Goma", command=self.usar_goma, font=("Arial", 10, "bold"))
        btn_goma.pack(side=tk.LEFT, padx=5)

        btn_limpiar = tk.Button(panel_herramientas, text="🗑️ Limpiar Todo", command=self.limpiar_lienzo, font=("Arial", 10, "bold"))
        btn_limpiar.pack(side=tk.LEFT, padx=5)

        # Botones de Exportación
        btn_latex = tk.Button(panel_herramientas, text="∑ Exportar a LaTeX", command=self.exportar_latex, bg="#8e44ad", fg="white", font=("Arial", 10, "bold"))
        btn_latex.pack(side=tk.RIGHT, padx=10)

        btn_vector = tk.Button(panel_herramientas, text="📐 Guardar Vector (EPS/SVG)", command=self.exportar_vector, bg="#d35400", fg="white", font=("Arial", 10, "bold"))
        btn_vector.pack(side=tk.RIGHT, padx=5)

        btn_png = tk.Button(panel_herramientas, text="💾 Guardar PNG/JPG", command=self.exportar_imagen, bg="#27ae60", fg="white", font=("Arial", 10, "bold"))
        btn_png.pack(side=tk.RIGHT, padx=5)

        # Lienzo Digital (Canvas)
        self.canvas = tk.Canvas(self.root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Eventos del ratón para dibujar
        self.canvas.bind("<Button-1>", self.iniciar_trazo)
        self.canvas.bind("<B1-Motion>", self.dibujar_trazo)
        self.canvas.bind("<ButtonRelease-1>", self.terminar_trazo)

    # --- LÓGICA DE DIBUJO ---
    def usar_lapiz(self):
        self.color_pincel = "black"
        self.grosor_pincel = 3

    def usar_goma(self):
        self.color_pincel = "white"
        self.grosor_pincel = 20 # La goma es más gruesa

    def iniciar_trazo(self, event):
        self.x_previo = event.x
        self.y_previo = event.y

    def dibujar_trazo(self, event):
        if self.x_previo and self.y_previo:
            # Dibuja en la interfaz de usuario
            self.canvas.create_line(self.x_previo, self.y_previo, event.x, event.y, 
                                    width=self.grosor_pincel, fill=self.color_pincel, 
                                    capstyle=tk.ROUND, smooth=True)
            # Dibuja simultáneamente en la memoria RAM para exportar después
            self.draw_memoria.line([self.x_previo, self.y_previo, event.x, event.y], 
                                   fill=self.color_pincel, width=self.grosor_pincel)
            
            self.x_previo = event.x
            self.y_previo = event.y

    def terminar_trazo(self, event):
        self.x_previo = None
        self.y_previo = None

    def limpiar_lienzo(self):
        self.canvas.delete("all")
        self.draw_memoria.rectangle([0, 0, 900, 500], fill="white")

    # --- LÓGICA DE EXPORTACIÓN ---
    def exportar_imagen(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png", 
            filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")]
        )
        if ruta:
            self.imagen_memoria.save(ruta)
            messagebox.showinfo("Éxito", f"Ecuación guardada como imagen en:\n{ruta}")

    def exportar_vector(self):
        """
        Exporta el lienzo como un archivo vectorial PostScript (EPS).
        Este formato conserva las líneas como matemáticas puras (sin píxeles),
        ideal para papers científicos y fácilmente convertible a SVG.
        """
        ruta = filedialog.asksaveasfilename(
            defaultextension=".eps", 
            filetypes=[("Vector EPS", "*.eps")]
        )
        if ruta:
            self.canvas.postscript(file=ruta, colormode='color')
            messagebox.showinfo("Éxito", f"Vector matemático guardado en:\n{ruta}")

    def exportar_latex(self):
        """
        Módulo preparado para integración con IA.
        """
        mensaje = (
            "Para convertir escritura a mano en código LaTeX puramente tipográfico, "
            "se requiere conectar este software a una API de Inteligencia Artificial (como Mathpix o OpenAI Vision).\n\n"
            "Tu dibujo matemático actual puede guardarse como vector (.eps) para insertarlo directamente "
            "en tu documento LaTeX usando \\includegraphics{}."
        )
        messagebox.showinfo("Módulo de IA Requerido", mensaje)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = MathCanvasEditor(ventana)
    ventana.mainloop()