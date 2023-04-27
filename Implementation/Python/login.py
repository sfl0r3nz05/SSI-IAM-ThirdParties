from flask import Flask, request, session, jsonify
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'secreto'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'users'
mysql = MySQL(app)
bcrypt = Bcrypt(app)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Register route
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cur.fetchone()

    if user:
        return jsonify({'error': 'El usuario ya existe'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
    mysql.connection.commit()

    user = User(id=cur.lastrowid, username=username, password=hashed_password)
    session['user'] = {'id': user.id, 'username': user.username}
    return jsonify({'message': 'Registro exitoso'}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cur.fetchone()

    if not user:
        return jsonify({'error': 'El usuario no existe'}), 401

    if not bcrypt.check_password_hash(user[2], password):
        return jsonify({'error': 'La contraseña es incorrecta'}), 401

    session['user'] = {'id': user[0], 'username': user[1]}
    return jsonify({'message': 'Inicio de sesión exitoso'}), 200

if __name__ == '__main__':
    app.run(debug=True)
