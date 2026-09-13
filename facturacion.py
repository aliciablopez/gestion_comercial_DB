# facturacion.py

import tkinter as tk
from tkinter import messagebox, ttk

from database import (
    insertar_factura,
    obtener_clientes,
    obtener_facturas,
    obtener_productos,
)


class Facturacion:

  def __init__(self, pestana, modulo_stock=None):
    self.pestana = pestana
    self.modulo_stock = modulo_stock

    # ======================================================================
    # 1. FORMULARIO DE ENTRADA (DISPOSICIÓN ORIGINAL)
    # ======================================================================

    # CLIENTE
    tk.Label(self.pestana, text="Cliente:").grid(
        row=0, column=0, padx=5, pady=4, sticky="e"
    )
    self.combo_clientes = ttk.Combobox(self.pestana, width=23, state="readonly")
    self.combo_clientes.grid(row=0, column=1, padx=5, pady=4)

    # PRODUCTO
    tk.Label(self.pestana, text="Producto:").grid(
        row=1, column=0, padx=5, pady=4, sticky="e"
    )
    self.combo_productos = ttk.Combobox(
        self.pestana, width=23, state="readonly"
    )
    self.combo_productos.grid(row=1, column=1, padx=5, pady=4)

    # CANTIDAD
    tk.Label(self.pestana, text="Cantidad:").grid(
        row=2, column=0, padx=5, pady=4, sticky="e"
    )
    self.caja_cantidad = tk.Entry(self.pestana, width=25)
    self.caja_cantidad.grid(row=2, column=1, padx=5, pady=4)

    # TOTAL ACUMULADO VISUAL
    self.lbl_total = tk.Label(
        self.pestana, text="Total: $ 0.00", font=("Arial", 11, "bold")
    )
    self.lbl_total.grid(row=3, column=0, columnspan=2, padx=5, pady=8)

    # ======================================================================
    # 2. TREEVIEW / TABLA DE DETALLE DE FACTURA
    # ======================================================================
    columnas = ("Producto", "Cantidad", "Precio Unitario", "Subtotal")

    self.tabla = ttk.Treeview(
        self.pestana, columns=columnas, show="headings", height=10
    )

    anchos = [220, 100, 120, 120]
    for idx, columna in enumerate(columnas):
      self.tabla.heading(columna, text=columna)
      self.tabla.column(columna, width=anchos[idx], anchor="center")

    self.tabla.grid(
        row=6, column=0, columnspan=5, padx=15, pady=(10, 15), sticky="ew"
    )

    # ======================================================================
    # 3. BOTONES DE ACCIÓN (COLUMNA DERECHA ORIGINAL)
    # ======================================================================
    tk.Button(
        self.pestana, text="Nueva Factura", command=self.nueva_factura, width=16
    ).grid(row=0, column=4, padx=15, pady=2, sticky="w")

    tk.Button(
        self.pestana, text="Agregar Ítem", command=self.agregar_item, width=16
    ).grid(row=1, column=4, padx=15, pady=2, sticky="w")

    tk.Button(
        self.pestana, text="Quitar Ítem", command=self.quitar_item, width=16
    ).grid(row=2, column=4, padx=15, pady=2, sticky="w")

    tk.Button(
        self.pestana,
        text="Guardar Factura",
        command=self.guardar_factura,
        width=16,
    ).grid(row=3, column=4, padx=15, pady=2, sticky="w")

    tk.Button(
        self.pestana,
        text="Ver Historial",
        command=self.ver_historial_facturas,
        width=16,
    ).grid(row=4, column=4, padx=15, pady=2, sticky="w")

    self.cargar_desplegables()

  # ======================================================================
  # 4. MÉTODOS Y LÓGICA DE NEGOCIO
  # ======================================================================

  def cargar_desplegables(self):
    """Recarga los desplegables de clientes y productos."""
    clientes = obtener_clientes()
    productos = obtener_productos()

    self.combo_clientes["values"] = [
        f"{c['razon_social']} ({c['cuit']})" for c in clientes
    ]
    self.combo_productos["values"] = [
        f"{p['nombre']} - ${p['precio']:.2f}" for p in productos
    ]

  def limpiar_campos(self):
    self.combo_clientes.set("")
    self.combo_productos.set("")
    self.caja_cantidad.delete(0, tk.END)

  def nueva_factura(self):
    self.limpiar_campos()
    for item in self.tabla.get_children():
      self.tabla.delete(item)
    self.lbl_total.config(text="Total: $ 0.00")
    self.cargar_desplegables()

  def agregar_item(self):
    producto_str = self.combo_productos.get().strip()
    cant_str = self.caja_cantidad.get().strip()

    if not producto_str or not cant_str:
      messagebox.showerror(
          "Error",
          "Selecciona un producto e ingresa la cantidad.",
          parent=self.pestana,
      )
      return

    try:
      cantidad = int(cant_str)
      if cantidad <= 0:
        raise ValueError
    except ValueError:
      messagebox.showerror(
          "Error",
          "La cantidad debe ser un número entero mayor a 0.",
          parent=self.pestana,
      )
      return

    try:
      partes = producto_str.split(" - $")
      nombre_prod = partes[0]
      precio_unitario = float(partes[1])

      # ------------------------------------------------------------------
      # VALIDACIÓN DE STOCK DISPONIBLE (EVITA NUMEROS NEGATIVOS)
      # ------------------------------------------------------------------
      productos_db = obtener_productos()
      stock_disponible = 0
      producto_encontrado = False

      for p in productos_db:
        if p["nombre"] == nombre_prod:
          stock_disponible = p["stock"]
          producto_encontrado = True
          break

      if not producto_encontrado:
        messagebox.showerror(
            "Error", "El producto no existe en el inventario."
        )
        return

      if cantidad > stock_disponible:
        messagebox.showwarning(
            "Stock Insuficiente",
            f"No hay suficiente stock para '{nombre_prod}'.\n"
            f"Disponible actual: {stock_disponible} unidades.",
            parent=self.pestana,
        )
        return
      # ------------------------------------------------------------------

      subtotal = precio_unitario * cantidad

      self.tabla.insert(
          "",
          "end",
          values=(
              nombre_prod,
              cantidad,
              f"$ {precio_unitario:.2f}",
              f"$ {subtotal:.2f}",
          ),
      )

      self.recalcular_total()
      self.caja_cantidad.delete(0, tk.END)
      self.combo_productos.set("")

    except (ValueError, IndexError):
      messagebox.showerror(
          "Error",
          "No se pudo procesar el producto seleccionado.",
          parent=self.pestana,
      )

  def recalcular_total(self):
    total = 0.0
    for item in self.tabla.get_children():
      valores = self.tabla.item(item, "values")
      subtotal_str = valores[3].replace("$", "").strip()
      total += float(subtotal_str)

    self.lbl_total.config(text=f"Total: $ {total:.2f}")

  def quitar_item(self):
    seleccion = self.tabla.selection()
    if not seleccion:
      messagebox.showwarning(
          "Atención",
          "Selecciona un ítem de la tabla para quitarlo.",
          parent=self.pestana,
      )
      return

    for item in seleccion:
      self.tabla.delete(item)

    self.recalcular_total()

  def guardar_factura(self):
    cliente = self.combo_clientes.get().strip()
    items_tabla = self.tabla.get_children()

    if not cliente:
      messagebox.showerror(
          "Error",
          "Debes seleccionar un cliente para emitir la factura.",
          parent=self.pestana,
      )
      return

    if not items_tabla:
      messagebox.showerror(
          "Error",
          "La factura debe contener al menos un producto.",
          parent=self.pestana,
      )
      return

    detalles = []
    total = 0.0

    for item in items_tabla:
      valores = self.tabla.item(item, "values")
      prod_nombre = valores[0]
      cant = int(valores[1])
      precio_u = float(valores[2].replace("$", "").strip())
      subt = float(valores[3].replace("$", "").strip())

      detalles.append({
          "producto": prod_nombre,
          "cantidad": cant,
          "precio_unitario": precio_u,
          "subtotal": subt,
      })
      total += subt

    exito = insertar_factura(cliente, total, detalles)

    if exito:
      messagebox.showinfo(
          "Éxito",
          "Factura emitida y registrada correctamente.",
          parent=self.pestana,
      )

      # Actualización automática de la pestaña de Stock
      if self.modulo_stock:
        self.modulo_stock.cargar_datos_en_tabla()

      self.nueva_factura()
    else:
      messagebox.showerror(
          "Error",
          "No se pudo guardar la factura en la base de datos.",
          parent=self.pestana,
      )

  def ver_historial_facturas(self):
    ventana_historial = tk.Toplevel(self.pestana)
    ventana_historial.title("Historial de Facturas Emitidas")
    ventana_historial.geometry("650x400")
    ventana_historial.resizable(False, False)
    ventana_historial.transient(self.pestana)
    ventana_historial.grab_set()

    tk.Label(
        ventana_historial, text="Comprobantes Emitidos", font=("Arial", 12, "bold")
    ).pack(pady=10)

    columnas_hist = ("N° Factura", "Cliente", "Total", "Fecha")
    tabla_historial = ttk.Treeview(
        ventana_historial, columns=columnas_hist, show="headings", height=12
    )

    anchos_hist = [80, 250, 100, 150]
    for idx, col in enumerate(columnas_hist):
      tabla_historial.heading(col, text=col)
      tabla_historial.column(col, width=anchos_hist[idx], anchor="center")

    tabla_historial.pack(padx=15, pady=10, fill="both", expand=True)

    facturas = obtener_facturas()
    for f in facturas:
      tabla_historial.insert(
          "",
          "end",
          values=(
              f["id"],
              f["cliente_info"],
              f"$ {f['total']:.2f}",
              f["fecha"],
          ),
      )

    tk.Button(
        ventana_historial,
        text="Cerrar",
        command=ventana_historial.destroy,
        width=12,
    ).pack(pady=10)