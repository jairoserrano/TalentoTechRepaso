from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
  return render_template("servicios.html", titulo="Inicio y Servicios")


@app.route('/ofertas')
def ofertas():
  return render_template("ofertas.html", titulo="Ofertas")


@app.route('/productos')
def productos():
  return render_template("productos.html", titulo="Productos")


@app.route('/equipo')
def equipo():
  return render_template("equipo.html", titulo="Equipo Humano")


@app.route('/contacto')
def contacto():
  return render_template("contacto.html", titulo="Contáctenos!")


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=8080)
