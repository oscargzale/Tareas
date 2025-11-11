import random
import datetime
from tabulate import tabulate

# ============================
# Datos iniciales
# ============================
usuarios = ["alice", "bob", "charlie", "david"]
servidores = ["web01", "db01", "mail01"]

# Matriz donde guardaremos los intentos
intentos = []  # cada intento será [usuario, servidor, ip, tipo, hora]


# ============================
# Funciones principales
# ============================

def RegistrarIntento(usuario, servidor, ip, tipo):
    """Registra un nuevo intento de acceso"""
    hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    intentos.append([usuario, servidor, ip, tipo, hora])


def MostrarReporte():
    """Muestra todos los intentos en forma de tabla"""
    if not intentos:
        print("No hay intentos registrados.")
        return
    print("\n===== REPORTE DE ACCESOS =====")
    print(tabulate(intentos, headers=["Usuario", "Servidor", "IP", "Tipo", "Hora"], tablefmt="grid"))


def GenerarAlertas():
    """Detecta IPs o usuarios con actividad sospechosa"""
    alertas = []
    
    # 1. Contar intentos por IP
    ip_count = {}
    for intento in intentos:
        ip = intento[2]
        ip_count[ip] = ip_count.get(ip, 0) + 1
    
    for ip, cantidad in ip_count.items():
        if cantidad > 3:
            alertas.append(f"⚠️ IP sospechosa: {ip} con {cantidad} intentos.")

    # 2. Contar intentos fallidos por usuario
    user_fails = {}
    for intento in intentos:
        user, tipo = intento[0], intento[3]
        if tipo.lower() == "fallido":
            user_fails[user] = user_fails.get(user, 0) + 1
    
    for user, cantidad in user_fails.items():
        if cantidad > 2:
            alertas.append(f"🚨 Usuario con múltiples fallos: {user} ({cantidad} intentos).")

    if not alertas:
        print("\nNo se detectaron alertas.")
    else:
        print("\n===== ALERTAS DETECTADAS =====")
        for a in alertas:
            print(a)


# ============================
# Simulación de registros
# ============================

# Generar algunos accesos de ejemplo
for _ in range(10):
    user = random.choice(usuarios)
    server = random.choice(servidores)
    ip = f"192.168.1.{random.randint(1,10)}"
    tipo = random.choice(["exitoso", "fallido"])
    RegistrarIntento(user, server, ip, tipo)

# Mostrar resultados
MostrarReporte()
GenerarAlertas()
