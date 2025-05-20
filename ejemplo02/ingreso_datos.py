# Se importan los módulos necesarios 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# IMportamos las clases mapeadas (Club y Jugador) desde el archivo genera_tablas
from genera_tablas import Club, Jugador

# Importamos la cadena de conexión a la base de datos desde configuracion
from configuracion import cadena_base_datos

# Se crea el motor de conexión a la base de datos
engine = create_engine(cadena_base_datos)

# Se crea la clase Session vinculada al engine
Session = sessionmaker(bind=engine)
session = Session()

# Se definen las rutas a los archivos con los datos 
club_file = os.path.join('data', '/home/alex/Escritorio/plataformas_web/taller07-AlexJavierQ/ejemplo02/data/datos_clubs.txt')
jugador_file = os.path.join('data', '/home/alex/Escritorio/plataformas_web/taller07-AlexJavierQ/ejemplo02/data/datos_jugadores.txt')

# Función para cargar los clubes desde el archivo
def cargar_clubes():
    # Abrimos el archivo 'datos_clubs.txt' en modo lectura con codificación UTF-8
    with open(club_file, "r", encoding="utf-8") as file:  
        # Recorremos línea por línea el archivo
        for linea in file:
            # Eliminamos espacios en blanco y saltos de línea, luego indicamos el separador
            datos = linea.strip().split(";")   
            # Separamos los datos de la línea: deben ser 3 (nombre, deporte y fundación)
            nombre, deporte, fundacion = datos
            
            # Creamos una instancia de la clase Club con los valores obtenidos
            club = Club(
                nombre=nombre.strip(),          # Eliminamos espacios al inicio y final
                deporte=deporte.strip(),        # Eliminamos espacios 
                fundacion=int(fundacion.strip())# Convertimos el año de fundación a entero
            )
            
            # Agregamos el club creado a la sesión 
            session.add(club)
    
    # Guardamos todos los clubes añadidos de la sesión a la base de datos
    session.commit()
    
    # Confirmamos mediante el mensaje
    print("Clubes cargados correctamente.")


# Función para cargar los jugadores desde el archivo
def cargar_jugadores():
    # Abrimos el archivo 'datos_jugadores.txt' en modo lectura con codificación UTF-8
    with open(jugador_file, "r", encoding="utf-8") as file:  
        # Recorremos cada línea del archivo
        for linea in file:
            # Limpiamos espacios y separamos los datos por el carácter ';'
            datos = linea.strip().split(";")

            # Se espera que haya 4 datos: club, posición, dorsal y nombre del jugador
            nombre_club, posicion, dorsal, nombre_jugador = datos

            # Buscamos en la base de datos el club al que pertenece este jugador
            club = session.query(Club).filter_by(nombre=nombre_club.strip()).first()

            # Si el club existe, creamos y agregamos el jugador a la sesión
            if club:
                jugador = Jugador(
                    nombre=nombre_jugador.strip(),  # Nombre del jugador
                    dorsal=int(dorsal.strip()),     # Número del dorsal trasnformado a entero
                    posicion=posicion.strip(),      # Posición del jugador
                    club=club                       # Relación con el club encontrado
                )
                session.add(jugador)
            else:
                # Si no se encuentra el club, mostramos una advertencia
                print(f"Club no encontrado: {nombre_club}")
    
    # Guardamos todos los jugadores añadidos en la base de datos
    session.commit()
    print("Jugadores cargados correctamente.")


# Se ejecutan ambas funciones
cargar_clubes()
cargar_jugadores()

