from ui import iniciar_aplicacion
from db import crear_tabla_peliculas

def run_app():
    """
    Ejecuta la aplicación. Primero crea la tabla de películas en la base de datos,
    luego inicia la aplicación de la interfaz de usuario.
    """
    crear_tabla_peliculas()  # Crea la tabla de películas en la base de datos
    iniciar_aplicacion()  # Inicia la interfaz de usuario de la aplicación

if __name__ == "__main__":
    # Punto de entrada de la aplicación. Ejecuta la función run_app si el script se está ejecutando directamente.
    run_app()

