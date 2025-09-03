clientes = []
contador_clientes = 1  # ID único para cada cliente

def registrar_cliente():
    global contador_clientes
    print("\n--- Registro de Cliente ---")
    nombre = input("Nombre completo: ")
    dni = input("DNI: ")

    for cliente in clientes:
        if cliente['dni'] == dni:
            print("Cliente ya registrado.")
            return

    cliente = {
        "id": contador_clientes,
        "nombre": nombre,
        "dni": dni
    }

    clientes.append(cliente)
    print(f"✅ Cliente registrado con éxito. ID asignado: {contador_clientes}")
    contador_clientes += 1

registrar_cliente()