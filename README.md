# Sistema de Gestión Comercial

Proyecto de laboratorio desarrollado en Python y Tkinter.

## Descripción
Sistema de gestión comercial con interfaz gráfica orientada a pestañas para la administración de:
- Clientes
- Empleados
- Proveedores
- Stock
- Facturación

## Tecnologías
- Python 3
- Tkinter (Interfaz Gráfica)
- SQLite3 (Motor de Base de Datos Relacional)
- Git y GitHub (Control de Versiones)

## Persistencia de Datos
El sistema utiliza **SQLite3** como motor de almacenamiento relacional local. Todos los registros de clientes, empleados, proveedores, inventario de productos, cabeceras de facturas y sus correspondientes detalles se almacenan de manera persistente en el archivo local `sistema_facturacion.db`.

La inicialización del esquema y la creación de las tablas ocurren de forma automática al ejecutar la aplicación si el archivo de base de datos no existe previamente.

## Estructura del Proyecto
- `main.py`: Punto de entrada de la aplicación e inicializador de la ventana principal.
- `database.py`: Módulo conector y ejecutor de consultas SQL (CRUD y transacciones).
- `interfaz.py`: Contenedor principal del cuaderno de pestañas (`ttk.Notebook`).
- `clientes.py`: Vista y gestión de clientes.
- `empleados.py`: Vista y gestión de empleados.
- `proveedores.py`: Vista y gestión de proveedores.
- `stock.py`: Vista y control del inventario de productos.
- `facturacion.py`: Vista de emisión de facturas, cálculo de totales e historial.

## Ejecución

1. Clona el repositorio o ubícate en la carpeta del proyecto.
2. Asegúrate de tener Python 3 instalado.
3. Ejecuta desde la terminal:

```bash
python main.py