# ejercicio_listas.py

# Crear la lista inicial
puertos_abiertos = [22, 80, 443, 8080]
print("Lista inicial:", puertos_abiertos)

# a) Agregar el puerto 21
puertos_abiertos.append(21)
print("\na) Lista después de agregar el puerto 21:", puertos_abiertos)

# b) Eliminar el puerto 8080
if 8080 in puertos_abiertos:
    puertos_abiertos.remove(8080)
print("b) Lista después de eliminar el puerto 8080:", puertos_abiertos)

# c) Mostrar la lista ordenada de menor a mayor
puertos_ordenados = sorted(puertos_abiertos)
print("c) Lista ordenada:", puertos_ordenados)
