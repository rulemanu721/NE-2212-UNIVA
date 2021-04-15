from dao import schedulerdao
from flask import Flask, request, render_template, redirect, url_for, flash, session, escape
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'



mysql = MySQL(app)

@app.route('/index2')
def Index2():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id,name, email, type FROM user')
    data = cur.fetchall()
    cur.close()
    return render_template('index2.html', contacts = data)

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id,name, email, type FROM user WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        type1 = request.form['type']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE user
            SET name = %s,
                email = %s,
                type = %s
            WHERE id = %s
        """, (name, email, type1, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index2'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM user WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index2'))

# Aceso basico a la pagina
@app.route("/")
def index():
    return render_template("index1.html")


@app.route("/index")
def index_p():
    if "username" in session:
        return render_template("index.html")
    return "Debes logearte"

@app.route("/signUp", methods=["POST"])
def signUp():
    username = str(request.form["username"])
    password = str(request.form["password"])
    email = str(request.form["email"])
    type1 = str(request.form["type1"])
    cursor = mysql.connection.cursor()

    
    cursor.execute("INSERT INTO user (name,password,email,type)VALUES(%s,MD5(%s),%s,%s)",
                   (username, password, email, type1))
    mysql.connection.commit()
    success_message='Dado de alta correctamente'
    flash(success_message)    
    return redirect(url_for("login"))

@app.route("/login")
def login():   
    return render_template("login.html",title="data")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("index1.html")

@app.route("/provider")
def about():
    if "username" in session:
        return render_template("provider.html")
    return "Debes logearte"


@app.route("/checkUser", methods=["POST"])
def check():
    username = str(request.form["user"])
    password = str(request.form["password"])
    cursor = mysql.connection.cursor()
    #cursor.execute("SELECT type FROM user_vista WHERE name ='"+username+"'AND password ='"+password+"'")
    cursor.execute('SELECT type FROM user_vista WHERE name = %s AND password = md5(%s)', (username, password))
    schools=cursor.fetchall()

    if schools is None or len(schools) == 0:
        return "Datos incorrectos"
    if len(schools) == 1:

        session["username"]=username

        for row in schools:
            if row[0]== 1:
                return redirect(url_for("index_p"))
        for row in schools:        
            if row[0]== 2:
                return redirect(url_for("about"))

        

# Accesible a través del procesamiento de programación get / post
@app.route("/scheduler",methods=["GET","POST","PUT","DELETE"])
def scheduler():
    # Si la solicitud es get
    if request.method == 'GET':
        # el inicio y el final se pasan como parámetros en formato aaaa-mm-dd.
        start = request.args.get('start')
        end = request.args.get('end')
        # Pase el inicio y el final a Schedulerdao.getScheduler en formato Dictoionary.
        return schedulerdao.getScheduler({'start':start , 'end' : end})

    # Si la solicitud es posterior
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        title = request.form['title']
        

        # Dictoionary Cree una variable de horario del formulario. Programado para ser modificado para recibir parámetros más tarde
        schedule = {'title' : title, 'start' : start, 'end' : end}
        # schedule ingresar
        return  schedulerdao.setScheduler(schedule)

    # se elimina
    if request.method == 'DELETE':
        id = request.form['id']
        return  schedulerdao.delScheduler(id)

    # si es put
    if request.method == 'PUT':
        schedule = request.form
        return schedulerdao.putScheduler(schedule)

if __name__ =='__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
