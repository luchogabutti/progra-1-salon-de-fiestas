import os
import json

ARCHIVO_CLIENTES = "clientes.json"
ARCHIVO_RESERVAS = "reservas.json"

clientes = []
reservas = []


def es_numero(cadena):
    """True si todos los caracteres son dígitos."""
    if len(cadena) == 0:
        return False
    for c in cadena:
        if c not in "0123456789":
            return False
    return True

def buscar_indice_por_id(lista, id_bus):
    """Devuelve el índice de la reserva con ese ID o -1 si no existe."""
    for i in range(len(lista)):
        if lista[i]["id"] == id_bus:
            return i
    return -1


def convertir_fecha(fecha_texto):
    """Convierte 'DD/MM/AAAA' o 'DD-MM-AAAA' a 'AAAA-MM-DD'."""
    fecha_texto = fecha_texto.replace("-", "/")
    partes = fecha_texto.split("/")
    if len(partes) != 3:
        return None
    if es_numero(partes[0]) and es_numero(partes[1]) and es_numero(partes[2]):
        dia = int(partes[0])
        mes = int(partes[1])
        anio = int(partes[2])
        if not (1 <= mes <= 12):
            return None
        if not (1 <= dia <= 31):
            return None
        if anio < 0:
            return None
        return f"{anio:04d}-{mes:02d}-{dia:02d}"
    else:
        return None


def generar_id_reserva():
    """Devuelve un ID incremental para reservas."""
    max_id = 0
    for r in reservas:
        if "id" in r and es_numero(str(r["id"])) and int(r["id"]) > max_id:
            max_id = int(r["id"])
    return max_id + 1


def existe_reserva_en_fecha(fecha_iso, excluir_id=None):
    """True si existe reserva en esa fecha (opcional: excluye una ID)."""
    for r in reservas:
        if r["fecha"] == fecha_iso:
            if excluir_id is None or r["id"] != excluir_id:
                return True
    return False


def guardar_clientes():
    """Guarda los clientes en un archivo JSON."""
    with open(ARCHIVO_CLIENTES, "w") as f:
        json.dump(clientes, f)


def cargar_clientes():
    """Carga los clientes desde un archivo JSON si existe."""
    if not os.path.exists(ARCHIVO_CLIENTES):
        return []
    try:
        with open(ARCHIVO_CLIENTES, "r") as f:
            data = json.load(f)
            if type(data) is list:
                return data
            else:
                return []
    except:
        return []


def guardar_reservas():
    """Guarda las reservas en un archivo JSON."""
    with open(ARCHIVO_RESERVAS, "w") as f:
        json.dump(reservas, f)


def cargar_reservas():
    """Carga las reservas desde un archivo JSON si existe."""
    if not os.path.exists(ARCHIVO_RESERVAS):
        return []
    try:
        with open(ARCHIVO_RESERVAS, "r") as f:
            data = json.load(f)
            if type(data) is list:
                return data
            else:
                return []
    except:
        return []


def nuevo_cliente(nombre, dni):
    """Registra un nuevo cliente en la estructura 'clientes'."""
    if not es_numero(dni):
        print("\n¡Error! El DNI debe ser un número. Volviendo al menú principal...")
        return
    for c in clientes:
        if c["dni"] == dni:
            print("\n¡Error! Ya existe un cliente con ese DNI.")
            return
    clientes.append({"nombre": nombre.strip(), "dni": dni.strip()})
    guardar_clientes()
    print("\nCliente registrado con éxito y guardado en archivo json.")


def listar_clientes():
    """Muestra la lista completa de clientes."""
    if not clientes:
        print("\nNo hay clientes registrados. Volviendo al menu principal...")
    else:
        print("\nLista de clientes:")
        for c in clientes:
            print("Nombre:", c["nombre"], "- DNI:", c["dni"])


menu_opciones = {"1": "Infantil", "2": "Adultos", "3": "Premium"}
musica_opciones = {"1": "DJ", "2": "Banda", "3": "Playlist personalizada"}
servicios_opciones = {
    "1": "Decoracion tematica",
    "2": "Fotografia",
    "3": "Animacion",
    "4": "Cotillon"
}


def registrar_reserva():
    """Registra una nueva reserva con menú, música y servicios."""
    print("\nRegistrar reserva")
    nombre = input("Nombre del cliente: ").strip()
    tipo = input("Tipo de fiesta: ").strip()
    fecha_texto = input("Fecha (DD/MM/AAAA): ").strip()

    fecha_iso = convertir_fecha(fecha_texto)
    if fecha_iso is None:
        print("\nFormato de fecha inválido. Usar DD/MM/AAAA (ej: 18/09/2023).")
        return

    if existe_reserva_en_fecha(fecha_iso):
        print("No se puede reservar: ya existe una reserva en esa fecha.")
        return

    print("\nMenús disponibles:")
    for k, v in menu_opciones.items():
        print(f"{k}. {v}")
    sel_menu = input("Seleccione menú: ").strip()
    menu = menu_opciones.get(sel_menu, "Sin definir")

    print("\nMúsica disponible:")
    for k, v in musica_opciones.items():
        print(f"{k}. {v}")
    sel_musica = input("Seleccione música: ").strip()
    musica = musica_opciones.get(sel_musica, "Sin definir")

    print("\nServicios adicionales (separe por coma, o ENTER para ninguno):")
    for k, v in servicios_opciones.items():
        print(f"{k}. {v}")
    sel_serv = input("Seleccione: ").strip()
    servicios = []
    if sel_serv != "":
        partes = sel_serv.split(",")
        for p in partes:
            clave = p.strip()
            if clave in servicios_opciones:
                servicios.append(servicios_opciones[clave])

    reserva = {
        "id": generar_id_reserva(),
        "nombre": nombre,
        "tipo": tipo,
        "fecha": fecha_iso,
        "menu": menu,
        "musica": musica,
        "servicios": servicios
    }
    reservas.append(reserva)
    guardar_reservas()
    print("\nReserva registrada con éxito.")


def listar_reservas():
    """Muestra la lista de reservas."""
    if not reservas:
        print("\nNo hay reservas registradas. Volviendo al menu principal...")
    else:
        print("\nLista de reservas")
        reservitas = reservas[:]
        reservitas.sort(key=lambda x: x["fecha"])
        for r in reservitas:
            serv_txt = ", ".join(r["servicios"]) if r["servicios"] else "Ninguno"
            print(f"ID {r['id']} - Cliente: {r['nombre']} - Fiesta: {r['tipo']} - Fecha: {r['fecha']} - Menú: {r['menu']} - Música: {r['musica']} - Servicios: {serv_txt}")


def modificar_reserva():
    """Modifica una reserva por ID."""
    listar_reservas()
    if not reservas:
        return 

    try:
        id_sel = int(input("\nID de la reserva a modificar: ").strip())
    except ValueError:
        print("ID inválido. Debe ingresar un numero entero.")
        return

    objetivo = None
    for r in reservas:
        if r["id"] == id_sel:
            objetivo = r
            break

    if objetivo is None:
        print("No se encontró la reserva.")
        return

    print("Deje vacío para mantener el valor anterior.")
    nuevo_tipo = input(f"Tipo de fiesta ({objetivo['tipo']}): ").strip()
    if nuevo_tipo != "":
        objetivo["tipo"] = nuevo_tipo

    nueva_fecha = input(f"Fecha ({objetivo['fecha']}) - DD/MM/AAAA: ").strip()
    if nueva_fecha != "":
        nueva_iso = convertir_fecha(nueva_fecha)
        if nueva_iso is None:
            print("Formato inválido, se mantiene la fecha anterior.")
        else:
            if existe_reserva_en_fecha(nueva_iso, excluir_id=objetivo["id"]):
                print("Esa fecha ya está ocupada.")
            else:
                objetivo["fecha"] = nueva_iso

    cambiar_menu = input("¿Cambiar menú? (s/N): ").strip().lower()
    if cambiar_menu == "s":
        print("\nMenús disponibles:")
        for k, v in menu_opciones.items():
            print(f"{k}. {v}")
        sel = input("Seleccione menú: ").strip()
        objetivo["menu"] = menu_opciones.get(sel, objetivo["menu"])

    cambiar_musica = input("¿Cambiar música? (s/N): ").strip().lower()
    if cambiar_musica == "s":
        print("\nMúsica disponible:")
        for k, v in musica_opciones.items():
            print(f"{k}. {v}")
        sel = input("Seleccione música: ").strip()
        objetivo["musica"] = musica_opciones.get(sel, objetivo["musica"])

    cambiar_servicios = input("¿Cambiar servicios? (s/N): ").strip().lower()
    if cambiar_servicios == "s":
        print("\nServicios adicionales (separe por coma, o ENTER para ninguno):")
        for k, v in servicios_opciones.items():
            print(f"{k}. {v}")
        sel = input("Seleccione: ").strip()
        nuevos = []
        if sel != "":
            partes = sel.split(",")
            for p in partes:
                clave = p.strip()
                if clave in servicios_opciones:
                    nuevos.append(servicios_opciones[clave])
        objetivo["servicios"] = nuevos

    guardar_reservas()
    print("Reserva modificada con éxito.")


def eliminar_reserva():
    """Elimina una reserva por ID."""
    listar_reservas()
    if not reservas:
        return

    try:
        id_sel = int(input("\nID de la reserva a eliminar: ").strip())
    except ValueError:
        print("ID inválido. Debe ingresar un numero entero.")
        return

    idx = buscar_indice_por_id(reservas, id_sel)
    if idx == -1:
        print("No se encontró la reserva.")
        return

    print(f"Se eliminará la reserva ID {reservas[idx]['id']} de {reservas[idx]['nombre']} en {reservas[idx]['fecha']}.")
    conf = input("Confirmar (ELIMINAR): ").strip()
    if conf == "ELIMINAR":
        reservas.pop(idx)
        guardar_reservas()
        print("Reserva eliminada con éxito.")
    else:
        print("Operación cancelada.")


def menu():
    """Menú principal del sistema."""
    global clientes, reservas

    clientes_cargados = cargar_clientes()
    clientes = clientes_cargados
    reservas_cargadas = cargar_reservas()
    reservas = reservas_cargadas


    while True:
        print("\nSistema de Gestión del Salón de Fiestas ")
        print("\nMenú principal:")
        print("\n1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Registrar reserva")
        print("4. Listar reservas")
        print("5. Modificar reserva")
        print("6. Eliminar reserva")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            nombre = input("\nIngrese el nombre y apellido: ")
            dni = input("Ingrese el DNI: ")
            nuevo_cliente(nombre, dni)
        elif opcion == "2":
            listar_clientes()
        elif opcion == "3":
            registrar_reserva()
        elif opcion == "4":
            listar_reservas()
        elif opcion == "5":
            modificar_reserva()
        elif opcion == "6":
            eliminar_reserva()
        elif opcion == "0":
            print("\n¡Gracias por usar el sistema, hasta la próxima!")
            return False
        else:
            print("\nOpción inválida, intente de nuevo.")


if __name__ == "__main__":
    menu()
