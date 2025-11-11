# ejercicio_tuplas.py

# Crear la tupla
vulnerabilidades = (
    "SQL Injection",
    "Cross-Site Scripting",
    "Buffer Overflow",
    "Denegación de Servicio"
)

print("Tupla completa:", vulnerabilidades)

# a) Mostrar el segundo elemento
# (recordar: los índices en Python empiezan en 0)
segundo = vulnerabilidades[1]
print("\na) Segundo elemento:", segundo)

# b) Mostrar los dos últimos elementos
ultimos_dos = vulnerabilidades[-2:]   # slicing
print("b) Dos últimos elementos:", ultimos_dos)

# c) Intentar modificar un elemento (mostramos qué pasa con try/except)
print("\nc) Intento de modificar un elemento (debe producir TypeError):")
try:
    vulnerabilidades[0] = "Otro ataque"
except TypeError as e:
    print("   Error capturado:", type(e).__name__, "-", e)

# Alternativa: si realmente necesitas cambiar algo, conviertes a lista, modificas y vuelves a tupla
print("\n   Alternativa: convertir a lista, modificar y volver a tupla:")
lista_vuln = list(vulnerabilidades)
lista_vuln[0] = "Inyección SQL (modificada)"
vulnerabilidades_mod = tuple(lista_vuln)
print("   Tupla modificada (nueva):", vulnerabilidades_mod)
