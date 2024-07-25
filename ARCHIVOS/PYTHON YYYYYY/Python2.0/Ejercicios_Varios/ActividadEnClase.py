#validacion de entrada
def validar_entrada(valor: str, tipo: str) -> str:
    while True:
        entrada = input(f"{valor}: ")
        if tipo == "num" and entrada.isdigit():
            return int(entrada)
        elif tipo == "str" and not entrada.isdigit():
            return entrada
        else:
            mensaje = "Solo se aceptan " + ("números" if tipo == "num" else "texto")
            print(f"{mensaje}, ¡{valor}! :")


#SE inicia las listas           
nombres = [];
identificaciones = [];

tam = validar_entrada("Digite valor: ", "num");
#Se ingresa ingresa datos
for x in range(tam):
    print("Ingrese los datos de la personas", x +1);
    nombre = validar_entrada("Nombre: ", "str");
    identificacion = validar_entrada("Identificacion: ", "num");
    
    #Se ingresa los datos a las listas
    nombres.append(nombre);
    identificaciones.append(identificacion);
    
    #INteramos la lista con un for
for i in range(tam):
    print("Montrando los datos de las personas", i +1);
    
    print(f"Nombre:  {nombres[i]}" );
    print(f"Identificacion: {identificaciones[i]}");