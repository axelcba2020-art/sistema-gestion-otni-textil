import tkinter as tk
from logica.clientes import guardar_cliente, listar_clientes

def abrir_ventana():
    ventana = tk.Tk()
    ventana.title("OTNI TEXTIL - Sistema")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Sistema OTNI TEXTIL").pack(pady=10)

    entrada = tk.Entry(ventana)
    entrada.pack()

    def guardar():
        nombre = entrada.get()
        if guardar_cliente(nombre):
            print("Cliente guardado")
            entrada.delete(0, tk.END)

      tk.Button(ventana, text="Guardar Cliente", command=guardar).pack(pady=5)
      tk.Button(ventana, text="Ver Clientes", command=lambda: print(listar_clientes())).pack(pady=5)

      ventana.mainloop()

if __name__ == "__main__":
    abrir_ventana()
