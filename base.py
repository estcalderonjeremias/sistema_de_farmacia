import sqlite3

conn = sqlite3.connect("usuarios.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    legajo INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_categoria VARCHAR(35) NOT NULL UNIQUE   
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS marca (
    id_marca INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_marca VARCHAR(35) NOT NULL UNIQUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(35) NOT NULL UNIQUE,
    stock INTEGER NOT NULL,
    precio INTEGER NOT NULL,
    legajo_marca INTEGER,
    legajo_categoria INTEGER,
    FOREIGN KEY (legajo_marca) REFERENCES marca(legajo_marca),
    FOREIGN KEY (legajo_categoria) REFERENCES categoria(legajo_categoria)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(35) NOT NULL UNIQUE,
    id_producto INTEGER,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    num_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    cant_vendida INTEGER NOT NULL,
    id_producto INTEGER,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
)
""")

conn.commit()
conn.close()