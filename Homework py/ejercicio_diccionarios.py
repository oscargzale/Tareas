# ejercicio_diccionarios.py

# Crear el diccionario inicial
dispositivo_red = {
    'IP': '192.168.1.10',
    'Hostname': 'Firewall-Corp',
    'Estado': 'Activo'
}

print("Diccionario inicial:", dispositivo_red)

# a) Mostrar el valor de la clave 'Hostname'
print("\na) Hostname del dispositivo:", dispositivo_red['Hostname'])

# b) Agregar una nueva clave 'Ubicación' con el valor 'Centro de Datos'
dispositivo_red['Ubicación'] = 'Centro de Datos'
print("b) Diccionario después de agregar 'Ubicación':", dispositivo_red)

# c) Cambiar el valor de 'Estado' a 'Inactivo'
dispositivo_red['Estado'] = 'Inactivo'
print("c) Diccionario después de cambiar 'Estado':", dispositivo_red)

# d) Mostrar todo el diccionario actualizado
print("\nd) Diccionario final actualizado:")
for clave, valor in dispositivo_red.items():
    print(f"   {clave}: {valor}")
