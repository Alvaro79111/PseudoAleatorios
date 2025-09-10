import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from scipy.stats import norm, chi2

# ------------------------------
# Algoritmos de generación
# ------------------------------ 
def cuadrados_medios(seed, n):
    # Algoritmo de cuadrados medios: genera n números pseudoaleatorios a partir de una semilla
    resultados = []
    x = seed
    for _ in range(n):
        cuadrado = str(x**2).zfill(8)  # asegurar longitud de 8 dígitos
        medio = int(cuadrado[2:6])     # extraer los 4 dígitos centrales
        r = medio / 10000              # normalizar a [0,1)
        resultados.append((x, cuadrado, medio, r))
        x = medio
    return resultados


def productos_medios(seed, n):
    # Algoritmo de productos medios: usa dos semillas para generar n números
    resultados = []
    x = seed
    y = seed + 1234  # otra semilla para producto
    for _ in range(n):
        producto = str(x * y).zfill(8)
        medio = int(producto[2:6])
        r = medio / 10000
        resultados.append((x, y, producto, medio, r))
        x, y = y, medio
    return resultados


def multiplicador_constante(seed, n, a=73):
    # Algoritmo de multiplicador constante: Xi+1 = a * Xi, se extraen los 4 dígitos centrales
    resultados = []
    x = seed
    for _ in range(n):
        producto = x * a
        s = str(producto).zfill(8)
        medio = int(s[2:6])
        r = medio / 10000
        resultados.append((x, producto, medio, r))
        x = medio
    return resultados

# ------------------------------
# Pruebas estadísticas
# ------------------------------
def prueba_medias(valores, alpha):
    # Prueba de medias: verifica si la media de los Ri está dentro del intervalo esperado
    n = len(valores)
    media = sum(valores)/n
    z0 = (media - 0.5) / (math.sqrt(1/(12*n)))  # estadístico Z
    z_alpha = norm.ppf(1 - alpha/2)             # valor crítico para el nivel de significancia
    return media, z0, z_alpha, abs(z0) < z_alpha


def prueba_varianza(valores, alpha):
    # Prueba de varianza: compara la varianza muestral con los límites teóricos
    n = len(valores)
    media = sum(valores)/n
    var = sum((x - media)**2 for x in valores)/(n-1)
    chi_inf = chi2.ppf(alpha/2, n-1)            # límite inferior chi-cuadrado
    chi_sup = chi2.ppf(1 - alpha/2, n-1)        # límite superior chi-cuadrado
    stat = (n-1)*var                            # estadístico de prueba
    return var, stat, chi_inf, chi_sup, chi_inf <= stat <= chi_sup


def prueba_uniformidad(valores, alpha, k=10):
    # Prueba de uniformidad (chi-cuadrado): compara frecuencias observadas vs esperadas
    n = len(valores)
    frec_obs = [0]*k
    for v in valores:
        idx = min(int(v*k), k-1)
        frec_obs[idx] += 1
    esperada = n/k
    chi_calc = sum((fo-esperada)**2/esperada for fo in frec_obs)
    chi_tabla = chi2.ppf(1-alpha, k-1)
    return frec_obs, chi_calc, chi_tabla, chi_calc < chi_tabla

# ------------------------------
# Interfaz gráfica
# ------------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Pseudoaleatorios")
        self.root.state('zoomed')
        # --- Configuración de estilos visuales ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.TFrame", background="#eaf0f6")
        style.configure("Custom.TLabel", background="#eaf0f6", foreground="#2e3f4f", font=("Arial", 18, "bold"))
        style.configure("Custom.TLabelframe", background="#f6fafd", font=("Arial", 14, "bold"), foreground="#2e3f4f")
        style.configure("Custom.TLabelframe.Label", font=("Arial", 14, "bold"), foreground="#2e3f4f", background="#dbeafe")
        style.configure("Custom.TButton", font=("Arial", 13, "bold"), background="#3b82f6", foreground="#fff")
        style.map("Custom.TButton", background=[('active', '#2563eb')])
        style.configure("Treeview", font=("Arial", 11), rowheight=28, background="#f8fafc", fieldbackground="#f8fafc")
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#dbeafe", foreground="#222222")
        style.map("Treeview.Heading", background=[('active', '#bae6fd')])
        self.root.configure(bg="#eaf0f6")
        # --- Canvas con scrollbar para todo el contenido ---
        self.main_canvas = tk.Canvas(root, borderwidth=0, background="#eaf0f6", highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(root, orient="vertical", command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=self.v_scroll.set)
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.v_scroll.pack(side="right", fill="y")
        self.frame = ttk.Frame(self.main_canvas, style="Custom.TFrame")
        self.frame_id = self.main_canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.main_canvas.bind('<Configure>', self.on_canvas_configure)
        # --- Frame superior fijo para inputs ---
        self.inputs_frame = ttk.LabelFrame(self.frame, text="Datos iniciales", style="Custom.TLabelframe")
        self.inputs_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=18, pady=(18, 8))
        self.inputs_frame.grid_columnconfigure(0, weight=1)
        self.inputs_frame.grid_columnconfigure(1, weight=1)
        # --- Frame principal para tabla y pruebas ---
        self.main_content_frame = ttk.Frame(self.frame, style="Custom.TFrame")
        self.main_content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=2)
        self.main_content_frame.grid_columnconfigure(1, weight=1)
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.algoritmo = tk.StringVar()
        self.setup_algoritmo()

    def on_frame_configure(self, event):
        # Ajusta el scroll del canvas al tamaño del frame interior
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Ajusta el ancho del frame al del canvas
        canvas_width = event.width
        self.main_canvas.itemconfig(self.frame_id, width=canvas_width)

    def limpiar_inputs(self):
        # Elimina widgets del frame de inputs
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()

    def limpiar_main_content(self):
        # Elimina widgets del frame principal (tabla y pruebas)
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

    def add_scrollable_tree(self, parent, columns, height=8):
        # Crea una tabla Treeview con scrollbars vertical y horizontal
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True)
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#e0e0e0", foreground="#222222")
        style.map("Treeview.Heading", background=[('active', '#d0d0d0')])
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=height, style="Treeview")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        return tree

    def setup_algoritmo(self):
        # Pantalla inicial: selección de algoritmo
        self.limpiar_inputs()
        self.limpiar_main_content()
        ttk.Label(self.inputs_frame, text="Seleccione un algoritmo:", style="Custom.TLabel").grid(row=0, column=0, sticky="e", padx=8, pady=8)
        opciones = ["Cuadrados Medios", "Productos Medios", "Multiplicador Constante"]
        self.combo = ttk.Combobox(self.inputs_frame, textvariable=self.algoritmo, values=opciones, state="readonly", font=("Arial", 13))
        self.combo.grid(row=0, column=1, sticky="w", padx=8, pady=8)
        btn = ttk.Button(self.inputs_frame, text="Siguiente", style="Custom.TButton", command=self.setup_parametros)
        btn.grid(row=0, column=2, sticky="w", padx=8, pady=8)

    def setup_parametros(self):
        # Muestra los campos de entrada según el algoritmo seleccionado
        if not self.algoritmo.get():
            messagebox.showerror("Error", "Debe seleccionar un algoritmo")
            return
        self.limpiar_inputs()
        self.limpiar_main_content()
        ttk.Label(self.inputs_frame, text=f"{self.algoritmo.get()}", style="Custom.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", padx=8, pady=(8, 2))
        ttk.Label(self.inputs_frame, text="Número de pseudoaleatorios:", font=("Arial", 13)).grid(row=1, column=0, sticky="e", padx=8, pady=6)
        self.n_entry = ttk.Entry(self.inputs_frame, font=("Arial", 13), width=12)
        self.n_entry.grid(row=1, column=1, sticky="w", padx=8, pady=6)
        self.n_entry.focus()
        row = 2
        if self.algoritmo.get() == "Cuadrados Medios":
            ttk.Label(self.inputs_frame, text="Semilla (mínimo 4 dígitos):", font=("Arial", 13)).grid(row=row, column=0, sticky="e", padx=8, pady=6)
            self.seed_entry = ttk.Entry(self.inputs_frame, font=("Arial", 13), width=12)
            self.seed_entry.grid(row=row, column=1, sticky="w", padx=8, pady=6)
            row += 1
        elif self.algoritmo.get() == "Productos Medios":
            ttk.Label(self.inputs_frame, text="Semilla X (mínimo 4 dígitos):", font=("Arial", 13)).grid(row=row, column=0, sticky="e", padx=8, pady=6)
            self.seedx_entry = ttk.Entry(self.inputs_frame, font=("Arial", 13), width=12)
            self.seedx_entry.grid(row=row, column=1, sticky="w", padx=8, pady=6)
            row += 1
            ttk.Label(self.inputs_frame, text="Semilla Y (mínimo 4 dígitos):", font=("Arial", 13)).grid(row=row, column=0, sticky="e", padx=8, pady=6)
            self.seedy_entry = ttk.Entry(self.inputs_frame, font=("Arial", 13), width=12)
            self.seedy_entry.grid(row=row, column=1, sticky="w", padx=8, pady=6)
            row += 1
        elif self.algoritmo.get() == "Multiplicador Constante":
            ttk.Label(self.inputs_frame, text="Semilla (mínimo 4 dígitos):", font=("Arial", 13)).grid(row=row, column=0, sticky="e", padx=8, pady=6)
            self.seed_entry = ttk.Entry(self.inputs_frame, font=("Arial", 13), width=12)
            self.seed_entry.grid(row=row, column=1, sticky="w", padx=8, pady=6)
            row += 1
            ttk.Label(self.inputs_frame, text="Constante a (entero > 0):", font=("Arial", 13)).grid(row=row, column=0, sticky="e", padx=8, pady=6)
            self.const_entry = ttk.Entry(self.inputs_frame, font=("Arial", 13), width=12)
            self.const_entry.insert(0, "73")
            self.const_entry.grid(row=row, column=1, sticky="w", padx=8, pady=6)
            row += 1
        ttk.Button(self.inputs_frame, text="Calcular", style="Custom.TButton", command=self.calcular).grid(row=row, column=0, columnspan=2, pady=12)
        ttk.Button(self.inputs_frame, text="Volver", style="Custom.TButton", command=self.setup_algoritmo).grid(row=row, column=2, pady=12)

    def calcular(self):
        # Valida entradas y ejecuta el algoritmo seleccionado
        try:
            n = int(self.n_entry.get())
            if n <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "El número de pseudoaleatorios debe ser un entero positivo")
            return
        if self.algoritmo.get() == "Cuadrados Medios":
            try:
                seed = int(self.seed_entry.get())
            except:
                messagebox.showerror("Error", "La semilla debe ser un número entero")
                return
            if len(str(seed)) < 4:
                messagebox.showerror("Error", "La semilla debe tener al menos 4 dígitos")
                return
            self.resultados = self.cuadrados_medios(seed, n)
            self.valores = [r[3] for r in self.resultados]
            self.colnames = ["Xi", "Xi^2", "Medio", "Ri"]
            self.titulo_resultados = "Resultados - Cuadrados Medios"
        elif self.algoritmo.get() == "Productos Medios":
            try:
                seedx = int(self.seedx_entry.get())
                seedy = int(self.seedy_entry.get())
            except:
                messagebox.showerror("Error", "Las semillas deben ser números enteros")
                return
            if len(str(seedx)) < 4 or len(str(seedy)) < 4:
                messagebox.showerror("Error", "Ambas semillas deben tener al menos 4 dígitos")
                return
            self.resultados = self.productos_medios(seedx, seedy, n)
            self.valores = [r[4] for r in self.resultados]
            self.colnames = ["Xi", "Yi", "Xi*Yi", "Medio", "Ri"]
            self.titulo_resultados = "Resultados - Productos Medios"
        else:  # Multiplicador Constante
            try:
                seed = int(self.seed_entry.get())
                a = int(self.const_entry.get())
                if a <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Error", "La semilla y la constante deben ser números enteros válidos")
                return
            if len(str(seed)) < 4:
                messagebox.showerror("Error", "La semilla debe tener al menos 4 dígitos")
                return
            self.resultados = self.multiplicador_constante(seed, n, a)
            self.valores = [r[3] for r in self.resultados]
            self.colnames = ["Xi", "a*Xi", "Medio", "Ri"]
            self.titulo_resultados = "Resultados - Multiplicador Constante"
        self.mostrar_tabla()

    def mostrar_tabla(self):
        # Muestra la tabla de resultados y el panel de pruebas
        self.limpiar_main_content()
        # Tabla de pseudoaleatorios a la izquierda
        self.tabla_frame = ttk.LabelFrame(self.main_content_frame, text=self.titulo_resultados, style="Custom.TLabelframe")
        self.tabla_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=0)
        cols = self.colnames
        tree = self.add_scrollable_tree(self.tabla_frame, cols, height=16)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        for row in self.resultados:
            tree.insert("", "end", values=row)
        # Frame derecho para datos de pruebas y resultados
        self.right_frame = ttk.Frame(self.main_content_frame, style="Custom.TFrame")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.setup_pruebas(right=True)

    def setup_pruebas(self, right=False):
        # Panel para ingresar parámetros de pruebas estadísticas
        if hasattr(self, 'pruebas_frame'):
            self.pruebas_frame.destroy()
        parent = self.right_frame if right else self.frame
        self.pruebas_frame = ttk.LabelFrame(parent, text="Pruebas estadísticas", style="Custom.TLabelframe")
        self.pruebas_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(self.pruebas_frame, text="Nivel de significancia (α):", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.alpha_entry = ttk.Entry(self.pruebas_frame, font=("Arial", 12))
        self.alpha_entry.insert(0, "0.05")
        self.alpha_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.pruebas_frame, text="Intervalos para uniformidad (k):", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.k_entry = ttk.Entry(self.pruebas_frame, font=("Arial", 12))
        self.k_entry.insert(0, "10")
        self.k_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.pruebas_frame, text="Ejecutar pruebas", style="Custom.TButton", command=self.ejecutar_pruebas).grid(row=2, column=0, columnspan=2, pady=12)

    def ejecutar_pruebas(self):
        # Ejecuta las pruebas estadísticas y muestra los resultados
        try:
            alpha = float(self.alpha_entry.get())
            if not (0 < alpha < 1):
                raise ValueError
        except:
            messagebox.showerror("Error", "Alpha inválido")
            return
        try:
            k = int(self.k_entry.get())
            if k < 2:
                raise ValueError
        except:
            messagebox.showerror("Error", "k inválido")
            return
        # --- Cálculos de pruebas estadísticas ---
        media, z0, z_alpha, res_media = prueba_medias(self.valores, alpha)
        var, stat, chi_inf, chi_sup, res_var = prueba_varianza(self.valores, alpha)
        frec, chi_calc, chi_tabla, res_uni, tabla_uni = self.prueba_uniformidad_detallada(self.valores, alpha, k)
        self.mostrar_resultados_pruebas(media, z0, z_alpha, res_media, var, stat, chi_inf, chi_sup, res_var, frec, chi_calc, chi_tabla, res_uni, tabla_uni)

    def mostrar_resultados_pruebas(self, media, z0, z_alpha, res_media, var, stat, chi_inf, chi_sup, res_var, frec, chi_calc, chi_tabla, res_uni, tabla_uni):
        # Mostrar resultados en el frame derecho
        for widget in self.right_frame.winfo_children():
            if widget != self.pruebas_frame:
                widget.destroy()
        res_frame = ttk.LabelFrame(self.right_frame, text="Resultados de pruebas", style="Custom.TLabelframe")
        res_frame.pack(fill="both", expand=True, padx=5, pady=5)
        n = len(self.valores)
        # --- Cálculo de límites para media y varianza ---
        lim_inf_media = 0.5 - z_alpha * (1/(12*n))**0.5
        lim_sup_media = 0.5 + z_alpha * (1/(12*n))**0.5
        lim_inf_var = chi_inf / (12*(n-1))
        lim_sup_var = chi_sup / (12*(n-1))
        txt = f"""
Prueba de Medias:\n  Media = {media:.4f}\n  Z0 = {z0:.4f}\n  Zα = {z_alpha:.4f}\n  Límite inferior = {lim_inf_media:.4f}\n  Límite superior = {lim_sup_media:.4f}\n  Resultado: {'Aceptado' if res_media else 'Rechazado'}\n\nPrueba de Varianza:\n  Varianza = {var:.4f}\n  χ²calc = {stat:.4f}\n  χ²inf = {chi_inf:.4f}\n  χ²sup = {chi_sup:.4f}\n  Límite inferior = {lim_inf_var:.4f}\n  Límite superior = {lim_sup_var:.4f}\n  Resultado: {'Aceptado' if res_var else 'Rechazado'}\n\nPrueba de Uniformidad:\n  χ²calc = {chi_calc:.4f}\n  χ²tabla = {chi_tabla:.4f}\n  Resultado: {'Aceptado' if res_uni else 'Rechazado'}\n        """
        label = ttk.Label(res_frame, text=txt, justify="left", font=("Arial", 12))
        label.pack(anchor="w", padx=5, pady=5)
        # Tabla de uniformidad
        cols = ["Intervalo", "Frecuencia Observada", "Frecuencia Esperada", "(fo-fe)^2/fe"]
        tree = self.add_scrollable_tree(res_frame, cols, height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        for row in tabla_uni:
            tree.insert("", "end", values=row)

    # --- Algoritmos con formato de medio ---
    def cuadrados_medios(self, seed, n):
        # Implementación con padding y extracción de 4 dígitos centrales
        resultados = []
        x = seed
        for _ in range(n):
            cuadrado = str(x**2).zfill(8)
            medio = cuadrado[2:6]
            if len(medio) == 3:
                medio = '0' + medio
            medio_int = int(medio)
            r = medio_int / 10000
            resultados.append((x, cuadrado, medio, r))
            x = medio_int
        return resultados

    def productos_medios(self, seedx, seedy, n):
        # Implementación con dos semillas y extracción de 4 dígitos centrales
        resultados = []
        x = seedx
        y = seedy
        for _ in range(n):
            producto = str(x * y).zfill(8)
            medio = producto[2:6]
            if len(medio) == 3:
                medio = '0' + medio
            medio_int = int(medio)
            r = medio_int / 10000
            resultados.append((x, y, producto, medio, r))
            x, y = y, medio_int
        return resultados

    def multiplicador_constante(self, seed, n, a=73):
        # Implementación con multiplicador y extracción de 4 dígitos centrales
        resultados = []
        x = seed
        for _ in range(n):
            producto = x * a
            s = str(producto).zfill(8)
            medio = s[2:6]
            if len(medio) == 3:
                medio = '0' + medio
            medio_int = int(medio)
            r = medio_int / 10000
            resultados.append((x, producto, medio, r))
            x = medio_int
        return resultados

    def prueba_uniformidad_detallada(self, valores, alpha, k=10):
        # Prueba de uniformidad con desglose de tabla para cada intervalo
        n = len(valores)
        frec_obs = [0]*k
        for v in valores:
            idx = min(int(v*k), k-1)
            frec_obs[idx] += 1
        esperada = n/k
        chi_calc = 0
        tabla = []
        for i in range(k):
            fo = frec_obs[i]
            fe = esperada
            chi = (fo-fe)**2/fe
            chi_calc += chi
            intervalo = f"[{i/k:.2f}, {(i+1)/k:.2f})"
            tabla.append((intervalo, fo, f"{fe:.2f}", f"{chi:.4f}"))
        chi_tabla = chi2.ppf(1-alpha, k-1)
        return frec_obs, chi_calc, chi_tabla, chi_calc < chi_tabla, tabla

if __name__ == "__main__":
    # Punto de entrada principal
    root = tk.Tk()
    app = App(root)
    root.mainloop()
