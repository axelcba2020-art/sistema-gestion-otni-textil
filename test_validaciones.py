# test_validaciones.py
# Pruebas unitarias para el Sistema de Gestión OTNI Textil

def validar_precio(precio):
    """Valida que el precio sea mayor a cero."""
    if isinstance(precio, (int, float)) and precio > 0:
        return True
    return False

def validar_stock(cantidad):
    """Valida que el stock sea un número entero no negativo."""
    if isinstance(cantidad, int) and cantidad >= 0:
        return True
    return False

# Pruebas de ejecución
if __name__ == "__main__":
    print("--- EJECUTANDO PRUEBAS DEL SISTEMA OTNI TEXTIL ---")
    
    # Prueba 1: Precio válido
    assert validar_precio(15000.0) == True, "Error: El precio válido falló"
    print("✔ Prueba 1: Validación de precio correcto PASADA")

    # Prueba 2: Precio inválido
    assert validar_precio(-500) == False, "Error: El precio negativo no fue rechazado"
    print("✔ Prueba 2: Rechazo de precio negativo PASADA")

    # Prueba 3: Stock válido
    assert validar_stock(10) == True, "Error: El stock válido falló"
    print("✔ Prueba 3: Validación de stock correcto PASADA")

    # Prueba 4: Stock inválido
    assert validar_stock(-5) == False, "Error: El stock negativo no fue rechazado"
    print("✔ Prueba 4: Rechazo de stock negativo PASADA")

    print("-------------------------------------------------")
    print("¡Todas las pruebas automatizadas se ejecutaron con éxito!")
