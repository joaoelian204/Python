import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import database as db

class GestorDeInventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Inventarios")

        self.categorias = ["Granos", "Bebidas", "Pastas"]

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        self.label = tk.Label(self.main_frame, text="Gestor de Inventarios", font=("Arial", 16))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.btn_agregar = tk.Button(self.main_frame, text="Agregar producto", command=self.agregar_producto)
        self.btn_agregar.grid(row=1, column=0, pady=5)

        self.btn_eliminar = tk.Button(self.main_frame, text="Eliminar producto", command=self.eliminar_producto)
        self.btn_eliminar.grid(row=2, column=0, pady=5)

        self.btn_mostrar = tk.Button(self.main_frame, text="Mostrar productos", command=self.mostrar_productos)
        self.btn_mostrar.grid(row=3, column=0, pady=5)

        self.btn_ver_eliminados = tk.Button(self.main_frame, text="Ver productos eliminados", command=self.mostrar_todos_los_eliminados)
        self.btn_ver_eliminados.grid(row=4, column=0, pady=5)

        self.btn_buscar = tk.Button(self.main_frame, text="Mostrar todos los productos y buscar", command=self.mostrar_todos_los_productos_y_buscar)
        self.btn_buscar.grid(row=5, column=0, pady=5)

        self.btn_salir = tk.Button(self.main_frame, text="Salir", command=self.root.quit)
        self.btn_salir.grid(row=6, column=0, pady=5)

    def seleccionar_categoria(self):
        categoria = simpledialog.askstring("Categoría", "Ingrese la categoría (Granos, Bebidas, Pastas):")
        if categoria in self.categorias:
            return categoria
        else:
            messagebox.showerror("Error", "Categoría no válida.")
            return None

    def agregar_producto(self):
        categoria = self.seleccionar_categoria()
        if categoria:
            cantidad = simpledialog.askinteger("Cantidad", "Cuantos productos va a ingresar:")
            for _ in range(cantidad):
                nombre_producto = simpledialog.askstring("Producto", "Ingrese nuevo producto:")
                db.insertar_producto_db(nombre_producto, categoria)
            messagebox.showinfo("Éxito", f"Se ha añadido correctamente los productos ingresados a la categoría {categoria}")

    def eliminar_producto(self):
        categoria = self.seleccionar_categoria()
        if categoria:
            productos = db.mostrar_productos_db()
            producto_a_eliminar = simpledialog.askstring("Eliminar producto", "Ingrese el nombre del producto a eliminar:")
            db.cursorBD.execute("SELECT * FROM PRODUCTO WHERE NOMBRE = ? AND CATEGORIA = ?", (producto_a_eliminar, categoria))
            producto = db.cursorBD.fetchone()
            if producto:
                db.eliminar_producto_db(producto[0])
                messagebox.showinfo("Éxito", f"El producto '{producto_a_eliminar}' ha sido eliminado de la categoría {categoria}")
            else:
                messagebox.showerror("Error", f"El producto '{producto_a_eliminar}' no se encontró en la categoría {categoria}")

    def mostrar_productos(self):
        categoria = self.seleccionar_categoria()
        if categoria:
            productos = db.mostrar_productos_db()
            ventana_productos = tk.Toplevel(self.root)
            ventana_productos.title(f"Productos - {categoria}")

            tree = ttk.Treeview(ventana_productos, columns=("ID", "Nombre", "Categoría"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Nombre", text="Nombre")
            tree.heading("Categoría", text="Categoría")
            tree.pack(fill="both", expand=True)

            for producto in productos:
                if producto[2] == categoria:
                    tree.insert("", "end", values=(producto[0], producto[1], producto[2]))

    def mostrar_todos_los_productos_y_buscar(self):
        productos = db.mostrar_productos_db()
        ventana_productos = tk.Toplevel(self.root)
        ventana_productos.title("Todos los productos")

        tree = ttk.Treeview(ventana_productos, columns=("ID", "Nombre", "Categoría"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Categoría", text="Categoría")
        tree.pack(fill="both", expand=True)

        for producto in productos:
            tree.insert("", "end", values=(producto[0], producto[1], producto[2]))

        producto_a_buscar = simpledialog.askstring("Buscar producto", "Ingrese el producto a buscar:")
        encontrados = [p for p in productos if p[1].lower() == producto_a_buscar.lower()]
        if encontrados:
            messagebox.showinfo("Encontrado", f"El producto '{producto_a_buscar}' se encuentra {len(encontrados)} veces en el inventario.")
        else:
            messagebox.showinfo("No encontrado", f"El producto '{producto_a_buscar}' no se encuentra en el inventario.")

    def mostrar_todos_los_eliminados(self):
        productos_eliminados = db.mostrar_todos_los_eliminados_db()
        ventana_productos_eliminados = tk.Toplevel(self.root)
        ventana_productos_eliminados.title("Productos eliminados")

        tree = ttk.Treeview(ventana_productos_eliminados, columns=("ID", "Nombre", "Categoría", "Fecha de eliminación"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Categoría", text="Categoría")
        tree.heading("Fecha de eliminación", text="Fecha de eliminación")
        tree.pack(fill="both", expand=True)

        for producto in productos_eliminados:
            tree.insert("", "end", values=(producto[0], producto[1], producto[2], producto[3]))

