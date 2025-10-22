"""GUI using tkinter for interacting with generators and tests.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from . import generators, tests


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Pseudoaleatorios")
        self.root.state('zoomed')
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
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        main_frame.pack(fill="both", expand=True)
        title = ttk.Label(main_frame, text="Generador de Números Pseudoaleatorios", style="Custom.TLabel", anchor="center")
        title.pack(pady=(40, 18))
        btn_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        btn_frame.pack(pady=(0, 18))
        btn_frame.pack_propagate(False)
        btn_frame.configure(width=800)
        from .interfaces.cuadrados_medios import CuadradosMediosApp
        from .interfaces.productos_medios import ProductosMediosApp
        from .interfaces.multiplicador_constante import MultiplicadorConstanteApp
        def abrir_cuadrados():
            self.show_full_interface(CuadradosMediosApp)
        def abrir_productos():
            self.show_full_interface(ProductosMediosApp)
        def abrir_multiplicador():
            self.show_full_interface(MultiplicadorConstanteApp)
        botones = [
            ("Cuadrados Medios", "#2563eb", abrir_cuadrados),
            ("Productos Medios", "#059669", abrir_productos),
            ("Multiplicador Constante", "#f59e42", abrir_multiplicador)
        ]
        for i, (texto, color, cmd) in enumerate(botones):
            btn = tk.Button(
                btn_frame,
                text=texto,
                font=("Arial", 15, "bold"),
                bg=color,
                fg="#fff",
                activebackground="#1e293b",
                activeforeground="#fff",
                relief="raised",
                bd=3,
                height=2,
                width=22,
                cursor="hand2",
                command=cmd
            )
            btn.grid(row=0, column=i, padx=24, pady=8, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        footer = ttk.Label(main_frame, text="Desarrollado por Alvaro | Octubre 2025", font=("Arial", 11), foreground="#64748b", background="#eaf0f6")
        footer.pack(side="bottom", pady=(18, 4))

    def show_full_interface(self, InterfaceClass):
        for widget in self.root.winfo_children():
            widget.destroy()
        # Botón volver siempre visible arriba a la izquierda
        topbar = ttk.Frame(self.root, style="Custom.TFrame")
        topbar.pack(fill="x")
        volver_btn = ttk.Button(topbar, text="← Volver", style="Custom.TButton", command=self.show_main_menu)
        volver_btn.pack(side="left", padx=18, pady=18)
        # Interfaz del módulo ocupa el resto de la pantalla
        content_frame = ttk.Frame(self.root, style="Custom.TFrame")
        content_frame.pack(fill="both", expand=True)
        content_frame.pack_propagate(False)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        InterfaceClass(content_frame, self.show_main_menu)


def run_app():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
