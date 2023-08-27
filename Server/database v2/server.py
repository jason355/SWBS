from flask import Flask, jsonify, make_response
import json
import mysql.connector

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset = utf-8"


cnx = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="escko83@4L",
    database="message_database"
)
cursor = cnx.cursor()


@app.route('/104', methods=['GET'])
def get_users():
    data = []
    cursor.execute("Select * From C104")
    get = cursor.fetchall()
    for row in get:
        record = {
            'teacher': row[1],
            'content': row[2],
            'sendTime': str(row[3])
        }
        data.append(record)

        # response = make_response(jsonify(data))
        # response.headers['Content-Type'] = 'application/json;charset=ASCII'

        response = json.dumps(data, ensure_ascii=False)
        print(response)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
