# interfaz.py

from tkinter import ttk

# Importamos los módulos de cada pestaña
from clientes import Clientes
from empleados import Empleados
from proveedores import Proveedores
from stock import Stock
from facturacion import Facturacion


class AplicacionPrincipal:

    def __init__(self, ventana_raiz):
        # Guardamos la ventana principal enviada desde main.py
        self.ventana_raiz = ventana_raiz
        self.ventana_raiz.title("Sistema de Gestión Comercial y Facturación - MVP")
        self.ventana_raiz.geometry("850x550")
        self.ventana_raiz.resizable(False, False)

        # ----------------------------------------------------------------------
        # 1. PANEL DE PESTAÑAS (NOTEBOOK)
        # ----------------------------------------------------------------------
        self.notebook = ttk.Notebook(self.ventana_raiz)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Creación de las estructuras (Marcos/Frames) de cada pestaña
        self.frame_clientes = ttk.Frame(self.notebook)
        self.frame_empleados = ttk.Frame(self.notebook)
        self.frame_proveedores = ttk.Frame(self.notebook)
        self.frame_stock = ttk.Frame(self.notebook)
        self.frame_facturacion = ttk.Frame(self.notebook)

        # Agregamos los marcos al panel con sus respectivos nombres
        self.notebook.add(self.frame_clientes, text="Clientes")
        self.notebook.add(self.frame_empleados, text="Empleados")
        self.notebook.add(self.frame_proveedores, text="Proveedores")
        self.notebook.add(self.frame_stock, text="Stock")
        self.notebook.add(self.frame_facturacion, text="Facturación")

        # ----------------------------------------------------------------------
        # 2. CONSTRUCCIÓN DE CONTENIDOS Y CONEXIÓN DE MÓDULOS
        # ----------------------------------------------------------------------
        # Pestañas de gestión de personas
        self.modulo_clientes = Clientes(self.frame_clientes)
        self.modulo_empleados = Empleados(self.frame_empleados)
        self.modulo_proveedores = Proveedores(self.frame_proveedores)

        # Módulo de Stock (guardamos su referencia)
        self.modulo_stock = Stock(self.frame_stock)

        # Módulo de Facturación: le enviamos la referencia del módulo de Stock
        # para que pueda pedirle que recargue la tabla al guardar una venta
        self.modulo_facturacion = Facturacion(
            self.frame_facturacion, self.modulo_stock
        )

        # ----------------------------------------------------------------------
        # 3. SENSOR AUTOMÁTICO DE CAMBIO DE PESTAÑA
        # ----------------------------------------------------------------------
        # Cuando el usuario hace clic en cualquier pestaña, se ejecuta la función
        self.notebook.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)

    def al_cambiar_pestana(self, _event):
        """Si la pestaña seleccionada es 'Stock', obliga a recargar la tabla visual."""
        pestana_activa = self.notebook.select()
        nombre_pestana = self.notebook.tab(pestana_activa, "text")

        if nombre_pestana == "Stock":
            self.modulo_stock.cargar_datos_en_tabla()