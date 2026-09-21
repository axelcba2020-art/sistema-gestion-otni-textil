import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

def calcular_resumen_mensual(ventas, clientes, año, mes):
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
        "total_ventas": sum(float(venta.get("total", 0)) for venta in ventas_del_mes),
        "productos_vendidos": sum(
            int(venta.get("cantidad", 0)) for venta in ventas_del_mes
        ),
        "clientes_nuevos": len(clientes_del_mes),
    }


class ReportesFrame(ttk.Frame):
    def __init__(self, master, ventas=None, clientes=None):
        super().__init__(master)
        self.ventas = ventas if ventas is not None else []
        self.clientes = clientes if clientes is not None else []
        hoy = date.today()
        self.mes_var = tk.StringVar(value=f"{hoy.year:04d}-{hoy.month:02d}")
        self._crear_interfaz()


    def _crear_interfaz(self):
        encabezado = ttk.Frame(self, padding=16)
        encabezado.pack(fill="x")


        ttk.Label(encabezado, text="Resultados del mes").pack(side="left")
        ttk.Label(encabezado, text="Mes (AAAA-MM):").pack(side="left", padx=(24, 6))
        ttk.Entry(encabezado, textvariable=self.mes_var, width=10).pack(side="left")
        ttk.Button(encabezado, text="Actualizar", command=self._actualizar).pack(
            side="left", padx=8
        )


        self.resumen = ttk.Frame(self, padding=(16, 0))
        self.resumen.pack(fill="x")
        self.indicadores = {}
        for clave, titulo in (
            ("total_ventas", "TOTAL VENTAS"),
            ("productos_vendidos", "PRODUCTOS VENDIDOS"),
            ("clientes_nuevos", "CLIENTES NUEVOS"),
        ):
            tarjeta = ttk.LabelFrame(self.resumen, text=titulo, padding=16)
            tarjeta.pack(side="left", fill="both", expand=True, padx=5, pady=10)
            etiqueta = ttk.Label(tarjeta, font=("Arial", 14, "bold"))
            etiqueta.pack()
            self.indicadores[clave] = etiqueta


        self._actualizar()


    def _actualizar(self):
        try:
            año, mes = (int(parte) for parte in self.mes_var.get().strip().split("-"))
            if not 1 <= mes <= 12:
                raise ValueError
        except ValueError:
            for etiqueta in self.indicadores.values():
                etiqueta.configure(text="Formato inválido")
            return


        resumen = calcular_resumen_mensual(self.ventas, self.clientes, año, mes)
        self.indicadores["total_ventas"].configure(
            text=f"$ {resumen['total_ventas']:,.2f}"
        )
        self.indicadores["productos_vendidos"].configure(
            text=str(resumen["productos_vendidos"])
        )
        self.indicadores["clientes_nuevos"].configure(
            text=str(resumen["clientes_nuevos"])
        )