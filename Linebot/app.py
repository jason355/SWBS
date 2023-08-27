
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import mydatabase as mydb
from datetime import datetime

app = Flask(__name__)

user_states = {}

broadcast_content = ""

line_bot_api = LineBotApi(
    "OQUfgG/04yXRUmv660eCqHp7zedaGzRBKzb1WCJ8gzNp7F7p+Yh8Iaod7/e3wLRk2H6Fh/3zig5l58zlcHaQjPO1qrhS/qt3rEXqszLj9SjcyuJUMJeSlWsW62Zb0983w8O050LDJ0XYsEgh2aI+QQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("a41d4e206f57d19d2569eb415aaeabc0")


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your access token/channel secret.")
        abort(400)

    return 'Ok'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text
    global broadcast_content
    # 檢查用戶的狀態
    if user_id in user_states and user_states[user_id] != "空閒":
        user_state = user_states[user_id]

        if user_state == "新增廣播訊息_步驟1":
            # 使用者在步驟1，這時要求輸入廣播內容
            broadcast_content = user_message

            # 更改用戶的狀態為步驟2
            user_states[user_id] = "新增廣播訊息_步驟2"
            reply_message = "請輸入班級數字。"
        elif user_state == "新增廣播訊息_步驟2":
            # 使用者在步驟2，這時要求輸入班級數字
            class_number = user_message
            user_states[user_id] = "空閒"
            teacher, fromWhere = mydb.getTeacher(user_id)
            print(teacher, fromWhere)
            mydb.insertMessage(
                teacher, fromWhere, broadcast_content, class_number, 1, datetime.now())

            reply_message = "已儲存廣播內容和班級數字。"

        elif user_state == "個人身分設定1":
            teacherName = user_message
            mydb.insertIdNam(user_id, teacherName)
            user_states[user_id] = "個人身分設定2"
            reply_message = f"已儲存!您新更改的名字為:{teacherName}\n 再來請輸入您的處室"  #

        elif user_state == "個人身分設定2":
            fromWhere = user_message
            user_states[user_id] = "空閒"
            reply_message = f"已更新 處室名稱為:{fromWhere}"  #
            mydb.insertFromWhere(user_id, fromWhere)

    else:
        if "新增廣播訊息" in user_message:
            if mydb.getTeacher(user_id) != None:
                user_states[user_id] = "新增廣播訊息_步驟1"
                reply_message = "請輸入廣播內容。"
            else:
                reply_message = "您尚未身分驗證，請使用個人身分設定功能"
        elif "設定個人資訊" in user_message:
            reply_message = "請輸入您的姓名"
            user_states[user_id] = "個人身分設定1"
        else:
            # 其他情況下的回應
            reply_message = "請使用 Quick Reply 選項觸發「新增廣播訊息」功能。"

    # 回應使用者
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()
