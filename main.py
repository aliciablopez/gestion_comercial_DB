# main.py

import tkinter as tk
from database import inicializar_base_datos
from interfaz import AplicacionPrincipal


def main():
    # Paso 1: Inicializamos la base de datos (crea las tablas si no existen)
    inicializar_base_datos()

    # Paso 2: Creamos la ventana principal del sistema
    ventana = tk.Tk()

    # Paso 3: Construimos la interfaz sobre esa ventana
    AplicacionPrincipal(ventana)

    # Paso 4: Mantenemos la ventana abierta y activa esperando las acciones del usuario
    ventana.mainloop()


# Punto de entrada principal al ejecutar este archivo
if __name__ == "__main__":
    main()