# empleados.py

# Responsabilidad del módulo: Construir y administrar la pestaña "Empleados".
# Maneja la captura de datos (Nombre, Legajo, Puesto) y la interacción
# directa con las funciones CRUD de empleados en database.py.

import tkinter as tk
from tkinter import messagebox, ttk

# Importamos las funciones específicas de empleados desde database.py
from database import (
    actualizar_empleado,
    eliminar_empleado,
    insertar_empleado,
    obtener_empleados,
)


class Empleados:

    def __init__(self, pestana):
        self.pestana = pestana

        # ======================================================================
        # 1. FORMULARIO DE ENTRADA
        # ======================================================================

        # NOMBRE
        tk.Label(self.pestana, text="Nombre Completo:").grid(
            row=0, column=0, padx=5, pady=4, sticky="e"
        )
        self.caja_nombre = tk.Entry(self.pestana, width=25)
        self.caja_nombre.grid(row=0, column=1, padx=5, pady=4)

        # LEGAJO
        tk.Label(self.pestana, text="Legajo:").grid(
            row=1, column=0, padx=5, pady=4, sticky="e"
        )
        self.caja_legajo = tk.Entry(self.pestana, width=25)
        self.caja_legajo.grid(row=1, column=1, padx=5, pady=4)

        # PUESTO
        tk.Label(self.pestana, text="Puesto:").grid(
            row=2, column=0, padx=5, pady=4, sticky="e"
        )
        self.caja_puesto = tk.Entry(self.pestana, width=25)
        self.caja_puesto.grid(row=2, column=1, padx=5, pady=4)

        # ======================================================================
        # 2. TREEVIEW / TABLA DE EMPLEADOS
        # ======================================================================
        columnas = ("Nombre", "Legajo", "Puesto")

        self.tabla = ttk.Treeview(
            self.pestana, columns=columnas, show="headings", height=10
        )

        anchos = [250, 150, 200]

        for idx, columna in enumerate(columnas):
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, width=anchos[idx], anchor="center")

        self.tabla.grid(
            row=6, column=0, columnspan=5, padx=15, pady=(10, 15), sticky="ew"
        )

        # ======================================================================
        # 3. FUNCIONES INTERNAS Y PERSISTENCIA
        # ======================================================================

        def cargar_tabla_desde_db():
            """Consulta SQLite y recarga la vista visual."""
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            empleados = obtener_empleados()

            for emp in empleados:
                self.tabla.insert(
                    "",
                    "end",
                    iid=emp["id"],
                    values=(
                        emp["nombre"],
                        emp["legajo"],
                        emp["puesto"],
                    ),
                )

        def limpiar_campos():
            self.caja_nombre.delete(0, tk.END)
            self.caja_legajo.delete(0, tk.END)
            self.caja_puesto.delete(0, tk.END)

        def nuevo_empleado():
            limpiar_campos()
            self.tabla.selection_remove(self.tabla.selection())
            self.caja_nombre.focus()

        def cargar_datos_seleccionados(event=None):
            seleccion = self.tabla.selection()
            if not seleccion:
                return

            item_id = seleccion[0]
            valores = self.tabla.item(item_id, "values")

            limpiar_campos()
            self.caja_nombre.insert(0, valores[0])
            self.caja_legajo.insert(0, valores[1])
            self.caja_puesto.insert(0, valores[2])

        def guardar():
            """Captura las entradas, valida y llama a la persistencia en SQLite."""
            nombre = self.caja_nombre.get().strip()
            legajo = self.caja_legajo.get().strip()
            puesto = self.caja_puesto.get().strip()

            if not nombre or not legajo:
                messagebox.showerror(
                    "Error",
                    "El Nombre y el Legajo son obligatorios.",
                    parent=self.pestana,
                )
                return

            # LLAMADA CLAVE A LA BASE DE DATOS
            exito = insertar_empleado(nombre, legajo, puesto)

            if exito:
                messagebox.showinfo(
                    "Éxito", "Empleado guardado con éxito.", parent=self.pestana
                )
                limpiar_campos()
                cargar_tabla_desde_db()  # Refresca la tabla visual
            else:
                messagebox.showerror(
                    "Error",
                    "Ya existe un empleado con ese número de Legajo.",
                    parent=self.pestana,
                )

        def modificar():
            seleccion = self.tabla.selection()
            if not seleccion:
                messagebox.showwarning(
                    "Atención",
                    "Selecciona un empleado de la tabla para modificar.",
                    parent=self.pestana,
                )
                return

            id_empleado = seleccion[0]
            valores = self.tabla.item(id_empleado, "values")

            ventana_edicion = tk.Toplevel(self.pestana)
            ventana_edicion.title("Modificar Empleado")
            ventana_edicion.geometry("400x280")
            ventana_edicion.resizable(False, False)
            ventana_edicion.transient(self.pestana)
            ventana_edicion.grab_set()

            tk.Label(
                ventana_edicion,
                text="Modificar datos del empleado",
                font=("Arial", 12, "bold"),
            ).pack(pady=(15, 10))

            tk.Label(ventana_edicion, text="Nombre:").pack(anchor="w", padx=30)
            caja_edicion_nombre = tk.Entry(ventana_edicion, width=40)
            caja_edicion_nombre.pack(padx=30, pady=(2, 8))
            caja_edicion_nombre.insert(0, valores[0])

            tk.Label(ventana_edicion, text="Legajo:").pack(anchor="w", padx=30)
            caja_edicion_legajo = tk.Entry(ventana_edicion, width=40)
            caja_edicion_legajo.pack(padx=30, pady=(2, 8))
            caja_edicion_legajo.insert(0, valores[1])

            tk.Label(ventana_edicion, text="Puesto:").pack(anchor="w", padx=30)
            caja_edicion_puesto = tk.Entry(ventana_edicion, width=40)
            caja_edicion_puesto.pack(padx=30, pady=(2, 12))
            caja_edicion_puesto.insert(0, valores[2])

            def guardar_modificacion():
                nom_mod = caja_edicion_nombre.get().strip()
                leg_mod = caja_edicion_legajo.get().strip()
                pue_mod = caja_edicion_puesto.get().strip()

                if not nom_mod or not leg_mod:
                    messagebox.showerror(
                        "Error",
                        "Nombre y Legajo son obligatorios.",
                        parent=ventana_edicion,
                    )
                    return

                exito = actualizar_empleado(
                    id_empleado, nom_mod, leg_mod, pue_mod
                )

                if exito:
                    ventana_edicion.destroy()
                    messagebox.showinfo(
                        "Éxito",
                        "Empleado modificado correctamente.",
                        parent=self.pestana,
                    )
                    cargar_tabla_desde_db()
                else:
                    messagebox.showerror(
                        "Error",
                        "Ya existe otro empleado con ese legajo.",
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

        def eliminar():
            seleccion = self.tabla.selection()
            if not seleccion:
                messagebox.showwarning(
                    "Atención",
                    "Selecciona un empleado de la tabla para eliminar.",
                    parent=self.pestana,
                )
                return

            id_empleado = seleccion[0]
            valores = self.tabla.item(id_empleado, "values")

            confirmar = messagebox.askyesno(
                "Confirmar baja",
                f"¿Deseas eliminar al empleado {valores[0]} (Legajo: {valores[1]})?",
                parent=self.pestana,
            )

            if confirmar:
                eliminar_empleado(id_empleado)
                limpiar_campos()
                cargar_tabla_desde_db()
                messagebox.showinfo(
                    "Éxito",
                    "Empleado eliminado correctamente.",
                    parent=self.pestana,
                )

        # ======================================================================
        # 4. BOTONES Y ENLACES
        # ======================================================================
        self.tabla.bind("<<TreeviewSelect>>", cargar_datos_seleccionados)

        tk.Button(
            self.pestana,
            text="Nuevo Empleado",
            command=nuevo_empleado,
            width=16,
        ).grid(row=0, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Guardar Empleado",
            command=guardar,
            width=16,
        ).grid(row=1, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Modificar Empleado",
            command=modificar,
            width=16,
        ).grid(row=2, column=4, padx=15, pady=2, sticky="w")

        tk.Button(
            self.pestana,
            text="Eliminar Empleado",
            command=eliminar,
            width=16,
        ).grid(row=3, column=4, padx=15, pady=2, sticky="w")

        # Cargar la tabla al inicializar
        cargar_tabla_desde_db()