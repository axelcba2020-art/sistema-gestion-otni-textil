import tkinter as tk
from tkinter import ttk
from pathlib import Path

from gui.login import LoginFrame
from gui.menu import MenuFrame
from assets.style import aplicar_estilos


_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


class OTNITEXTILAPP:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("OTNI TEXTIL")
        root.geometry("700x600")
        root.resizable(True, True)
        root.iconbitmap(_ASSETS_DIR / "logo.ico")

        self.style = ttk.Style(self.root)
        aplicar_estilos(self.style)

        self.usuario_actual = None
        self.menu = None
        self.login = None

        # Se conservan estos atributos para compatibilidad
        # con los módulos existentes.
        self.productos = []
        self.ventas = []
        self.clientes = []
        self.usuarios = []

        self.crear_login()

    def limpiar_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_login(self):
        self.limpiar_root()
        self.login = LoginFrame(
            self.root,
            self.iniciar_sesion
        )

    def iniciar_sesion(self, usuario):
        self.usuario_actual = usuario

        self.limpiar_root()

        self.menu = MenuFrame(
            self.root,
            self.mostrar_inicio,
            self.cerrar_sesion,
            self.usuarios,
            self.clientes,
            self.productos,
            self.ventas,
            usuario_actual=self.usuario_actual
        )

        self.menu.mostrar_inicio()

    def mostrar_inicio(self):
        if self.menu is not None:
            self.menu.mostrar_inicio()

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.menu = None
        self.limpiar_root()
        self.crear_login()
