import sqlite3
import pandas as pd
import os

def init_db_from_excel():
    # Eliminar la base de datos si ya existe
    if os.path.exists('inventario.db'):
        os.remove('inventario.db')
        print("Base de datos existente eliminada.")

    # Leer el archivo Excel
    try:
        df = pd.read_excel('inventario.xlsx')
    except Exception as e:
        print("Error al leer el archivo Excel:", e)
        return

    # Verificar columnas requeridas
    required_columns = {'Tipo', 'Nombre', 'Cantidad', 'Vencimiento'}
    if not required_columns.issubset(df.columns):
        print("El archivo Excel debe contener las columnas: Tipo, Nombre, Cantidad, Vencimiento")
        return

    # Convertir columna 'Vencimiento' a texto en formato YYYY-MM-DD
    df['Vencimiento'] = pd.to_datetime(df['Vencimiento']).dt.strftime('%Y-%m-%d')

    # Crear conexión y tabla
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            vencimiento DATE NOT NULL
        )
    ''')

    # Insertar datos
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO inventario (tipo, nombre, cantidad, vencimiento)
            VALUES (?, ?, ?, ?)
        ''', (
            row['Tipo'],
            row['Nombre'],
            int(row['Cantidad']),
            row['Vencimiento']  # ya es string
        ))

    conn.commit()
    conn.close()
    print("Inventario inicial cargado exitosamente.")

if __name__ == '__main__':
    init_db_from_excel()
