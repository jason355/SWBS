import re
import implementV2_5_1 as f
from implementV2_5_1 import Teacher, Bot
import databaseV2_5_1 as db
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
# Bs (Bordcast stage)廣播訊息階段 (1: 選擇單獨或群發/2.1 個別發送/2.2 群體發送/ 3 取得文字)
# Fs (Free stage)空閒
# Ss (Setting stage)設定教師個人資訊 (1/2/3 等待管理員確認)
# Hs (History stage)檢視歷史訊息階段
# ACs (Admin Confirm stage) 
# Cs (Confirm stage)
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    # backdata = event.postback.data
    backdata = dict(parse_qsl(event.postback.data))



    # 首次加入，建立物件
    if user_id not in Manager.users:
        temp = db.getTeacher(user_id)
        if temp != "Error" or None:
            Manager.users[user_id] = Teacher(user_id, status = "Fs", name=temp.name, office=temp.name)
        else:
            Manager.users[user_id] = Teacher(user_id, status="Ss1")
            reply_message = "老師好, 請輸入您的名稱"
            line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
   
    # 確認發送訊息
    if backdata.get('action') == "@confirm_yes":  
        Manager.confirm_yes(event, user_id)

    elif backdata.get('action') == "@confirm_no":
        Manager.confirm_no(event, user_id)

    elif backdata.get("action") == "@文字廣播":
        Manager.postback_Bs(event, user_id)

    elif backdata.get("action") == "@教師個人資訊":
        Manager.postback_Ss(event, user_id)

    elif backdata.get("action") == "@歷史訊息":
        Manager.postback_Hs(event, user_id)
    
    elif backdata.get('action') == "@幫助":
        reply_message = "##暫定"


    elif backdata.get('action') == "@select_class":
        Manager.postback_Sc(event, user_id)

    elif backdata.get('action') == "@select_group":
       Manager.postback_Sg(event, user_id)

    elif backdata.get('action') == "@cancel":
        Manager.postback_C(event, user_id)

    elif backdata.get('action') == "@CofS_Y":
        Manager.postback_US(event, user_id, "CofS_Y")
    
    elif backdata.get('action') == "@CofS_N":
        Manager.postback_US(event, user_id, "CofS_N")

    # 重新發送-修改時間
    elif backdata.get('action') == "@CST":
        if Manager.users[user_id].status == "Hs":
            reply_message = "尚未開發"
            Manager.users[user_id].status = "Fs"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    # 重新發送-修改內容
    elif backdata.get('action') == "@CC":
        if Manager.users[user_id].status == "Hs":
            reply_message = "尚未開發"
            Manager.users[user_id].status = "Fs"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    
    # 重新發送-整體修改
    elif backdata.get('action') == "@CA":
        if Manager.users[user_id].status == "Hs":
            reply_message = "尚未開發"
            Manager.users[user_id].status = "Fs"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    





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
                Manager.users[user_id].isAdm = 1
        elif teacher == False:
            Manager.users[user_id].status = "Ss1"
            reply_message =  "老師好, 請輸入您的名稱"
            line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
        
        else:
            reply_message = "資料庫錯誤，錯誤代碼:E0002，請洽管理人員"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
            print(f"**There are more than one {user_id} in the database!!**")
        
    # print(Manager.users[user_id].status)

    # 個人資訊設定1
    if Manager.users[user_id].status == "Ss1":
        Manager.handle_Ss1(event, user_id, text)
    
    # 個人資訊設定2
    elif Manager.users[user_id].status == "Ss2":
        Manager.handle_Ss2(event, user_id, text)


    # 廣播訊息 2.1
    elif Manager.users[user_id].status == "Bs2.1":
        Manager.handle_Bs2_1(event, user_id, text)
    
    # 廣播訊息 2.2
    elif Manager.users[user_id].status == "Bs2.2":
        Manager.handle_Bs2_2(event, user_id, text)
    
    # 廣播訊息 3
    elif Manager.users[user_id].status == "Bs3":
        Manager.handle_Bs3(event, user_id, text)
    
    # 空閒
    elif Manager.users[user_id].status == "Fs":
        Manager.handle_Fs(event, user_id, text)

    # 管理員認證
    elif Manager.users[user_id].status == "ACs":
        Manager.handle_Admin1(event, user_id, text)

if __name__ == '__main__':
    app.run()
