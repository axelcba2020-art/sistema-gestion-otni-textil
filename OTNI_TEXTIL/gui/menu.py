import tkinter as tk
from tkinter import ttk, messagebox

from gui.inicio import InicioFrame
from gui.stock import StockFrame
from gui.clientes import ClientesFrame
from gui.ventas import VentasFrame
from gui.reportes import ReportesFrame
from gui.empleados import EmpleadosFrame

from assets.style import aplicar_estilos

class MenuFrame(ttk.Frame):
    def __init__(
        self,
        master,
        _ingresar,
        _cerrar_sesion=None,
        usuarios=None,
        clientes=None,
        productos=None,
        ventas=None,
    ):
        super().__init__(master)
        self.ingresar = _ingresar
        self.cerrar_sesion_callback = _cerrar_sesion
        self.usuarios = usuarios if usuarios is not None else []
        self.clientes = clientes if clientes is not None else []
        self.productos = productos if productos is not None else []
        self.ventas = ventas if ventas is not None else []
        self.root = self.winfo_toplevel()
        self.titulo = None
        self.subtitulo = None
        self.boton_admin = None
        self.boton_atras = None
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self._crear_header()

        self.panel = ttk.Frame(self)
        self.panel.pack(fill="both", expand=True)
        self.panel.columnconfigure(1, weight=1)
        self.panel.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(self.panel)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=(10, 0))

        self.botones = ttk.Frame(self.sidebar)
        self.botones.pack(anchor="nw", fill="y")

        self.contenido = ttk.Frame(self.panel)
        self.contenido.grid(row=0, column=1, sticky="nsew")

        self.crear_botones()
        self.mostrar_inicio()

    def _crear_header(self):
        inner = ttk.Frame(self)
        self.header = inner
        inner.pack(fill="x", ipadx=10, ipady=10)
        inner.columnconfigure(1, weight=1)

        menu_admin = tk.Menu(inner, tearoff=0)
        menu_admin.add_command(
            label="Cerrar sesión",
            command=self._cerrar_sesion
        )

        self.boton_admin = ttk.Menubutton(
            inner,
            text="Admin 👤",
            cursor="hand2",
            menu=menu_admin,
            direction="below"
        )
        self.boton_admin.grid(row=0, column=1, sticky="e", pady=10)

        self.titulo = ttk.Label(
            inner,
            text="INDUMENTARIA OTNI TEXTIL",
            font=("Arial", 11, "bold")
        )
        self.titulo.grid(row=0, column=0, sticky="w", padx=10)

        self.subtitulo = ttk.Label(
            self,
            text="🏠 INICIO",
            font=("Arial", 10, "bold")
        )
        self.subtitulo.pack(anchor="w", padx=10, pady=(0, 5))

    def _cerrar_sesion(self):
        if self.cerrar_sesion_callback is not None:
            self.cerrar_sesion_callback()
        else:
            self.root.destroy()

    def crear_botones(self):
        botones = [
            ("📦 STOCK", self.mostrar_stock),
            ("👥 CLIENTES", self.mostrar_clientes),
            ("💰 VENTAS", self.mostrar_ventas),
            ("📃 REPORTES", self.mostrar_reportes),
            ("👤 USUARIOS", self.mostrar_usuarios),
        ]

        for texto, comando in botones:
            ttk.Button(
                self.botones,
                text=texto,
                cursor="hand2",
                width=18,
                command=comando
            ).pack(anchor="w", padx=10, pady=8)

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_pantalla(self, titulo, frame):
        self.limpiar_contenido()
        self.sidebar.grid_remove()
        self.subtitulo.configure(text=titulo)
        self.boton_admin.grid_remove()

        if self.boton_atras is None:
            self.boton_atras = ttk.Button(
                self.header,
                text="← Atrás",
                cursor="hand2",
                command=self.volver_menu
            )
        self.boton_atras.grid(row=0, column=1, sticky="e", pady=10)
        frame(self.contenido).pack(fill="both", expand=True)

    def volver_menu(self):
        self.limpiar_contenido()
        if self.boton_atras is not None:
            self.boton_atras.grid_remove()
        self.boton_admin.grid(row=0, column=1, sticky="e", pady=10)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=(10, 0))
        self.mostrar_inicio()

    def mostrar_inicio(self):
        self.limpiar_contenido()
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=(10, 0))
        self.subtitulo.configure(text="🏠 INICIO")
        self.boton_admin.grid(row=0, column=1, sticky="e", pady=10)
        if self.boton_atras is not None:
            self.boton_atras.grid_remove()
        InicioFrame(self.contenido).pack(fill="both", expand=True)

    def mostrar_stock(self):
        self.mostrar_pantalla(
            "📦 STOCK",
            lambda contenido: StockFrame(contenido, self.productos)
        )

    def mostrar_clientes(self):
        self.mostrar_pantalla(
            "👥 CLIENTES",
            lambda contenido: ClientesFrame(contenido, self.clientes),
        )

    def mostrar_ventas(self):
        self.mostrar_pantalla(
            "💰 VENTAS",
            lambda contenido: VentasFrame(contenido, self.clientes, self.productos, self.ventas),
        )

    def mostrar_reportes(self):
        self.mostrar_pantalla(
            "📃 REPORTES",
            lambda contenido: ReportesFrame(contenido, self.ventas, self.clientes),
        )

    def mostrar_usuarios(self):
        self.mostrar_pantalla(
            "👤 USUARIOS",
            lambda contenido: EmpleadosFrame(contenido, self.usuarios),
        )
