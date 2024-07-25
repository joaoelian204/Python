import sqlite3
import datetime

# Conectar a la base de datos (o crearla si no existe)
conexion = sqlite3.connect('reservas.db')
cursor = conexion.cursor()

# Crear la tabla de reservas si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    apellido TEXT,
    fecha TEXT,
    hora TEXT,
    personas INTEGER,
    fecha_registro TEXT
)
''')
conexion.commit()

def validar_entrada(mensaje: str, tipo: str) -> str:
    while True:
        entrada = input(mensaje) 
        if tipo == "num" and entrada.isdigit():
            return int(entrada)
        elif tipo == "str" and not entrada.isdigit():
            return entrada.title().strip()
        else:
            print(f"Solo se aceptan {('números' if tipo == 'num' else 'texto')}")

def RegistroReserva():
    print("\nHaga su reserva\n") 
    veces = validar_entrada("Cuantas reservas va a realizar: ", "num")
    print("\n")
    for i in range(veces):
        print(f"Reserva #{i+1}\n")
        nombre = validar_entrada("Ingrese su nombre: ", "str").lower()
        apellido = validar_entrada("Ingrese su apellido: ", "str").lower()
        fecha = validar_entrada("Ingrese la fecha de la reserva: ", "str")
        hora = validar_entrada("Ingrese la hora de la reserva: ", "str")
        personas = validar_entrada("Ingrese el número de personas: ", "num")
        fecha_registro = datetime.date.today().isoformat()

        # Insertar la reserva en la base de datos
        cursor.execute('''
            INSERT INTO reservas (nombre, apellido, fecha, hora, personas, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, fecha, hora, personas, fecha_registro))
        conexion.commit()

        print(f"\nReserva realizada por {nombre.title()} {apellido.title()} para el {fecha} a las {hora} para {personas} personas.\n")
    print("\n--Todas las reservas han sido realizadas con éxito")

def BuscarReservaPorFecha():
    fecha_buscar = validar_entrada("\nIngrese la fecha de la reserva que desea buscar: ", "str")
    cursor.execute('''
        SELECT id, nombre, apellido, fecha, hora, personas, fecha_registro
        FROM reservas
        WHERE fecha = ?
    ''', (fecha_buscar,))
    reservas_encontradas = cursor.fetchall()
    
    if reservas_encontradas:
        print(f"\nReservas encontradas para la fecha {fecha_buscar}:")
        for reserva in reservas_encontradas:
            print(f"\n >> ID: {reserva[0]} - {reserva[1].title()} {reserva[2].title()} - Fecha: {reserva[3]} - Hora: {reserva[4]} - Personas: {reserva[5]} - Fecha de registro: {reserva[6]}")
        
        while True:
            print("\n¿Qué desea hacer?\n1. Modificar una reserva\n2. Eliminar una reserva\n3. Regresar al menú principal\n")
            opcion = validar_entrada("Seleccione una opción: ", "num")
            if opcion == 1:
                metodo_busqueda = validar_entrada("¿Desea modificar por nombre o ID? (nombre/id): ", "str").lower()
                if metodo_busqueda == "nombre":
                    nombre_buscar = validar_entrada("Ingrese el nombre de la reserva que desea modificar: ", "str").lower()
                    cursor.execute('SELECT * FROM reservas WHERE LOWER(nombre) = ?', (nombre_buscar,))
                    reservas = cursor.fetchall()
                    
                    if reservas:
                        print(f"\nReservas encontradas para {nombre_buscar.title()}:")
                        for reserva in reservas:
                            print(f"\n >> ID: {reserva[0]} - {reserva[1].title()} {reserva[2].title()} - Fecha: {reserva[3]} - Hora: {reserva[4]} - Personas: {reserva[5]}")
                        
                        reserva_id = validar_entrada("Ingrese el ID de la reserva que desea modificar: ", "num")
                        cursor.execute('SELECT * FROM reservas WHERE id = ?', (reserva_id,))
                        reserva = cursor.fetchone()
                        
                        if reserva:
                            while True:
                                print("\n¿Qué desea modificar?\n1. Nombre\n2. Apellido\n3. Fecha\n4. Hora\n5. Número de personas\n6. Regresar\n")
                                opcion_modificar = validar_entrada("Seleccione una opción: ", "num")
                                if opcion_modificar == 1:
                                    nuevo_nombre = validar_entrada("Ingrese el nuevo nombre: ", "str").lower()
                                    cursor.execute('UPDATE reservas SET nombre = ? WHERE id = ?', (nuevo_nombre, reserva_id))
                                elif opcion_modificar == 2:
                                    nuevo_apellido = validar_entrada("Ingrese el nuevo apellido: ", "str").lower()
                                    cursor.execute('UPDATE reservas SET apellido = ? WHERE id = ?', (nuevo_apellido, reserva_id))
                                elif opcion_modificar == 3:
                                    nueva_fecha = validar_entrada("Ingrese la nueva fecha: ", "str")
                                    cursor.execute('UPDATE reservas SET fecha = ? WHERE id = ?', (nueva_fecha, reserva_id))
                                elif opcion_modificar == 4:
                                    nueva_hora = validar_entrada("Ingrese la nueva hora: ", "str")
                                    cursor.execute('UPDATE reservas SET hora = ? WHERE id = ?', (nueva_hora, reserva_id))
                                elif opcion_modificar == 5:
                                    nuevas_personas = validar_entrada("Ingrese el nuevo número de personas: ", "num")
                                    cursor.execute('UPDATE reservas SET personas = ? WHERE id = ?', (nuevas_personas, reserva_id))
                                elif opcion_modificar == 6:
                                    break
                                else:
                                    print("\nOpción no válida.")
                                    continue

                                conexion.commit()
                                print("\nReserva modificada con éxito.")
                                cursor.execute('SELECT * FROM reservas WHERE id = ?', (reserva_id,))
                                reserva = cursor.fetchone()
                                print(f"\n >> ID: {reserva[0]} - {reserva[1].title()} {reserva[2].title()} - Fecha: {reserva[3]} - Hora: {reserva[4]} - Personas: {reserva[5]}")
                        else:
                            print(f"\n - No se encontró una reserva con ID {reserva_id}.")
                    else:
                        print(f"\n - No se encontraron reservas para el nombre {nombre_buscar.title()}.")
                elif metodo_busqueda == "id":
                    reserva_id = validar_entrada("Ingrese el ID de la reserva que desea modificar: ", "num")
                    cursor.execute('SELECT * FROM reservas WHERE id = ?', (reserva_id,))
                    reserva = cursor.fetchone()

                    if reserva:
                        while True:
                            print("\n¿Qué desea modificar?\n1. Nombre\n2. Apellido\n3. Fecha\n4. Hora\n5. Número de personas\n6. Regresar\n")
                            opcion_modificar = validar_entrada("Seleccione una opción: ", "num")
                            if opcion_modificar == 1:
                                nuevo_nombre = validar_entrada("Ingrese el nuevo nombre: ", "str").lower()
                                cursor.execute('UPDATE reservas SET nombre = ? WHERE id = ?', (nuevo_nombre, reserva_id))
                            elif opcion_modificar == 2:
                                nuevo_apellido = validar_entrada("Ingrese el nuevo apellido: ", "str").lower()
                                cursor.execute('UPDATE reservas SET apellido = ? WHERE id = ?', (nuevo_apellido, reserva_id))
                            elif opcion_modificar == 3:
                                nueva_fecha = validar_entrada("Ingrese la nueva fecha: ", "str")
                                cursor.execute('UPDATE reservas SET fecha = ? WHERE id = ?', (nueva_fecha, reserva_id))
                            elif opcion_modificar == 4:
                                nueva_hora = validar_entrada("Ingrese la nueva hora: ", "str")
                                cursor.execute('UPDATE reservas SET hora = ? WHERE id = ?', (nueva_hora, reserva_id))
                            elif opcion_modificar == 5:
                                nuevas_personas = validar_entrada("Ingrese el nuevo número de personas: ", "num")
                                cursor.execute('UPDATE reservas SET personas = ? WHERE id = ?', (nuevas_personas, reserva_id))
                            elif opcion_modificar == 6:
                                break
                            else:
                                print("\nOpción no válida.")
                                continue

                            conexion.commit()
                            print("\nReserva modificada con éxito.")
                            cursor.execute('SELECT * FROM reservas WHERE id = ?', (reserva_id,))
                            reserva = cursor.fetchone()
                            print(f"\n >> ID: {reserva[0]} - {reserva[1].title()} {reserva[2].title()} - Fecha: {reserva[3]} - Hora: {reserva[4]} - Personas: {reserva[5]}")
                    else:
                        print(f"\n - No se encontró una reserva con ID {reserva_id}.")
                else:
                    print("\nMétodo de búsqueda no válido.")
            elif opcion == 2:
                print("\n¿Qué desea eliminar?\n1. Eliminar por nombre\n2. Eliminar por ID\n3. Regresar\n")
                opcion_eliminar = validar_entrada("Seleccione una opción: ", "num")
                if opcion_eliminar == 1:
                    nombre_eliminar = validar_entrada("Ingrese el nombre de la reserva que desea eliminar: ", "str").lower()
                    cursor.execute('SELECT * FROM reservas WHERE LOWER(nombre) = ?', (nombre_eliminar,))
                    reservas = cursor.fetchall()
                    
                    if reservas:
                        print(f"\nReservas encontradas para {nombre_eliminar.title()}:")
                        for reserva in reservas:
                            print(f"\n >> ID: {reserva[0]} - {reserva[1].title()} {reserva[2].title()} - Fecha: {reserva[3]} - Hora: {reserva[4]} - Personas: {reserva[5]}")
                        
                        reserva_id = validar_entrada("Ingrese el ID de la reserva que desea eliminar: ", "num")
                        cursor.execute('SELECT * FROM reservas WHERE id = ?', (reserva_id,))
                        reserva = cursor.fetchone()
                        
                        if reserva:
                            confirmacion = validar_entrada(f"¿Está seguro que desea eliminar la reserva de {reserva[1].title()} {reserva[2].title()}? (si/no): ", "str").lower()
                            if confirmacion == 'si':
                                cursor.execute('DELETE FROM reservas WHERE id = ?', (reserva_id,))
                                conexion.commit()
                                print("\nReserva eliminada con éxito.")
                            else:
                                print("\nEliminación cancelada.")
                        else:
                            print(f"\n - No se encontró una reserva con ID {reserva_id}.")
                    else:
                        print(f"\n - No se encontraron reservas para el nombre {nombre_eliminar.title()}.")
                elif opcion_eliminar == 2:
                    reserva_id = validar_entrada("Ingrese el ID de la reserva que desea eliminar: ", "num")
                    cursor.execute('SELECT * FROM reservas WHERE id = ?', (reserva_id,))
                    reserva = cursor.fetchone()

                    if reserva:
                        confirmacion = validar_entrada(f"¿Está seguro que desea eliminar la reserva de {reserva[1].title()} {reserva[2].title()}? (si/no): ", "str").lower()
                        if confirmacion == 'si':
                            cursor.execute('DELETE FROM reservas WHERE id = ?', (reserva_id,))
                            conexion.commit()
                            print("\nReserva eliminada con éxito.")
                        else:
                            print("\nEliminación cancelada.")
                    else:
                        print(f"\n - No se encontró una reserva con ID {reserva_id}.")
                elif opcion_eliminar == 3:
                    break
                else:
                    print("\nOpción no válida.")
            elif opcion == 3:
                break
            else:
                print("\nOpción no válida.")
    else:
        print(f"\n - No se encontraron reservas para la fecha {fecha_buscar}.")

def VerTodasLasReservas():
    cursor.execute('SELECT * FROM reservas')
    reservas = cursor.fetchall()
    
    if reservas:
        print("\nTodas las reservas:")
        for reserva in reservas:
            print(f"\n >> ID: {reserva[0]} - {reserva[1].title()} {reserva[2].title()} - Fecha: {reserva[3]} - Hora: {reserva[4]} - Personas: {reserva[5]} - Fecha de registro: {reserva[6]}")
    else:
        print("\n - No hay reservas registradas.")

def main():
    opcion = {
        1: RegistroReserva,
        2: BuscarReservaPorFecha,
        3: VerTodasLasReservas,
        4: exit
    }
    while True:
        print("\nMenu Principal\n", "\n1. Realizar reserva", "\n2. Buscar reserva por fecha", "\n3. Ver todas las reservas", "\n4. Salir\n")
        
        opcion_elegida = validar_entrada("Seleccione una opción: ", "num")
        funcion = opcion.get(opcion_elegida)
        funcion() if funcion else print("\nOpción no válida")

if __name__ == "__main__":
    main()

# Cerrar la conexión a la base de datos al final del programa
conexion.close()

