ALGORITMO SistemaDeInventarioDeRed
	
    // ==============================
    // VARIABLES Y ESTRUCTURAS
    // ==============================
    DEFINIR equipos, ubicaciones, ips, estados COMO CADENA
    DEFINIR opcion, contador, i COMO ENTERO
    DIMENSION equipos[100]
    DIMENSION ubicaciones[100]
    DIMENSION ips[100]
    DIMENSION estados[100]
    contador <- 0
	
    // ==============================
    // SUBPROCESOS Y FUNCIONES
    // ==============================
	
    SUBPROCESO RegistrarEquipo()
        DEFINIR nombre, ip, tipo, ubicacion, estado COMO CADENA
		
        ESCRIBIR "Ingrese el nombre del equipo:"
        LEER nombre
        ESCRIBIR "Ingrese la dirección IP:"
        LEER ip
        ESCRIBIR "Ingrese el tipo de equipo (Router, Switch, PC, etc.):"
        LEER tipo
        ESCRIBIR "Ingrese la ubicación del equipo:"
        LEER ubicacion
        ESCRIBIR "Ingrese el estado del equipo (Activo/Inactivo):"
        LEER estado
		
        contador <- contador + 1
        equipos[contador] <- CONCATENAR(nombre, " - ", tipo)
        ips[contador] <- ip
        ubicaciones[contador] <- ubicacion
        estados[contador] <- estado
		
        ESCRIBIR "Equipo registrado correctamente."
FINSUBPROCESO


SUBPROCESO MostrarInventario()
	SI contador = 0 ENTONCES
		ESCRIBIR "No hay equipos registrados."
	SINO
		ESCRIBIR "===== INVENTARIO DE EQUIPOS ====="
		PARA i <- 1 HASTA contador HACER
			ESCRIBIR i, ") ", equipos[i]
			ESCRIBIR "    IP: ", ips[i]
			ESCRIBIR "    Ubicación: ", ubicaciones[i]
			ESCRIBIR "    Estado: ", estados[i]
			ESCRIBIR "------------------------------------"
		FINPARA
	FINSI
FINSUBPROCESO


SUBPROCESO GenerarAlertas()
	DEFINIR alerta COMO LOGICO
	alerta <- FALSO
	
	SI contador = 0 ENTONCES
		ESCRIBIR "No hay equipos para analizar."
	SINO
		ESCRIBIR "===== ALERTAS DE EQUIPOS INACTIVOS ====="
		PARA i <- 1 HASTA contador HACER
			SI estados[i] = "Inactivo" O estados[i] = "inactivo" ENTONCES
				ESCRIBIR "ALERTA: El equipo ", equipos[i], " (", ips[i], ") está INACTIVO."
				alerta <- VERDADERO
			FINSI
		FINPARA
		
		SI alerta = FALSO ENTONCES
			ESCRIBIR "Todos los equipos están activos."
		FINSI
	FINSI
FINSUBPROCESO


// ==============================
// MENÚ PRINCIPAL
// ==============================
opcion <- -1

MIENTRAS opcion <> 0 HACER
	ESCRIBIR ""
	ESCRIBIR "===== SISTEMA DE INVENTARIO DE RED ====="
	ESCRIBIR "1) Registrar equipo"
	ESCRIBIR "2) Mostrar inventario"
	ESCRIBIR "3) Generar alertas"
	ESCRIBIR "0) Salir"
	ESCRIBIR "Seleccione una opción:"
	LEER opcion
	
	SEGUN opcion HACER
		1:
			RegistrarEquipo()
		2:
			MostrarInventario()
		3:
			GenerarAlertas()
		0:
			ESCRIBIR "Saliendo del sistema..."
		DE OTRO MODO:
			ESCRIBIR "Opción no válida, intente nuevamente."
	FINSEGUN
FINMIENTRAS

FINALGORITMO
