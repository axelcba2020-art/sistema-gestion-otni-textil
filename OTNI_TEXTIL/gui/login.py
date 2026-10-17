import tkinter as tk
from tkinter import ttk, messagebox

from assets.style import aplicar_estilos
from database import obtener_conexion


class LoginFrame(ttk.Frame):
    def __init__(self, master, iniciar_sesion, usuarios=None):
        super().__init__(master)

        self.iniciar_sesion_callback = iniciar_sesion

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
        ).pack(anchor="w")

        self.entry_usuario = ttk.Entry(
            frame_usuario,
            style="Card.TEntry",
            width=40
        )
        self.entry_usuario.pack(anchor="center", padx=10, pady=(5, 10))

        frame_contrasena = ttk.Frame(self.form, style="Main.TFrame")
        frame_contrasena.pack(anchor="center", pady=10)

        ttk.Label(
            frame_contrasena,
            text="Ingrese su contraseña:",
            style="Card.TLabel",
        ).pack(anchor="w")

        self.entry_contrasena = ttk.Entry(
            frame_contrasena,
            show="*",
            style="Card.TEntry",
            width=40
        )
        self.entry_contrasena.pack(padx=10, pady=(5, 10))

        self.entry_usuario.bind(
            "<Return>",
            lambda event: self.entry_contrasena.focus_set()
        )
        self.entry_contrasena.bind(
            "<Return>",
            lambda event: self._validar_usuario()
        )

        ttk.Button(
            self.form,
            text="Iniciar sesión",
            style="Button.TButton",
            width=15,
            cursor="hand2",
            command=self._validar_usuario
        ).pack(anchor="center", padx=10, pady=(5, 10))

        self.entry_usuario.focus_set()

    def _validar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get()

        if not usuario:
            messagebox.showwarning(
                "Campo vacío",
                "Por favor, ingresá tu usuario."
            )
            self.entry_usuario.focus_set()
            return

        if not contrasena:
            messagebox.showwarning(
                "Campo vacío",
                "Por favor, ingresá tu contraseña."
            )
            self.entry_contrasena.focus_set()
            return

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT
                    ID_Empleado,
                    Nombre,
                    Apellido,
                    Usuario,
                    Contrasena,
                    Rol
                FROM Empleado
                WHERE Usuario = %s
                LIMIT 1
            """

            cursor.execute(consulta, (usuario,))
            empleado = cursor.fetchone()

            if empleado is None or empleado["Contrasena"] != contrasena:
                messagebox.showerror(
                    "Acceso denegado",
                    "El usuario o la contraseña no son válidos."
                )
                self.entry_contrasena.delete(0, tk.END)
                self.entry_contrasena.focus_set()
                return

            usuario_actual = {
                "ID_Empleado": empleado["ID_Empleado"],
                "nombre": empleado["Nombre"],
                "apellido": empleado["Apellido"],
                "usuario": empleado["Usuario"],
                "rol": empleado["Rol"],
            }

            self.iniciar_sesion_callback(usuario_actual)

        except Exception as error:
            messagebox.showerror(
                "Error de conexión",
                "No se pudo validar el inicio de sesión con la base de datos.\n\n"
                "Verificá que MySQL esté funcionando y que la configuración "
                "de conexión sea correcta.\n\n"
                f"Detalle: {error}"
            )

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()
