from flask import Flask, render_template, request, session, jsonify
import json, os, sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = "yWb2f@QOf77R9hhEX@sFYdt8cc7&LC2S"


# 
def conectar_base_de_datos():
  conn = sqlite3.connect('data/base_de_datos.sqlite')
  conn.row_factory = sqlite3.Row
  return conn


# Función para revisar si el usuario está autenticado
def revisar_sesion():
  if ('usuario' in session):
    return True
  else:
    return False

@app.route('/')
def index():
  return render_template("inicio.html", titulo="Página de Inicio")


@app.route('/login', methods=['POST'])
def login_validar():
  if revisar_sesion():
    return render_template("dashboard.html", titulo="Usuarios autenticados")
  
  if request.form.get("login") == "admin" and request.form.get(
      "password") == "123456":
    session['usuario'] = "admin"
    return render_template("dashboard.html", titulo="Usuarios autenticados")
  else:
    return render_template("login.html", titulo="Usuario no autenticado")


@app.route('/logout')
def logout():
  session.pop('usuario', None)
  return render_template("inicio.html", titulo="Página de Inicio")


@app.route('/login', methods=['GET'])
def login_formulario():
  if revisar_sesion():
    try:
      conn = conectar_base_de_datos()
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM contactos")
      datos = cursor.fetchall()
      conn.close()
    except:
      datos = []
      
    return render_template("dashboard.html", 
                           titulo="Usuarios autenticados",
                           datos=datos
                           )
  
  return render_template("login.html", titulo="Ingreso a usuarios")


@app.route('/ofertas')
def ofertas():
  # apertura de archivos de texto plano
  #with open("data/ofertas.txt", "r") as archivo:
  #  ofertas = archivo.readlines()
  
  # mecanismo de seguridad para revisar si el usuario está autenticado
  if not revisar_sesion():
    return render_template("login.html", titulo="Ingreso a usuarios")

  # apertura de archivos con formato json
  with open("data/ofertas.json", "r") as archivo:
    data = json.load(archivo)

  return render_template("ofertas.html",
                         titulo="Las mejores Ofertas",
                         ofertas=data['ofertas'])


@app.route('/ofertas/<id>')
def abrir_oferta(id):
  # apertura de archivos de texto plano
  #with open("data/ofertas.txt", "r") as archivo:
  #  ofertas = archivo.readlines()

  # apertura de archivos con formato json
  with open("data/ofertas.json", "r") as archivo:
    ofertas = json.load(archivo)

  seleccionada = None
  for oferta in ofertas['ofertas']:
    if oferta["id"] == int(id):
      seleccionada = oferta

  return render_template("oferta.html",
                         titulo="Las mejores Ofertas",
                         oferta=seleccionada)


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


@app.route('/contacto/<id>', methods=['GET'])
def ver_contacto(id):
  conn = conectar_base_de_datos()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM contactos WHERE id=?", (id,))
  contacto = cursor.fetchone()
  return render_template("ver_contacto.html", titulo="Información", contacto=contacto)


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

  archivo_csv = "data/contactos.csv"

  # Validaciones
  if name == "" or email == "" or address1 == "" or phone == "" or city == "" or state == "":
    validacion = "Error: No hay datos para contacto."
  else:
    # La información se almacenará en la base de datos
    validacion = "Gracias por contactarnos, pronto nos pondremos en contacto con usted."

    # Crear el archivo si no existe, adicionando la cabecera
    if os.path.exists(archivo_csv) == False:
      with open(archivo_csv, "w") as archivo:
        archivo.write("name,email,address1,address2,phone,city,state,zip,message\n")
    
    # Adicionar la información al archivo desde el formulario de contacto.
    with open(archivo_csv, "a") as archivo:
      archivo.write(f"{name},{email},{address1},{address2},{phone},{city},{state},{zip},{message}\n")
  
  # Almacenar en la base de datos
  conn = conectar_base_de_datos()
  cursor = conn.cursor()
  cursor.execute("""
                 INSERT INTO contactos 
                 (name, email, address1, address2, phone, city, state, zip, message)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                 """, (name, email, address1, address2, phone, city, state, zip, message)
                 )
  conn.commit()
  
  return render_template("base.html",
                         titulo="Pronto te contactaremos.",
                         validacion=validacion)


@app.route("/informacion")
def informacion():
  
  datos = pd.read_csv("data/contactos.csv")
  #return datos.to_html()
  #ciudades_unicas = datos["city"].unique().tolist()
  #return jsonify({"ciudades": ciudades_unicas})
  #ciudades_conteo = datos["city"].value_counts().to_dict()
  #return jsonify(ciudades_conteo)
  #return datos.to_json(orient="records")
  return datos.columns.to_list()

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=8080)
