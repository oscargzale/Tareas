# inventario_equipos.py
import ipaddress
from tabulate import tabulate

# ============================
# Datos base
# ============================

equipos = []         # Vector con nombres de equipos
ubicaciones = []     # Vector con ubicaciones
matriz_datos = []    # Matriz con [IP, tipo, estado] de cada equipo


# ============================
# Funciones principales
# ============================

def validar_ip(ip):
    """Verifica que la IP tenga formato válido."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def RegistrarEquipo():
    """Registra un nuevo equipo con su información básica."""
    print("\n=== REGISTRAR EQUIPO DE RED ===")
    nombre = input("Nombre del equipo: ").strip()

    if nombre in equipos:
        print("⚠️  Este equipo ya existe en el inventario.")
        return

    ip = input("Dirección IP: ").strip()
    if not validar_ip(ip):
        print("❌ IP no válida. Intente nuevamente.")
        return

    tipo = input("Tipo de equipo (Router, Switch, PC, etc.): ").strip()
    ubicacion = input("Ubicación física: ").strip()

    estado = input("¿Está activo? (S/N): ").strip().upper()
    estado = "Activo" if estado == "S" else "Inactivo"

    # Guardar en vectores y matriz
    equipos.append(nombre)
    ubicaciones.append(ubicacion)
    matriz_datos.append([ip, tipo, estado])

    print(f"✅ Equipo '{nombre}' registrado correctamente.")


def MostrarInventario():
    """Muestra todos los equipos registrados en forma de tabla."""
    if not equipos:
        print("No hay equipos registrados aún.")
        return

    print("\n=== INVENTARIO DE EQUIPOS DE RED ===")
    datos_tabla = []
    for i in range(len(equipos)):
        ip, tipo, estado = matriz_datos[i]
        datos_tabla.append([equipos[i], ip, tipo, ubicaciones[i], estado])

    headers = ["Equipo", "IP", "Tipo", "Ubicación", "Estado"]
    print(tabulate(datos_tabla, headers=headers, tablefmt="grid"))


def GenerarAlertas():
    """Muestra una lista de equipos que están inactivos."""
    print("\n=== ALERTAS DE EQUIPOS INACTIVOS ===")
    alertas = []
    for i in range(len(equipos)):
        if matriz_datos[i][2] == "Inactivo":
            alertas.append([equipos[i], matriz_datos[i][0], ubicaciones[i]])

    if not alertas:
        print("✅ Todos los equipos están activos.")
    else:
        print(tabulate(alertas, headers=["Equipo", "IP", "Ubicación"], tablefmt="grid"))


def BuscarEquipo():
    """Permite buscar un equipo por nombre."""
    nombre = input("Ingrese el nombre del equipo a buscar: ").strip()
    if nombre not in equipos:
        print("❌ Equipo no encontrado.")
        return

    idx = equipos.index(nombre)
    ip, tipo, estado = matriz_datos[idx]
    print(f"\nEquipo: {nombre}")
    print(f"IP: {ip}")
    print(f"Tipo: {tipo}")
    print(f"Ubicación: {ubicaciones[idx]}")
    print(f"Estado: {estado}")


# ============================
# Menú principal
# ============================

def menu():
    while True:
        print("\n=== SISTEMA DE INVENTARIO DE EQUIPOS DE RED ===")
        print("1) Registrar nuevo equipo")
        print("2) Mostrar inventario completo")
        print("3) Generar alertas (equipos inactivos)")
        print("4) Buscar equipo por nombre")
        print("0) Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            RegistrarEquipo()
        elif opcion == "2":
            MostrarInventario()
        elif opcion == "3":
            GenerarAlertas()
        elif opcion == "4":
            BuscarEquipo()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    print("Inicio del Sistema de Inventario de Equipos de Red 🖥️")
    menu()
