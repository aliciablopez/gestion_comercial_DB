# proveedores.py

# Responsabilidad del módulo: Construir y administrar el contenido de la pestaña "Proveedores".
# Este módulo NO crea (esa infraestructura pertenece a interfaz.py)
#   - la ventana principal Tk()
#   - el Notebook
#   - las pestañas

# Este módulo recibe la pestaña correspondiente y construye dentro de ella:
#   1. El formulario de proveedores.
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
    actualizar_proveedor,
    eliminar_proveedor,
    insertar_proveedor,
    obtener_proveedores,
)

# ------------------------------------------------------------------------------
# tk: Proporciona los widgets básicos de Tkinter:
#   Label  → etiquetas
#   Entry  → cajas de entrada
#   Button → botones
# ------------------------------------------------------------------------------
# ttk: Proporciona widgets adicionales de Tkinter.
# En este módulo utilizamos Treeview → mostrar los registros de proveedores.
# ------------------------------------------------------------------------------
# messagebox: Permite mostrar mensajes emergentes:
#   showinfo()    → información
#   showwarning() → advertencia
#   showerror()   → error
#   askyesno()    → confirmación


# ==============================================================================
# 2. CLASE PROVEEDORES
# ==============================================================================
class Proveedores:

    def __init__(self, pestana):
        # ----------------------------------------------------------------------
        # RECIBIR LA PESTAÑA
        # "pestana" es un parámetro enviado por interfaz.py.
        # La clase trabaja dentro del espacio que recibió.
        # ----------------------------------------------------------------------

        self.pestana = pestana

        # ==========================================================================
        # 3. FORMULARIO DE PROVEEDORES
        # ==========================================================================

        # ----------------------------------------------------------------------
        # RAZÓN SOCIAL
        # ----------------------------------------------------------------------

        tk.Label(self.pestana, text="Razón Social:").grid(
            row=0, column=0, padx=5, pady=4, sticky="e"
        )

        self.caja_razon_social = tk.Entry(self.pestana, width=25)

        self.caja_razon_social.grid(row=0, column=1, padx=5, pady=4)

        # ----------------------------------------------------------------------
        # CONTACTO
        # ----------------------------------------------------------------------

        tk.Label(self.pestana, text="Contacto:").grid(
            row=1, column=0, padx=5, pady=4, sticky="e"
        )

        self.caja_contacto = tk.Entry(self.pestana, width=25)

        self.caja_contacto.grid(row=1, column=1, padx=5, pady=4)

        # ----------------------------------------------------------------------
        # CUIT
        # ----------------------------------------------------------------------

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

        # ----------------------------------------------------------------------
        # CONFIGURACIÓN DE LAS COLUMNAS
        # ----------------------------------------------------------------------

        anchos = [250, 200, 150]

        for idx, columna in enumerate(columnas):
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, width=anchos[idx], anchor="center")

        # ----------------------------------------------------------------------
        # UBICACIÓN DEL TREEVIEW
        # ----------------------------------------------------------------------

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

        # ----------------------------------------------------------------------
        # CARGAR TABLA DESDE LA BASE DE DATOS (READ)
        # Borra el contenido visual del Treeview y lo vuelve a poblar con
        # la información actualizada que proviene de la base de datos SQLite.
        # ----------------------------------------------------------------------
        def cargar_tabla_desde_db():
            # Limpiamos las filas de la vista previa del Treeview
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            # Consultamos la base de datos
            proveedores = obtener_proveedores()

            # Insertamos cada fila asignando el id de la DB como iid del Treeview
            for prov in proveedores:
                self.tabla.insert(
                    "",
                    "end",
                    iid=prov["id"],
                    values=(
                        prov["razon_social"],
                        prov["contacto"],
                        prov["cuit"],
                    ),
                )

        # ----------------------------------------------------------------------
        # LIMPIAR CAMPOS
        # ----------------------------------------------------------------------

        def limpiar_campos():

            self.caja_razon_social.delete(0, tk.END)

            self.caja_contacto.delete(0, tk.END)

            self.caja_cuit.delete(0, tk.END)

        # ----------------------------------------------------------------------
        # NUEVO PROVEEDOR
        # ----------------------------------------------------------------------

        def nuevo_proveedor():

            limpiar_campos()

            # Eliminamos cualquier selección existente.
            self.tabla.selection_remove(self.tabla.selection())

            # Colocamos el cursor en el primer campo.
            self.caja_razon_social.focus()

        # ----------------------------------------------------------------------
        # READ: CARGAR DATOS DE LA FILA SELECCIONADA AL FORMULARIO
        # ----------------------------------------------------------------------

        def cargar_datos_seleccionados(event=None):

            seleccion = self.tabla.selection()

            if not seleccion:
                return

            item_id = seleccion[0]

            valores = self.tabla.item(item_id, "values")

            limpiar_campos()

            self.caja_razon_social.insert(0, valores[0])

            self.caja_contacto.insert(0, valores[1])

            self.caja_cuit.insert(0, valores[2])

        # ----------------------------------------------------------------------
        # CREATE: GUARDAR PROVEEDOR
        # ----------------------------------------------------------------------

        def guardar():

            razon_social = self.caja_razon_social.get().strip()
            contacto = self.caja_contacto.get().strip()
            cuit = self.caja_cuit.get().strip()

            # Validaciones de entrada
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

            # Delegamos la inserción a la base de datos
            exito = insertar_proveedor(razon_social, contacto, cuit)

            if exito:
                messagebox.showinfo(
                    "Éxito", "Proveedor guardado.", parent=self.pestana
                )

                limpiar_campos()
                cargar_tabla_desde_db()
            else:
                messagebox.showerror(
                    "Error",
                    "Ya existe un proveedor con ese CUIT.",
                    parent=self.pestana,
                )

        # ----------------------------------------------------------------------
        # UPDATE: MODIFICAR PROVEEDOR
        # ----------------------------------------------------------------------

        def modificar():

            seleccion = self.tabla.selection()

            if not seleccion:

                messagebox.showwarning(
                    "Atención",
                    "Selecciona un proveedor de la tabla para modificar.",
                    parent=self.pestana,
                )

                return

            # El ID interno del Treeview corresponde al ID en la tabla de la DB
            id_proveedor = seleccion[0]

            valores = self.tabla.item(id_proveedor, "values")

            # Ventana emergente de edición
            ventana_edicion = tk.Toplevel(self.pestana)

            ventana_edicion.title("Modificar Proveedor")

            ventana_edicion.geometry("400x280")

            ventana_edicion.resizable(False, False)

            ventana_edicion.transient(self.pestana)

            ventana_edicion.grab_set()

            # Campos de texto de edición
            tk.Label(
                ventana_edicion,
                text="Modificar datos del proveedor",
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

                # Intentamos actualizar directamente en la base de datos
                exito = actualizar_proveedor(
                    id_proveedor, razon_mod, contacto_mod, cuit_mod
                )

                if exito:
                    ventana_edicion.destroy()

                    messagebox.showinfo(
                        "Éxito",
                        "El proveedor fue modificado correctamente.",
                        parent=self.pestana,
                    )

                    cargar_tabla_desde_db()
                else:
                    messagebox.showerror(
                        "Error",
                        "Ya existe otro proveedor con ese CUIT.",
                        parent=ventana_edicion,
                    )

            # Botones dentro de la ventana de edición
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

        # ----------------------------------------------------------------------
        # DELETE: ELIMINAR PROVEEDOR
        # ----------------------------------------------------------------------

        def eliminar():

            seleccion = self.tabla.selection()

            if not seleccion:

                messagebox.showwarning(
                    "Atención",
                    "Selecciona un proveedor de la tabla para eliminar.",
                    parent=self.pestana,
                )

                return

            id_proveedor = seleccion[0]

            valores = self.tabla.item(id_proveedor, "values")

            razon_social = valores[0]
            contacto = valores[1]
            cuit = valores[2]

            confirmar = messagebox.askyesno(
                "Confirmar baja",
                f"¿Deseas eliminar el siguiente proveedor?\n\n"
                f"Razón Social: {razon_social}\n"
                f"Contacto: {contacto}\n"
                f"CUIT: {cuit}\n\n"
                f"Esta operación no se puede deshacer.",
                parent=self.pestana,
            )

            if confirmar:

                # Eliminamos directamente en la base de datos
                eliminar_proveedor(id_proveedor)

                limpiar_campos()

                cargar_tabla_desde_db()

                messagebox.showinfo(
                    "Baja realizada",
                    "El proveedor fue eliminado correctamente.",
                    parent=self.pestana,
                )

        # ==========================================================================
        # 6. ENLACE DEL EVENTO DE SELECCIÓN
        # ==========================================================================

        self.tabla.bind("<<TreeviewSelect>>", cargar_datos_seleccionados)

        # ==========================================================================
        # 7. BOTONES CRUD
        # ==========================================================================

        tk.Button(
            self.pestana,
            text="Nuevo Proveedor",
            command=nuevo_proveedor,
            width=16,
        ).grid(row=0, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Guardar Proveedor",
            command=guardar,
            width=16,
        ).grid(row=1, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Modificar Proveedor",
            command=modificar,
            width=16,
        ).grid(row=2, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Eliminar Proveedor",
            command=eliminar,
            width=16,
        ).grid(row=3, column=4, padx=15, pady=2, sticky="w")

        # Cargar los datos desde SQLite al momento de iniciar la pestaña
        cargar_tabla_desde_db()