from tkinter import *
from tkinter import ttk
import sqlite3


class Product:
    db_name = "database.db"

    def __init__(self, window):
        self.window = window
        self.window.title("Aplicacion de productos")

        # creating a frame container
        frame = LabelFrame(self.window, text="Registrar un nuevo producto")
        frame.grid(row=0, column=0, columnspan=2, pady=20)

        # label and name input
        Label(frame, text="Nombre: ").grid(row=0, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=0, column=1)

        # label and price input
        Label(frame, text="Precio: ").grid(row=1, column=0)
        self.price = Entry(frame)
        self.price.grid(row=1, column=1)

        # button add product
        self.save_button = ttk.Button(frame, text="Guardar Producto", command=self.add_product, cursor="hand1")
        self.save_button.grid(row=2, columnspan=2, sticky="WE")

        # ouput messages
        self.message = Label(self.window, text="mensaje", fg="blue")
        self.message.grid(row=1, columnspan=2, sticky="WE")

        # table
        self.table = ttk.Treeview(self.window, height=10, columns=("#1", "#2"))
        self.table.grid(row=2, column=0, columnspan=2)
        self.table.heading("#0", text="Id")
        self.table.heading("#1", text="Nombre")
        self.table.heading("#2", text="Precio")

        # buttons
        edit_button = ttk.Button(self.window, text="Editar", command=self.edit_product, cursor="hand1")
        edit_button.grid(row=3, column=0, sticky="WE")
        delete_button = ttk.Button(self.window, text="Eliminar", command=self.delete_product, cursor="hand1")
        delete_button.grid(row=3, column=1, sticky="WE")

        # filling the rows
        self.get_products()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()  # obtenemos un cursor a la conexion
            result = cursor.execute(query, parameters)  # ejecutamos una consulta
            conn.commit()  # guardamos los cambios
        return result

    def get_products(self):
        # Limpiando tabla
        records = self.table.get_children()
        for element in records:
            self.table.delete(element)
        # Hacer consulta
        query = "SELECT * FROM products ORDER BY name ASC"
        rows = self.run_query(query)  # obtengo las filas
        for row in rows:
            self.table.insert("", END, text=row[0], values=(row[1], row[2]))

    def add_product(self):
        if self.validation_product():
            query = "INSERT INTO products VALUES(NULL, ?, ?)"
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message["text"] = f"El producto {self.name.get()} ha sido agregado"
            self.message["fg"] = "green"
            self.name.delete(0, END)  # limpiamos la caja de texto name
            self.price.delete(0, END)  # limpiamos la caja de texto price
        else:
            self.message["text"] = "El nombre y el precio son requeridos"
            self.message["fg"] = "red"
        self.get_products()  # refrescamos los productos

    def validation_product(self):
        # validar si el campo name y price no estan vacios
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def delete_product(self):
        id_item = self.table.item(self.table.selection())["text"]
        if id_item:
            name_product = self.table.item(self.table.selection())["values"][0]
            query = "DELETE FROM products WHERE id = ?"
            self.run_query(query, (id_item,))
            self.message["text"] = f"El producto {name_product} ha sido eliminado"
            self.get_products()
        else:
            self.message["text"] = "Seleccione un item a eliminar"
            self.message["fg"] = "red"
            return

    def edit_product(self):
        id_item = self.table.item(self.table.selection())["text"]

        if id_item:
            name = self.table.item(self.table.selection())["values"][0]
            price = self.table.item(self.table.selection())["values"][1]

            self.edit_window = Toplevel()
            self.edit_window.title("Editar Producto")

            Label(self.edit_window, text="Nombre").grid(row=0, column=0)
            new_name = Entry(self.edit_window, textvariable=StringVar(value=name))
            new_name.grid(row=0, column=1)

            Label(self.edit_window, text="Precio").grid(row=1, column=0)
            new_price = Entry(self.edit_window, textvariable=IntVar(value=price))
            new_price.grid(row=1, column=1)

            update_button = Button(
                self.edit_window,
                text="Update",
                command=lambda:self.edit_records(new_name.get(), new_price.get(), id_item)
            )
            update_button.grid(row=2, columnspan=2)
        else:
            self.message["text"] = "Seleccione un item a editar"
            self.message["fg"] = "red"
            return

    def edit_records(self, new_name, new_price, id_item):
        query = "UPDATE products SET name = ?, price = ? WHERE id = ?"
        parameters = (new_name, new_price, id_item)
        self.run_query(query, parameters)
        self.edit_window.destroy()
        self.message["text"] = f"Record {new_name} update successfully"
        self.message["fg"] = "green"
        self.get_products()


if __name__ == "__main__":
    window = Tk()
    application = Product(window)
    window.mainloop()
