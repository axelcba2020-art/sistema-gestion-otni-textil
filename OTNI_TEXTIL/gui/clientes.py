
import tkinter as tk
from tkinter import ttk, messagebox
from validaciones.validador_otni import validar_cliente
from database import obtener_conexion
from mysql.connector import Error


class ClientesFrame(ttk.Frame):
    def __init__(self, master, clientes=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", padx=16, pady=(16, 8))

        self.buscar_var = tk.StringVar()

        ttk.Label(
            encabezado, text="Buscar cliente:"
        ).pack(side="left", padx=(0, 6))

        ttk.Entry(
            encabezado,
            textvariable=self.buscar_var,
            width=28
        ).pack(side="left")

        self.buscar_var.trace_add(
            "write", lambda *_: self._actualizar_tabla()
        )

        ttk.Button(
            encabezado,
            text="Agregar cliente",
            cursor="hand2",
            command=self._nuevo_cliente
        ).pack(side="right")

        tabla_frame = ttk.Frame(self)
        tabla_frame.pack(
            fill="both", expand=True, padx=16, pady=(0, 16)
        )

        columnas = (
            "ID", "NOMBRE", "APELLIDO", "DNI",
            "TELÉFONO", "CORREO", "DIRECCIÓN"
        )

        self.tree = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )
        self.tree.pack(side="left", fill="both", expand=True)

        anchos = {
            "ID": 45,
            "NOMBRE": 110,
            "APELLIDO": 110,
            "DNI": 95,
            "TELÉFONO": 110,
            "CORREO": 180,
            "DIRECCIÓN": 180
        }

        for columna in columnas:
            self.tree.heading(columna, text=columna)
            self.tree.column(
                columna, width=anchos[columna], anchor="w"
            )

        scrollbar_vertical = ttk.Scrollbar(
            tabla_frame, orient="vertical", command=self.tree.yview
        )
        scrollbar_vertical.pack(side="right", fill="y")

        scrollbar_horizontal = ttk.Scrollbar(
            self, orient="horizontal", command=self.tree.xview
        )
        scrollbar_horizontal.pack(fill="x", padx=16)

        self.tree.configure(
            yscrollcommand=scrollbar_vertical.set,
            xscrollcommand=scrollbar_horizontal.set
        )

        self.lbl_vacio = ttk.Label(tabla_frame, justify="center")

        footer = ttk.Frame(self)
        footer.pack(fill="x", padx=16, pady=(0, 16))

        ttk.Button(
            footer,
            text="Editar",
            cursor="hand2",
            command=self._editar_cliente
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            footer,
            text="Eliminar",
            cursor="hand2",
            command=self._eliminar_cliente
        ).pack(side="left", padx=(8, 0))

        self.lbl_total = ttk.Label(footer, text="Clientes: 0")
        self.lbl_total.pack(side="right")

        self._actualizar_tabla()

    def _actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        texto = self.buscar_var.get().strip()
        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            sql = """
                SELECT ID_Cliente, Nombre, Apellido, DNI,
                       Telefono, Email, Direccion
                FROM Cliente
                WHERE Nombre LIKE %s
                   OR Apellido LIKE %s
                   OR DNI LIKE %s
                   OR Telefono LIKE %s
                   OR Email LIKE %s
                   OR Direccion LIKE %s
                ORDER BY ID_Cliente
            """

            patron = f"%{texto}%"
            cursor.execute(sql, (patron,) * 6)
            clientes = cursor.fetchall()

            for cliente in clientes:
                self.tree.insert(
                    "", "end",
                    values=tuple(
                        "" if valor is None else valor
                        for valor in cliente
                    )
                )

            if clientes:
                self.lbl_vacio.place_forget()
            else:
                mensaje = (
                    "No se encontraron clientes"
                    if texto
                    else "No hay clientes registrados\nAgregá uno para comenzar"
                )
                self.lbl_vacio.configure(text=mensaje)
                self.lbl_vacio.place(
                    relx=0.5, rely=0.5, anchor="center"
                )

            self.lbl_total.configure(
                text=f"Clientes: {len(clientes)}"
            )

        except Error as error:
            messagebox.showerror(
                "Error de base de datos",
                f"No se pudieron consultar los clientes.\n\n{error}",
                parent=self
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    def _nuevo_cliente(self):
        self._mostrar_formulario()

    def _editar_cliente(self):
        seleccion = self.tree.selection()

        if not seleccion:
            messagebox.showinfo(
                "Sin selección",
                "Seleccioná un cliente para editarlo.",
                parent=self
            )
            return

        valores = self.tree.item(seleccion[0], "values")

        cliente = {
            "id": int(valores[0]),
            "nombre": valores[1],
            "apellido": valores[2],
            "dni": valores[3],
            "telefono": valores[4],
            "email": valores[5],
            "direccion": valores[6]
        }

        self._mostrar_formulario(cliente)

    def _eliminar_cliente(self):
        seleccion = self.tree.selection()

        if not seleccion:
            messagebox.showinfo(
                "Sin selección",
                "Seleccioná un cliente para eliminarlo.",
                parent=self
            )
            return

        valores = self.tree.item(seleccion[0], "values")
        cliente_id = int(valores[0])
        nombre = f"{valores[1]} {valores[2]}"

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Querés eliminar al cliente {nombre}?\n\n"
            "Esta acción no se puede deshacer.",
            parent=self
        )

        if not confirmar:
            return

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute(
                "DELETE FROM Cliente WHERE ID_Cliente = %s",
                (cliente_id,)
            )

            conexion.commit()

            messagebox.showinfo(
                "Cliente eliminado",
                "El cliente se eliminó correctamente.",
                parent=self
            )

            self._actualizar_tabla()

        except Error as error:
            if conexion is not None and conexion.is_connected():
                conexion.rollback()

            messagebox.showerror(
                "No se pudo eliminar",
                "No se pudo eliminar el cliente. "
                "Es posible que tenga ventas asociadas.\n\n"
                f"Detalle: {error}",
                parent=self
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    def _mostrar_formulario(self, cliente=None):
        ventana = tk.Toplevel(self)
        ventana.title("Editar cliente" if cliente else "Nuevo cliente")
        ventana.resizable(False, False)
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        formulario = ttk.Frame(ventana, padding=16)
        formulario.pack(fill="both", expand=True)

        campos = {}

        datos = (
            ("nombre", "Nombre"),
            ("apellido", "Apellido"),
            ("dni", "DNI"),
            ("telefono", "Teléfono"),
            ("email", "Correo electrónico"),
            ("direccion", "Dirección")
        )

        for fila, (clave, etiqueta) in enumerate(datos):
            ttk.Label(
                formulario, text=f"{etiqueta}:"
            ).grid(
                row=fila, column=0, sticky="w",
                padx=(0, 12), pady=6
            )

            campo = ttk.Entry(formulario, width=32)
            campo.grid(row=fila, column=1, pady=6)

            if cliente:
                campo.insert(0, cliente.get(clave, ""))

            campos[clave] = campo

        orden = list(campos.values())

        for indice, campo in enumerate(orden[:-1]):
            campo.bind(
                "<Return>",
                lambda event, siguiente=orden[indice + 1]:
                self._enfocar_siguiente(siguiente)
            )

        orden[-1].bind(
            "<Return>",
            lambda event: self._guardar_cliente(
                ventana, campos, cliente
            )
        )

        ttk.Button(
            formulario,
            text="Guardar cambios" if cliente else "Guardar cliente",
            cursor="hand2",
            command=lambda: self._guardar_cliente(
                ventana, campos, cliente
            )
        ).grid(
            row=len(datos), column=0, columnspan=2, pady=(12, 0)
        )

        campos["nombre"].focus_set()

    def _enfocar_siguiente(self, siguiente):
        siguiente.focus_set()
        return "break"

    def _guardar_cliente(self, ventana, campos, cliente_original=None):
        datos = {
            clave: campo.get().strip()
            for clave, campo in campos.items()
        }

        if not all(
            datos[campo]
            for campo in ("nombre", "apellido", "dni", "telefono")
        ):
            messagebox.showwarning(
                "Datos incompletos",
                "Completá nombre, apellido, DNI y teléfono.",
                parent=ventana
            )
            return

        es_valido, mensaje = validar_cliente(
            datos["nombre"],
            datos["apellido"],
            datos["dni"]
        )

        if not es_valido:
            messagebox.showwarning(
                "Datos inválidos", mensaje, parent=ventana
            )
            return

        if datos["email"] and (
            "@" not in datos["email"]
            or "." not in datos["email"].split("@")[-1]
        ):
            messagebox.showwarning(
                "Correo inválido",
                "Ingresá un correo válido o dejá el campo vacío.",
                parent=ventana
            )
            return

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            if cliente_original:
                cursor.execute(
                    """
                    SELECT ID_Cliente
                    FROM Cliente
                    WHERE DNI = %s AND ID_Cliente <> %s
                    """,
                    (datos["dni"], cliente_original["id"])
                )
            else:
                cursor.execute(
                    "SELECT ID_Cliente FROM Cliente WHERE DNI = %s",
                    (datos["dni"],)
                )

            if cursor.fetchone():
                messagebox.showwarning(
                    "DNI existente",
                    "Ya existe otro cliente con ese DNI.",
                    parent=ventana
                )
                return

            if cliente_original:
                sql = """
                    UPDATE Cliente
                    SET Nombre = %s,
                        Apellido = %s,
                        DNI = %s,
                        Telefono = %s,
                        Email = %s,
                        Direccion = %s
                    WHERE ID_Cliente = %s
                """

                parametros = (
                    datos["nombre"],
                    datos["apellido"],
                    datos["dni"],
                    datos["telefono"],
                    datos["email"] or None,
                    datos["direccion"] or None,
                    cliente_original["id"]
                )
            else:
                sql = """
                    INSERT INTO Cliente
                        (Nombre, Apellido, DNI, Telefono, Email, Direccion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                parametros = (
                    datos["nombre"],
                    datos["apellido"],
                    datos["dni"],
                    datos["telefono"],
                    datos["email"] or None,
                    datos["direccion"] or None
                )

            cursor.execute(sql, parametros)
            conexion.commit()

            ventana.destroy()

            messagebox.showinfo(
                "Operación exitosa",
                "Los datos del cliente se guardaron correctamente.",
                parent=self
            )

            self._actualizar_tabla()

        except Error as error:
            if conexion is not None and conexion.is_connected():
                conexion.rollback()

            messagebox.showerror(
                "Error de base de datos",
                "No se pudieron guardar los datos.\n\n"
                f"Detalle: {error}",
                parent=ventana
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()
