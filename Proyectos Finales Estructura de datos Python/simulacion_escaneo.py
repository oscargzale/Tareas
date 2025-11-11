# simulacion_escaneo.py
import random
import datetime

# try to use tabulate if available
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except Exception:
    HAS_TABULATE = False

# ============================
# Estructuras de datos
# ============================
hosts = []           # vector de hosts (ej: "192.168.1.10")
matriz_servicios = []  # lista de listas: por host -> [[servicio, puerto, version], ...]
intentos_scan = []     # matriz de intentos de escaneo: [host, tipo_scan, hora, origen_ip]
vulnerabilidades = []  # matriz de vulnerabilidades encontradas: [host, servicio, puerto, descripcion, riesgo, hora]

# Parámetros para alertas
UMBRAL_RIESGO_ALTO = 7.0  # si riesgo >= este -> alerta importante


# ============================
# Utilidades
# ============================
def ahora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generar_version_base(servicio):
    """Genera una versión simulada; algunas versiones son 'vulnerables' por convención."""
    # ejemplo: versiones antiguas tienen número menor
    major = random.choice([1, 2, 3, 4])
    minor = random.randint(0, 9)
    patch = random.randint(0, 9)
    return f"{major}.{minor}.{patch}"


def riesgo_por_regla(servicio, version, puerto):
    """
    Heurística simple para asignar un 'riesgo' numérico 0-10.
    - Servicios comunes: http, ssh, ftp, smb, rdp, db
    - Versiones con major <=2 son más vulnerables (simulado)
    - Puertos no estándar elevan el riesgo levemente
    """
    base = 1.0
    s = servicio.lower()
    if s in ("http", "https"):
        base += 2.0
    if s in ("ssh",):
        base += 1.5
    if s in ("ftp","smb","rdp"):
        base += 2.5
    if s.startswith("db") or s in ("mysql","postgres","mssql"):
        base += 3.0

    # version
    try:
        major = int(str(version).split(".")[0])
        if major <= 2:
            base += 2.0
        elif major == 3:
            base += 1.0
    except Exception:
        base += 1.0

    # puerto no estándar
    if puerto not in (80, 443, 22, 21, 3389, 3306, 1433):
        base += 0.7

    # factor aleatorio
    base += random.uniform(0, 2.0)
    # normalizar a escala 0-10
    riesgo = min(round(base, 1), 10.0)
    return riesgo


# ============================
# Funciones principales
# ============================
def RegistrarHost(host_ip):
    """Agrega un host y le asigna una lista vacía de servicios."""
    if host_ip in hosts:
        print("Host ya registrado.")
        return
    hosts.append(host_ip)
    matriz_servicios.append([])  # lista vacía de servicios
    print(f"Host {host_ip} registrado.")


def AgregarServicio(host_ip, servicio, puerto, version=None):
    """Agrega un servicio (puerto/version) al host indicado."""
    if host_ip not in hosts:
        print("Host no encontrado. Registra el host primero.")
        return
    idx = hosts.index(host_ip)
    if version is None:
        version = generar_version_base(servicio)
    matriz_servicios[idx].append([servicio, puerto, version])
    print(f"Servicio {servicio} en puerto {puerto} (v{version}) agregado a {host_ip}.")


def RegistrarIntentoScan(host_ip, tipo_scan="tcp-scan", origen_ip=None):
    """Registra un intento de escaneo (solo histórico)."""
    if origen_ip is None:
        origen_ip = f"10.0.0.{random.randint(2,250)}"
    intentos_scan.append([host_ip, tipo_scan, ahora(), origen_ip])
    print(f"[{ahora()}] Intento de escaneo {tipo_scan} sobre {host_ip} desde {origen_ip} registrado.")


def AnalizarVulnerabilidades(host_ip=None):
    """
    Analiza los servicios registrados y genera entradas en la lista 'vulnerabilidades'.
    Si host_ip es None se analiza todos los hosts.
    """
    targets = [host_ip] if host_ip else list(hosts)
    for h in targets:
        if h not in hosts:
            print(f"Host {h} no registrado, se omite.")
            continue
        idx = hosts.index(h)
        servicios = matriz_servicios[idx]
        # Simular un analisis: por cada servicio calcular riesgo y, si riesgo>2, guardar vulnerabilidad
        for s in servicios:
            servicio, puerto, version = s[0], s[1], s[2]
            riesgo = riesgo_por_regla(servicio, version, puerto)
            if riesgo >= 2.0:  # umbral mínimo para considerarlo "vulnerabilidad" (simulado)
                descripcion = f"Posible vulnerabilidad en {servicio} v{version} en puerto {puerto}."
                vulnerabilidades.append([h, servicio, puerto, descripcion, riesgo, ahora()])
                print(f"[ANALISIS] {h} - {servicio}:{puerto} riesgo={riesgo}")


def MostrarReporte():
    """Muestra un reporte resumen con hosts, servicios, y vulnerabilidades encontradas."""
    print("\n=== REPORTE DE HOSTS Y SERVICIOS ===")
    for i, h in enumerate(hosts):
        print(f"\nHost: {h}")
        if matriz_servicios[i]:
            for svc in matriz_servicios[i]:
                print(f"  - {svc[0]} | puerto: {svc[1]} | v{svc[2]}")
        else:
            print("  (sin servicios registrados)")

    print("\n=== VULNERABILIDADES ENCONTRADAS ===")
    if not vulnerabilidades:
        print("No se encontraron vulnerabilidades (aún).")
    else:
        headers = ["Host", "Servicio", "Puerto", "Descripción", "Riesgo", "Hora"]
        if HAS_TABULATE:
            print(tabulate(vulnerabilidades, headers=headers, tablefmt="grid"))
        else:
            print(" | ".join(headers))
            print("-" * 100)
            for v in vulnerabilidades:
                print(f"{v[0]} | {v[1]} | {v[2]} | {v[3]} | {v[4]} | {v[5]}")

    # resumen de riesgo por host
    print("\n=== RESUMEN DE RIESGO POR HOST ===")
    resumen = {}
    for v in vulnerabilidades:
        host = v[0]
        riesgo = float(v[4])
        resumen[host] = max(resumen.get(host, 0.0), riesgo)
    if not resumen:
        print("Sin riesgos detectados.")
    else:
        for host, riesgo in resumen.items():
            etiqueta = "ALTO" if riesgo >= UMBRAL_RIESGO_ALTO else "MEDIO" if riesgo >= 4.0 else "BAJO"
            print(f"{host}: riesgo máximo detectado = {riesgo} ({etiqueta})")


def GenerarAlertas():
    """Genera alertas basadas en vulnerabilidades encontradas y en p
