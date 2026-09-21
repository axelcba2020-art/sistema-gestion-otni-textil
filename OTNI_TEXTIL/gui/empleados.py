import tkinter as tk
from tkinter import ttk, messagebox

class EmpleadosFrame(ttk.Frame):
    def __init__(self, master, usuarios):
        super().__init__(master)
        self.usuarios = usuarios
        self.pack(fill="both", expand=True)

        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", padx=16, pady=(16, 8))

        self.buscar_var = tk.StringVar()
        ttk.Label(encabezado, text="Buscar usuario:").pack(side="left", padx=(0, 6))
        buscar = ttk.Entry(encabezado, textvariable=self.buscar_var, width=28)
        buscar.pack(side="left")
        self.buscar_var.trace_add("write", lambda *_: self._actualizar_tabla())

        ttk.Button(
            encabezado,
            text="Agregar usuario",
            cursor="hand2",
            command=self._nuevo_usuario,
        ).pack(side="right")

        tabla_frame = ttk.Frame(self)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))


        columnas = ("NOMBRE", "APELLIDO", "USUARIO", "ROL")
        self.tree = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse",
        )
        self.tree.pack(side="left", fill="both", expand=True)


        for columna in columnas:
            self.tree.heading(columna, text=columna)
            self.tree.column(columna, width=150, anchor="w")


        scrollbar = ttk.Scrollbar(
            tabla_frame, orient="vertical", command=self.tree.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.lbl_vacio = ttk.Label(tabla_frame, justify="center")
        self._crear_footer()
        self._actualizar_tabla()

    def _crear_footer(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=16, pady=(0, 16))
        
        
        ttk.Button(frame, text="Editar", cursor="hand2", command=self._editar_usuario).pack(side="left", padx=(8, 0))
        ttk.Button(frame, text="Eliminar", cursor="hand2", command=self._eliminar_usuario).pack(side="left", padx=(8, 0))
        
        
        self.lbl_stock_bajo = ttk.Label(frame, text="Usuarios: 0")
        self.lbl_stock_bajo.pack(side="right")
        


    def _actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        texto_busqueda = self.buscar_var.get().strip().lower()
        usuarios_visibles = [
            usuario for usuario in self.usuarios
            if not texto_busqueda or any(
                texto_busqueda in str(usuario.get(campo, "")).lower()
                for campo in ("nombre", "apellido", "usuario", "rol")
            )
        ]

        for usuario in usuarios_visibles:
            self.tree.insert(
                "",
                "end",
                values=(
                    usuario["nombre"],
                    usuario["apellido"],
                    usuario["usuario"],
                    usuario["rol"],
                ),
            )

        if usuarios_visibles:
            self.lbl_vacio.place_forget()
        else:
            self.lbl_vacio.configure(
                text=("No se encontraron usuarios" if texto_busqueda
                      else "No hay usuarios registrados\nAgrega uno para comenzar")
            )
            self.lbl_vacio.place(relx=0.5, rely=0.5, anchor="center")
        self.lbl_stock_bajo.configure(text=f"Usuarios: {len(usuarios_visibles)}")


    def _nuevo_usuario(self):
        self._mostrar_formulario()

    def _editar_usuario(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Selecciona un usuario para editarlo.")
            return

        usuario = self._usuario_seleccionado(seleccion[0])
        if usuario is not None:
            self._mostrar_formulario(usuario)

    def _eliminar_usuario(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Selecciona un usuario para eliminarlo.")
            return

        usuario = self._usuario_seleccionado(seleccion[0])
        if usuario is None:
            return
        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar al usuario {usuario['usuario']}?",
        ):
            self.usuarios.remove(usuario)
            self._actualizar_tabla()

    def _usuario_seleccionado(self, item):
        valores = self.tree.item(item, "values")
        return next(
            (usuario for usuario in self.usuarios if usuario["usuario"] == valores[2]),
            None,
        )

    def _mostrar_formulario(self, usuario=None):
        ventana = tk.Toplevel(self)
        ventana.title("Editar usuario" if usuario else "Nuevo usuario")
        ventana.resizable(False, False)
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()


        formulario = ttk.Frame(ventana, padding=16)
        formulario.pack(fill="both", expand=True)


        campos = {}
        campos_ordenados = []
        datos = (
            ("nombre", "Nombre"),
            ("apellido", "Apellido"),
            ("usuario", "Usuario"),
            ("rol", "Rol"),
            ("contrasena", "Contraseña"),
        )
        for fila, (clave, etiqueta) in enumerate(datos):
            ttk.Label(formulario, text=f"{etiqueta}:").grid(
                row=fila, column=0, sticky="w", padx=(0, 12), pady=6
            )
            campo = ttk.Entry(
                formulario, width=28, show="*" if clave == "contraseña" else ""
            )
            campo.grid(row=fila, column=1, pady=6)
            if usuario:
                campo.insert(0, usuario.get(clave, ""))
            campos[clave] = campo
            campos_ordenados.append(campo)


        for indice, campo in enumerate(campos_ordenados[:-1]):
            campo.bind(
                "<Return>",
                lambda event, siguiente=campos_ordenados[indice + 1]:
                self._enfocar_siguiente(siguiente),
            )
        campos_ordenados[-1].bind(
            "<Return>", lambda event: self._guardar_usuario(ventana, campos, usuario)
        )


        boton_guardar = ttk.Button(
            formulario,
            text="Guardar cambios" if usuario else "Guardar usuario",
            cursor="hand2",
            command=lambda: self._guardar_usuario(ventana, campos, usuario),
        )
        boton_guardar.grid(row=len(datos), column=0, columnspan=2, pady=(12, 0))
        campos["nombre"].focus_set()


    def _enfocar_siguiente(self, siguiente):
        siguiente.focus_set()
        return "break"


    def _guardar_usuario(self, ventana, campos, usuario_original=None):
        datos = {clave: campo.get().strip() for clave, campo in campos.items()}
        if not all(datos.values()):
            messagebox.showwarning(
                "Datos incompletos",
                "Completa todos los campos del usuario.",
                parent=ventana,
            )
            return


        if any(
            usuario["usuario"] == datos["usuario"] and usuario is not usuario_original
            for usuario in self.usuarios
        ):
            messagebox.showwarning(
                "Usuario existente",
                "Ya existe un usuario con ese nombre.",
                parent=ventana,
            )
            return


        if usuario_original is None:
            self.usuarios.append(datos)
        else:
            usuario_original.update(datos)
        ventana.destroy()
        self._actualizar_tabla()





