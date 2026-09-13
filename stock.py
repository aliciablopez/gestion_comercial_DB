# stock.py

import tkinter as tk
from tkinter import messagebox, ttk

# Importamos las funciones de la bóveda (base de datos)
from database import (
    actualizar_producto,
    eliminar_producto,
    insertar_producto,
    obtener_productos,
)


class Stock:

    def __init__(self, pestana):
        # Guardamos la referencia a la pestaña de la interfaz donde se dibuja este módulo
        self.pestana = pestana

        # ----------------------------------------------------------------------
        # 1. FORMULARIO DE ENTRADA (CAMPOS DE TEXTO Y ETIQUETAS)
        # ----------------------------------------------------------------------

        # Campo para el Nombre del Producto
        tk.Label(self.pestana, text="Producto:").grid(
            row=0, column=0, padx=5, pady=4, sticky="e"
        )
        self.caja_nombre = tk.Entry(self.pestana, width=25)
        self.caja_nombre.grid(row=0, column=1, padx=5, pady=4)

        # Campo para el Precio Unitario
        tk.Label(self.pestana, text="Precio:").grid(
            row=1, column=0, padx=5, pady=4, sticky="e"
        )
        self.caja_precio = tk.Entry(self.pestana, width=25)
        self.caja_precio.grid(row=1, column=1, padx=5, pady=4)

        # Campo para la Cantidad en Stock
        tk.Label(self.pestana, text="Stock:").grid(
            row=2, column=0, padx=5, pady=4, sticky="e"
        )
        self.caja_stock = tk.Entry(self.pestana, width=25)
        self.caja_stock.grid(row=2, column=1, padx=5, pady=4)

        # Variable auxiliar para guardar el ID del elemento seleccionado
        self.id_seleccionado = None

        # ----------------------------------------------------------------------
        # 2. TABLA VISUAL (TREEVIEW)
        # ----------------------------------------------------------------------
        # Definimos las columnas que se mostrarán en pantalla
        columnas = ("ID", "Producto", "Precio", "Stock", "Estado Stock")
        self.tabla = ttk.Treeview(
            self.pestana, columns=columnas, show="headings", height=10
        )

        # Configuramos los anchos de cada columna
        anchos = [50, 200, 100, 80, 120]
        for idx, col in enumerate(columnas):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=anchos[idx], anchor="center")

        # Ubicamos la tabla dentro de la pestaña usando la grilla
        self.tabla.grid(
            row=4, column=0, columnspan=5, padx=15, pady=(10, 15), sticky="ew"
        )

        # ----------------------------------------------------------------------
        # 3. BOTONES DE ACCIÓN
        # ----------------------------------------------------------------------
        # Botón Guardar: inserta un nuevo producto en la base de datos
        tk.Button(
            self.pestana, text="Guardar", command=self.guardar_datos, width=14
        ).grid(row=0, column=4, padx=15, pady=2, sticky="w")

        # Botón Modificar: actualiza los valores del producto seleccionado
        tk.Button(
            self.pestana, text="Modificar", command=self.modificar_datos, width=14
        ).grid(row=1, column=4, padx=15, pady=2, sticky="w")

        # Botón Eliminar: borra el producto seleccionado de la base de datos
        tk.Button(
            self.pestana, text="Eliminar", command=self.eliminar_datos, width=14
        ).grid(row=2, column=4, padx=15, pady=2, sticky="w")

        # Botón Refrescar: fuerza la recarga de los datos de la base de datos a la tabla
        tk.Button(
            self.pestana, text="Refrescar", command=self.cargar_datos_en_tabla, width=14
        ).grid(row=3, column=4, padx=15, pady=2, sticky="w")

        # Carga inicial de datos al abrir el programa por primera vez
        self.cargar_datos_en_tabla()

    # --------------------------------------------------------------------------
    # 4. MÉTODOS DE LA CLASE (LÓGICA INTERNA)
    # --------------------------------------------------------------------------

    def cargar_datos_en_tabla(self):
        """Limpia la tabla visual y la vuelve a llenar con los datos actualizados de la base de datos."""
        # Paso A: Borramos todas las filas actuales de la tabla en pantalla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Paso B: Consultamos los datos actualizados en la base de datos
        productos = obtener_productos()

        # Paso C: Recorremos los registros devueltos y los insertamos en la tabla
        for p in productos:
            # Evaluación del stock de seguridad (límite: 5 unidades o menos)
            estado = "REPONER" if p["stock"] <= 5 else "OK"

            self.tabla.insert(
                "",
                "end",
                values=(
                    p["id"],
                    p["nombre"],
                    f"$ {p['precio']:.2f}",
                    p["stock"],
                    estado,
                ),
            )

    def limpiar_campos(self):
        """Vacía las cajas de texto del formulario para permitir un nuevo ingreso."""
        self.caja_nombre.delete(0, tk.END)
        self.caja_precio.delete(0, tk.END)
        self.caja_stock.delete(0, tk.END)
        self.id_seleccionado = None

    def guardar_datos(self):
        """Lee el formulario, valida las entradas e inserta un registro nuevo."""
        nombre = self.caja_nombre.get().strip()
        precio = self.caja_precio.get().strip()
        stock = self.caja_stock.get().strip()

        # Validación de campos vacíos
        if not nombre or not precio or not stock:
            messagebox.showerror(
                "Error", "Todos los campos son obligatorios.", parent=self.pestana
            )
            return

        # Validación de tipos numericos
        try:
            precio_num = float(precio)
            stock_num = int(stock)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Precio debe ser un numero y Stock un entero.",
                parent=self.pestana,
            )
            return

        # Intento de inserción en la base de datos
        if insertar_producto(nombre, precio_num, stock_num):
            messagebox.showinfo(
                "Exito", "Producto guardado correctamente.", parent=self.pestana
            )
            self.limpiar_campos()
            self.cargar_datos_en_tabla()
        else:
            messagebox.showerror(
                "Error", "No se pudo guardar el producto.", parent=self.pestana
            )

    def modificar_datos(self):
        """Actualiza la información del producto seleccionado en la tabla."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Atencion",
                "Selecciona un producto de la tabla.",
                parent=self.pestana,
            )
            return

        # Obtenemos los valores de la fila seleccionada
        valores = self.tabla.item(seleccion[0], "values")
        id_prod = valores[0]

        nombre = self.caja_nombre.get().strip()
        precio = self.caja_precio.get().strip().replace("$", "")
        stock = self.caja_stock.get().strip()

        # Intento de actualización en la base de datos
        if actualizar_producto(id_prod, nombre, float(precio), int(stock)):
            messagebox.showinfo(
                "Exito", "Producto actualizado correctamente.", parent=self.pestana
            )
            self.limpiar_campos()
            self.cargar_datos_en_tabla()
        else:
            messagebox.showerror(
                "Error", "No se pudo actualizar el producto.", parent=self.pestana
            )

    def eliminar_datos(self):
        """Elimina de la base de datos el producto seleccionado en la tabla."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Atencion",
                "Selecciona un producto para eliminar.",
                parent=self.pestana,
            )
            return

        valores = self.tabla.item(seleccion[0], "values")
        id_prod = valores[0]

        # Intento de eliminación en la base de datos
        if eliminar_producto(id_prod):
            messagebox.showinfo(
                "Exito", "Producto eliminado correctamente.", parent=self.pestana
            )
            self.limpiar_campos()
            self.cargar_datos_en_tabla()
        else:
            messagebox.showerror(
                "Error", "No se pudo eliminar el producto.", parent=self.pestana
            )