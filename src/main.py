listaCliente = []
documentoCliente = []
reservas = []
MIN_SEPARACION_DIAS = 1


def es_numero(cadena):
    """True si todos los caracteres son dígitos"""
    if len(cadena) == 0:
        return False
    for c in cadena:
        if c not in "0123456789":
            return False
    return True


def nuevo_cliente(nombre, dni):
    """Registra un nuevo cliente"""
    if not es_numero(dni):
        """validamos que el el DNI ingresado sea un numero"""
        print("\n¡Error! El DNI debe ser un número. Redirigiendo al menú principal...")
        return
    listaCliente.append(nombre)
    documentoCliente.append(dni)
    print("\nCliente registrado con éxito.")


def listar_clientes():
    """Muestra la lista de clientes"""
    if len(listaCliente) == 0:
        print("No hay clientes registrados.")
    else:
        print("\nLista de clientes:")
        for i in range(len(listaCliente)):
            print("Nombre:", listaCliente[i], "- DNI:", documentoCliente[i])


def convertir_fecha(fecha_texto):
    """Convierte 'DD/MM/AAAA' o 'DD-MM-AAAA' a [dia, mes, anio]"""
    fecha_texto = fecha_texto.replace("-", "/")
    partes = fecha_texto.split("/")
    if len(partes) != 3:
        return None
    if es_numero(partes[0]) and es_numero(partes[1]) and es_numero(partes[2]):
        dia = int(partes[0])
        mes = int(partes[1])
        anio = int(partes[2])
        return [dia, mes, anio]
    else:
        return None


def diferencia_dias(fecha1, fecha2):
    """Devuelve la diferencia de días entre dos fechas"""
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    total1 = fecha1[2] * 365 + sum(dias_por_mes[:fecha1[1]-1]) + fecha1[0]
    total2 = fecha2[2] * 365 + sum(dias_por_mes[:fecha2[1]-1]) + fecha2[0]
    return total1 - total2


def fecha_disponible(fecha_nueva):
    """Verifica si la fecha está libre"""
    for r in reservas:
        fecha_existente = [r[2], r[3], r[4]]
        dif = diferencia_dias(fecha_nueva, fecha_existente)
        if -MIN_SEPARACION_DIAS < dif < MIN_SEPARACION_DIAS:
            return False
    return True


def registrar_reserva():
    """Registra una nueva reserva"""
    print("\nRegistrar reserva")
    nombre = input("Nombre del cliente: ")
    tipo = input("Tipo de fiesta: ")
    fecha_texto = input("Fecha (DD/MM/AAAA): ")
    fecha = convertir_fecha(fecha_texto)

    if fecha is None:
        print("\nFormato de fecha inválido. Usar DD/MM/AAAA (ej: 18/09/2023).")
        return
    dia, mes, anio = fecha[0], fecha[1], fecha[2]
    if mes < 1 or mes > 12:
        print("\nError: El mes debe estar entre 1 y 12 inclusive.")
        return
    if dia <= 1 or dia >= 31:
        print("\nError: El día debe estar entre 1 y 31 inclusive.")
        return
    if anio < 0:
        print("\nError: El año no puede ser negativo.")
        return

    if fecha_disponible(fecha):
        reservas.append([nombre, tipo, dia, mes, anio])
        print("\nReserva registrada con éxito.")
    else:
        print("No se puede reservar: deben pasar al menos",
              MIN_SEPARACION_DIAS, "día(s) entre eventos.")


def listar_reservas():
    """Muestra la lista de reservas"""
    if len(reservas) == 0:
        print("No hay reservas registradas.")
    else:
        print("\nLista de reservas")
        for r in reservas:
            print("Cliente: ", r[0], " - Fiesta: ", r[1],
                  " - Fecha: ", r[2], "/", r[3], "/", r[4], sep="")


def menu():
    """Menú principal"""
    while True:
        print("\nSistema de Gestión del Salón de Fiestas ")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Registrar reserva")
        print("4. Listar reservas")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre y apellido: ")
            dni = input("DNI: ")
            nuevo_cliente(nombre, dni)
        elif opcion == "2":
            listar_clientes()
        elif opcion == "3":
            registrar_reserva()
        elif opcion == "4":
            listar_reservas()
        elif opcion == "0":
            print("¡Gracias por usar el sistema, hasta la próxima!")
            return False
        else:
            print("\nOpción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()
