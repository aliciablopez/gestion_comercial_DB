# config.py

# ==============================================================================
# CONFIGURACIÓN GENERAL Y CONSTANTES DEL SISTEMA
# ==============================================================================

# Definición centralizada de Roles para el Control de Acceso
ROL_ADMIN = "admin"
ROL_GERENTE = "gerente"
ROL_VENTAS = "empleado_ventas"
ROL_COMPRAS = "empleado_compras"

# Lista de roles disponibles para despliegues visuales (ComboBox / Selección)
ROLES_DISPONIBLES = [
    ROL_ADMIN,
    ROL_GERENTE,
    ROL_VENTAS,
    ROL_COMPRAS,
]

# Etiquetas amigables para mostrar en la interfaz gráfica
ROLES_NOMBRES = {
    ROL_ADMIN: "Administrador",
    ROL_GERENTE: "Gerente",
    ROL_VENTAS: "Empleado de Ventas",
    ROL_COMPRAS: "Empleado de Compras",
}

