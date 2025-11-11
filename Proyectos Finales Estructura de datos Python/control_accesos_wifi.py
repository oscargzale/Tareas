# control_accesos_wifi.py
import datetime
import random

# Intentar usar tabulate para tablas más bonitas
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except Exception:
    HAS_TABULATE = False

# ===================================
# Estructuras de datos
# ===================================
dispositivos_registrados = []   # vector de MACs permitidas
matriz_conexiones = []          # lista de listas: [MAC, IP, Usuario, Hora, Autorizado]
MAX_CONEXIONES = 5              # límite máximo de conexiones simultáneas
LISTA_BLOQUEO = []              # dispositivos bloqueados (por seguridad)


# ===================================
# Funciones auxiliares
# ===================================
def ahora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generar_ip():
    """Genera una IP aleatoria para simulación."""
    return f"192.168.1.{random.randint(2, 254)}"


def generar_mac():
    """Genera una MAC aleatoria para simulación."""
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))


# ===================================
# Funciones principales
# ===================================
def RegistrarDispositivo(mac, usuario):
    """Agrega un dispositivo autorizado a la red (MAC permitida)."""
    if mac in dispositivos_registrados:
        print("⚠️ Dispositivo ya registrado.")
        return
    dispositivos_registrados.append(mac)
    print(f"✅ Dispositivo {mac} registrado exitosamente para {usuario}.")


def ValidarAcceso(mac, ip, usuario):
    """
    Verifica si un dispositivo puede acceder:
    - Si está registrado y no se supera el límite: permite conexión.
    - Si no está registrado: alerta de acceso no autorizado.
    """
    global matriz_conexiones

    # Revisar si MAC está bloqueada
    if mac in LISTA_BLOQUEO:
        print(f"🚫 ACCESO DENEGADO: MAC {mac} está bloqueada.")
        return

    autorizado = mac in dispositivos_registrados

    # Verificar límite de conexiones
    conexiones_activas = len([c for c in matriz_conexiones if c[4] == True])
    if conexiones_activas >= MAX_CONEXIONES and autorizado:
        print("⚠️ Límite de conexiones alcanzado. No se puede conectar otro dispositivo.")
        return

    registro = [mac, ip, usuario, ahora(), autorizado]
    matriz_conexiones.append(registro)

    if autorizado:
        print(f"✅ {usuario} conectado desde {mac} ({ip}) - Acceso autorizado.")
    else:
        print(f"🚨 ALERTA: Acceso no autorizado detectado -> MAC {mac} ({ip})")
        LISTA_BLOQUEO.append(mac)  # bloqueo automático
        print(f"🔒 Dispositivo {mac} agregado a la lista de bloqueo.")


def MostrarConexiones():
    """Muestra todas las conexiones activas y su estado."""
    print("\n=== CONEXIONES ACTUALES ===")
    if not matriz_conexiones:
        print("No hay conexiones registradas.")
        return

    headers = ["MAC", "IP", "Usuario", "Hora", "Autorizado"]
    if HAS_TABULATE:
        print(tabulate(matriz_conexiones, headers=headers, tablefmt="grid"))
    else:
        print(" | ".join(headers))
        print("-" * 80)
        for c in matriz_conexiones:
            print(" | ".join(str(x) for x in c))


def GenerarAlertas():
    """Genera alertas de dispositivos bloqueados y accesos no autorizados."""
    print("\n=== ALERTAS DE SEGURIDAD ===")
    no_autorizados = [c for c in matriz_conexiones if c[4] == False]
    if not no_autorizados and not LISTA_BLOQUEO:
        print("Sin alertas por ahora. Todo está bajo control ✅")
        return

    # Mostrar accesos no autorizados
    if no_autorizados:
        print("\n🚨 Accesos no autorizados detectados:")
        for c in no_autorizados:
            print(f" - MAC {c[0]} ({c[1]}) - Usuario: {c[2]} - Hora: {c[3]}")

    # Mostrar lista de bloqueo
    if LISTA_BLOQUEO:
        print("\n🔒 Dispositivos actualmente bloqueados:")
        for mac in LISTA_BLOQUEO:
            print(f" - {mac}")


def SimularConexiones():
    """Genera datos de ejemplo para pruebas rápidas."""
    # Registrar dispositivos válidos
    RegistrarDispositivo("AA:BB:CC:DD:EE:01", "Juan")
    RegistrarDispositivo("AA:BB:CC:DD:EE:02", "Ana")
    RegistrarDispositivo("AA:BB:CC:DD:EE:03", "Pedro")

    # Simular conexiones (algunas válidas, otras no)
    ValidarAcceso("AA:BB:CC:DD:EE:01", generar_ip(), "Juan")
    ValidarAcceso("AA:BB:CC:DD:EE:02", generar_ip(), "Ana")
    ValidarAcceso(generar_mac(), generar_ip(), "Intruso1")
    ValidarAcceso("AA:BB:CC:DD:EE:03", generar_ip(), "Pedro")
    ValidarAcceso(generar_mac(), generar_ip(), "Intruso2")
    print("\nSimulación de conexiones completada ✅")


# ===================================
# Menú interactivo
# ===================================
def menu():
    while True:
        print("\n=== CON
