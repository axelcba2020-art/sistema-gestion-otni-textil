
import tkinter as tk
from tkinter import ttk, messagebox
import unicodedata

from database import obtener_conexion


class EmpleadosFrame(ttk.Frame):
    def __init__(self, master, usuarios=None, usuario_actual=None):
        super().__init__(master)

        self.usuarios = usuarios if usuarios is not None else []
        self.usuario_actual = usuario_actual or {}

        if not self._verificar_permisos():
            self.destroy()
            return

        self.pack(fill="both", expand=True, padx=10, pady=10)
        self._crear_interfaz()
        self._cargar_empleados()

    # --------------------------------------------------
    # PERMISOS
    # --------------------------------------------------

    def _verificar_permisos(self):
        rol = str(
            self.usuario_actual.get("rol", "")
        ).strip().casefold()

        if rol not in ("administrador", "admin"):
            messagebox.showerror(
                "Acceso denegado",
                "No tenés permisos para administrar empleados."
            )
            return False

        return True

    # --------------------------------------------------
    # UTILIDADES PARA MYSQL
    # --------------------------------------------------

    def _normalizar(self, texto):
        texto = unicodedata.normalize("NFKD", str(texto))
        texto = "".join(
            c for c in texto
            if not unicodedata.combining(c)
        )
        return texto.casefold().replace(" ", "").replace("_", "")

    def _obtener_columnas(self, cursor):
        cursor.execute("SELECT * FROM Empleado LIMIT 0")
        nombres = [columna[0] for columna in cursor.description]

        return {
            self._normalizar(nombre): nombre
            for nombre in nombres
        }

    def _columna(self, columnas, *alternativas):
        for alternativa in alternativas:
            nombre = columnas.get(self._normalizar(alternativa))
            if nombre:
                return nombre
        return None

    def _citar_columna(self, nombre):
        return "`" + nombre.replace("`", "``") + "`"

    def _obtener_conexion_y_columnas(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor(
            dictionary=True,
            buffered=True
        )

        try:
            columnas = self._obtener_columnas(cursor)

            id_col = self._columna(
                columnas, "ID_Empleado", "IdEmpleado"
            )
            nombre_col = self._columna(columnas, "Nombre")
            apellido_col = self._columna(columnas, "Apellido")
            usuario_col = self._columna(columnas, "Usuario")
            rol_col = self._columna(columnas, "Rol")
            clave_col = self._columna(
                columnas,
                "Contraseña",
                "Contrasena",
                "Password",
                "Clave"
            )

            if not all((
                id_col,
                nombre_col,
                apellido_col,
                usuario_col,
                rol_col,
                clave_col
            )):
                raise RuntimeError(
                    "No se encontraron todas las columnas necesarias "
                    "en la tabla Empleado."
                )

            campos = {
                "id": id_col,
                "nombre": nombre_col,
                "apellido": apellido_col,
                "usuario": usuario_col,
                "rol": rol_col,
                "clave": clave_col,
            }

            return conexion, cursor, campos

        except Exception:
            cursor.close()
            conexion.close()
            raise

    # --------------------------------------------------
    # INTERFAZ
    # --------------------------------------------------

    def _crear_interfaz(self):
        ttk.Label(
            self,
            text="Gestión de empleados",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 10))

        ttk.Label(
            self,
            text="Desde acá podés agregar, editar o eliminar empleados."
        ).pack(pady=(0, 10))

        columnas = ("ID", "NOMBRE", "APELLIDO", "USUARIO", "ROL")

        self.tabla = ttk.Treeview(
            self,
            columns=columnas,
            show="headings",
            height=14
        )

        encabezados = {
            "ID": ("ID", 55),
            "NOMBRE": ("Nombre", 160),
            "APELLIDO": ("Apellido", 160),
            "USUARIO": ("Usuario", 150),
            "ROL": ("Rol", 130),
        }

        for columna, (titulo, ancho) in encabezados.items():
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(
                columna,
                width=ancho,
                anchor="center"
            )

        self.tabla.pack(
            fill="both",
            expand=True,
            pady=(0, 10)
        )

        self.tabla.bind(
            "<Double-1>",
            lambda evento: self._editar_seleccionado()
        )

        botones = ttk.Frame(self)
        botones.pack(fill="x", pady=5)

        ttk.Button(
            botones,
            text="Agregar empleado",
            command=self._nuevo_empleado
        ).pack(side="left", padx=4)

        ttk.Button(
            botones,
            text="Editar seleccionado",
            command=self._editar_seleccionado
        ).pack(side="left", padx=4)

        ttk.Button(
            botones,
            text="Eliminar seleccionado",
            command=self._eliminar_seleccionado
        ).pack(side="left", padx=4)

        ttk.Button(
            botones,
            text="Actualizar lista",
            command=self._cargar_empleados
        ).pack(side="right", padx=4)

    # --------------------------------------------------
    # CARGAR EMPLEADOS
    # --------------------------------------------------

    def _cargar_empleados(self):
        if not self._verificar_permisos():
            return

        conexion = None
        cursor = None

        try:
            conexion, cursor, campos = (
                self._obtener_conexion_y_columnas()
            )

            consulta = (
                f"SELECT * FROM Empleado ORDER BY "
                f"{self._citar_columna(campos['id'])}"
            )
            cursor.execute(consulta)
            empleados = cursor.fetchall()

            for item in self.tabla.get_children():
                self.tabla.delete(item)

            for empleado in empleados:
                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        empleado[campos["id"]],
                        empleado[campos["nombre"]],
                        empleado[campos["apellido"]],
                        empleado[campos["usuario"]],
                        empleado[campos["rol"]],
                    )
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los empleados.\n\n{error}"
            )

        finally:
            if cursor:
                cursor.close()

            if conexion and conexion.is_connected():
                conexion.close()

    # --------------------------------------------------
    # EMPLEADO SELECCIONADO
    # --------------------------------------------------

    def _obtener_seleccionado(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Atención",
                "Primero seleccioná un empleado."
            )
            return None

        valores = self.tabla.item(
            seleccion[0], "values"
        )

        return {
            "id": valores[0],
            "nombre": valores[1],
            "apellido": valores[2],
            "usuario": valores[3],
            "rol": valores[4],
        }

    # --------------------------------------------------
    # AGREGAR Y EDITAR
    # --------------------------------------------------

    def _nuevo_empleado(self):
        if not self._verificar_permisos():
            return

        self._mostrar_formulario()

    def _editar_seleccionado(self):
        if not self._verificar_permisos():
            return

        empleado = self._obtener_seleccionado()

        if empleado:
            self._mostrar_formulario(empleado)

    def _mostrar_formulario(self, empleado=None):
        if not self._verificar_permisos():
            return

        ventana = tk.Toplevel(self)
        ventana.title(
            "Editar empleado" if empleado
            else "Agregar empleado"
        )
        ventana.geometry("380x390")
        ventana.resizable(False, False)
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        formulario = ttk.Frame(ventana, padding=20)
        formulario.pack(fill="both", expand=True)

        ttk.Label(
            formulario,
            text="Editar empleado" if empleado else "Nuevo empleado",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 15))

        variables = {}

        for etiqueta, clave in (
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Usuario", "usuario"),
        ):
            ttk.Label(formulario, text=etiqueta).pack(anchor="w")

            variable = tk.StringVar(
                value=empleado[clave] if empleado else ""
            )
            variables[clave] = variable

            ttk.Entry(
                formulario,
                textvariable=variable
            ).pack(fill="x", pady=(2, 8))

        ttk.Label(formulario, text="Rol").pack(anchor="w")

        variables["rol"] = tk.StringVar(
            value=empleado["rol"] if empleado else "Vendedor"
        )

        ttk.Combobox(
            formulario,
            textvariable=variables["rol"],
            values=("Administrador", "Vendedor"),
            state="readonly"
        ).pack(fill="x", pady=(2, 8))

        ttk.Label(
            formulario,
            text=(
                "Contraseña (obligatoria)"
                if not empleado
                else "Nueva contraseña (opcional)"
            )
        ).pack(anchor="w")

        clave_variable = tk.StringVar()

        entrada_clave = ttk.Entry(
            formulario,
            textvariable=clave_variable,
            show="*"
        )
        entrada_clave.pack(fill="x", pady=(2, 5))

        if empleado:
            ttk.Label(
                formulario,
                text="Dejala vacía para conservar la actual.",
                foreground="gray"
            ).pack(anchor="w", pady=(0, 8))

        def guardar():
            if not self._verificar_permisos():
                return

            nombre = variables["nombre"].get().strip()
            apellido = variables["apellido"].get().strip()
            usuario = variables["usuario"].get().strip()
            rol = variables["rol"].get().strip()
            clave = clave_variable.get()

            if not nombre or not apellido or not usuario:
                messagebox.showwarning(
                    "Datos incompletos",
                    "Completá el nombre, apellido y usuario.",
                    parent=ventana
                )
                return

            if rol not in ("Administrador", "Vendedor"):
                messagebox.showwarning(
                    "Rol inválido",
                    "Seleccioná un rol válido.",
                    parent=ventana
                )
                return

            if not empleado and not clave:
                messagebox.showwarning(
                    "Contraseña requerida",
                    "Ingresá una contraseña para el nuevo empleado.",
                    parent=ventana
                )
                return

            conexion = None
            cursor = None

            try:
                conexion, cursor, campos = (
                    self._obtener_conexion_y_columnas()
                )

                id_col = self._citar_columna(campos["id"])
                nombre_col = self._citar_columna(campos["nombre"])
                apellido_col = self._citar_columna(campos["apellido"])
                usuario_col = self._citar_columna(campos["usuario"])
                rol_col = self._citar_columna(campos["rol"])
                clave_col = self._citar_columna(campos["clave"])

                consulta_usuario = (
                    f"SELECT {id_col} FROM Empleado "
                    f"WHERE {usuario_col} = %s"
                )
                parametros = [usuario]

                if empleado:
                    consulta_usuario += f" AND {id_col} != %s"
                    parametros.append(empleado["id"])

                cursor.execute(
                    consulta_usuario,
                    tuple(parametros)
                )

                if cursor.fetchone():
                    messagebox.showwarning(
                        "Usuario existente",
                        "Ya existe un empleado con ese nombre de usuario.",
                        parent=ventana
                    )
                    return

                if empleado:
                    if clave:
                        consulta = (
                            f"UPDATE Empleado SET "
                            f"{nombre_col} = %s, "
                            f"{apellido_col} = %s, "
                            f"{usuario_col} = %s, "
                            f"{rol_col} = %s, "
                            f"{clave_col} = %s "
                            f"WHERE {id_col} = %s"
                        )
                        valores = (
                            nombre, apellido, usuario,
                            rol, clave, empleado["id"]
                        )
                    else:
                        consulta = (
                            f"UPDATE Empleado SET "
                            f"{nombre_col} = %s, "
                            f"{apellido_col} = %s, "
                            f"{usuario_col} = %s, "
                            f"{rol_col} = %s "
                            f"WHERE {id_col} = %s"
                        )
                        valores = (
                            nombre, apellido, usuario,
                            rol, empleado["id"]
                        )

                    cursor.execute(consulta, valores)
                    mensaje = "Empleado actualizado correctamente."

                else:
                    consulta = (
                        f"INSERT INTO Empleado "
                        f"({nombre_col}, {apellido_col}, "
                        f"{usuario_col}, {rol_col}, {clave_col}) "
                        f"VALUES (%s, %s, %s, %s, %s)"
                    )

                    cursor.execute(
                        consulta,
                        (nombre, apellido, usuario, rol, clave)
                    )
                    mensaje = "Empleado agregado correctamente."

                conexion.commit()

                messagebox.showinfo(
                    "Operación exitosa",
                    mensaje,
                    parent=ventana
                )

                ventana.destroy()
                self._cargar_empleados()

            except Exception as error:
                if conexion and conexion.is_connected():
                    conexion.rollback()

                messagebox.showerror(
                    "Error",
                    f"No se pudo guardar el empleado.\n\n{error}",
                    parent=ventana
                )

            finally:
                if cursor:
                    cursor.close()

                if conexion and conexion.is_connected():
                    conexion.close()

        botones = ttk.Frame(formulario)
        botones.pack(fill="x", pady=(10, 0))

        ttk.Button(
            botones,
            text="Guardar",
            command=guardar
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            botones,
            text="Cancelar",
            command=ventana.destroy
        ).pack(side="left")

        entrada_clave.bind(
            "<Return>",
            lambda evento: guardar()
        )

    # --------------------------------------------------
    # ELIMINAR EMPLEADO
    # --------------------------------------------------

    def _eliminar_seleccionado(self):
        if not self._verificar_permisos():
            return

        empleado = self._obtener_seleccionado()

        if not empleado:
            return

        id_actual = self.usuario_actual.get("ID_Empleado")

        if (
            id_actual is not None
            and str(id_actual) == str(empleado["id"])
        ):
            messagebox.showwarning(
                "Operación no permitida",
                "No podés eliminar el empleado con el que "
                "iniciaste sesión."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Querés eliminar al empleado "
            f"{empleado['nombre']} {empleado['apellido']}?"
        )

        if not confirmar:
            return

        conexion = None
        cursor = None

        try:
            conexion, cursor, campos = (
                self._obtener_conexion_y_columnas()
            )

            consulta = (
                f"DELETE FROM Empleado WHERE "
                f"{self._citar_columna(campos['id'])} = %s"
            )

            cursor.execute(consulta, (empleado["id"],))
            conexion.commit()

            messagebox.showinfo(
                "Operación exitosa",
                "Empleado eliminado correctamente."
            )

            self._cargar_empleados()

        except Exception as error:
            if conexion and conexion.is_connected():
                conexion.rollback()

            messagebox.showerror(
                "Error",
                "No se pudo eliminar el empleado.\n\n"
                "Si tiene ventas asociadas, la base de datos "
                "puede impedir la eliminación.\n\n"
                f"Detalle: {error}"
            )

        finally:
            if cursor:
                cursor.close()

            if conexion and conexion.is_connected():
                conexion.close()
