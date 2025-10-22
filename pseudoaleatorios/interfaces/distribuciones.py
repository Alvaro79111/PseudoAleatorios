"""Interfaz para cálculo y visualización de distribuciones a partir de números pseudoaleatorios."""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import gamma, norm, binom, poisson
import pandas as pd
import datetime

class DistribucionesApp:
    def __init__(self, parent, valores, volver_callback):
        self.parent = parent
        self.valores = valores
        self.volver_callback = volver_callback
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
        self.setup_selector()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def setup_selector(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        # Botón volver arriba a la izquierda
        topbar = ttk.Frame(self.frame, style="Custom.TFrame")
        topbar.pack(fill="x")
        volver_btn = ttk.Button(topbar, text="← Volver a resultados de pseudoaleatorios", style="Custom.TButton", command=self.volver_callback)
        volver_btn.pack(side="left", padx=18, pady=8)
        ttk.Label(self.frame, text="Distribuciones", font=("Arial", 18, "bold"), foreground="#3b82f6").pack(pady=(8, 8))
        tipo_var = tk.StringVar(value="Variables")
        selector = ttk.Combobox(self.frame, values=["Variables", "Discretas"], textvariable=tipo_var, state="readonly", font=("Arial", 13))
        selector.pack(pady=8)
        dist_frame = ttk.Frame(self.frame)
        dist_frame.pack(pady=12)
        def update_buttons(*_):
            for widget in dist_frame.winfo_children():
                widget.destroy()
            if tipo_var.get() == "Variables":
                opciones = [
                    ("Uniforme", self.show_uniforme_var),
                    ("K-Erlang", self.show_kerlang),
                    ("Exponencial", self.show_exponencial),
                    ("Gamma", self.show_gamma),
                    ("Normal", self.show_normal),
                    ("Weibull", self.show_weibull)
                ]
            else:
                opciones = [
                    ("Uniforme", self.show_uniforme_disc),
                    ("Bernoulli", self.show_bernoulli),
                    ("Binomial", self.show_binomial),
                    ("Poisson", self.show_poisson)
                ]
            for i, (nombre, cmd) in enumerate(opciones):
                btn = tk.Button(dist_frame, text=nombre, font=("Arial", 13, "bold"), bg="#2563eb", fg="#fff", activebackground="#1e293b", activeforeground="#fff", relief="raised", bd=2, width=16, cursor="hand2", command=cmd)
                btn.grid(row=0, column=i, padx=10, pady=6)
        selector.bind("<<ComboboxSelected>>", update_buttons)
        update_buttons()
        ttk.Button(self.frame, text="Volver", command=self.volver_callback, style="Custom.TButton").pack(pady=12)

    def show_inputs(self, nombre, campos, calcular_fn):
        for widget in self.frame.winfo_children():
            widget.destroy()
        # Botón volver arriba a la izquierda
        topbar = ttk.Frame(self.frame, style="Custom.TFrame")
        topbar.pack(fill="x")
        volver_btn = ttk.Button(topbar, text="← Volver al menú de distribuciones", style="Custom.TButton", command=self.setup_selector)
        volver_btn.pack(side="left", padx=18, pady=8)
        ttk.Label(self.frame, text=nombre, font=("Arial", 18, "bold"), foreground="#059669").pack(pady=(8, 8))
        entries = {}
        for campo, tipo, default in campos:
            row = ttk.Frame(self.frame)
            row.pack(pady=4)
            ttk.Label(row, text=f"{campo}:", font=("Arial", 13)).pack(side="left", padx=4)
            ent = ttk.Entry(row, font=("Arial", 13), width=10)
            ent.insert(0, str(default))
            ent.pack(side="left", padx=4)
            entries[campo] = (ent, tipo)
        def calcular():
            try:
                params = {k: tipo(ent.get()) for k, (ent, tipo) in entries.items()}
                resultados = calcular_fn(self.valores, **params)
                self.show_resultados(nombre, resultados, lambda: self.show_inputs(nombre, campos, calcular_fn))
            except Exception as e:
                messagebox.showerror("Error", f"Entradas inválidas: {e}")
        ttk.Button(self.frame, text="Calcular", command=calcular, style="Custom.TButton").pack(pady=12)

    def show_resultados(self, nombre, resultados, volver_calculo=None):
        for widget in self.frame.winfo_children():
            widget.destroy()
        # Botones volver arriba
        topbar = ttk.Frame(self.frame, style="Custom.TFrame")
        topbar.pack(fill="x")
        volver_menu_btn = ttk.Button(topbar, text="← Volver al menú de distribuciones", style="Custom.TButton", command=self.setup_selector)
        volver_menu_btn.pack(side="left", padx=18, pady=8)
        if volver_calculo:
            volver_calc_btn = ttk.Button(topbar, text="↺ Volver al cálculo", style="Custom.TButton", command=volver_calculo)
            volver_calc_btn.pack(side="left", padx=8, pady=8)
        ttk.Label(self.frame, text=f"Resultados - {nombre}", font=("Arial", 16, "bold"), foreground="#3b82f6").pack(pady=(8, 8))
        # --- Layout horizontal tabla + gráfico ---
        main_content = ttk.Frame(self.frame)
        main_content.pack(fill="both", expand=True, padx=10, pady=10)
        main_content.columnconfigure(0, weight=1)
        main_content.columnconfigure(1, weight=1)
        # Tabla
        tabla_frame = ttk.Frame(main_content)
        tabla_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        cols = ["#", "Valor"]
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=18)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        for i, val in enumerate(resultados):
            tree.insert("", "end", values=(i+1, f"{val:.4f}"))
        tree.pack(fill="both", expand=True)
        # Gráfico
        grafico_frame = ttk.Frame(main_content)
        grafico_frame.grid(row=0, column=1, sticky="nsew")
        fig = Figure(figsize=(6, 5), dpi=100)  # Proporción horizontal
        ax = fig.add_subplot(111)
        ax.hist(resultados, bins=min(20, max(5, int(len(resultados)/10))), color="#2563eb", edgecolor="#fff", alpha=0.85)
        ax.set_title(f"Histograma - {nombre}", fontsize=16)
        ax.set_xlabel("Valor", fontsize=12)
        ax.set_ylabel("Frecuencia", fontsize=12)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        # --- Fin gráfico ---
        btns = ttk.Frame(self.frame)
        btns.pack(pady=8)
        def exportar_excel():
            df = pd.DataFrame({"Valor": resultados})
            nombre_archivo = f"distribucion_{nombre}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(nombre_archivo, index=False)
            messagebox.showinfo("Exportación", f"Tabla exportada como {nombre_archivo}")
        ttk.Button(btns, text="Exportar a Excel", command=exportar_excel, style="Custom.TButton").pack(side="left", padx=8)
        if volver_calculo:
            ttk.Button(btns, text="↺ Volver al cálculo", command=volver_calculo, style="Custom.TButton").pack(side="left", padx=8)
        ttk.Button(btns, text="← Volver al menú de distribuciones", command=self.setup_selector, style="Custom.TButton").pack(side="left", padx=8)

    # Métodos para cada distribución
    def show_uniforme_var(self):
        campos = [
            ("minimo", float, 0.0),
            ("maximo", float, 1.0),
        ]
        # Formula: minimo + (maximo - minimo) * Ri
        def calcular_uniforme(valores, minimo, maximo):
            return [minimo + (maximo - minimo) * v for v in valores]
        self.show_inputs("Uniforme (Variable)", campos, calcular_uniforme)

    def show_kerlang(self):
        campos = [
            ("K", int, 2),
            ("media", float, 1.0),
        ]
        # Formula: inv.gamma(Ri; K; media/K)
        def calcular_kerlang(valores, K, media):
            return gamma.ppf(valores, K, scale=media/K)
        self.show_inputs("K-Erlang", campos, calcular_kerlang)

    def show_exponencial(self):
        campos = [
            ("media", float, 1.0),
        ]
        # Formula: inv.gamma(Ri; 1; media)
        def calcular_exponencial(valores, media):
            return gamma.ppf(valores, 1, scale=media)
        self.show_inputs("Exponencial", campos, calcular_exponencial)

    def show_gamma(self):
        campos = [
            ("media", float, 2.0),
            ("varianza", float, 1.0),
        ]
        # Formula: INV.GAMMA(Ri;(media^2)/varianza;varianza/media)
        def calcular_gamma(valores, media, varianza):
            a = (media**2)/varianza
            scale = varianza/media
            return gamma.ppf(valores, a, scale=scale)
        self.show_inputs("Gamma", campos, calcular_gamma)

    def show_normal(self):
        campos = [
            ("media", float, 0.0),
            ("varianza", float, 1.0),
        ]
        # Formula: INV.NORM(Ri;media;RAIZ(varianza))
        def calcular_normal(valores, media, varianza):
            return norm.ppf(valores, loc=media, scale=varianza**0.5)
        self.show_inputs("Normal", campos, calcular_normal)

    def show_weibull(self):
        campos = [
            ("alfa", float, 2.0),
            ("beta", float, 1.0),
            ("gama", float, 0.0),
        ]
        # Formula: gama + (beta^2) * ((-LN(1-Ri))^(1/alfa))
        def calcular_weibull(valores, alfa, beta, gama):
            return [gama + (beta**2) * ((-np.log(1-v))**(1/alfa)) for v in valores]
        self.show_inputs("Weibull", campos, calcular_weibull)

    def show_uniforme_disc(self):
        campos = [
            ("minimo", int, 0),
            ("maximo", int, 10),
        ]
        # Formula: aleatorio.entre(max y minimo)
        def calcular_uniforme_disc(valores, minimo, maximo):
            return [np.random.randint(minimo, maximo+1) for _ in valores]
        self.show_inputs("Uniforme (Discreta)", campos, calcular_uniforme_disc)

    def show_bernoulli(self):
        campos = [
            ("media", float, 0.5),
        ]
        # Formula: SI(Ri<1-media;0;1)
        def calcular_bernoulli(valores, media):
            return [0 if v < 1-media else 1 for v in valores]
        self.show_inputs("Bernoulli", campos, calcular_bernoulli)

    def show_binomial(self):
        campos = [
            ("media", float, 5.0),
            ("varianza", float, 2.0),
        ]
        # Formula: INV.BINOM((media^2)/(media-varianza);(media-varianza)/media;Ri)
        def calcular_binomial(valores, media, varianza):
            n = int((media**2)/(media-varianza))
            p = (media-varianza)/media
            return binom.ppf(valores, n, p)
        self.show_inputs("Binomial", campos, calcular_binomial)

    def show_poisson(self):
        campos = [
            ("media", float, 2.0),
            ("varianza", float, 2.0),
        ]
        # Formula: usa media como lambda, varianza solo para mostrar
        def calcular_poisson(valores, media, varianza):
            # En Poisson, media = varianza = lambda
            return poisson.ppf(valores, media)
        self.show_inputs("Poisson", campos, calcular_poisson)
