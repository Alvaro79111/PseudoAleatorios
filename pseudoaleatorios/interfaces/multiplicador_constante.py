"""Interfaz para el generador de Multiplicador Constante."""
import tkinter as tk
from tkinter import ttk, messagebox
from ..generators import multiplicador_constante
from .. import tests
import pandas as pd
import datetime

class MultiplicadorConstanteApp:
    def __init__(self, parent, volver_callback):
        self.parent = parent
        self.volver_callback = volver_callback
        self.resultados = None
        # Frame con scroll y mousewheel
        self.canvas = tk.Canvas(parent, borderwidth=0, background="#eaf0f6")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.vsb.pack(side="right", fill="y")
        self.frame = ttk.Frame(self.canvas)
        self.frame.update_idletasks()
        self.canvas.create_window((0,0), window=self.frame, anchor="nw", width=self.canvas.winfo_width())
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # Scroll con rueda del ratón multiplataforma
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)  # Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)  # Linux
        self.frame.pack(fill="both", expand=True)
        self.setup_parametros()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def setup_parametros(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        ttk.Label(self.frame, text="Multiplicador Constante", font=("Arial", 18, "bold"), foreground="#f59e42").pack(pady=(18, 8))
        ttk.Label(self.frame, text="Número de pseudoaleatorios:", font=("Arial", 13)).pack(pady=6)
        self.n_entry = ttk.Entry(self.frame, font=("Arial", 13), width=12)
        self.n_entry.pack(pady=6)
        self.n_entry.focus()
        ttk.Label(self.frame, text="Semilla (mínimo 4 dígitos):", font=("Arial", 13)).pack(pady=6)
        self.seed_entry = ttk.Entry(self.frame, font=("Arial", 13), width=12)
        self.seed_entry.pack(pady=6)
        ttk.Label(self.frame, text="Constante a (entero > 0):", font=("Arial", 13)).pack(pady=6)
        self.const_entry = ttk.Entry(self.frame, font=("Arial", 13), width=12)
        self.const_entry.insert(0, "73")
        self.const_entry.pack(pady=6)
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=12)
        ttk.Button(btn_frame, text="Calcular", command=self.calcular, style="Custom.TButton").pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Volver", command=self.volver_callback, style="Custom.TButton").pack(side="left", padx=8)

    def calcular(self):
        try:
            n = int(self.n_entry.get())
            seed = int(self.seed_entry.get())
            a = int(self.const_entry.get())
            if n <= 0 or len(str(seed)) < 4 or a <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Entradas inválidas")
            return
        self.resultados = multiplicador_constante(seed, n, a)
        valores = [r[3] for r in self.resultados]
        self.mostrar_tabla(self.resultados, valores)

    def mostrar_tabla(self, resultados, valores):
        for widget in self.frame.winfo_children():
            widget.destroy()
        # --- Tabla de resultados ---
        tabla_frame = ttk.LabelFrame(self.frame, text="Resultados - Multiplicador Constante", style="Custom.TLabelframe")
        tabla_frame.pack(fill="x", padx=10, pady=10)
        cols = ["Xi", "a*Xi", "Medio", "Ri"]
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=16)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        for row in resultados:
            tree.insert("", "end", values=row)
        tree.pack(fill="x", expand=True)
        # --- Botones de acción ---
        def exportar_excel():
            import pandas as pd
            import datetime
            df = pd.DataFrame(resultados, columns=["Xi", "a*Xi", "Medio", "Ri"])
            nombre = f"multiplicador_constante_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(nombre, index=False)
            messagebox.showinfo("Exportación", f"Tabla exportada como {nombre}")
        btns = ttk.Frame(self.frame)
        btns.pack(pady=18)
        ttk.Button(btns, text="Pruebas estadísticas", command=lambda: self.mostrar_pruebas(valores), style="Custom.TButton").pack(side="left", padx=16)
        ttk.Button(btns, text="Distribuciones", command=lambda: self.abrir_distribuciones(valores), style="Custom.TButton").pack(side="left", padx=16)
        ttk.Button(btns, text="Exportar a Excel", command=exportar_excel, style="Custom.TButton").pack(side="left", padx=16)
        ttk.Button(self.frame, text="Volver al menú principal", command=self.volver_callback, style="Custom.TButton").pack(pady=8)

    def abrir_distribuciones(self, valores):
        from .distribuciones import DistribucionesApp
        for widget in self.parent.winfo_children():
            widget.destroy()
        DistribucionesApp(self.parent, valores, self.volver_callback)

    def mostrar_pruebas(self, valores):
        for widget in self.frame.winfo_children():
            widget.destroy()
        topbar = ttk.Frame(self.frame, style="Custom.TFrame")
        topbar.pack(fill="x")
        volver_btn = ttk.Button(topbar, text="← Volver a resultados de pseudoaleatorios", style="Custom.TButton", command=lambda: self.mostrar_tabla(self.resultados, valores))
        volver_btn.pack(side="left", padx=18, pady=8)
        ttk.Label(self.frame, text="Pruebas estadísticas", font=("Arial", 16, "bold"), foreground="#f59e42").pack(pady=(8, 8))
        ttk.Label(self.frame, text="Nivel de significancia (α):", font=("Arial", 12)).pack(pady=5)
        alpha_entry = ttk.Entry(self.frame, font=("Arial", 12))
        alpha_entry.insert(0, "0.05")
        alpha_entry.pack(pady=5)
        ttk.Label(self.frame, text="Intervalos para uniformidad (k):", font=("Arial", 12)).pack(pady=5)
        k_entry = ttk.Entry(self.frame, font=("Arial", 12))
        k_entry.insert(0, "10")
        k_entry.pack(pady=5)
        def ejecutar():
            try:
                alpha = float(alpha_entry.get())
                k = int(k_entry.get())
                if not (0 < alpha < 1) or k < 2:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Parámetros inválidos")
                return
            media, z0, z_alpha, res_media = tests.prueba_medias(valores, alpha)
            var, stat, chi_inf, chi_sup, res_var = tests.prueba_varianza(valores, alpha)
            frec, chi_calc, chi_tabla, res_uni, tabla_uni = tests.prueba_uniformidad_detallada(valores, alpha, k)
            self.mostrar_resultados_pruebas(media, z0, z_alpha, res_media, var, stat, chi_inf, chi_sup, res_var, frec, chi_calc, chi_tabla, res_uni, tabla_uni, lambda: self.mostrar_pruebas(valores), lambda: self.mostrar_tabla(self.resultados, valores))
        ttk.Button(self.frame, text="Calcular", command=ejecutar, style="Custom.TButton").pack(pady=12)
        ttk.Button(self.frame, text="Volver", command=self.volver_callback, style="Custom.TButton").pack(pady=4)

    def mostrar_resultados_pruebas(self, media, z0, z_alpha, res_media, var, stat, chi_inf, chi_sup, res_var, frec, chi_calc, chi_tabla, res_uni, tabla_uni, volver_calculo=None, volver_resultados=None):
        for widget in self.frame.winfo_children():
            widget.destroy()
        topbar = ttk.Frame(self.frame, style="Custom.TFrame")
        topbar.pack(fill="x")
        volver_menu_btn = ttk.Button(topbar, text="← Volver a resultados de pseudoaleatorios", style="Custom.TButton", command=lambda: self.mostrar_tabla(self.resultados, [r[3] for r in self.resultados]))
        volver_menu_btn.pack(side="left", padx=18, pady=8)
        if volver_calculo:
            volver_calc_btn = ttk.Button(topbar, text="↺ Volver al cálculo de pruebas", style="Custom.TButton", command=volver_calculo)
            volver_calc_btn.pack(side="left", padx=8, pady=8)
        ttk.Label(self.frame, text="Resultados de pruebas", font=("Arial", 16, "bold"), foreground="#f59e42").pack(pady=(8, 8))
        # Layout horizontal 3 columnas igual que productos_medios
        res_frame = ttk.LabelFrame(self.frame, text="Resultados de pruebas", style="Custom.TLabelframe")
        res_frame.pack(fill="both", expand=True, padx=5, pady=5)
        n = len(frec)
        lim_inf_media = 0.5 - z_alpha * (1/(12*n))**0.5
        lim_sup_media = 0.5 + z_alpha * (1/(12*n))**0.5
        lim_inf_var = chi_inf / (12*(n-1))
        lim_sup_var = chi_sup / (12*(n-1))
        main_content = ttk.Frame(res_frame)
        main_content.pack(fill="both", expand=True)
        main_content.columnconfigure(0, weight=1)
        main_content.columnconfigure(1, weight=1)
        main_content.columnconfigure(2, weight=1)
        # Columna 1: Medias
        txt_medias = f"""
Media = {media:.4f}
Z0 = {z0:.4f}
Zα = {z_alpha:.4f}
Límite inf = {lim_inf_media:.4f}
Límite sup = {lim_sup_media:.4f}
Resultado: {'Aceptado' if res_media else 'Rechazado'}
"""
        frame_medias = ttk.Frame(main_content)
        frame_medias.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(frame_medias, text="Prueba de Medias", font=("Arial", 13, "bold"), foreground="#f59e42").pack(pady=6)
        ttk.Label(frame_medias, text=txt_medias, justify="left", font=("Arial", 12)).pack(padx=4, pady=4)
        # Columna 2: Varianza
        txt_var = f"""
Varianza = {var:.4f}
χ²calc = {stat:.4f}
χ²inf = {chi_inf:.4f}
χ²sup = {chi_sup:.4f}
Límite inf = {lim_inf_var:.4f}
Límite sup = {lim_sup_var:.4f}
Resultado: {'Aceptado' if res_var else 'Rechazado'}
"""
        frame_var = ttk.Frame(main_content)
        frame_var.grid(row=0, column=1, sticky="nsew", padx=(0, 8))
        ttk.Label(frame_var, text="Prueba de Varianza", font=("Arial", 13, "bold"), foreground="#f59e42").pack(pady=6)
        ttk.Label(frame_var, text=txt_var, justify="left", font=("Arial", 12)).pack(padx=4, pady=4)
        # Columna 3: Uniformidad
        txt_uni = f"""
χ²calc = {chi_calc:.4f}
χ²tabla = {chi_tabla:.4f}
Resultado: {'Aceptado' if res_uni else 'Rechazado'}
"""
        frame_uni = ttk.Frame(main_content)
        frame_uni.grid(row=0, column=2, sticky="nsew", padx=(0, 8))
        ttk.Label(frame_uni, text="Prueba de Uniformidad", font=("Arial", 13, "bold"), foreground="#f59e42").pack(pady=6)
        ttk.Label(frame_uni, text=txt_uni, justify="left", font=("Arial", 12)).pack(padx=4, pady=4)
        # Tabla de uniformidad debajo de las columnas
        tabla_uni_frame = ttk.Frame(res_frame)
        tabla_uni_frame.pack(fill="x", padx=8, pady=8)
        tree = ttk.Treeview(tabla_uni_frame, columns=["Intervalo", "Frecuencia Observada", "Frecuencia Esperada", "(fo-fe)^2/fe"], show="headings", height=8)
        for col in ["Intervalo", "Frecuencia Observada", "Frecuencia Esperada", "(fo-fe)^2/fe"]:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        for row in tabla_uni:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True, pady=6)
        vsb_uni = ttk.Scrollbar(tabla_uni_frame, orient="vertical", command=tree.yview)
        vsb_uni.pack(side="right", fill="y")
        tree.configure(yscrollcommand=vsb_uni.set)
        ttk.Button(self.frame, text="Volver", command=self.volver_callback, style="Custom.TButton").pack(pady=8)
