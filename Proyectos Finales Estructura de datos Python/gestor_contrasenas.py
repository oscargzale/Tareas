# gestor_contrasenas.py
import re

# ============================
# Datos base
# ============================

usuarios = []       # vector con nombres de usuario
contrasenas = []    # vector con contraseñas
niveles_seguridad = []  # vector paralelo con nivel (Débil / Media / Fuerte)


# ============================
# Funciones principales
# ============================

def VerificarContraseña(password):
    """
    Verifica la fuerza de una contraseña según varios criterios:
    - Longitud mínima (8)
    - Mayúsculas
    - Minúsculas
    - Números
    - Caracteres especiales
    Retorna: (nivel, razones)
    """
    razones = []
    longitud_ok = len(password) >= 8
    mayuscula = any(c.isupper() for c in password)
    minuscula = any(c.islower() for c in password)
    numero = any(c.isdigit() for c in password)
    especial = any(c in "!@#$%^&*()-_=+[]{};:,.<>?/|" for c in password)

    # Evaluación de fuerza
    puntaje = sum([longitud_ok, mayuscula, minuscula, numero, especial])

    if puntaje <= 2:
        nivel = "Débil"
    elif puntaje == 3 or puntaje == 4:
        nivel = "Media"
    else:
        nivel = "Fuerte"

    # Razones de advertencia
    if not longitud_ok:
        razones.append("Muy corta (<8)")
    if not mayuscula:
        razones.append("Falta mayúscula")
    if not minuscula:
        razones.append("Falta minúscula")
    if not numero:
        razones.append("Falta número")
    if not especial:
        razones.append("Falta símbolo especial")

    return nivel, razones


def RegistrarUsuario():
    """Registra un nuevo usuario y contraseña, verifica la fuerza y guarda en las listas."""
    usuario = input("Ingrese nombre de usuario: ").strip()
    if usuario in usuarios:
        print("⚠️  Este usuario ya existe.")
        return

    password = input("Ingrese una contraseña: ").strip()

    nivel, razones = VerificarContraseña(password)

    usuarios.append(usuario)
    contrasenas.append(password)
    niveles_seguridad.append(nivel)

    print(f"\nUsuario '{usuario}' registrado correctamente.")
    print(f"Nivel de seguridad de la contraseña: {nivel}")
    if razones:
        print("Advertencias:", ", ".join(razones))


def MostrarUsuarios():
    """Muestra todos los usuarios con su nivel de seguridad."""
    if not usuarios:
        print("No hay usuarios registrados aún.")
        return
    print("\n=== LISTA DE USUARIOS ===")
    print(f"{'Usuario':<15} {'Nivel de Contraseña':<10}")
    print("-" * 30)
    for i in range(len(usuarios)):
        print(f"{usuarios[i]:<15} {niveles_seguridad[i]:<10}")


def GenerarAlertas():
    """Muestra usuarios con contraseñas débiles."""
    print("\n=== ALERTAS DE CONTRASEÑAS DÉBILES ===")
    alertas = []
    for i in range(len(usuarios)):
        if niveles_seguridad[i] == "Débil":
            alertas.append((usuarios[i], contrasenas[i]))

    if not alertas:
        print("✅ No se detectaron contraseñas débiles.")
    else:
        for u, p in alertas:
            print(f"⚠️  Usuario: {u}  |  Contraseña débil: {p}")


def MostrarDetallesUsuario():
    """Permite ver el nivel y razones específicas de un usuario."""
    nombre = input("Ingrese el nombre del usuario a consultar: ").strip()
    if nombre not in usuarios:
        print("Usuario no encontrado.")
        return
    idx = usuarios.index(nombre)
    pwd = contrasenas[idx]
    nivel, razones = VerificarContraseña(pwd)
    print(f"\nUsuario: {nombre}")
    print(f"Contraseña: {pwd}")
    print(f"Nivel: {nivel}")
    if razones:
        print("Debilidades:", ", ".join(razones))
    else:
        print("Contraseña sin debilidades detectadas.")


# ============================
# Menú principal
# ============================

def menu():
    while True:
        print("\n=== GESTOR DE CONTRASEÑAS SEGURAS ===")
        print("1) Registrar nuevo usuario")
        print("2) Mostrar todos los usuarios")
        print("3) Generar alertas de contraseñas débiles")
        print("4) Consultar detalle de un usuario")
        print("0) Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            RegistrarUsuario()
        elif opcion == "2":
            MostrarUsuarios()
        elif opcion == "3":
            GenerarAlertas()
        elif opcion == "4":
            MostrarDetallesUsuario()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    print("Inicio del Gestor de Contraseñas Seguras 🧩")
    menu()
