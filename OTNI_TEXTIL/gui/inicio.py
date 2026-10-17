
from tkinter import ttk
import traceback

from database import obtener_conexion


class InicioFrame(ttk.Frame):
    def __init__(self, master, productos=None, clientes=None, ventas=None):
        super().__init__(master)

        self.productos = productos if productos is not None else []
        self.clientes = clientes if clientes is not None else []
        self.ventas = ventas if ventas is not None else []

        self.pack(fill="both", expand=True)

        self.valores = {}
        self._crear_tarjetas()
        self.actualizar_estadisticas()

    def _crear_tarjetas(self):
        centro = ttk.Frame(self)
        centro.pack(fill="both", expand=True, padx=10, pady=20)

        tarjetas = ttk.Frame(centro)
        tarjetas.pack(fill="both", expand=True)

        nombres = (
            "PRODUCTOS",
            "CLIENTES",
            "VENTAS",
            "STOCK BAJO",
        )

        for columna, titulo in enumerate(nombres):
            tarjeta = ttk.LabelFrame(
                tarjetas,
                text=titulo,
                padding=15,
            )

            tarjeta.grid(
                row=0,
                column=columna,
                sticky="nsew",
                padx=5,
                pady=5,
            )

            tarjetas.columnconfigure(columna, weight=1)

            etiqueta_valor = ttk.Label(
                tarjeta,
                text="...",
                font=("Arial", 12, "bold"),
            )
            etiqueta_valor.pack(padx=10, pady=10)

            self.valores[titulo] = etiqueta_valor

    def actualizar_estadisticas(self):
        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            consultas = {
                "PRODUCTOS": "SELECT COUNT(*) AS total FROM Producto",
                "CLIENTES": "SELECT COUNT(*) AS total FROM Cliente",
                "VENTAS": "SELECT COUNT(*) AS total FROM Venta",
            }

            for tarjeta, consulta in consultas.items():
                cursor.execute(consulta)
                resultado = cursor.fetchone()

                self.valores[tarjeta].configure(
                    text=str(resultado["total"])
                )

            cursor.execute("SHOW COLUMNS FROM Producto")
            columnas = {
                fila["Field"].lower(): fila["Field"]
                for fila in cursor.fetchall()
            }

            posibles_stock = (
                "stock",
                "stock_actual",
                "cantidad",
                "existencias",
            )

            columna_stock = next(
                (
                    columnas[nombre]
                    for nombre in posibles_stock
                    if nombre in columnas
                ),
                None,
            )

            if columna_stock is None:
                self.valores["STOCK BAJO"].configure(text="N/D")
                print("No se encontró la columna de stock en Producto.")
                return

            posibles_minimos = (
                "stock_minimo",
                "stock_min",
                "cantidad_minima",
                "minimo",
            )

            columna_minimo = next(
                (
                    columnas[nombre]
                    for nombre in posibles_minimos
                    if nombre in columnas
                ),
                None,
            )

            stock_sql = f"`{columna_stock}`"

            if columna_minimo is not None:
                minimo_sql = f"`{columna_minimo}`"

                consulta_stock = f"""
                    SELECT COUNT(*) AS total
                    FROM Producto
                    WHERE {stock_sql} <= {minimo_sql}
                """

                cursor.execute(consulta_stock)

            else:
                consulta_stock = f"""
                    SELECT COUNT(*) AS total
                    FROM Producto
                    WHERE {stock_sql} <= %s
                """

                cursor.execute(consulta_stock, (5,))

            resultado = cursor.fetchone()

            self.valores["STOCK BAJO"].configure(
                text=str(resultado["total"])
            )

        except Exception:
            print("Error al cargar las estadísticas del menú:")
            traceback.print_exc()

            for etiqueta in self.valores.values():
                etiqueta.configure(text="N/D")

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()
