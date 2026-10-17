
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from database import obtener_conexion
from mysql.connector import Error


def calcular_resumen_mensual(ventas, clientes, año, mes):
    """Mantiene la función original por compatibilidad con el proyecto."""
    prefijo = f"{año:04d}-{mes:02d}"

    ventas_del_mes = [
        venta for venta in ventas
        if str(venta.get("fecha", "")).startswith(prefijo)
    ]

    clientes_del_mes = [
        cliente for cliente in clientes
        if str(cliente.get("fecha_alta", "")).startswith(prefijo)
    ]

    return {
        "total_ventas": sum(
            float(venta.get("total", 0))
            for venta in ventas_del_mes
        ),
        "productos_vendidos": sum(
            int(venta.get("cantidad", 0))
            for venta in ventas_del_mes
        ),
        "clientes_nuevos": len(clientes_del_mes),
    }


class ReportesFrame(ttk.Frame):
    def __init__(self, master, ventas=None, clientes=None):
        super().__init__(master)

        self.pack(fill="both", expand=True)

        hoy = date.today()
        self.mes_var = tk.StringVar(
            value=f"{hoy.year:04d}-{hoy.month:02d}"
        )

        self._crear_interfaz()

    def _crear_interfaz(self):
        encabezado = ttk.Frame(self, padding=16)
        encabezado.pack(fill="x")

        ttk.Label(
            encabezado,
            text="Resultados del mes",
            font=("Arial", 12, "bold")
        ).pack(side="left")

        ttk.Label(
            encabezado,
            text="Mes (AAAA-MM):"
        ).pack(side="left", padx=(24, 6))

        ttk.Entry(
            encabezado,
            textvariable=self.mes_var,
            width=10
        ).pack(side="left")

        ttk.Button(
            encabezado,
            text="Actualizar",
            cursor="hand2",
            command=self._actualizar
        ).pack(side="left", padx=8)

        self.resumen = ttk.Frame(self, padding=(16, 0))
        self.resumen.pack(fill="x")

        self.indicadores = {}

        for clave, titulo in (
            ("total_ventas", "TOTAL VENTAS"),
            ("productos_vendidos", "PRODUCTOS VENDIDOS"),
            ("clientes_nuevos", "CLIENTES NUEVOS"),
        ):
            tarjeta = ttk.LabelFrame(
                self.resumen,
                text=titulo,
                padding=16
            )
            tarjeta.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5,
                pady=10
            )

            etiqueta = ttk.Label(
                tarjeta,
                text="Cargando...",
                font=("Arial", 14, "bold")
            )
            etiqueta.pack()

            self.indicadores[clave] = etiqueta

        self._actualizar()

    def _actualizar(self):
        texto_mes = self.mes_var.get().strip()

        try:
            if (
                len(texto_mes) != 7
                or texto_mes[4] != "-"
            ):
                raise ValueError

            año = int(texto_mes[:4])
            mes = int(texto_mes[5:7])

            if año < 1 or not 1 <= mes <= 12:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Mes inválido",
                "Ingresá un mes válido con el formato AAAA-MM.\n"
                "Por ejemplo: 2026-10.",
                parent=self
            )
            return

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # Total de ventas registradas durante el mes.
            cursor.execute(
                """
                SELECT COALESCE(SUM(Total), 0)
                FROM Venta
                WHERE Fecha >= %s
                  AND Fecha < %s
                """,
                (
                    f"{año:04d}-{mes:02d}-01",
                    self._primer_dia_mes_siguiente(año, mes)
                )
            )

            total_ventas = float(cursor.fetchone()[0] or 0)

            # Cantidad total de unidades vendidas en el mes.
            cursor.execute(
                """
                SELECT COALESCE(SUM(dv.Cantidad), 0)
                FROM Detalle_Venta dv
                INNER JOIN Venta v
                    ON v.ID_Venta = dv.ID_Venta
                WHERE v.Fecha >= %s
                  AND v.Fecha < %s
                """,
                (
                    f"{año:04d}-{mes:02d}-01",
                    self._primer_dia_mes_siguiente(año, mes)
                )
            )

            productos_vendidos = int(cursor.fetchone()[0] or 0)

            # Clientes creados durante el mes.
            # La tabla actual no tiene una fecha de alta,
            # por lo que no es posible calcular este indicador
            # de forma histórica con los datos existentes.
            cursor.execute("""
                SHOW COLUMNS FROM Cliente LIKE 'Fecha_Alta'
            """)

            tiene_fecha_alta = cursor.fetchone() is not None

            if tiene_fecha_alta:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM Cliente
                    WHERE Fecha_Alta >= %s
                      AND Fecha_Alta < %s
                    """,
                    (
                        f"{año:04d}-{mes:02d}-01",
                        self._primer_dia_mes_siguiente(año, mes)
                    )
                )

                clientes_nuevos = int(cursor.fetchone()[0] or 0)
            else:
                clientes_nuevos = None

            self.indicadores["total_ventas"].configure(
                text=f"$ {total_ventas:,.2f}"
            )

            self.indicadores["productos_vendidos"].configure(
                text=str(productos_vendidos)
            )

            self.indicadores["clientes_nuevos"].configure(
                text=(
                    str(clientes_nuevos)
                    if clientes_nuevos is not None
                    else "No disponible"
                )
            )

        except Error as error:
            messagebox.showerror(
                "Error de base de datos",
                f"No se pudieron generar los reportes.\n\n{error}",
                parent=self
            )

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()

    @staticmethod
    def _primer_dia_mes_siguiente(año, mes):
        if mes == 12:
            return f"{año + 1:04d}-01-01"

        return f"{año:04d}-{mes + 1:02d}-01"
