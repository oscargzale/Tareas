ALGORITMO GestorDeContrasenasSeguras
	
    // ==============================
    // VARIABLES Y ESTRUCTURAS
    // ==============================
    DEFINIR usuarios, contrasenas COMO CADENA
    DEFINIR opcion, contador COMO ENTERO
    DEFINIR i COMO ENTERO
    DIMENSION usuarios[100]
    DIMENSION contrasenas[100]
    contador <- 0
	
    // ==============================
    // SUBPROCESOS / FUNCIONES
    // ==============================
	
    SUBPROCESO RegistrarUsuario()
        DEFINIR usuario, contrasena COMO CADENA
        ESCRIBIR "Ingrese el nombre de usuario:"
        LEER usuario
        ESCRIBIR "Ingrese la contraseña:"
        LEER contrasena
		
        contador <- contador + 1
        usuarios[contador] <- usuario
        contrasenas[contador] <- contrasena
		
        ESCRIBIR "Usuario registrado correctamente."
FINSUBPROCESO


FUNCION esFuerte <- VerificarContrasena(contrasena)
	DEFINIR tieneMayus, tieneMinus, tieneNumero COMO LOGICO
	DEFINIR i COMO ENTERO
	DEFINIR caracter COMO CADENA
	
	tieneMayus <- FALSO
	tieneMinus <- FALSO
	tieneNumero <- FALSO
	
	SI LONGITUD(contrasena) < 8 ENTONCES
		esFuerte <- FALSO
		SALIRFUNCION
	FINSI
	
	PARA i <- 1 HASTA LONGITUD(contrasena) HACER
		caracter <- SUBCADENA(contrasena, i, 1)
		SI caracter >= "A" Y caracter <= "Z" ENTONCES
			tieneMayus <- VERDADERO
		FINSI
		SI caracter >= "a" Y caracter <= "z" ENTONCES
			tieneMinus <- VERDADERO
		FINSI
		SI caracter >= "0" Y caracter <= "9" ENTONCES
			tieneNumero <- VERDADERO
		FINSI
	FINPARA
	
	SI tieneMayus Y tieneMinus Y tieneNumero ENTONCES
		esFuerte <- VERDADERO
	SINO
		esFuerte <- FALSO
	FINSI
FINFUNCION


SUBPROCESO GenerarAlertas()
	DEFINIR i COMO ENTERO
	DEFINIR fuerte COMO LOGICO
	SI contador = 0 ENTONCES
		ESCRIBIR "No hay usuarios registrados."
	SINO
		ESCRIBIR "===== ALERTAS DE CONTRASEÑAS ====="
		PARA i <- 1 HASTA contador HACER
			fuerte <- VerificarContrasena(contrasenas[i])
			SI NO fuerte ENTONCES
				ESCRIBIR "ALERTA: La contraseña del usuario ", usuarios[i], " es débil."
			FINSI
		FINPARA
	FINSI
FINSUBPROCESO


SUBPROCESO MostrarUsuarios()
	SI contador = 0 ENTONCES
		ESCRIBIR "No hay usuarios registrados."
	SINO
		ESCRIBIR "===== LISTA DE USUARIOS ====="
		PARA i <- 1 HASTA contador HACER
			ESCRIBIR i, ") ", usuarios[i]
		FINPARA
	FINSI
FINSUBPROCESO

// ==============================
// MENÚ PRINCIPAL
// ==============================
opcion <- -1

MIENTRAS opcion <> 0 HACER
	ESCRIBIR ""
	ESCRIBIR "===== GESTOR DE CONTRASEÑAS SEGURAS ====="
	ESCRIBIR "1) Registrar usuario"
	ESCRIBIR "2) Mostrar usuarios"
	ESCRIBIR "3) Generar alertas de contraseñas débiles"
	ESCRIBIR "0) Salir"
	ESCRIBIR "Seleccione una opción:"
	LEER opcion
	
	SEGUN opcion HACER
		1:
			RegistrarUsuario()
		2:
			MostrarUsuarios()
		3:
			GenerarAlertas()
		0:
			ESCRIBIR "Saliendo del sistema..."
		DE OTRO MODO:
			ESCRIBIR "Opción no válida. Intente nuevamente."
	FINSEGUN
FINMIENTRAS

FINALGORITMO
