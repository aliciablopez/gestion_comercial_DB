# stock.py

import tkinter as tk
from tkinter import messagebox, ttk

from database import (
    actualizar_producto,
    eliminar_producto,
    insertar_producto,
    obtener_productos,
)


class Stock:

    def __init__(self, pestana):
        self.pestana = pestana

        # ======================================================================
        # 1. FORMULARIO DE ENTRADA DE PRODUCTOS
        # ======================================================================
        tk.Label(self.pestana, text="Nombre:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.txt_nombre = tk.Entry(self.pestana, width=25)
        self.txt_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.pestana, text="Precio:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.txt_precio = tk.Entry(self.pestana, width=25)
        self.txt_precio.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.pestana, text="Stock:").grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )
        self.txt_stock = tk.Entry(self.pestana, width=25)
        self.txt_stock.grid(row=2, column=1, padx=5, pady=5)

        # ======================================================================
        # 2. BOTONES DE ACCIÓN (COLUMNA DERECHA)
        # ======================================================================
        tk.Button(
            self.pestana,
            text="Agregar",
            command=self.agregar_datos,
            width=14,
        ).grid(row=0, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Modificar",
            command=self.modificar_datos,
            width=14,
        ).grid(row=1, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Eliminar",
            command=self.eliminar_datos,
            width=14,
        ).grid(row=2, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Limpiar",
            command=self.limpiar_campos,
            width=14,
        ).grid(row=3, column=4, padx=15, pady=2, sticky="w")

        # ======================================================================
        # 3. TABLA DE PRODUCTOS (TREEVIEW)
        # ======================================================================
        columnas = ("ID", "Nombre", "Precio", "Stock")
        self.tabla = ttk.Treeview(
            self.pestana, columns=columnas, show="headings", height=12
        )

        anchos = [60, 250, 120, 100]
        for idx, col in enumerate(columnas):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=anchos[idx], anchor="center")

        self.tabla.grid(
            row=5, column=0, columnspan=5, padx=15, pady=15, sticky="ew"
        )

        # Configuración de alerta visual para stock bajo (menos de 5 unidades)
        self.tabla.tag_configure(
            "alerta_stock", background="#FFCCCC", foreground="black"
        )

        # Cargar los datos almacenados al iniciar
        self.cargar_datos_en_tabla()

    # ==========================================================================
    # MÉTODOS Y LÓGICA DE GESTIÓN DE STOCK
    # ==========================================================================

    def cargar_datos_en_tabla(self):
        """Limpia y recarga la tabla con los productos de la base de datos."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        productos = obtener_productos()
        for p in productos:
            tags = ()
            if p["stock"] <= 5:
                tags = ("alerta_stock",)

            self.tabla.insert(
                "",
                "end",
                values=(
                    p["id"],
                    p["nombre"],
                    f"$ {p['precio']:.2f}",
                    p["stock"],
                ),
                tags=tags,
            )

    def limpiar_campos(self):
        """Limpia los campos del formulario principal."""
        self.txt_nombre.delete(0, tk.END)
        self.txt_precio.delete(0, tk.END)
        self.txt_stock.delete(0, tk.END)

    def agregar_datos(self):
        """Registra un nuevo producto en la base de datos."""
        nombre = self.txt_nombre.get().strip()
        precio_str = self.txt_precio.get().strip()
        stock_str = self.txt_stock.get().strip()

        if not nombre or not precio_str or not stock_str:
            messagebox.showerror(
                "Error",
                "Todos los campos son obligatorios.",
                parent=self.pestana,
            )
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
            if precio < 0 or stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error",
                "El precio y el stock deben ser valores numéricos positivos.",
                parent=self.pestana,
            )
            return

        if insertar_producto(nombre, precio, stock):
            messagebox.showinfo(
                "Éxito",
                "Producto guardado correctamente.",
                parent=self.pestana,
            )
            self.limpiar_campos()
            self.cargar_datos_en_tabla()
        else:
            messagebox.showerror(
                "Error",
                "No se pudo guardar el producto.",
                parent=self.pestana,
            )

    def modificar_datos(self):
        """Abre una ventana emergente (Toplevel) para modificar el producto seleccionado."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Atención",
                "Selecciona un producto de la tabla para modificar.",
                parent=self.pestana,
            )
            return

        valores = self.tabla.item(seleccion[0], "values")
        id_prod = valores[0]
        nombre_actual = valores[1]
        precio_actual = valores[2].replace("$", "").strip()
        stock_actual = valores[3]

        # Ventana emergente (Toplevel)
        ventana_editar = tk.Toplevel(self.pestana)
        ventana_editar.title("Modificar Producto")
        ventana_editar.geometry("300x200")
        ventana_editar.resizable(False, False)

        ventana_editar.transient(self.pestana)
        ventana_editar.grab_set()

        tk.Label(ventana_editar, text="Nombre:").grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )
        txt_nom = tk.Entry(ventana_editar, width=20)
        txt_nom.grid(row=0, column=1, padx=10, pady=10)
        txt_nom.insert(0, nombre_actual)

        tk.Label(ventana_editar, text="Precio:").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        txt_pre = tk.Entry(ventana_editar, width=20)
        txt_pre.grid(row=1, column=1, padx=10, pady=10)
        txt_pre.insert(0, precio_actual)

        tk.Label(ventana_editar, text="Stock:").grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )
        txt_stk = tk.Entry(ventana_editar, width=20)
        txt_stk.grid(row=2, column=1, padx=10, pady=10)
        txt_stk.insert(0, stock_actual)

        tk.Button(
            ventana_editar,
            text="Guardar Cambios",
            command=lambda: self.confirmar_modificacion(
                ventana_editar, id_prod, txt_nom, txt_pre, txt_stk
            ),
        ).grid(row=3, column=0, columnspan=2, pady=15)

    def confirmar_modificacion(
        self, ventana_popup, id_prod, txt_nom, txt_pre, txt_stk
    ):
        """Procesa los cambios de la ventana emergente y actualiza la base de datos."""
        nombre = txt_nom.get().strip()
        precio_str = txt_pre.get().strip()
        stock_str = txt_stk.get().strip()

        if not nombre or not precio_str or not stock_str:
            messagebox.showerror(
                "Error",
                "Todos los campos son obligatorios.",
                parent=ventana_popup,
            )
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror(
                "Error",
                "El precio debe ser un número y el stock un número entero.",
                parent=ventana_popup,
            )
            return

        if actualizar_producto(id_prod, nombre, precio, stock):
            messagebox.showinfo(
                "Éxito",
                "Producto actualizado correctamente.",
                parent=self.pestana,
            )
            ventana_popup.destroy()
            self.limpiar_campos()
            self.cargar_datos_en_tabla()
        else:
            messagebox.showerror(
                "Error",
                "No se pudo actualizar el producto.",
                parent=ventana_popup,
            )

    def eliminar_datos(self):
        """Elimina el producto seleccionado de la base de datos."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Atención",
                "Selecciona un producto de la tabla para eliminar.",
                parent=self.pestana,
            )
            return

        valores = self.tabla.item(seleccion[0], "values")
        id_prod = valores[0]
        nombre_prod = valores[1]

        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Estás seguro de eliminar el producto '{nombre_prod}'?",
            parent=self.pestana,
        )

        if respuesta:
            if eliminar_producto(id_prod):
                messagebox.showinfo(
                    "Éxito",
                    "Producto eliminado correctamente.",
                    parent=self.pestana,
                )
                self.limpiar_campos()
                self.cargar_datos_en_tabla()
            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo eliminar el producto.",
                    parent=self.pestana,
                )