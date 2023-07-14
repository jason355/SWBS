from flask import Flask, jsonify
import sqlite3
import random

conn = sqlite3.connect('database.dp')
cursor = conn.cursor()

# cursor.execute("Select * From C104")
rows = cursor.fetchall()

data = ["Hello 你好", "我是一隻會動的貓", "你是?", "好喔",
        "what the fuck is this...", "我相信中之敏不會看到這個", "所以我可以來說她的壞話", "嘿嘿嘿", "你知道subway都開在捷運站旁邊嗎?", "喝合理"]


app = Flask(__name__)


@app.route('/')
def main():

    return "Hello This is Just a test page."


@app.route('/104')
def class104():
    # 3
    text = random.choice(data)
    return text


if __name__ == '__main__':
    app.run()
