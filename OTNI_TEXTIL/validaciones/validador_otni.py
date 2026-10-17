# Módulo de Validaciones - OTNI Textil
# Encargada: Lorena Carballo

def validar_producto(nombre, precio, stock):
    """
    Valida que los datos del producto sean correctos antes de guardar.
    """
    if not nombre or not nombre.strip():
        return False, "El nombre del producto no puede estar vacío."
    
    try:
        precio_num = float(precio)
        if precio_num < 0:
            return False, "El precio no puede ser un valor negativo."
    except ValueError:
        return False, "El precio debe ser un número válido."
        
    try:
        stock_num = int(stock)
        if stock_num < 0:
            return False, "El stock no puede ser negativo."
    except ValueError:
        return False, "El stock debe ser un número entero."
        
    return True, "Producto válido."

def validar_cliente(nombre, apellido, dni):
    """
    Valida los datos ingresados para el cliente.
    """
    if not nombre or not nombre.strip():
        return False, "El nombre del cliente es obligatorio."
        
    if not apellido or not apellido.strip():
        return False, "El apellido del cliente es obligatorio."
        
    if not dni or not str(dni).isdigit():
        return False, "El DNI debe contener únicamente números."
        
    return True, "Cliente válido."
