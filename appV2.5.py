import re
import implementV2_5 as f
from implementV2_5 import Teacher, Bot
import databaseV2_5 as db
from urllib.parse import parse_qsl
from linebot.models import  FollowEvent, MessageEvent, TextMessage, TextSendMessage, PostbackTemplateAction, PostbackEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from flask import request, abort
from flask import Flask, request, abort
app = Flask(__name__)


# mydb = datafun.initialize_db()

line_bot_api = LineBotApi('OQUfgG/04yXRUmv660eCqHp7zedaGzRBKzb1WCJ8gzNp7F7p+Yh8Iaod7/e3wLRk2H6Fh/3zig5l58zlcHaQjPO1qrhS/qt3rEXqszLj9SjcyuJUMJeSlWsW62Zb0983w8O050LDJ0XYsEgh2aI+QQdB04t89/1O/w1cDnyilFU=') # 
handler = WebhookHandler('a41d4e206f57d19d2569eb415aaeabc0') # 


users = {}
global pattern
global AdminConfirmPatter

Manager = Bot(line_bot_api, db, users)




class_list = ['701', '702', '703', '704', '705', '706', '801', '802', '803', '804', '805', '806', '901', '902', '903', '904', '905',
              '906', '101', '102', '103', '104', '105', '106', '111', '112', '113', '114', '115', '116', '121', '122', '123', '124', '125', '126']
grade_list = ['1', '2', '3', '4', '5','7', '8', '9']


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



# 教師初次登入
@handler.add(FollowEvent)
def handle_follow(event):
    global user
    
    user_id = event.source.user_id
    users[user_id] = Teacher(user_id, status = "Ss1")
    reply_message = "老師好, 請輸入您的名稱"
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))

# 指令縮寫說明
# Bs (Bordcast stage)廣播訊息階段 (1/2/2.1/2.2)
# Fs (Free stage)空閒
# Ss (Setting stage)設定教師個人資訊 (1/2)
# Hs (History stage)檢視歷史訊息階段
# ACs (Admin Confirm stage) 
# Cs (Confirm stage)
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    print(user_id)
    # backdata = event.postback.data
    backdata = dict(parse_qsl(event.postback.data))

    # 首次加入，建立物件
    if user_id not in users:
        users[user_id] = Teacher(user_id, status = "Fs")
   
    # 確認發送訊息
    if backdata.get('action') == "confirm_yes":  
        Manager.confirm_yes(event, user_id)

    elif backdata.get('action') == "confirm_no":
        Manager.confirm_no(event, user_id)

    elif backdata.get("action") == "文字廣播":
        Manager.postback_Bs(event, user_id)

    elif backdata.get("action") == "教師個人資訊":
        Manager.postback_Ss(event, user_id)

    elif backdata.get("action") == "歷史訊息":
        Manager.postback_Hs(event, user_id)


    elif backdata.get('action') == "select_class":
        Manager.postback_Sc(event, user_id)

    elif backdata.get('action') == "select_group":
       Manager.postback_Sg(event, user_id)

    elif backdata.get('action') == "cancel":
        Manager.postback_C(event, user_id)

    elif backdata.get('action') == "CofS_Y":
        Manager.postback_US(event, user_id, "CofS_Y")
    
    elif backdata.get('action') == "CofS_N":
        Manager.postback_US(event, user_id, "CofS_N")

    elif backdata.get('action') == "Adm_Yes":
        Manager.postback_Adm(event, user_id, "Adm_Yes")
    
    elif backdata.get("action") == "Adm_No":
        Manager.postback_Adm(event, user_id, "Adm_No")





# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id

    # 判斷是否有在字典中
    if user_id not in users:
        Manager.users[user_id] = Teacher(user_id, status = "Fs")
        
        # 將資料庫中資訊放入老師物間中
        teacher = db.getTeacher(user_id)
        if teacher != "Error" and teacher != False:
            Manager.users[user_id].name = teacher.name
            Manager.users[user_id].office = teacher.office
            
            if teacher.isAdmin == 1:
                Manager.users[user_id].isAdm = [True, []]

    # 個人資訊設定1
    if Manager.users[user_id].status == "Ss1":
        Manager.handle_Ss1(event, user_id, text)
    
    # 個人資訊設定2
    elif Manager.users[user_id].status == "Ss2":
        Manager.handle_Ss2(event, user_id, text)

    # 廣播訊息1
    elif Manager.users[user_id].status == "Bs1":
        Manager.handle_Bs1(event, user_id, text)
    
    # 廣播訊息2
    elif Manager.users[user_id].status == "Bs2":
        Manager.handle_Bs2(event, user_id, text)
    
    # 廣播訊息 2.1
    elif Manager.users[user_id].status == "Bs2.1":
        Manager.handle_Bs2_1(event, user_id, text)
    
    # 廣播訊息 2.2
    elif Manager.users[user_id].status == "Bs2.2":
        Manager.handle_Bs2_2(event, user_id, text)
    
    
    # 空閒
    elif Manager.users[user_id].status == "Fs":
        Manager.handle_Fs(event, user_id, text)


    elif Manager.users[user_id].status == "ACs":
        Manager.handle_admin1(event, user_id)

if __name__ == '__main__':
    app.run()