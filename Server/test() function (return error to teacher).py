
import implementV2_7_1 as f
from implementV2_7_1 import Teacher, Bot
import databaseV2_7_1 as db
from urllib.parse import parse_qsl
from linebot.models import  FollowEvent, MessageEvent, TextMessage, TextSendMessage, UnfollowEvent, PostbackEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from flask import request, abort
from flask import Flask, request, abort, jsonify
app = Flask(__name__)




@app.route("/test", methods=['POST'])
def test():
    data = request.json  # 從 POST 請求中取得 JSON 資料
    message = data.get("content")
    cls = data.get("cls")
    time = data.get("time")
    tea = data.get("name")
    print(cls, time, tea, message)
    id = db.getID(tea)
    if id :
        #line_bot_api.push_message(id, TextSendMessage(text=f"資料傳輸失敗\n原定派送班級 :{cls}\n訊息內容 :{message}\n發送時間 :{time}"))
        print(f"資料傳輸失敗\n原定派送班級 :{cls}\n訊息內容 :{message}\n發送時間 :{time}")

    print("data process success")
    return  jsonify({"status": "success"})


        

if __name__ == '__main__':
    app.run(host="192.168.56.1", port=8080)
