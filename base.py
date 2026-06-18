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
    legajo_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_categoria VARCHAR(35) NOT NULL UNIQUE   
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS marca (
    legajo_marca INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_marca VARCHAR(35) NOT NULL UNIQUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS productos (
    legajo_ptoducto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(35) NOT NULL UNIQUE,
    stock INTEGER NOT NULL,
    precio INTEGER NOT NULL,
    legajo_marca INTEGER,
    legajo_categoria INTEGER,
    FOREIGN KEY (legajo_marca) REFERENCES marca(legajo_marca)
    FOREIGN KEY (legajo_categoria) REFERENCES marca(legajo_categoria)
)
""")