from tkinter import ttk

class InicioFrame(ttk.Frame):
    def __init__(self, master, productos=None, clientes=None, ventas=None ):
        super().__init__(master)

        self.productos = productos if productos is not None else []
        self.clientes = clientes if clientes is not None else []
        self.ventas = ventas if ventas is not None else []

        self.pack(fill="both", expand=True)
        self._crear_tarjetas()

    def _crear_tarjetas(self):
        centro = ttk.Frame(self)
        centro.pack(fill="both", expand=True, padx=10, pady=20)

        tarjetas = ttk.Frame(centro)
        tarjetas.pack(fill="both", expand=True)

        stock_bajo = sum(
            int(producto.get("stock", 0)) < 10
            for producto in self.productos
        )

        for columna, (titulo, valor) in enumerate((
            ("PRODUCTOS", len(self.productos)),
            ("CLIENTES", len(self.clientes)),
            ("VENTAS", len(self.ventas)),
            ("STOCK BAJO", stock_bajo),
        )):
            tarjeta = ttk.LabelFrame(
                tarjetas,
                text=titulo,
                padding=15,
            )
            tarjeta.grid(row=0, column=columna, sticky="nsew", padx=5, pady=5)
            tarjetas.columnconfigure(columna, weight=1)

            ttk.Label(
                tarjeta,
                text=str(valor),
                font=("arial", 12, "bold"),
            ).pack(padx=10, pady=10)
        