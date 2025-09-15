listaCliente = []
documentoCliente = []

# Registro de nuevos clientes
def nuevo_cliente(nombre, dni):
    listaCliente.append(nombre)
    documentoCliente.append(dni)
    print("Cliente registrado con éxito.")

def listar_clientes():
    if len(listaCliente) == 0:
        print("No hay clientes registrados.")
    else:
        print("\n--- Lista de clientes ---")
        for i in range(len(listaCliente)):
            print("Nombre:", listaCliente[i], "- DNI:", documentoCliente[i])

#Menú principal
def menu():
    while True:
        print("\n--- Sistema de Gestión del Salón de Fiestas ---")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre y apellido: ")
            dni = input("DNI: ")
            nuevo_cliente(nombre, dni)
        elif opcion == "2":
            listar_clientes()
        elif opcion == "0":
            print("\n¡Gracias por usar el sistema, hasta la próxima!")
            break
        else:
            print("\nOpción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()
