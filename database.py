# database.py
import sqlite3

def crear_base_datos():
    conexion = sqlite3.connect("recetas.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            categoria TEXT NOT NULL,
            rapida BOOLEAN NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()
