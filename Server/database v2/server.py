from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

cnx = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="escko83@4L",
    database="message_database"
)
cursor = cnx.cursor()


@app.route('/api/users', methods=['GET'])
def get_users():
    user_list3
    return jsonify(user_list)


if __name__ == '__main__':
    app.run()
