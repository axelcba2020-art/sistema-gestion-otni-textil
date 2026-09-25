import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from gui.clientes import ClientesFrame
from gui.stock import StockFrame

class VentasFrame(ttk.Frame):
    def __init__(self, master, clientes, productos, ventas):
        super().__init__(master)

        self.clientes = clientes if clientes is not None else [
            {"nombre": "Juan", "apellido": "Perez", "dni": "32.456.789"}
        ]
        self.productos = productos if productos is not None else [
            {"nombre": "Remera básica", "precio": 4200, "stock": 28},
            {"nombre": "Pantalón cargo", "precio": 6800, "stock": 14},
        ]
        self.ventas = ventas if ventas is not None else[]
        self.lineas = []
        self.pack(fill="both", expand=True)

        self._crear_formulario()
        self._crear_tabla()
        self._crear_acciones()

    def _nombre_cliente(self, cliente):
        return f"{cliente.get('nombre', '')} {cliente.get('apellido', '')}".strip()

    def _producto_por_nombre(self, nombre):
        for producto in self.productos:
            if producto.get("nombre") == nombre:
                return producto
        return None

    def _crear_formulario(self):
        formulario = ttk.LabelFrame(self, text="Nueva venta", padding=10)
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.cliente_var = tk.StringVar()
        clientes = [self._nombre_cliente(cliente) for cliente in self.clientes]
        self.cliente_combo = ttk.Combobox(
            formulario,
            textvariable=self.cliente_var,
            values=clientes,
            state="readonly",
            width=28,
        )
        self.cliente_combo.grid(row=0, column=1, padx=10, pady=10)
        if clientes:
            self.cliente_combo.set(clientes[0])

        ttk.Label(formulario, text="Producto:").grid(row=0, column=2, sticky="w")
        self.producto_var = tk.StringVar()
        productos = [producto.get("nombre", "") for producto in self.productos]
        self.producto_combo = ttk.Combobox(
            formulario,
            textvariable=self.producto_var,
            values=productos,
            state="readonly",
            width=20,
        )
        self.producto_combo.grid(row=0, column=3, padx=10, pady=10)
        if productos:
            self.producto_combo.set(productos[0])

        ttk.Label(formulario, text="Cantidad:").grid(row=0, column=4, sticky="w")
        self.cantidad_var = tk.StringVar(value="1")
        ttk.Spinbox(
            formulario,
            from_=1,
            to=999,
            textvariable=self.cantidad_var,
            width=6,
        ).grid(row=0, column=5, padx=10, pady=10)

    def _crear_tabla(self):
        marco = ttk.Frame(self)
        marco.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("CLIENTE", "PRODUCTO", "CANTIDAD", "TOTAL")
        self.tree = ttk.Treeview(marco, columns=columnas, show="headings", height=10)
        self.tree.pack(side="left", fill="both", expand=True)

        for columna in columnas:
            self.tree.heading(columna, text=columna)
            self.tree.column(columna, anchor="center", width=140)

        scrollbar = ttk.Scrollbar(marco, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.lbl_vacio = ttk.Label(
            marco,
            text="Todavía no hay ventas registradas",
            justify="center",
            foreground="#666666",
        )
        self.lbl_vacio.place(relx=0.5, rely=0.5, anchor="center")

    def _crear_acciones(self):
        acciones = ttk.Frame(self)
        acciones.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(acciones, text="Registrar venta", command=self._registrar_venta).pack(side="left")
        ttk.Button(acciones, text="Quitar venta", command=self._quitar_venta).pack(side="left", padx=(8, 0))

    def _registrar_venta(self):
        cliente_nombre = self.cliente_var.get().strip()
        producto_nombre = self.producto_var.get().strip()
        cantidad_val = self.cantidad_var.get().strip()

        if not cliente_nombre or not producto_nombre:
            messagebox.showwarning("Datos incompletos", "Seleccioná un cliente y un producto.")
            return

        try:
            cantidad = int(cantidad_val)
        except ValueError:
            messagebox.showwarning("Cantidad inválida", "La cantidad debe ser un número entero.")
            return

        producto = self._producto_por_nombre(producto_nombre)
        if producto is None:
            messagebox.showerror("Producto no encontrado", "No se encontró el producto seleccionado.")
            return

        stock_actual = int(producto.get("stock", 0))
        if cantidad > stock_actual:
            messagebox.showwarning("Stock insuficiente", f"Solo hay {stock_actual} unidades disponibles.")
            return

        self.ventas.append({
            "fecha": date.today().isoformat(),
            "cliente": cliente_nombre,
            "producto": producto_nombre,
            "cantidad": cantidad,
            "precio_unitario": float(producto.get("precio", 0)),
            "total": float(producto.get("precio", 0)) * cantidad
        })
        self._actualizar_tabla()

    def _quitar_venta(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Seleccioná una venta para quitarla.")
            return

        item = seleccion[0]
        item_id = self.tree.index(item)
        self.ventas.pop(item_id)
        self._actualizar_tabla()

    def _actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.ventas:
            self.lbl_vacio.place(relx=0.5, rely=0.5, anchor="center")
            return

        self.lbl_vacio.place_forget()
        for venta in self.ventas:
            self.tree.insert(
                "",
                "end",
                values=(
                    venta["cliente"],
                    venta["producto"],
                    venta["cantidad"],
                    f"$ {venta['total']:,.2f}",
                ),
            )

