ALGORITMO SimuladorFirewallBasico
	
    // ==============================
    // VARIABLES Y ESTRUCTURAS
    // ==============================
    DEFINIR opcion, contadorPaquetes, i, j, alertas COMO ENTERO
    DEFINIR ip, protocolo COMO CADENA
    DEFINIR puerto COMO ENTERO
    DEFINIR encontrado COMO LOGICO
	
    DIMENSION ipsBloqueadas[5]
    DIMENSION ipOrigen[100]
    DIMENSION puertoPaquete[100]
    DIMENSION protocoloPaquete[100]
	
    contadorPaquetes <- 0
	
    // IPs bloqueadas
    ipsBloqueadas[1] <- "192.168.1.5"
    ipsBloqueadas[2] <- "10.0.0.13"
    ipsBloqueadas[3] <- "172.16.0.2"
    ipsBloqueadas[4] <- "203.0.113.7"
    ipsBloqueadas[5] <- "45.33.12.1"
	
	
    // ==============================
    // SUBPROCESOS
    // ==============================
	
    SUBPROCESO RegistrarPaquete()
        DEFINIR ip, protocolo COMO CADENA
        DEFINIR puerto COMO ENTERO
		
        ESCRIBIR "Ingrese la IP de origen:"
        LEER ip
        ESCRIBIR "Ingrese el puerto:"
        LEER puerto
        ESCRIBIR "Ingrese el protocolo (TCP/UDP/ICMP):"
        LEER protocolo
		
        contadorPaquetes <- contadorPaquetes + 1
        ipOrigen[contadorPaquetes] <- ip
        puertoPaquete[contadorPaquetes] <- puerto
        protocoloPaquete[contadorPaquetes] <- protocolo
		
        ESCRIBIR "Paquete registrado correctamente."
FINSUBPROCESO


SUBPROCESO MostrarRegistros()
	SI contadorPaquetes = 0 ENTONCES
		ESCRIBIR "No hay paquetes registrados."
	SINO
		ESCRIBIR "===== REGISTROS DE PAQUETES ====="
		ESCRIBIR "IP Origen | Puerto | Protocolo"
		ESCRIBIR "---------------------------------"
		PARA i <- 1 HASTA contadorPaquetes HACER
			ESCRIBIR ipOrigen[i], " | ", puertoPaquete[i], " | ", protocoloPaquete[i]
		FINPARA
	FINSI
FINSUBPROCESO


SUBPROCESO GenerarAlertas()
	DEFINIR i, j COMO ENTERO
	DEFINIR encontrado COMO LOGICO
	alertas <- 0
	
	PARA i <- 1 HASTA contadorPaquetes HACER
		encontrado <- FALSO
		
		// Verificar IP bloqueada
		PARA j <- 1 HASTA 5 HACER
			SI ipOrigen[i] = ipsBloqueadas[j] ENTONCES
				ESCRIBIR "ALERTA: Paquete bloqueado de IP ", ipOrigen[i]
				encontrado <- VERDADERO
				alertas <- alertas + 1
			FINSI
		FINPARA
		
		// Verificar puertos sospechosos
		SI puertoPaquete[i] = 23 O puertoPaquete[i] = 3389 ENTONCES
			ESCRIBIR "PUERTO SOSPECHOSO DETECTADO: ", puertoPaquete[i]
			alertas <- alertas + 1
		FINSI
	FINPARA
	
	SI alertas = 0 ENTONCES
		ESCRIBIR "No se detectaron amenazas."
	FINSI
FINSUBPROCESO


// ==============================
// MENÚ PRINCIPAL
// ==============================
opcion <- -1

MIENTRAS opcion <> 0 HACER
	ESCRIBIR ""
	ESCRIBIR "===== SIMULADOR DE FIREWALL BASICO ====="
	ESCRIBIR "1) Registrar paquete entrante"
	ESCRIBIR "2) Mostrar registros de paquetes"
	ESCRIBIR "3) Generar alertas"
	ESCRIBIR "0) Salir"
	ESCRIBIR "Seleccione una opcion:"
	LEER opcion
	
	SEGUN opcion HACER
		1:
			RegistrarPaquete()
		2:
			MostrarRegistros()
		3:
			GenerarAlertas()
		0:
			ESCRIBIR "Saliendo del sistema..."
		DE OTRO MODO:
			ESCRIBIR "Opcion no valida. Intente nuevamente."
	FINSEGUN
FINMIENTRAS

FINALGORITMO
