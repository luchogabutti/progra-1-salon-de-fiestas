def menu():
    while True:
        print("\n--- Sistema de Gestión - Salón de Fiestas ---")
        print("1. Registrar reserva")
        print("2. Listar reservas")
        print("3. Modificar reserva")
        print("4. Cancelar reserva")
        print("5. Generar reporte")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print(" Aquí iría la lógica para registrar una reserva")
        elif opcion == "2":
            print(" Aquí iría la lógica para listar reservas")
        elif opcion == "3":
            print(" Aquí iría la lógica para modificar una reserva")
        elif opcion == "4":
            print(" Aquí iría la lógica para cancelar una reserva")
        elif opcion == "5":
            print(" Aquí iría la lógica para generar un reporte")
        elif opcion == "0":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()
