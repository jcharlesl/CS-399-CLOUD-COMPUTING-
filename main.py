
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='hellosql'
app.config['MYSQL_DB']='hellodb'
socket = "winter-dynamics-371520:northamerica-northeast2:hellosql"
app.config['MYSQL_UNIX_SOCKET']=f'''/cloudsql/{socket}''' 
mysql = MySQL(app)
DB = 'FFEF_A'

@app.route ('/')
def form():
    return render_template('form.html')

@app.route ('/landing')
def landingform():
    return render_template('landing.html')

@app.route('/login', methods= ['POST','GET'])
def login():
    if request.method == 'GET':
	    return 'LOG IN PROPERLY PLEASE.'
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']		
        email = request.form['email']
        donate = request.form['donate']
        choice = request.form['choice']
        cur = mysql.connection.cursor()
        cur.execute(f'''INSERT INTO {DB} VALUES (%s,%s,%s,%s,%s)''',(first_name,last_name,email,choice,donate))
        mysql.connection.commit()
        cur.close()
        return redirect('/landing')

@app.route('/landing', methods= ['POST','GET'])
def landing():
    if request.method == 'GET':
	    return redirect ('/')
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM {DB}''')
        rv = cur.fetchall()
        return str(rv)

if __name__=='__main__':
	app.run(debug=True)
