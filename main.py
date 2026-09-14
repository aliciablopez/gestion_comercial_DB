# main.py

import tkinter as tk
from database import inicializar_base_datos
from interfaz import AplicacionPrincipal
from login import VentanaLogin


def iniciar_aplicacion():
  # 1. Asegurar que las tablas existan en la base de datos
  inicializar_base_datos()

  # 2. Desplegar la ventana de Login
  raiz_login = tk.Tk()
  app_login = VentanaLogin(raiz_login)
  raiz_login.mainloop()

  # 3. Si el login se completó con éxito, abrir la ventana principal
  if app_login.usuario_validado:
    rol_usuario = app_login.usuario_validado["rol"]

    raiz_principal = tk.Tk()
    app_principal = AplicacionPrincipal(raiz_principal, rol_usuario)
    raiz_principal.mainloop()


if __name__ == "__main__":
  iniciar_aplicacion()