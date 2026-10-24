# test_sistema.py
# Módulo de pruebas y validaciones de datos para OTNI Textil

def validar_precio(precio):
    """Valida que el precio sea mayor a cero."""
    try:
        val = float(precio)
        return val > 0
    except (ValueError, TypeError):
        return False

def validar_stock(cantidad):
    """Valida que el stock sea un entero no negativo."""
    try:
        val = int(cantidad)
        return val >= 0
    except (ValueError, TypeError):
        return False

def validar_codigo_producto(codigo):
    """Valida que el código no esté vacío."""
    if isinstance(codigo, str) and codigo.strip():
        return True
    return False

# Ejecución de casos de prueba
if __name__ == "__main__":
    print("==================================================")
    print("   EJECUCIÓN DE PRUEBAS - SISTEMA OTNI TEXTIL   ")
    print("==================================================")
    
    # 1. Prueba de Precios
    assert validar_precio(15000.0) == True, "Error en precio válido"
    assert validar_precio(-500) == False, "Error en precio negativo"
    print("✔ [PASADO] Validación de Precios")

    # 2. Prueba de Stock
    assert validar_stock(25) == True, "Error en stock válido"
    assert validar_stock(-2) == False, "Error en stock negativo"
    print("✔ [PASADO] Validación de Stock")

    # 3. Prueba de Código de Producto
    assert validar_codigo_producto("PROD-001") == True, "Error en código de producto"
    assert validar_codigo_producto("") == False, "Error en código vacío"
    print("✔ [PASADO] Validación de Códigos de Producto")

    print("--------------------------------------------------")
    print("¡Todas las pruebas unitarias se ejecutaron con éxito!")
    print("==================================================")
