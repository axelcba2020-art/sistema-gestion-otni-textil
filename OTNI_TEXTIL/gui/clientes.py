import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class ClientesFrame(ttk.Frame):
    def __init__(self, master, clientes=None):
        super().__init__(master)
        self.clientes = clientes if clientes is not None else [
            {
                "nombre": "Juan",
                "apellido": "Perez",
                "dni": "32.456.789",
                "telefono": "351-xxx-xxxx",
            }
        ]
        self.pack(fill="both", expand=True)

        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", padx=16, pady=(16, 8))

        self.buscar_var = tk.StringVar()
        ttk.Label(encabezado, text="Buscar cliente:").pack(side="left", padx=(0, 6))
        buscar = ttk.Entry(encabezado, textvariable=self.buscar_var, width=28)
        buscar.pack(side="left")
        self.buscar_var.trace_add("write", lambda *_: self._actualizar_tabla())

        ttk.Button(
            encabezado,
            text="Agregar cliente",
            cursor="hand2",
            command=self._nuevo_cliente,
        ).pack(side="right")

        tabla_frame = ttk.Frame(self)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))


        columnas = ("NOMBRE", "APELLIDO", "DNI", "TELÉFONO")
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
        
        
        ttk.Button(frame, text="Editar", cursor="hand2", command=self._editar_cliente).pack(side="left", padx=(8, 0))
        ttk.Button(frame, text="Eliminar", cursor="hand2", command=self._eliminar_cliente).pack(side="left", padx=(8, 0))
        
        
        self.lbl_stock_bajo = ttk.Label(frame, text="Clientes: 0")
        self.lbl_stock_bajo.pack(side="right")
        


    def _actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        texto_busqueda = self.buscar_var.get().strip().lower()
        clientes_visibles = [
            cliente for cliente in self.clientes
            if not texto_busqueda or any(
                texto_busqueda in str(cliente.get(campo, "")).lower()
                for campo in ("nombre", "apellido", "dni", "telefono")
            )
        ]

        for usuario in clientes_visibles:
            self.tree.insert(
                "",
                "end",
                values=(
                    usuario["nombre"],
                    usuario["apellido"],
                    usuario["dni"],
                    usuario["telefono"],
                ),
            )

        if clientes_visibles:
            self.lbl_vacio.place_forget()
        else:
            self.lbl_vacio.configure(
                text=("No se encontraron clientes" if texto_busqueda
                      else "No hay clientes registrados\nAgrega uno para comenzar")
            )
            self.lbl_vacio.place(relx=0.5, rely=0.5, anchor="center")
        self.lbl_stock_bajo.configure(text=f"Clientes: {len(clientes_visibles)}")


    def _nuevo_cliente(self):
        self._mostrar_formulario()

    def _editar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Selecciona un cliente para editarlo.")
            return

        cliente = self._cliente_seleccionado(seleccion[0])
        if cliente is not None:
            self._mostrar_formulario(cliente)

    def _eliminar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Selecciona un cliente para eliminarlo.")
            return

        cliente = self._cliente_seleccionado(seleccion[0])
        if cliente is None:
            return
        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar al cliente {cliente['nombre']} {cliente['apellido']}?",
        ):
            self.clientes.remove(cliente)
            self._actualizar_tabla()

    def _cliente_seleccionado(self, item):
        valores = self.tree.item(item, "values")
        return next(
            (cliente for cliente in self.clientes if cliente["dni"] == valores[2]),
            None,
        )

    def _mostrar_formulario(self, cliente=None):
        ventana = tk.Toplevel(self)
        ventana.title("Editar cliente" if cliente else "Nuevo cliente")
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
            ("dni", "DNI"),
            ("telefono", "Teléfono"),
        )
        for fila, (clave, etiqueta) in enumerate(datos):
            ttk.Label(formulario, text=f"{etiqueta}:").grid(
                row=fila, column=0, sticky="w", padx=(0, 12), pady=6
            )
            campo = ttk.Entry(formulario, width=28)
            campo.grid(row=fila, column=1, pady=6)
            if cliente:
                campo.insert(0, cliente.get(clave, ""))
            campos[clave] = campo
            campos_ordenados.append(campo)


        for indice, campo in enumerate(campos_ordenados[:-1]):
            campo.bind(
                "<Return>",
                lambda event, siguiente=campos_ordenados[indice + 1]:
                self._enfocar_siguiente(siguiente),
            )
        campos_ordenados[-1].bind(
            "<Return>", lambda event: self._guardar_cliente(ventana, campos, cliente)
        )


        boton_guardar = ttk.Button(
            formulario,
            text="Guardar cambios" if cliente else "Guardar cliente",
            cursor="hand2",
            command=lambda: self._guardar_cliente(ventana, campos, cliente),
        )
        boton_guardar.grid(row=len(datos), column=0, columnspan=2, pady=(12, 0))
        campos["nombre"].focus_set()


    def _enfocar_siguiente(self, siguiente):
        siguiente.focus_set()
        return "break"


    def _guardar_cliente(self, ventana, campos, cliente_original=None):
        datos = {clave: campo.get().strip() for clave, campo in campos.items()}
        if not all(datos.values()):
            messagebox.showwarning(
                "Datos incompletos",
                "Completa todos los campos del cliente.",
                parent=ventana,
            )
            return


        if any(
            cliente["dni"] == datos["dni"] and cliente is not cliente_original
            for cliente in self.clientes
        ):
            messagebox.showwarning(
                "Cliente existente",
                "Ya existe un cliente con ese DNI.",
                parent=ventana,
            )
            return


        if cliente_original is None:
            datos["fecha_alta"] = date.today().isoformat()
            self.clientes.append(datos)
        else:
            cliente_original.update(datos)
        ventana.destroy()
        self._actualizar_tabla()
