import tkinter as tk
from tkinter import ttk, messagebox
import random

class JuegoVidaConway:
    def __init__(self, padre, volver_callback):
        self.padre = padre
        self.volver_callback = volver_callback
        self.tamano = 20  # Tamaño inicial del tablero (20x20)
        self.tamano_celda = 25  # Tamaño de cada celda en píxeles
        self.tablero = []
        self.contador_tiempo = 0  # Contador de generaciones
        self._ui()  # Inicializar la interfaz

    def _ui(self):
        # Contenedor principal
        contenedor = ttk.Frame(self.padre)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        # Título del juego
        titulo = ttk.Label(contenedor, text="Juego de la Vida de Conway", font=("Arial", 22, "bold"))
        titulo.pack(pady=10)

        # Dividir interfaz en dos columnas: tablero y controles
        marco_principal = ttk.Frame(contenedor)
        marco_principal.pack(fill="both", expand=True)

        # Frame izquierdo: lienzo del tablero con scroll
        marco_lienzo = ttk.Frame(marco_principal)
        marco_lienzo.pack(side="left", fill="both", expand=True)

        # Scrollbars para el lienzo
        self.scroll_x = ttk.Scrollbar(marco_lienzo, orient="horizontal")
        self.scroll_y = ttk.Scrollbar(marco_lienzo, orient="vertical")

        # Canvas donde se dibuja el tablero
        self.lienzo = tk.Canvas(marco_lienzo, bg="#f8fafc", 
                                xscrollcommand=self.scroll_x.set,
                                yscrollcommand=self.scroll_y.set)
        self.lienzo.grid(row=0, column=0, sticky="nsew")
        self.scroll_x.grid(row=1, column=0, sticky="ew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        self.scroll_x.config(command=self.lienzo.xview)
        self.scroll_y.config(command=self.lienzo.yview)

        marco_lienzo.rowconfigure(0, weight=1)
        marco_lienzo.columnconfigure(0, weight=1)

        # Frame derecho: controles y contador
        marco_controles = ttk.Frame(marco_principal)
        marco_controles.pack(side="left", fill="y", padx=10)

        # Contador de tiempo (generaciones)
        self.contador_label = ttk.Label(marco_controles, text="Tiempo: 0", font=("Arial", 18, "bold"), foreground="#2563eb")
        self.contador_label.pack(pady=8)

        # Controles del juego
        ttk.Label(marco_controles, text="Tamaño del tablero:").pack(pady=(0, 5))
        self.tamano_var = tk.IntVar(value=self.tamano)
        entrada_tamano = ttk.Entry(marco_controles, textvariable=self.tamano_var, width=5)
        entrada_tamano.pack(pady=(0, 10))

        btn_tablero = ttk.Button(marco_controles, text="Crear tablero", command=self.crear_tablero)
        btn_tablero.pack(fill="x", pady=2)

        self.btn_siguiente = ttk.Button(marco_controles, text="Siguiente paso (Espacio)", command=self.siguiente_tiempo)
        self.btn_siguiente.pack(fill="x", pady=2)

        btn_volver = ttk.Button(marco_controles, text="← Volver", command=self.volver_callback)
        btn_volver.pack(fill="x", pady=(20, 2))

        # Eventos
        self.lienzo.bind("<Button-1>", self.cambiar_celda)
        self.padre.bind("<space>", lambda e: self.siguiente_tiempo())

        # Crear primer tablero
        self.crear_tablero()

    def crear_tablero(self):
        # Obtener el nuevo tamaño del tablero desde el input
        self.tamano = self.tamano_var.get()
        # Generar tablero con valores aleatorios (0 o 1)
        self.tablero = [[random.choice([0, 1]) for _ in range(self.tamano)] for _ in range(self.tamano)]
        self.contador_tiempo = 0
        self.dibujar_tablero()
        self.contador_label.config(text=f"Tiempo: {self.contador_tiempo}")

        # Ajustar tamaño visible del lienzo
        ancho_total = self.tamano * self.tamano_celda
        alto_total = self.tamano * self.tamano_celda
        self.lienzo.config(scrollregion=(0, 0, ancho_total, alto_total))

    def dibujar_tablero(self):
        # Elimina las celdas anteriores
        self.lienzo.delete("all")

        # Dibuja cada celda
        for i in range(self.tamano):
            for j in range(self.tamano):
                x0 = j * self.tamano_celda
                y0 = i * self.tamano_celda
                x1 = x0 + self.tamano_celda
                y1 = y0 + self.tamano_celda

                # Colores modernos: celda viva y muerta
                color = "#3b82f6" if self.tablero[i][j] else "#f1f5f9"
                borde = "#94a3b8"
                self.lienzo.create_rectangle(x0, y0, x1, y1, fill=color, outline=borde)

    def cambiar_celda(self, evento):
        # Convertir coordenadas del clic a índice de celda
        x_canvas = self.lienzo.canvasx(evento.x)
        y_canvas = self.lienzo.canvasy(evento.y)
        j = int(x_canvas // self.tamano_celda)
        i = int(y_canvas // self.tamano_celda)

        # Verificar si el clic está dentro de los límites del tablero
        if 0 <= i < self.tamano and 0 <= j < self.tamano:
            # Invertir el estado de la celda (viva/muerta)
            self.tablero[i][j] = 1 - self.tablero[i][j]
            self.dibujar_tablero()

    def siguiente_tiempo(self):
        # Crear una nueva matriz para la siguiente generación
        nuevo_tablero = [[0]*self.tamano for _ in range(self.tamano)]

        for i in range(self.tamano):
            for j in range(self.tamano):
                # Contar vecinos vivos alrededor de la celda (i, j)
                vecinos = sum(
                    self.tablero[x][y]
                    for x in range(max(0, i-1), min(self.tamano, i+2))
                    for y in range(max(0, j-1), min(self.tamano, j+2))
                    if (x, y) != (i, j)
                )
                # Reglas del juego de la vida
                if self.tablero[i][j] == 1:
                    nuevo_tablero[i][j] = 1 if vecinos in [2, 3] else 0
                else:
                    nuevo_tablero[i][j] = 1 if vecinos == 3 else 0

        # Actualizar el tablero y el contador
        self.tablero = nuevo_tablero
        self.contador_tiempo += 1
        self.dibujar_tablero()
        self.contador_label.config(text=f"Tiempo: {self.contador_tiempo}")
