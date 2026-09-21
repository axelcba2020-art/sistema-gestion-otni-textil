import tkinter as tk
from tkinter import ttk, messagebox

from assets.style import aplicar_estilos


class LoginFrame(ttk.Frame):
    def __init__(self, master, iniciar_sesion, usuarios):
        super().__init__(master)

        self.iniciar_sesion_callback = iniciar_sesion
        self.usuarios = usuarios
        self.pack(fill="both", expand=True)
        self.configure(style="Main.TFrame")

        self.style = ttk.Style(self)
        aplicar_estilos(self.style)
        self.crear_header()

        self.form = ttk.Frame(self, style="Main.TFrame", padding=(20, 20))
        self.form.pack(fill="both", expand=True)
        self.crear_formulario()

    def crear_header(self):
        self.header = ttk.Frame(self, style="Header.TFrame")
        self.header.pack(fill="x", ipadx=10, ipady=10)

        ttk.Label(
            self.header,
            text="OTNI TEXTIL",
            style="HeaderTitle.TLabel"
        ).pack(anchor="center", padx=10, pady=10)

        ttk.Label(
            self.header,
            text="Sistema de gestión empresarial",
            style="HeaderSubTitle.TLabel"
        ).pack(anchor="center", padx=10, pady=10)

    def crear_formulario(self):
        frame_usuario = ttk.Frame(self.form, style="Main.TFrame")
        frame_usuario.pack(anchor="center", pady=10)

        ttk.Label(
            frame_usuario,
            text="Ingrese su usuario:",
            style="Card.TLabel", 
        ).pack(anchor="w")#, padx=10, pady=10)

        self.entry_usuario = ttk.Entry(
                            frame_usuario, 
                            style="Card.TEntry", 
                            width=40
                        )
        self.entry_usuario.pack(anchor="center", padx=10, pady=(5, 10))

        
        frame_contraseña = ttk.Frame(self.form, style="Main.TFrame")
        frame_contraseña.pack(anchor="center", pady=10)

        ttk.Label(
            frame_contraseña,
            text="Ingrese su contraseña:",
            style="Card.TLabel", 
        ).pack(anchor="w")#, padx=10, pady=10)

        self.entry_contraseña = ttk.Entry(
                            frame_contraseña, 
                            show="*", 
                            style="Card.TEntry", 
                            width=40
        )
        self.entry_contraseña.pack(padx=10, pady=(5, 10))

        self.entry_usuario.bind("<Return>", lambda event: self.entry_contraseña.focus_set())
        self.entry_contraseña.bind("<Return>", lambda event: self._validar_usuario())

        ttk.Button(
            self.form,
            text="Iniciar sesión", 
            style="Button.TButton", 
            width=15, 
            cursor="hand2",
            command=self._validar_usuario
        ).pack(anchor="center", padx=10, pady=(5, 10))

    def _validar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        if not usuario:
            messagebox.showwarning("Campo vacío", "Por favor ingrese su usuario.")
            self.entry_usuario.focus_set()
            return

        contraseña = self.entry_contraseña.get()
        if not contraseña:
            messagebox.showwarning("Campo vacío", "Por favor ingrese su contraseña.")
            self.entry_contraseña.focus_set()
            return

        usuario_valido = next(
            (
                registrado
                for registrado in self.usuarios
                if registrado["usuario"] == usuario
                and registrado["contraseña"] == contraseña
            ),
            None,
        )
        if usuario_valido is None:
            messagebox.showerror(
                "Acceso denegado",
                "El usuario o la contraseña no son válidos.",
            )
            self.entry_contraseña.focus_set()
            return

        self.iniciar_sesion_callback(usuario_valido)
