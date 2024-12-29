# conexion.py
import pymysql

def get_connection():
    """Devuelve una conexión a la base de datos"""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="4party"
    )
