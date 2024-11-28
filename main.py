from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
  return render_template("base.html", titulo="Página de Inicio")


@app.route('/login', methods=['POST'])
def login_validar():
  if request.form.get("login") == "admin" and request.form.get(
      "password") == "123456":
    return render_template("dashboard.html", titulo="Usuarios autenticados")
  else:
    return render_template("login.html", titulo="Usuario no autenticado")


@app.route('/login', methods=['GET'])
def login_formulario():
  return render_template("login.html", titulo="Ingreso a usuarios")


@app.route('/ofertas')
def ofertas():
  return render_template("ofertas.html", titulo="Las mejores Ofertas")


@app.route('/servicios')
def servicios():
  return render_template("servicios.html", titulo="Servicios Destacados")


@app.route('/productos')
def productos():
  return render_template("productos.html", titulo="Productos Destacados")


@app.route('/productos-nuevos')
def productos_nuevos():
  return render_template("productos_nuevos.html",
                         titulo="Productos Destacados")


@app.route('/productos-destacados')
def productos_destacados():
  return render_template("productos_destacados.html",
                         titulo="Productos Destacados")


@app.route('/equipo')
def equipo():
  return render_template("equipo.html", titulo="El mejor Equipo Humano")


@app.route('/contacto', methods=['GET'])
def contacto():
  return render_template("contacto.html", titulo="Contáctenos!!!")


@app.route('/contacto', methods=['POST'])
def guardar_contacto():
  name = request.form.get("inputName")
  email = request.form.get("inputEmail")
  address1 = request.form.get("inputAddress")
  address2 = request.form.get("inputAddress2")
  phone = request.form.get("inputPhone")
  city = request.form.get("inputCity")
  state = request.form.get("inputState")
  zip = request.form.get("inputZip")
  message = request.form.get("inputMessage")

  # Validaciones
  if name == "" or email == "" or address1 == "" or phone == "" or city == "" or state == "":
    validacion = "Error: No hay datos para contacto."
  else:
    # La información se almacenará en la base de datos
    validacion = "Gracias por contactarnos, pronto nos pondremos en contacto con usted."

  return render_template("base.html",
                         titulo="Pronto te contactaremos.",
                         validacion=validacion)


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=8080)
