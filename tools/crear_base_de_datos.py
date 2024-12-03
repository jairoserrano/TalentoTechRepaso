import sqlite3

# SQL
# Lenguaje de Consulta Estructurado
#
# CRUD
# Crear      -- CREATE
# Leer       -- SELECT
# Actualizar -- UPDATE
# Borrar     -- DELETE
#


conn = sqlite3.connect('../data/base_de_datos.sqlite')
cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS contactos 
               (name TEXT, email TEXT, address1 TEXT, 
               address2 TEXT, phone TEXT, city TEXT, 
               state TEXT, zip TEXT, message TEXT
               )
               """)
conn.commit()
conn.close()