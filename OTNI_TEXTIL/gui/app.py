import tkinter as tk
from tkinter import ttk, messagebox

from gui.login import LoginFrame
from gui.inicio import InicioFrame
from gui.menu import MenuFrame
from gui.clientes import ClientesFrame
from gui.stock import StockFrame
from gui.ventas import VentasFrame
from gui.empleados import EmpleadosFrame
from gui.reportes import ReportesFrame


from assets.style import aplicar_estilos
from pathlib import Path
_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

class OTNITEXTILAPP:
    def __init__(self, root:tk.Tk):
        self.root = root
        root.title("OTNI TEXTIL")
        root.geometry("700x600")
        root.resizable(True, True)
        root.iconbitmap(_ASSETS_DIR / "logo.ico")
        # root.state("normal")
        # root.deiconify()

        # try:
        #     icon_path = _ASSETS_DIR / "logo.ico"
        #     if icon_path.exists():
        #         root.iconbitmap(str(icon_path))
        # except Exception:
        #     pass

        self.style = ttk.Style(self.root)
        aplicar_estilos(self.style)

        # self.frame = ttk.Frame(self.root, style="Main.TFrame")
        # self.frame.pack(fill="both", expand=True)

        self.productos = [
             {"nombre": "Remera básica", 
              "categoria": "Ropa", 
              "talle": "M", 
              "precio": 4200, 
              "stock": 28},
            {"nombre": "Pantalón cargo", 
             "categoria": "Ropa", 
             "talle": "42", 
             "precio": 6800, 
             "stock": 14},
             {"nombre": "Buzo algodón", 
              "categoria": "Ropa", 
              "talle": "L", 
              "precio": 7600, 
              "stock": 9},
            {"nombre": "Gorra OTNI", 
             "categoria": "Accesorios", 
             "talle": "Único", 
             "precio": 2500, 
             "stock": 31},
            {"nombre": "Bolso de tela", 
             "categoria": "Accesorios", 
             "talle": "Único", 
             "precio": 5400, 
             "stock": 7}
        ]

        self.usuarios = [
            {
                "nombre": "Nerea",
                "apellido": "Pereira",
                "usuario": "admin",
                "rol": "Administrador",
                "contraseña": "12345",
            }
        ]
        self.usuario_actual = None
        self.menu = None
        self.login = None
        self.ventas = []
        self.clientes = [
            {
                "nombre": "Juan",
                "apellido": "Perez",
                "dni": "32.456.789",
                "telefono": "351-xxx-xxxx",
            },
        ]
        self.crear_login()

    def limpiar_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_login(self):
        self.limpiar_root()
        self.login = LoginFrame(self.root, self.iniciar_sesion, self.usuarios)

    def iniciar_sesion(self, usuario):
        if self.login is not None and self.login.winfo_exists():
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
        )
        self.menu.mostrar_inicio()

    def mostrar_inicio(self):
        if self.menu is not None:
            self.menu.mostrar_inicio()

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.limpiar_root()
        self.menu = None
        self.crear_login()





    





