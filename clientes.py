# clientes.py

# Responsabilidad del módulo: Construir y administrar el contenido de la pestaña "Clientes".
# Este módulo NO crea (esa infraestructura pertenece a interfaz.py / main.py)
#   - la ventana principal Tk()
#   - el Notebook
#   - las pestañas

# Este módulo recibe la pestaña correspondiente y construye dentro de ella:
#   1. El formulario de clientes.
#   2. El Treeview para mostrar los registros.
#   3. Las funciones CRUD conectadas a la base de datos SQLite.
#   4. El enlace entre selección y formulario.
#   5. Los botones de operaciones.

# ==============================================================================
# 1. IMPORTACIONES
# ==============================================================================
import tkinter as tk
from tkinter import messagebox, ttk

# Importamos las funciones de persistencia desde la capa de base de datos
from database import (
    actualizar_cliente,
    eliminar_cliente,
    insertar_cliente,
    obtener_clientes,
)


# ==============================================================================
# 2. CLASE CLIENTES
# ==============================================================================
class Clientes:

    def __init__(self, pestana):
        # ----------------------------------------------------------------------
        # RECIBIR LA PESTAÑA
        # "pestana" es un parámetro enviado por main.py.
        # La clase trabaja dentro del espacio que recibió.
        # ----------------------------------------------------------------------
        self.pestana = pestana

        # ==========================================================================
        # 3. FORMULARIO DE CLIENTES
        # ==========================================================================

        # RAZÓN SOCIAL
        tk.Label(self.pestana, text="Razón Social:").grid(
            row=0, column=0, padx=5, pady=4, sticky="e"
        )
        self.caja_razon_social = tk.Entry(self.pestana, width=25)
        self.caja_razon_social.grid(row=0, column=1, padx=5, pady=4)

        # CONTACTO
        tk.Label(self.pestana, text="Contacto:").grid(
            row=1, column=0, padx=5, pady=4, sticky="e"
        )
        self.caja_contacto = tk.Entry(self.pestana, width=25)
        self.caja_contacto.grid(row=1, column=1, padx=5, pady=4)

        # CUIT
        tk.Label(self.pestana, text="CUIT:").grid(
            row=2, column=0, padx=5, pady=4, sticky="e"
        )
        self.caja_cuit = tk.Entry(self.pestana, width=25)
        self.caja_cuit.grid(row=2, column=1, padx=5, pady=4)

        # ==========================================================================
        # 4. TREEVIEW
        # ==========================================================================
        columnas = ("Razón Social", "Contacto", "CUIT")

        self.tabla = ttk.Treeview(
            self.pestana, columns=columnas, show="headings", height=10
        )

        anchos = [250, 200, 150]

        for idx, columna in enumerate(columnas):
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, width=anchos[idx], anchor="center")

        self.tabla.grid(
            row=6,
            column=0,
            columnspan=5,
            padx=15,
            pady=(10, 15),
            sticky="ew",
        )

        # ==========================================================================
        # 5. FUNCIONES AUXILIARES Y CRUD
        # ==========================================================================

        def cargar_tabla_desde_db():
            """Consulta SQLite y puebla la tabla Treeview."""
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            clientes = obtener_clientes()

            for cli in clientes:
                self.tabla.insert(
                    "",
                    "end",
                    iid=cli["id"],
                    values=(
                        cli["razon_social"],
                        cli["contacto"],
                        cli["cuit"],
                    ),
                )

        def limpiar_campos():
            """Vacía los campos de texto del formulario."""
            self.caja_razon_social.delete(0, tk.END)
            self.caja_contacto.delete(0, tk.END)
            self.caja_cuit.delete(0, tk.END)

        def nuevo_cliente():
            """Prepara la interfaz para una nueva entrada."""
            limpiar_campos()
            self.tabla.selection_remove(self.tabla.selection())
            self.caja_razon_social.focus()

        def cargar_datos_seleccionados(event=None):
            """Transfiere los datos de la fila seleccionada a los Entry."""
            seleccion = self.tabla.selection()
            if not seleccion:
                return

            item_id = seleccion[0]
            valores = self.tabla.item(item_id, "values")

            limpiar_campos()
            self.caja_razon_social.insert(0, valores[0])
            self.caja_contacto.insert(0, valores[1])
            self.caja_cuit.insert(0, valores[2])

        def guardar():
            """Inserta un nuevo cliente en SQLite tras validar entradas."""
            razon_social = self.caja_razon_social.get().strip()
            contacto = self.caja_contacto.get().strip()
            cuit = self.caja_cuit.get().strip()

            if not razon_social or not cuit:
                messagebox.showerror(
                    "Error",
                    "Razón Social y CUIT son obligatorios.",
                    parent=self.pestana,
                )
                return

            if not cuit.isdigit():
                messagebox.showerror(
                    "Error",
                    "El CUIT debe contener solamente números.",
                    parent=self.pestana,
                )
                return

            exito = insertar_cliente(razon_social, contacto, cuit)

            if exito:
                messagebox.showinfo(
                    "Éxito", "Cliente guardado.", parent=self.pestana
                )
                limpiar_campos()
                cargar_tabla_desde_db()
            else:
                messagebox.showerror(
                    "Error",
                    "Ya existe un cliente con ese CUIT.",
                    parent=self.pestana,
                )

        def modificar():
            """Despliega ventana emergente para editar el cliente seleccionado."""
            seleccion = self.tabla.selection()
            if not seleccion:
                messagebox.showwarning(
                    "Atención",
                    "Selecciona un cliente de la tabla para modificar.",
                    parent=self.pestana,
                )
                return

            id_cliente = seleccion[0]
            valores = self.tabla.item(id_cliente, "values")

            ventana_edicion = tk.Toplevel(self.pestana)
            ventana_edicion.title("Modificar Cliente")
            ventana_edicion.geometry("400x280")
            ventana_edicion.resizable(False, False)
            ventana_edicion.transient(self.pestana)
            ventana_edicion.grab_set()

            tk.Label(
                ventana_edicion,
                text="Modificar datos del cliente",
                font=("Arial", 12, "bold"),
            ).pack(pady=(15, 10))

            tk.Label(ventana_edicion, text="Razón Social:").pack(
                anchor="w", padx=30
            )
            caja_edicion_razon = tk.Entry(ventana_edicion, width=40)
            caja_edicion_razon.pack(padx=30, pady=(2, 8))
            caja_edicion_razon.insert(0, valores[0])

            tk.Label(ventana_edicion, text="Contacto:").pack(
                anchor="w", padx=30
            )
            caja_edicion_contacto = tk.Entry(ventana_edicion, width=40)
            caja_edicion_contacto.pack(padx=30, pady=(2, 8))
            caja_edicion_contacto.insert(0, valores[1])

            tk.Label(ventana_edicion, text="CUIT:").pack(anchor="w", padx=30)
            caja_edicion_cuit = tk.Entry(ventana_edicion, width=40)
            caja_edicion_cuit.pack(padx=30, pady=(2, 12))
            caja_edicion_cuit.insert(0, valores[2])

            def guardar_modificacion():
                razon_mod = caja_edicion_razon.get().strip()
                contacto_mod = caja_edicion_contacto.get().strip()
                cuit_mod = caja_edicion_cuit.get().strip()

                if not razon_mod or not cuit_mod:
                    messagebox.showerror(
                        "Error",
                        "Razón Social y CUIT son obligatorios.",
                        parent=ventana_edicion,
                    )
                    return

                if not cuit_mod.isdigit():
                    messagebox.showerror(
                        "Error",
                        "El CUIT debe contener solamente números.",
                        parent=ventana_edicion,
                    )
                    return

                exito = actualizar_cliente(
                    id_cliente, razon_mod, contacto_mod, cuit_mod
                )

                if exito:
                    ventana_edicion.destroy()
                    messagebox.showinfo(
                        "Éxito",
                        "El cliente fue modificado correctamente.",
                        parent=self.pestana,
                    )
                    cargar_tabla_desde_db()
                else:
                    messagebox.showerror(
                        "Error",
                        "Ya existe otro cliente con ese CUIT.",
                        parent=ventana_edicion,
                    )

            marco_botones = tk.Frame(ventana_edicion)
            marco_botones.pack(pady=5)

            tk.Button(
                marco_botones,
                text="Guardar cambios",
                command=guardar_modificacion,
                width=16,
            ).pack(side="left", padx=5)

            tk.Button(
                marco_botones,
                text="Cancelar",
                command=ventana_edicion.destroy,
                width=12,
            ).pack(side="left", padx=5)

            caja_edicion_razon.focus()

        def eliminar():
            """Elimina el registro seleccionado tras confirmación del usuario."""
            seleccion = self.tabla.selection()
            if not seleccion:
                messagebox.showwarning(
                    "Atención",
                    "Selecciona un cliente de la tabla para eliminar.",
                    parent=self.pestana,
                )
                return

            id_cliente = seleccion[0]
            valores = self.tabla.item(id_cliente, "values")

            razon_social = valores[0]
            contacto = valores[1]
            cuit = valores[2]

            confirmar = messagebox.askyesno(
                "Confirmar baja",
                f"¿Deseas eliminar el siguiente cliente?\n\n"
                f"Razón Social: {razon_social}\n"
                f"Contacto: {contacto}\n"
                f"CUIT: {cuit}\n\n"
                f"Esta operación no se puede deshacer.",
                parent=self.pestana,
            )

            if confirmar:
                eliminar_cliente(id_cliente)
                limpiar_campos()
                cargar_tabla_desde_db()
                messagebox.showinfo(
                    "Baja realizada",
                    "El cliente fue eliminado correctamente.",
                    parent=self.pestana,
                )

        # ==========================================================================
        # 6. ENLACES Y BOTONES
        # ==========================================================================
        self.tabla.bind("<<TreeviewSelect>>", cargar_datos_seleccionados)

        tk.Button(
            self.pestana,
            text="Nuevo Cliente",
            command=nuevo_cliente,
            width=16,
        ).grid(row=0, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Guardar Cliente",
            command=guardar,
            width=16,
        ).grid(row=1, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Modificar Cliente",
            command=modificar,
            width=16,
        ).grid(row=2, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Eliminar Cliente",
            command=eliminar,
            width=16,
        ).grid(row=3, column=4, padx=15, pady=2, sticky="w")

        # Cargar los datos guardados en SQLite al construir la vista
        cargar_tabla_desde_db()