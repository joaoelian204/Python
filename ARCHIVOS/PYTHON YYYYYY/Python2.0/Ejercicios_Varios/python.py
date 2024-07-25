def operacion(a:int, b:int, c=0):
    """
    La funcion verifica si a es mayor a b si esto es verdad se resliza la resta de a - b, caso
    contrario se resta b - a
    Luego verifica si c es mayor que 0, si se cumple el resultado de la resta se multiplica por c
    los valores son enteros 
    a(int)
    b(int)
    c(int)
    """
    r = 0
    if a > b: 
        r = a - b
    else:
        r = b - a
    if c > 0:
        r *= c
    return a + b + r 

def i(v):
    num = (input(f"{v}: "))
    while True:
        if num.isnumeric():
            break
        num = (input(f"{v}: "))
    return int(num)
def ic(v):
    num = (input(f"{v}: "))
    while True:
        if num.isnumeric():
            return int(num)
            break
        elif num == "":
            return 0
            break
        num = (input(f"{v}: "))


print(operacion(a=i("valor de a"), b=i("valor de b"), c=ic("valor de c")))