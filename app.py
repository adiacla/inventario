from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        tipo = request.form['tipo']
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        vencimiento = request.form['vencimiento']
        # Guardar el nuevo producto en la base de datos
        conn = get_db_connection()
        conn.execute('INSERT INTO inventario (tipo, nombre, cantidad, vencimiento) VALUES (?, ?, ?, ?)',
                     (tipo, nombre, cantidad, vencimiento))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('nuevo.html')

@app.route('/retiro', methods=['GET', 'POST'])
def retiro():
    conn = get_db_connection()
    productos = conn.execute('SELECT nombre FROM inventario').fetchall()
    conn.close()

    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        # Lógica para actualizar la cantidad en la base de datos
        conn = get_db_connection()
        conn.execute('UPDATE inventario SET cantidad = cantidad - ? WHERE nombre = ?',
                     (cantidad, nombre))
        conn.commit()
        conn.close()
        return redirect('/')
    
    return render_template('retiro.html', productos=productos)

@app.route('/compras', methods=['GET', 'POST'])
def compras():
    conn = get_db_connection()
    productos = conn.execute('SELECT nombre FROM inventario').fetchall()
    conn.close()

    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        # Lógica para aumentar la cantidad en la base de datos
        conn = get_db_connection()
        conn.execute('UPDATE inventario SET cantidad = cantidad + ? WHERE nombre = ?',
                     (cantidad, nombre))
        conn.commit()
        conn.close()
        return redirect('/')
    
    return render_template('compras.html', productos=productos)

@app.route('/listar', methods=['GET', 'POST'])
def listar():
    conn = get_db_connection()
    tipos = conn.execute('SELECT DISTINCT tipo FROM inventario').fetchall()
    productos = []
    
    if request.method == 'POST':
        tipo = request.form['tipo']
        productos = conn.execute('SELECT * FROM inventario WHERE tipo = ?', (tipo,)).fetchall()
    
    conn.close()
    return render_template('listar.html', tipos=tipos, productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
