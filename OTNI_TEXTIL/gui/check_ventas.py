import tkinter as tk
from gui.ventas import VentasFrame

root = tk.Tk()
root.withdraw()
frame = VentasFrame(root, [{"nombre": "Ana", "apellido": "Lopez"}], [{"nombre": "Remera básica", "precio": 4200, "stock": 10}])
print('FRAME_OK', len(frame.winfo_children()))
print('FORM_COUNT', sum(1 for child in frame.winfo_children() if child.winfo_exists()))
frame._registrar_venta()
print('VENTAS', len(frame.ventas))
root.update()
root.destroy()
