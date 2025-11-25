import os
import json
from datetime import datetime
from opciones import menu_opciones, musica_opciones, servicios_opciones

ARCHIVO_CLIENTES = "clientes.json"
ARCHIVO_RESERVAS = "reservas.json"


def es_numero(cadena):
    """True si todos los caracteres son dígitos."""
    if len(cadena) == 0:
        return False
    for c in cadena:
        if c not in "0123456789":
            return False
    return True


def contiene_numeros(cadena):
    """True si la cadena contiene al menos un digito."""
    for c in cadena:
        if c in "0123456789":
            return True
    return False

def buscar_indice_por_id(lista, id_bus):
    """Devuelve el índice de la reserva con ese ID o -1 si no existe."""
    for i in range(len(lista)):
        if lista[i]["id"] == id_bus:
            return i
    return -1


def convertir_fecha(fecha_texto):
    """Convierte 'DD/MM/AAAA' o 'DD-MM-AAAA' a 'AAAA-MM-DD' usando datetime."""
    try:
        fecha = datetime.strptime(fecha_texto, "%d/%m/%Y")
        return fecha.strftime("%Y-%m-%d")
    except ValueError:
        try:
            fecha = datetime.strptime(fecha_texto, "%d-%m-%Y")
            return fecha.strftime("%Y-%m-%d")
        except ValueError:
            return None


def generar_id_reserva(reservas):
    """Devuelve un ID incremental para reservas."""
    max_id = 0
    for r in reservas:
        if "id" in r and es_numero(str(r["id"])) and int(r["id"]) > max_id:
            max_id = int(r["id"])
    return max_id + 1


def existe_reserva_en_fecha(reservas, fecha_iso, excluir_id=None):
    """True si existe reserva en esa fecha (opcional: excluye una ID)."""
    for r in reservas:
        if r["fecha"] == fecha_iso:
            if excluir_id is None or r["id"] != excluir_id:
                return True
    return False


def guardar_clientes(clientes, archivo):
    """Guarda los clientes en un archivo JSON."""
    with open(archivo, "w") as f:
        json.dump(clientes, f)


def cargar_clientes(archivo):
    """Carga los clientes desde un archivo JSON si existe."""
    if not os.path.exists(archivo):
        return []
    try:
        with open(archivo, "r") as f:
            data = json.load(f)
            if type(data) is list:
                return data
            else:
                return []
    except:
        return []


def guardar_reservas(reservas, archivo):
    """Guarda las reservas en un archivo JSON."""
    with open(archivo, "w") as f:
        json.dump(reservas, f)


def cargar_reservas(archivo):
    """Carga las reservas desde un archivo JSON si existe."""
    if not os.path.exists(archivo):
        return []
    try:
        with open(archivo, "r") as f:
            data = json.load(f)
            if type(data) is list:
                return data
            else:
                return []
    except:
        return []


def nuevo_cliente(clientes, nombre, dni, archivo):
    """Registra un nuevo cliente en la estructura 'clientes'."""
    if nombre.strip() == "":
        print("\n¡Error! El nombre es obligatorio. No puede estar vacio.")
        return clientes
    
    if contiene_numeros(nombre):
        print("\n¡Error! El nombre no puede contener números.")
        return clientes
    
    if dni.strip() == "":
        print("\n¡Error! El DNI es obligatorio. No puede estar vacio.")
        return clientes
    
    if not es_numero(dni):
        print("\n¡Error! El DNI debe ser un número. Volviendo al menú principal...")
        return clientes
    for c in clientes:
        if c["dni"] == dni:
            print("\n¡Error! Ya existe un cliente con ese DNI.")
            return clientes
    clientes.append({"nombre": nombre.strip(), "dni": dni.strip()})
    guardar_clientes(clientes, archivo)
    print("\nCliente registrado con éxito y guardado en archivo json.")
    return clientes


def listar_clientes(clientes):
    """Muestra la lista completa de clientes."""
    if not clientes:
        print("\nNo hay clientes registrados. Volviendo al menu principal...")
    else:
        print("\nLista de clientes:")
        for c in clientes:
            print("Nombre:", c["nombre"], "- DNI:", c["dni"])


def registrar_reserva(reservas, clientes, archivo):
    """Registra una nueva reserva con menú, música y servicios."""
    print("\nRegistrar reserva")
    dni = input("DNI del cliente: ").strip()
    
    if dni == "":
        print("\n¡Error! El DNI del cliente es obligatorio. No puede estar vacio.")
        return reservas
    
    if not es_numero(dni):
        print("\n¡Error! El DNI debe ser un número.")
        return reservas
    
    cliente_encontrado = None
    for c in clientes:
        if c["dni"] == dni:
            cliente_encontrado = c
            break
    
    if cliente_encontrado is None:
        print("\n¡Error! El cliente no esta registrado. Debe registrar el cliente primero antes de hacer una reserva.")
        return reservas
    
    nombre = cliente_encontrado["nombre"]
    print(f"Cliente encontrado: {nombre}")
    
    tipo = input("Tipo de fiesta: ").strip()
    
    if tipo == "":
        print("\n¡Error! El tipo de fiesta es obligatorio. No puede estar vacio.")
        return reservas
    
    fecha_texto = input("Fecha (DD/MM/AAAA): ").strip()
    
    if fecha_texto == "":
        print("\n¡Error! La fecha es obligatoria. No puede estar vacía.")
        return reservas

    fecha_iso = convertir_fecha(fecha_texto)
    if fecha_iso is None:
        print("\nFormato de fecha inválido. Usar DD/MM/AAAA (ej: 18/09/2023).")
        return reservas

    if existe_reserva_en_fecha(reservas, fecha_iso):
        print("No se puede reservar: ya existe una reserva en esa fecha.")
        return reservas

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
        "id": generar_id_reserva(reservas),
        "nombre": nombre,
        "tipo": tipo,
        "fecha": fecha_iso,
        "menu": menu,
        "musica": musica,
        "servicios": servicios
    }
    reservas.append(reserva)
    guardar_reservas(reservas, archivo)
    print("\nReserva registrada con éxito.")
    return reservas


def listar_reservas(reservas):
    """Muestra la lista de reservas."""
    if not reservas:
        print("\nNo hay reservas registradas. Volviendo al menu principal...")
    else:
        print("\nLista de reservas:")
        reservitas = reservas[:]
        reservitas.sort(key=lambda x: x["fecha"])
        for r in reservitas:
            serv_txt = ", ".join(r["servicios"]) if r["servicios"] else "Ninguno"
            print(f"ID {r['id']} - Cliente: {r['nombre']} - Fiesta: {r['tipo']} - Fecha: {r['fecha']} - Menú: {r['menu']} - Música: {r['musica']} - Servicios: {serv_txt}")


def modificar_reserva(reservas, archivo):
    """Modifica una reserva por ID."""
    listar_reservas(reservas)
    if not reservas:
        return reservas

    try:
        id_sel = int(input("\nID de la reserva a modificar: ").strip())
    except ValueError:
        print("ID inválido. Debe ingresar un numero entero.")
        return reservas

    objetivo = None
    for r in reservas:
        if r["id"] == id_sel:
            objetivo = r
            break

    if objetivo is None:
        print("No se encontró la reserva.")
        return reservas

    print("Deje vacío para mantener el valor anterior.")
    
    nuevo_nombre = input(f"Nombre del cliente ({objetivo['nombre']}): ").strip()
    if nuevo_nombre != "":
        objetivo["nombre"] = nuevo_nombre
    
    nuevo_tipo = input(f"Tipo de fiesta ({objetivo['tipo']}): ").strip()
    if nuevo_tipo != "":
        objetivo["tipo"] = nuevo_tipo

    nueva_fecha = input(f"Fecha ({objetivo['fecha']}) - DD/MM/AAAA: ").strip()
    if nueva_fecha != "":
        nueva_iso = convertir_fecha(nueva_fecha)
        if nueva_iso is None:
            print("Formato inválido, se mantiene la fecha anterior.")
        else:
            if existe_reserva_en_fecha(reservas, nueva_iso, excluir_id=objetivo["id"]):
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

    guardar_reservas(reservas, archivo)
    print("Reserva modificada con éxito.")
    return reservas


def eliminar_reserva(reservas, archivo):
    """Elimina una reserva por ID."""
    listar_reservas(reservas)
    if not reservas:
        return reservas

    try:
        id_sel = int(input("\nID de la reserva a eliminar: ").strip())
    except ValueError:
        print("ID inválido. Debe ingresar un numero entero.")
        return reservas

    idx = buscar_indice_por_id(reservas, id_sel)
    if idx == -1:
        print("No se encontró la reserva.")
        return reservas

    print(f"Se eliminará la reserva ID {reservas[idx]['id']} de {reservas[idx]['nombre']} en {reservas[idx]['fecha']}.")
    conf = input("Confirmar (ELIMINAR): ").strip()
    if conf == "ELIMINAR":
        reservas.pop(idx)
        guardar_reservas(reservas, archivo)
        print("Reserva eliminada con éxito.")
    else:
        print("Operación cancelada.")
    return reservas


def menu():
    """Menú principal del sistema."""
    clientes = cargar_clientes(ARCHIVO_CLIENTES)
    reservas = cargar_reservas(ARCHIVO_RESERVAS)

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
            clientes = nuevo_cliente(clientes, nombre, dni, ARCHIVO_CLIENTES)
        elif opcion == "2":
            listar_clientes(clientes)
        elif opcion == "3":
            reservas = registrar_reserva(reservas, clientes, ARCHIVO_RESERVAS)
        elif opcion == "4":
            listar_reservas(reservas)
        elif opcion == "5":
            reservas = modificar_reserva(reservas, ARCHIVO_RESERVAS)
        elif opcion == "6":
            reservas = eliminar_reserva(reservas, ARCHIVO_RESERVAS)
        elif opcion == "0":
            print("\n¡Gracias por usar el sistema, hasta la próxima!")
            return False
        else:
            print("\nOpción inválida, intente de nuevo.")


if __name__ == "__main__":
    menu()
