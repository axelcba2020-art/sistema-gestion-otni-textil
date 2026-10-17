
import tkinter as tk
import traceback
import sys
from pathlib import Path


# Agregar la carpeta principal OTNI_TEXTIL a la ruta de búsqueda.
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CARPETA_PROYECTO))

from gui.ventas import VentasFrame


def probar_pantalla_ventas():
    root = tk.Tk()
    root.withdraw()

    try:
        print("=" * 45)
        print("PRUEBA DE LA PANTALLA DE VENTAS")
        print("=" * 45)

        # Datos ficticios para probar la interfaz.
        clientes = [
            {
                "ID_Cliente": 1,
                "nombre": "Ana",
                "apellido": "Lopez"
            }
        ]

        productos = [
            {
                "ID_Producto": 1,
                "nombre": "Remera básica",
                "precio": 4200,
                "stock": 10
            }
        ]

        ventas = []

        # Empleado ficticio para comprobar la creación del formulario.
        usuario_actual = {
            "ID_Empleado": 1,
            "nombre": "Empleado de prueba",
            "apellido": "Test",
            "usuario": "prueba",
            "rol": "Empleado"
        }

        print("\nCreando la pantalla de ventas...")

        frame = VentasFrame(
            root,
            clientes=clientes,
            productos=productos,
            ventas=ventas,
            usuario_actual=usuario_actual
        )

        frame.update_idletasks()

        # Comprobar que el formulario se creó.
        elementos = frame.winfo_children()

        print("OK: La pantalla se creó correctamente.")
        print(f"Elementos del formulario: {len(elementos)}")
        print(f"Ventas en memoria: {len(ventas)}")

        # Verificar que el método de registro exista,
        # sin ejecutarlo.
        if callable(getattr(frame, "_registrar_venta", None)):
            print("OK: El método de registro de ventas existe.")
        else:
            print("ERROR: No se encontró _registrar_venta.")
            return False

        print("\nNo se registró ninguna venta.")
        print("No se modificó el stock.")
        print("La prueba no ejecutó operaciones de escritura en MySQL.")

        return True

    except Exception:
        print("\nERROR: Falló la prueba de la pantalla de ventas.")
        traceback.print_exc()
        return False

    finally:
        root.destroy()


if __name__ == "__main__":
    resultado = probar_pantalla_ventas()

    print("\n" + "=" * 45)

    if resultado:
        print("RESULTADO: PRUEBA SUPERADA")
    else:
        print("RESULTADO: PRUEBA FALLIDA")

    print("=" * 45)
