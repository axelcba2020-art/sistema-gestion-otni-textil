from tkinter import ttk

class InicioFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.pack(fill="both", expand=True)
        self._crear_tarjetas()

    def _crear_tarjetas(self):
        centro = ttk.Frame(self)
        centro.pack(fill="both", expand=True, padx=10, pady=20)

        tarjetas = ttk.Frame(centro)
        tarjetas.pack(fill="both", expand=True)

        for columna, (titulo, valor) in enumerate((
            ("PRODUCTOS", 0),
            ("CLIENTES", 0),
            ("VENTAS", 0),
            ("STOCK BAJO", 0),
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
        