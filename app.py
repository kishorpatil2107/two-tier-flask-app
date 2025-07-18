# import os
# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_mysqldb import MySQL

# app = Flask(__name__)

# # Configure MySQL from environment variables
# app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
# app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
# app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
# app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# # Initialize MySQL
# mysql = MySQL(app)

# def init_db():
#     with app.app_context():
#         cur = mysql.connection.cursor()
#         cur.execute('''
#         CREATE TABLE IF NOT EXISTS messages (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             message TEXT
#         );
#         ''')
#         mysql.connection.commit()  
#         cur.close()

# @app.route('/')
# def hello():
#     cur = mysql.connection.cursor()
#     cur.execute('SELECT message FROM messages')
#     messages = cur.fetchall()
#     cur.close()
#     return render_template('index.html', messages=messages)

# @app.route('/submit', methods=['POST'])
# def submit():
#     new_message = request.form.get('new_message')
#     cur = mysql.connection.cursor()
#     cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
#     mysql.connection.commit()
#     cur.close()
#     return jsonify({'message': new_message})

# if __name__ == '__main__':
#     init_db()
#     app.run(host='0.0.0.0', port=5000, debug=True)
import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# ----------------- MySQL Configuration ------------------
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL
mysql = MySQL(app)


# ----------------- Initialize DB Table ------------------
def init_db():
    with app.app_context():
        try:
            cur = mysql.connection.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    message TEXT
                );
            ''')
            mysql.connection.commit()
        except Exception as e:
            app.logger.error(f"Database initialization error: {e}")
        finally:
            cur.close()


# ----------------- Routes ------------------

@app.route('/')
def home():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT message FROM messages')
        messages = cur.fetchall()
    except Exception as e:
        app.logger.error(f"Failed to fetch messages: {e}")
        messages = []
    finally:
        cur.close()

    return render_template('index.html', messages=messages)


@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    try:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
        mysql.connection.commit()
    except Exception as e:
        app.logger.error(f"Failed to insert message: {e}")
        return jsonify({'error': 'Message insert failed'}), 500
    finally:
        cur.close()

    return jsonify({'message': new_message})


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200


# ----------------- Start Application ------------------

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

