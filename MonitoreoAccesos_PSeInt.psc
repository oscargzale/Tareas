Algoritmo MonitoreoAccesos_PSeInt
    // ========================================
    // Constantes y estructuras principales
    // ========================================
    Const MAX_INTENTOS <- 500
	
    Dimension usuarios[4]
    Dimension servidores[3]
    Dimension intentos[MAX_INTENTOS,5] // Cada fila: usuario, servidor, ip, tipo, hora
    Definir contadorIntentos Como Entero
    contadorIntentos <- 0
	
    // Inicializar usuarios y servidores de ejemplo
    usuarios[1] <- "alice"
    usuarios[2] <- "bob"
    usuarios[3] <- "charlie"
    usuarios[4] <- "david"
	
    servidores[1] <- "web01"
    servidores[2] <- "db01"
    servidores[3] <- "mail01"
	
	
    // ========================================
    // SubAlgoritmos
    // ========================================
	
    SubAlgoritmo RegistrarIntento(u, s, ip, tipo)
        Si contadorIntentos < MAX_INTENTOS Entonces
            contadorIntentos <- contadorIntentos + 1
            intentos[contadorIntentos,1] <- u
            intentos[contadorIntentos,2] <- s
            intentos[contadorIntentos,3] <- ip
            intentos[contadorIntentos,4] <- tipo
            intentos[contadorIntentos,5] <- "t" & ConvertirATexto(contadorIntentos)
            Escribir("? Intento registrado correctamente.")
        SiNo
            Escribir("?? Error: matriz de intentos llena.")
        FinSi
FinSubAlgoritmo


SubAlgoritmo MostrarReporte()
	Si contadorIntentos = 0 Entonces
		Escribir("No hay intentos registrados.")
		Regresar
	FinSi
	Escribir("===== REPORTE DE ACCESOS =====")
	Escribir("Usuario | Servidor | IP | Tipo | Hora")
	Escribir("------------------------------------------------------")
	Para i <- 1 Hasta contadorIntentos Hacer
		Escribir(intentos[i,1], " | ", intentos[i,2], " | ", intentos[i,3], " | ", intentos[i,4], " | ", intentos[i,5])
	FinPara
FinSubAlgoritmo


SubAlgoritmo GenerarAlertas()
	Definir ipsContadas[MAX_INTENTOS,2] Como Cadena
	Definir ipsCount, i, j, encontrado, alertas Como Entero
	ipsCount <- 0
	alertas <- 0
	
	// Contar intentos por IP
	Para i <- 1 Hasta contadorIntentos Hacer
		ipAct <- intentos[i,3]
		encontrado <- 0
		Para j <- 1 Hasta ipsCount Hacer
			Si ipsContadas[j,1] = ipAct Entonces
				ipsContadas[j,2] <- ConvertirATexto(ConvertirAEntero(ipsContadas[j,2]) + 1)
				encontrado <- 1
				Salir Para
                FinSi
            FinPara
            Si encontrado = 0 Entonces
                ipsCount <- ipsCount + 1
                ipsContadas[ipsCount,1] <- ipAct
                ipsContadas[ipsCount,2] <- "1"
            FinSi
        FinPara
		
        // Mostrar IPs sospechosas (>3 intentos)
        Para j <- 1 Hasta ipsCount Hacer
            Si ConvertirAEntero(ipsContadas[j,2]) > 3 Entonces
                Escribir("?? IP sospechosa: ", ipsContadas[j,1], " con ", ipsContadas[j,2], " intentos.")
                alertas <- alertas + 1
            FinSi
        FinPara
		
        // Contar intentos fallidos por usuario
        Definir userFails[MAX_INTENTOS,2] Como Cadena
        Definir usersCount Como Entero
        usersCount <- 0
		
        Para i <- 1 Hasta contadorIntentos Hacer
            usuarioAct <- intentos[i,1]
            tipo <- Minusculas(intentos[i,4])
            Si tipo = "fallido" Entonces
                encontrado <- 0
                Para j <- 1 Hasta usersCount Hacer
                    Si userFails[j,1] = usuarioAct Entonces
                        userFails[j,2] <- ConvertirATexto(ConvertirAEntero(userFails[j,2]) + 1)
                        encontrado <- 1
                        Salir Para
						FinSi
					FinPara
					Si encontrado = 0 Entonces
						usersCount <- usersCount + 1
						userFails[usersCount,1] <- usuarioAct
						userFails[usersCount,2] <- "1"
					FinSi
				FinSi
			FinPara
			
			Para j <- 1 Hasta usersCount Hacer
				Si ConvertirAEntero(userFails[j,2]) > 2 Entonces
					Escribir("?? Usuario con múltiples fallos: ", userFails[j,1], " (", userFails[j,2], " intentos).")
					alertas <- alertas + 1
				FinSi
			FinPara
			
			Si alertas = 0 Entonces
				Escribir("? No se detectaron alertas.")
			FinSi
FinSubAlgoritmo


// ========================================
// PROGRAMA PRINCIPAL
// ========================================

Definir opcion Como Entero
opcion <- -1

Mientras opcion <> 0 Hacer
	E
