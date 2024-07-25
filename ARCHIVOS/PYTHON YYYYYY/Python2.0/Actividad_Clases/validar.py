def validar_entrada(valor: str, tipo: str):# Función para validar la entrada del usuario.
    while True:
        entrada = input(f"{valor}")
        if tipo == "num" and entrada.isdigit():
            return int(entrada)
        elif tipo == "str" and not entrada.isdigit():
            return entrada.title().strip()
        else:
            mensaje = "Solo se aceptan " + ("números" if tipo == "num" else "texto")
            print(f"{mensaje}, ¡{valor}!")
