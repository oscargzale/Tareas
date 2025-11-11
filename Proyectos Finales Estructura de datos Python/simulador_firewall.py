# simulador_firewall.py
import datetime
import random

# Intentar usar tabulate para mostrar tablas; si no está, usar fallback
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except Exception:
    HAS_TABULATE = False

# ============================
# Datos / Estructuras
# ============================
ips_bloqueadas = ["10.0.0.5"]         # vector: IPs explicitamente bloqueadas
reglas_bloqueo_puertos = [23]         # puertos bloqueados (ejemplo: telnet)
reglas_bloqueo_protocolos = ["icmp"]  # protocolos bloqueados
registros = []  # matriz: cada fila -> [ip, puerto, protocolo, hora, estado, razon]

# Parámetros de alerta
UMBRAL_INTENTOS_BLOQUEADOS = 3  # si una IP tiene > este número de bloqueos -> alerta


# ============================
# Funciones principales
# ============================

def ahora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def aplicar_reglas(ip, puerto, protocolo):
    """
    Aplica reglas básicas y devuelve (permitido: bool, razon: str)
    Reglas:
      - Si IP en ips_bloqueadas -> bloquear
      - Si puerto en reglas_bloqueo_puertos -> bloquear
      - Si protocolo en reglas_bloqueo_protocolos -> bloquear
      - Si puerto < 1 o > 65535 -> bloquear por puerto inválido
      - Si ip mal formada -> bloquear (simple verificación)
      - En otro caso -> permitir
    """
    # 1) IP explícitamente bloqueada
    if ip in ips_bloqueadas:
        return False, "IP bloqueada (lista negra)"
    # 2) Verificar formato sencillo de IP (4 octetos 0-255)
    parts = ip.split(".")
    if len(parts) != 4:
        return False, "IP inválida (formato)"
    try:
        for p in parts:
            n = int(p)
            if n < 0 or n > 255:
                return False, "IP inválida (octeto fuera de rango)"
    except Exception:
        return False, "IP inválida (no numérica)"
    # 3) puerto válido
    if not isinstance(puerto, int) or puerto < 1 or puerto > 65535:
        return False, "Puerto inválido"
    # 4) puerto en regla de bloqueo
    if puerto in reglas_bloqueo_puertos:
        return False, f"Puerto bloqueado ({puerto})"
    # 5) protocolo en regla de bloqueo
    if protocolo.lower() in (p.lower() for p in reglas_bloqueo_protocolos):
        return False, f"Protocolo bloqueado ({protocolo})"
    # si pasó todo -> permitir
    return True, "Permitido"


def RegistrarPaquete(ip, puerto, protocolo):
    permitido, razon = aplicar_reglas(ip, puerto, protocolo)
    estado = "PERMITIDO" if permitido else "BLOQUEADO"
    fila = [ip, puerto, protocolo, ahora(), estado, razon]
    registros.append(fila)
    # Feedback inmediato
    if permitido:
        print(f"[{fila[3]}] Paquete PERMITIDO: {ip}:{puerto} {protocolo} — {razon}")
    else:
        print(f"[{fila[3]}] Paquete BLOQUEADO: {ip}:{puerto} {protocolo} — {razon}")


def MostrarRegistros(limit=None):
    """Muestra todos los registros (o hasta 'limit' si se especifica)."""
    to_show = registros if limit is None else registros[-limit:]
    headers = ["IP Origen", "Puerto", "Protocolo", "Hora", "Estado", "Razón"]
    if HAS_TABULATE:
        print(tabulate(to_show, headers=headers, tablefmt="grid"))
    else:
        # fallback simple
        print(" | ".join(headers))
        print("-" * 80)
        for r in to_show:
            print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}")


def GenerarAlertas():
    """Detecta IPs con muchos intentos bloqueados y muestra alertas."""
    bloqueos_por_ip = {}
    for r in registros:
        ip, estado = r[0], r[4]
        if estado == "BLOQUEADO":
            bloqueos_por_ip[ip] = bloqueos_por_ip.get(ip, 0) + 1

    alertas = []
    for ip, cnt in bloqueos_por_ip.items():
        if cnt >= UMBRAL_INTENTOS_BLOQUEADOS:
            alertas.append(f"🚨 ALERTA: IP {ip} con {cnt} intentos BLOQUEADOS (posible escaneo/brute force)")

    if not alertas:
        print("No se detectaron alertas críticas.")
    else:
        for a in alertas:
            print(a)


# ============================
# Utilidades: administración de reglas / IPs
# ============================

def bloquear_ip(ip):
    if ip in ips_bloqueadas:
        print("La IP ya está en la lista de bloqueadas.")
    else:
        ips_bloqueadas.append(ip)
        print(f"IP {ip} agregada a lista de bloqueadas.")


def desbloquear_ip(ip):
    if ip in ips_bloqueadas:
        ips_bloqueadas.remove(ip)
        print(f"IP {ip} removida de lista de bloqueadas.")
    else:
        print("La IP no está en la lista de bloqueadas.")


def agregar_regla_puerto(puerto):
    if puerto in reglas_bloqueo_puertos:
        print("Regla ya existe.")
    else:
        reglas_bloqueo_puertos.append(puerto)
        print(f"Puerto {puerto} añadido a reglas de bloqueo.")


def quitar_regla_puerto(puerto):
    if puerto in reglas_bloqueo_puertos:
        reglas_bloqueo_puertos.remove(puerto)
        print(f"Puerto {puerto} removido de reglas de bloqueo.")
    else:
        print("Esa regla no existe.")


def agregar_regla_protocolo(proto):
    if proto.lower() in (p.lower() for p in reglas_bloqueo_protocolos):
        print("Regla ya existe.")
    else:
        reglas_bloqueo_protocolos.append(proto)
        print(f"Protocolo {proto} añadido a reglas de bloqueo.")


def quitar_regla_protocolo(proto):
    found = None
    for p in reglas_bloqueo_protocolos:
        if p.lower() == proto.lower():
            found = p
            break
    if found:
        reglas_bloqueo_protocolos.remove(found)
        print(f"Protocolo {proto} removido de reglas de bloqueo.")
    else:
        print("Esa regla no existe.")


# ============================
# Simulación aleatoria (para pruebas)
# ============================

def ip_aleatoria():
    return f"192.168.1.{random.randint(1,254)}"

def simular_n_paquetes(n=10):
    protocolos = ["tcp", "udp", "icmp", "http"]
    for _ in range(n):
        ip = random.choice([ip_aleatoria(), "10.0.0.5", "256.1.1.1"])  # incluye IP bloqueada y una inválida
        puerto = random.choice([22, 23, 80, 443, 8080, 99999])
        proto = random.choice(protocolos)
        RegistrarPaquete(ip, puerto, proto)


# ============================
# Menú interactivo
# ============================
def menu():
    while True:
        print("\n=== SIMULADOR FIREWALL - MENÚ ===")
        print("1) Registrar paquete manual")
        print("2) Simular N paquetes aleatorios")
        print("3) Mostrar registros (todos)")
        print("4) Mostrar últimos 10 registros")
        print("5) Generar alertas")
        print("6) Mostrar/Modificar lista IPs bloqueadas")
        print("7) Mostrar/Modificar reglas de puerto")
        print("8) Mostrar/Modificar reglas de protocolo")
        print("9) Limpiar registros")
        print("0) Salir")
        op = input("Elige opción: ").strip()

        if op == "1":
            ip = input("IP origen: ").strip()
            try:
                puerto = int(input("Puerto: ").strip())
            except:
                print("Puerto inválido, debe ser entero.")
                continue
            proto = input("Protocolo (tcp/udp/icmp/http...): ").strip()
            RegistrarPaquete(ip, puerto, proto)
        elif op == "2":
            try:
                n = int(input("¿Cuántos paquetes simular? ").strip())
            except:
                n = 10
            simular_n_paquetes(n)
        elif op == "3":
            MostrarRegistros()
        elif op == "4":
            MostrarRegistros(limit=10)
        elif op == "5":
            GenerarAlertas()
        elif op == "6":
            print("IPs bloqueadas:", ips_bloqueadas)
            sub = input("a) bloquear IP  b) desbloquear IP  Enter para volver: ").strip().lower()
            if sub == "a":
                ip = input("IP a bloquear: ").strip()
                bloquear_ip(ip)
            elif sub == "b":
                ip = input("IP a desbloquear: ").strip()
                desbloquear_ip(ip)
        elif op == "7":
            print("Puertos bloqueados:", reglas_bloqueo_puertos)
            sub = input("a) agregar puerto  b) quitar puerto  Enter para volver: ").strip().lower()
            if sub == "a":
                try:
                    p = int(input("Puerto a bloquear: ").strip())
                    agregar_regla_puerto(p)
                except:
                    print("Puerto inválido.")
            elif sub == "b":
                try:
                    p = int(input("Puerto a quitar: ").strip())
                    quitar_regla_puerto(p)
                except:
                    print("Puerto inválido.")
        elif op == "8":
            print("Protocolos bloqueados:", reglas_bloqueo_protocolos)
            sub = input("a) agregar protocolo  b) quitar protocolo  Enter para volver: ").strip().lower()
            if sub == "a":
                proto = input("Protocolo a bloquear: ").strip()
                agregar_regla_protocolo(proto)
            elif sub == "b":
                proto = input("Protocolo a quitar: ").strip()
                quitar_regla_protocolo(proto)
        elif op == "9":
            registros.clear()
            print("Registros limpiados.")
        elif op == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    print("Inicio del Simulador de Firewall Básico")
    if HAS_TABULATE:
        print("Nota: tabulate detectado -> salida formateada en tablas.")
    else:
        print("Nota: tabulate NO detectado -> salida en texto plano (funciona igual).")
    menu()
