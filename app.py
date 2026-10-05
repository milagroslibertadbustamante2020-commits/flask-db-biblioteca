from flask import Flask, render_template, request, redirect, url_for
from database import conectar, crear_tablas

app = Flask(__name__)
crear_tablas()

@app.route("/")
def index():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT libros.id, libros.titulo, libros.genero, autores.nombre as autor FROM libros LEFT JOIN autores ON libros.autor_id = autores.id")
    libros = cursor.fetchall()
    cursor.execute("SELECT * FROM autores")
    autores = cursor.fetchall()
    conn.close()
    return render_template("index.html", libros=libros, autores=autores)

@app.route("/agregar_autor", methods=["POST"])
def agregar_autor():
    nombre = request.form.get("nombre")
    nacionalidad = request.form.get("nacionalidad")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO autores (nombre, nacionalidad) VALUES (?, ?)", (nombre, nacionalidad))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/agregar_libro", methods=["POST"])
def agregar_libro():
    titulo = request.form.get("titulo")
    genero = request.form.get("genero")
    autor_id = request.form.get("autor_id")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO libros (titulo, genero, autor_id) VALUES (?, ?, ?)", (titulo, genero, autor_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)