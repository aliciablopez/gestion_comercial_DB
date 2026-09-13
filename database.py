# database.py

import sqlite3

NOMBRE_DB = "sistema_facturacion.db"


def obtener_conexion():
  """Crea y devuelve una conexión a la base de datos SQLite."""
  conexion = sqlite3.connect(NOMBRE_DB)
  conexion.row_factory = sqlite3.Row
  return conexion


def inicializar_base_datos():
  """Crea las tablas necesarias si aún no existen."""
  conexion = obtener_conexion()
  cursor = conexion.cursor()

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            razon_social TEXT NOT NULL,
            contacto TEXT,
            cuit TEXT UNIQUE NOT NULL
        )
    """)

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            legajo TEXT UNIQUE NOT NULL,
            puesto TEXT
        )
    """)

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            razon_social TEXT NOT NULL,
            contacto TEXT,
            cuit TEXT UNIQUE NOT NULL
        )
    """)

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_info TEXT NOT NULL,
            total REAL NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factura_id INTEGER NOT NULL,
            producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (factura_id) REFERENCES facturas (id)
        )
    """)

  conexion.commit()
  conexion.close()


# ==============================================================================
# FUNCIONES CRUD PARA CLIENTES
# ==============================================================================


def obtener_clientes():
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  cursor.execute(
      "SELECT id, razon_social, contacto, cuit FROM clientes ORDER BY"
      " razon_social"
  )
  clientes = cursor.fetchall()
  conexion.close()
  return clientes


def insertar_cliente(razon_social, contacto, cuit):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  try:
    cursor.execute(
        """
            INSERT INTO clientes (razon_social, contacto, cuit)
            VALUES (?, ?, ?)
        """,
        (razon_social, contacto, cuit),
    )
    conexion.commit()
    conexion.close()
    return True
  except sqlite3.Error:
    conexion.close()
    return False


def actualizar_cliente(id_cliente, razon_social, contacto, cuit):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  try:
    cursor.execute(
        """
            UPDATE clientes
            SET razon_social = ?, contacto = ?, cuit = ?
            WHERE id = ?
        """,
        (razon_social, contacto, cuit, id_cliente),
    )
    conexion.commit()
    conexion.close()
    return True
  except sqlite3.Error:
    conexion.close()
    return False


def eliminar_cliente(id_cliente):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
  conexion.commit()
  conexion.close()
  return True


# ==============================================================================
# FUNCIONES CRUD PARA EMPLEADOS
# ==============================================================================


def obtener_empleados():
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  cursor.execute(
      "SELECT id, nombre, legajo, puesto FROM empleados ORDER BY nombre"
  )
  empleados = cursor.fetchall()
  conexion.close()
  return empleados


def insertar_empleado(nombre, legajo, puesto):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  try:
    cursor.execute(
        """
            INSERT INTO empleados (nombre, legajo, puesto)
            VALUES (?, ?, ?)
        """,
        (nombre, legajo, puesto),
    )
    conexion.commit()
    conexion.close()
    return True
  except sqlite3.Error:
    conexion.close()
    return False


def actualizar_empleado(id_empleado, nombre, legajo, puesto):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  try:
    cursor.execute(
        """
            UPDATE empleados
            SET nombre = ?, legajo = ?, puesto = ?
            WHERE id = ?
        """,
        (nombre, legajo, puesto, id_empleado),
    )
    conexion.commit()
    conexion.close()
    return True
  except sqlite3.Error:
    conexion.close()
    return False


def eliminar_empleado(id_empleado):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  cursor.execute("DELETE FROM empleados WHERE id = ?", (id_empleado,))
  conexion.commit()
  conexion.close()
  return True


# ==============================================================================
# FUNCIONES CRUD PARA PROVEEDORES
# ==============================================================================


def obtener_proveedores():
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  cursor.execute(
      "SELECT id, razon_social, contacto, cuit FROM proveedores ORDER BY"
      " razon_social"
  )
  proveedores = cursor.fetchall()
  conexion.close()
  return proveedores


def insertar_proveedor(razon_social, contacto, cuit):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  try:
    cursor.execute(
        """
            INSERT INTO proveedores (razon_social, contacto, cuit)
            VALUES (?, ?, ?)
        """,
        (razon_social, contacto, cuit),
    )
    conexion.commit()
    conexion.close()
    return True
  except sqlite3.Error:
    conexion.close()
    return False


def actualizar_proveedor(id_proveedor, razon_social, contacto, cuit):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  try:
    cursor.execute(
        """
            UPDATE proveedores
            SET razon_social = ?, contacto = ?, cuit = ?
            WHERE id = ?
        """,
        (razon_social, contacto, cuit, id_proveedor),
    )
    conexion.commit()
    conexion.close()
    return True
  except sqlite3.Error:
    conexion.close()
    return False


def eliminar_proveedor(id_proveedor):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  cursor.execute("DELETE FROM proveedores WHERE id = ?", (id_proveedor,))
  conexion.commit()
  conexion.close()
  return True


# ==============================================================================
# FUNCIONES CRUD PARA PRODUCTOS (STOCK)
# ==============================================================================


def obtener_productos():
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  cursor.execute(
      "SELECT id, nombre, precio, stock FROM productos ORDER BY nombre"
  )
  productos = cursor.fetchall()
  conexion.close()
  return productos


def insertar_producto(nombre, precio, stock):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  try:
    cursor.execute(
        """
            INSERT INTO productos (nombre, precio, stock)
            VALUES (?, ?, ?)
        """,
        (nombre, precio, stock),
    )
    conexion.commit()
    conexion.close()
    return True
  except sqlite3.Error:
    conexion.close()
    return False


def actualizar_producto(id_producto, nombre, precio, stock):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  try:
    cursor.execute(
        """
            UPDATE productos
            SET nombre = ?, precio = ?, stock = ?
            WHERE id = ?
        """,
        (nombre, precio, stock, id_producto),
    )
    conexion.commit()
    conexion.close()
    return True
  except sqlite3.Error:
    conexion.close()
    return False


def eliminar_producto(id_producto):
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
  conexion.commit()
  conexion.close()
  return True


# ==============================================================================
# FUNCIONES DE FACTURACIÓN
# ==============================================================================


def insertar_factura(cliente_info, total, detalles):
  """Guarda la cabecera, los ítems de detalle y descuenta el stock del producto."""
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  try:
    # 1. Insertar la cabecera de la factura
    cursor.execute(
        "INSERT INTO facturas (cliente_info, total) VALUES (?, ?)",
        (cliente_info, total),
    )
    factura_id = cursor.lastrowid

    # 2. Insertar los ítems del detalle y descontar el stock
    for item in detalles:
      prod_nombre = item["producto"]
      cant = item["cantidad"]
      precio_u = item["precio_unitario"]
      subt = item["subtotal"]

      cursor.execute(
          """
                INSERT INTO detalle_facturas (factura_id, producto, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """,
          (factura_id, prod_nombre, cant, precio_u, subt),
      )

      # Actualización de existencias en tiempo real
      cursor.execute(
          "UPDATE productos SET stock = stock - ? WHERE nombre = ?",
          (cant, prod_nombre),
      )

    conexion.commit()
    conexion.close()
    return True
  except sqlite3.Error:
    conexion.rollback()
    conexion.close()
    return False


def obtener_facturas():
  """Devuelve el historial de facturas emitidas ordenadas por fecha reciente."""
  conexion = obtener_conexion()
  cursor = conexion.cursor()
  cursor.execute(
      "SELECT id, cliente_info, total, fecha FROM facturas ORDER BY fecha DESC"
  )
  facturas = cursor.fetchall()
  conexion.close()
  return facturas