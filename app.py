from flask import Flask, render_template, redirect, request, session
from flask_mysqldb import MySQL

# Configuración de la aplicación Flask
app = Flask(__name__, template_folder='template')

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Inicializar MySQL
mysql = MySQL(app)

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

# Rutas de administración
@app.route('/adminPrincipal')
def admin_principal():
    return render_template('adminPrincipal.html')

@app.route('/adminCandidato')
def admin_candidato():
    return render_template('adminCandidatos.html')

@app.route('/adminUser', methods=["GET", "POST"])
def admin_user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()
    return render_template("adminUser.html", usuarios=usuarios)

# Ruta de voto
@app.route('/voto')
def voto():
    return render_template('voto.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Función de login
@app.route('/acceso-login', methods=["POST"])
def acceso_login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (correo, password,))
        account = cur.fetchone()
        cur.close()

        if account:
            session['logueando'] = True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']
            
            if session['id_rol'] == 1:
                return redirect('/adminPrincipal')
            elif session['id_rol'] == 2:
                return render_template('funcionario.html')
            elif session['id_rol'] == 3:
                return render_template('login.html', mensaje="Con esta cuenta solo puede votar")
        else:
            return render_template('login.html', mensaje="Usuario incorrecto")

# Registro
@app.route('/registro')
def registro():
    return render_template('registro.html')
@app.route('/crear-registro', methods=["POST"])
def crear_registro():
    curp = request.form['txtCURP']
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']
    seccion = request.form['txtSeccion']
    location = request.form['txtLocation']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (curp, correo, password, seccion, location, id_rol) VALUES (%s, %s, %s, %s, %s, 3)", (curp, correo, password, seccion, location))
    mysql.connection.commit()
    cur.close()
    return render_template("index.html", mensaje2="Usuario registrado exitosamente")

if __name__ == '__main__':
    app.secret_key = "alex_rp"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
