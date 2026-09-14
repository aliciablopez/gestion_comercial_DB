# login.py

import tkinter as tk
from tkinter import messagebox
from config import ROLES_NOMBRES
from database import validar_credenciales


class VentanaLogin:

  def __init__(self, ventana_raiz):
    self.ventana_raiz = ventana_raiz
    self.ventana_raiz.title("Inicio de Sesión - Sistema de Gestión")
    self.ventana_raiz.geometry("320x220")
    self.ventana_raiz.resizable(False, False)

    self.usuario_validado = None

    # Centrar elementos visuales
    tk.Label(
        self.ventana_raiz,
        text="Acceso al Sistema",
        font=("Arial", 12, "bold"),
    ).pack(pady=10)

    # Campo Usuario
    frame_usr = tk.Frame(self.ventana_raiz)
    frame_usr.pack(pady=5)
    tk.Label(frame_usr, text="Usuario:    ", width=10, anchor="e").pack(
        side="left"
    )
    self.txt_usuario = tk.Entry(frame_usr, width=20)
    self.txt_usuario.pack(side="left")
    self.txt_usuario.focus()

    # Campo Contraseña
    frame_pass = tk.Frame(self.ventana_raiz)
    frame_pass.pack(pady=5)
    tk.Label(frame_pass, text="Contraseña:", width=10, anchor="e").pack(
        side="left"
    )
    self.txt_contrasena = tk.Entry(frame_pass, width=20, show="*")
    self.txt_contrasena.pack(side="left")

    # Botón Ingresar
    tk.Button(
        self.ventana_raiz,
        text="Ingresar",
        command=self.autenticar,
        width=15,
        bg="#007ACC",
        fg="white",
    ).pack(pady=15)

    # Permitir presionar Enter para ingresar
    self.ventana_raiz.bind("<Return>", lambda event: self.autenticar())

  def autenticar(self):
    usr = self.txt_usuario.get().strip()
    pas = self.txt_contrasena.get().strip()

    if not usr or not pas:
      messagebox.showerror(
          "Error",
          "Por favor ingrese usuario y contraseña.",
          parent=self.ventana_raiz,
      )
      return

    # Consulta a la base de datos
    datos_usuario = validar_credenciales(usr, pas)

    if datos_usuario:
      self.usuario_validado = datos_usuario
      rol_tecnico = datos_usuario["rol"]
      nombre_rol = ROLES_NOMBRES.get(rol_tecnico, rol_tecnico)

      messagebox.showinfo(
          "Bienvenido",
          f"Acceso concedido como: {nombre_rol}",
          parent=self.ventana_raiz,
      )
      self.ventana_raiz.destroy()  # Cierra la ventana de login
    else:
      messagebox.showerror(
          "Acceso Denegado",
          "Usuario o contraseña incorrectos.",
          parent=self.ventana_raiz,
      )