import json
import re
import databaseV2_4 as db
from linebot.models.flex_message import FlexContainer
from datetime import datetime
from urllib.parse import parse_qsl
from linebot.models import DatetimePickerTemplateAction, MessageTemplateAction, ConfirmTemplate, FlexSendMessage, MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, URITemplateAction, PostbackTemplateAction, PostbackEvent, CarouselTemplate, CarouselColumn, TemplateSendMessage, ButtonsTemplate, FollowEvent, PostbackAction
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from linebot.v3.messaging import MessagingApi
from flask import request, abort
from flask import Flask, request, abort
app = Flask(__name__)


# mydb = datafun.initialize_db()

line_bot_api = LineBotApi('X8irZcY8i/i8v5vSZshQ/PEUXKzX4twNZc3v+7OgOnDy12/oSrAAtc90bpmlNuRIFAPK0DDWaqYsaSXSdW3/d2q54U82JCX1RGBeFL2+sAfWT0O/uK9MrlOnwtxdnpS7+M3n4QKI58Tix4odkwJFWQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d060df7ed691aca2f1cf8a2aa58620ac')


sendClassString = {}
send_class_list = {}
data = {}
tea_infor = {}
user_states = {}
confirmList = {}
note = {}
history_data = {}
global pattern
global AdminConfirmPatter
pattern = r'(\d+)[, ]*'
AdminConfirmPatter = r'(\d+-\d+|\d+)'

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


def sendButton(event):
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            
            template=ButtonsTemplate(
                title='請選擇服務：',
                thumbnail_image_url = "https://raw.githubusercontent.com/jason355/SWBS/main/img1.png",
                text='請務必先點選"教師個人資訊"按鈕以設定身分',
                actions=[
                    PostbackTemplateAction(
                        label='1 教師個人資訊',
                        data='action=教師個人資訊'
                    ),
                    PostbackTemplateAction(
                        label='2 發送廣播',
                        data='action=文字廣播'

                    ),
                    PostbackTemplateAction(
                        label='3 歷史訊息',
                        data='action=歷史訊息'
                    ),
                    PostbackTemplateAction(
                        label='4 幫助',
                        data = 'action=幫助'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！請洽資訊組長'))

# 教師初次登入
def handle_follow(event):
    user_id = event.source.user_id
    reply_message = "老師好, 請輸入您的名稱"
    user_states[user_id] = "Ss1"
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
    # backdata = event.postback.data
    backdata = dict(parse_qsl(event.postback.data))

    # 文字訊息按鈕
    if backdata.get("action") == "文字廣播":
        if db.findTeacher(user_id):
            if db.verified(user_id):
                reply_message = "請輸入廣播訊息"
                user_states[user_id] = "Bs1"
                line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
                cancelTemplate(user_id)
            else:
                reply_message = "管理員尚未驗證"
                user_states[user_id] = "Fs"
                line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
        else:
            reply_message = "您尚未註冊，請先設定教師個人資訊"
            user_states[user_id] = "Fs"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    elif backdata.get("action") == "教師個人資訊":
        reply_message = "設定教師個人資訊\n請輸入您的姓名"
        user_states[user_id] = "Ss1"
        line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
        cancelTemplate(user_id)

    elif backdata.get("action") == "歷史訊息":
        reply_message = "以下是您最近發送的歷史訊息"
        user_states[user_id] = "Hs"
        if user_id not in history_data:
            history_data[user_id] = []
        history_data[user_id] = db.getHistoryData(user_id)
        reply_message = "歷史訊息\n"
        sort_history_message(user_id)
        for i in range(1,len(history_data[user_id])+1, 1):
            if history_data[user_id][i-1].group_send != None:
                reply_message += f"▶️{i})  {history_data[user_id][i-1].time} To:{history_data[user_id][i-1].group_send} \n\t {history_data[user_id][i-1].content} \n"
            else:
                reply_message += f"▶️{i})  {history_data[user_id][i-1].time} To:{history_data[user_id][i-1].des_grade} \n\t {history_data[user_id][i-1].content} \n"
        line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
        cancelTemplate(user_id)
    # 確認發送訊息
    elif backdata.get('action') == "confirm_yes":  
        if user_states[user_id] == "Cs":
            reply_message = "成功發布訊息"
            line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
            user = db.getTeacher(user_id)
            if user != False and user != "Error":
                data[user_id]['teacher'] = user.teacher
                data[user_id]['office'] = user.fromWhere
                if len(send_class_list[user_id]) == 0:
                    db.insertData(data[user_id])
                else:
                    for C in send_class_list[user_id]:
                        if len(C) == 1:
                            data[user_id]["des_class"] = None
                            data[user_id]["des_grade"] = None
                            data[user_id]["group_send"] = C
                            db.insertData(data[user_id])
                            
                        else:
                            if int(C[2]) <= 6 and int(C[2]) > 0:
                                if int(C[0:1]) == 7 or int(C[0:1]) == 8 or int(C[0:1]) == 9:                    
                                        data[user_id]['des_grade'] = "0" + C[0:1]
                                        data[user_id]['des_class'] = C[2]
                                        db.insertData(data[user_id])
                                else:                                    
                                        data[user_id]['des_grade'] = C[0:2]
                                        data[user_id]['des_class'] = C[2]
                                        db.insertData(data[user_id])
                

            else:
                reply_message = "插入失敗，請設置教師個人資訊或洽資訊組"
                line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
            user_states[user_id] = "Fs"
            send_class_list[user_id].clear()
            data[user_id].clear()
            sendClassString[user_id] = ""

        else:
            reply_message = "請勿重複點選"
            line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))

    elif backdata.get('action') == "confirm_no":
        if user_states[user_id] == "Cs":
            reply_message = "訊息有誤 請重新輸入訊息\n請輸入您的廣播內容"
            user_states[user_id] = "Bs1"
            send_class_list[user_id].clear()
            data[user_id].clear()
            sendClassString[user_id] = ""
            line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
        else:
            reply_message ="請勿重複點選"
            line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))

    elif backdata.get('action') == "select_class":
        if user_states[user_id] == "Bs2":
            reply_message = "您選擇個別發送"
            user_states[user_id] = "Bs2.1"
            line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
            cancelTemplate(user_id)
        else:
            reply_message ="請勿重複點選"
            line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))

    elif backdata.get('action') == "select_single":
        if user_states[user_id] == "Bs2":
            reply_message = "選擇群發年級!\n請輸入傳送班級 (請輸入中文字後的代號)\n 全校 0 \n 高一 1 \n 高二 2 \n 高三 3 \n 高中 4 \n 國中 5 \n 七年級 7 \n 八年級 8 \n 九年級 9\n 特定跳班級 班級三位數並用逗號或空格隔開"
            user_states[user_id] = "Bs2.2"
            line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
            cancelTemplate(user_id)
        else:
            reply_message ="請勿重複點選"
            line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
    elif backdata.get('action') == "cancel":
        if user_states[user_id] != "Fs":
            user_states[user_id] = "Fs"
            reply_message = "已取消"
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))








# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id
    global data
    global tea_infor
    global send_class_list
    global sendClassString
    global note
    global confirmList
    if user_id not in note:
        note[user_id] = False
    if user_id not in sendClassString:
        sendClassString[user_id] = ""
    if user_id not in send_class_list:
        send_class_list[user_id] = []
    if user_id not in  user_states:
        user_states[user_id] = "Fs" 
    if user_id not in data:
        data[user_id] = {}

    user_state = user_states[user_id]
    # 廣播訊息 輸入廣播內容
    if user_state == "Bs1":
        if len(text) > 200:
            reply_message = f"輸入字數請勿超過200字, 目前字數{len(text)}"
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            cancelTemplate(user_id)
        elif text.count('\n') > 10:
            reply_message = "訊息請勿超過10行，目前行數" + text.count('\n')
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            cancelTemplate(user_id)
        else:
            data[user_id]['content'] = text
            reply_message = '請問發送對象為...(請輸入中文字後的代號)\n特定班級 0 \n 群發年級 1'
            user_states[user_id] = "Bs2"
            note[user_id] = True
            select_target(event, user_id)
            cancelTemplate(user_id)
    # 廣播訊息 發送選擇
    elif user_state == "Bs2":
        if text == '0':
            user_states[user_id] = 'Bs2.1'
            reply_message = "請輸入班級"
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            cancelTemplate(user_id)
        elif text == '1':
            user_states[user_id] = 'Bs2.2'
            reply_message = "選擇群發年級!\n請輸入傳送班級 (請輸入中文字後的代號)\n 全校 0 \n 高一 1 \n 高二 2 \n 高三 3 \n 高中 4 \n 國中 5 \n 七年級 7 \n 八年級 8 \n 九年級 9\n 特定跳班級 班級三位數並用逗號或空格隔開"
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            cancelTemplate(user_id)
        else:
            reply_message = '請輸入有效代碼'
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            cancelTemplate(user_id)
    # 廣播訊息 特定班級發送
    elif user_state == "Bs2.1":
        if text.isdigit() and len(text) == 3:
            data[user_id]['group_send'] = None
            sendClassString[user_id] = text
            if int(text[2]) <= 6 and int(text[2]) > 0:
                if int(text[0:1]) == 7 or int(text[0:1]) == 8 or int(text[0:1]) == 9:
                    data[user_id]['des_grade'] = "0" + text[0:1]
                    data[user_id]['des_class'] = text[2]
                else:
                    data[user_id]['des_grade'] = text[0:2]
                    data[user_id]['des_class'] = text[2]
                sendConfirm(event, user_id)
                note[user_id] = True
                user_states[user_id] = "Cs"
            else:
                reply_message = "請輸入在範圍內的班級"
                line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
                cancelTemplate(user_id)
        else:
            reply_message = "請輸入班級"
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            cancelTemplate(user_id)
    # 廣播訊息 群體發送
    elif user_state == "Bs2.2":
        number_groups = re.findall(pattern, text) # 使用正則表達式解析(僅可判斷以空格或逗號隔開)
        if number_groups != []:
            for group in number_groups:
                if len(group) == 1:   # 判斷為年級或班級
                    if group == "0":
                        sendClassString[user_id] = "全體廣播"
                        data[user_id]['des_class'] = None
                        data[user_id]['des_grade'] = None
                        data[user_id]['group_send'] = "0"
                        send_class_list[user_id].clear()
                        break
                    elif group == "4":
                        sendClassString[user_id] += "高中部 "
                        send_class_list[user_id].append(group)
                    elif group == "5":
                        sendClassString[user_id] += "國中部 "
                        send_class_list[user_id].append(group)
                    else:
                        if  group in grade_list:
                            if int(group) < 4:
                                if "4" not in number_groups:
                                    send_class_list[user_id].append(group)
                                    sendClassString[user_id] += group + "年級 "
                            else:
                                if "5" not in number_groups:
                                    send_class_list[user_id].append(group)
                                    sendClassString[user_id] += group + "年級 "
                        else:
                            note[user_id] = True
                            reply_message = "請輸入正確數字範圍"
                            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
                            break
                elif len(group) == 3:
                    if group in class_list:
                        if int(group[0:1]) < 4: 
                            if "4" not in number_groups:
                                sendClassString[user_id] += group + " "
                                send_class_list[user_id].append(group)
                                print(group)
                        else:
                            if "5" not in number_groups:
                                sendClassString[user_id] += group + " "
                                send_class_list[user_id].append(group)
                                print(group)

                    else:
                        reply_message = "請輸入正確班級"
                        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
                        note[user_id] = True
                        break
            user_states[user_id] = "Cs"
            sendConfirm(event, user_id)
        else:
            reply_message = "請輸入有效代碼"
            note[user_id] = True
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))


        # if note[user_id] != True:
        #     user_states[user_id] = "Cs"
        #     sendConfirm(event, user_id)
        #     note[user_id] = True
        # else:
        #     user_states[user_id] = "Bs2.2"


    # 設定教師個人資訊
    elif user_state == "Ss1":
        if user_id not in tea_infor:
            tea_infor[user_id] = {}
        tea_infor[user_id]['teacher'] = text
        reply_message = "輸入成功!\n 請輸入處室"
        user_states[user_id] = "Ss2"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
        cancelTemplate(user_id)

    elif user_state == "Ss2":
        tea_infor[user_id]['fromWhere'] = text
        tea_infor[user_id]['verifyStat'] = 0
        reply_message = "已送交，等待管理員認證"
        AdminList = db.findAdmin()
        if AdminList != False:
            for Admin in AdminList:
                line_bot_api.push_message(
                    Admin, TextSendMessage(text=f"有新教師加入請使用\"@\"來確認確認\n教師名稱:{tea_infor[user_id]['teacher']}\n處室:{tea_infor[user_id]['fromWhere']}"))
            db.insertTeaInfor(user_id, tea_infor[user_id])
            user_states[user_id] = "Fs"
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))

        else:
            db.insertTeaInfor(user_id, tea_infor[user_id])
            reply_message = "Error code: NAdm"
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
    
    elif user_state == "Fs":
        if text == "1":
            isRegis = db.findTeacher(user_id)
            user_states[user_id] = "Ss1"
            if isRegis != "Error" and isRegis != False:
                reply_message = "重新設定教師個人資訊\n請輸入您的姓名"
            else:
                reply_message = "設定教師個人資訊\n請輸入您的姓名"
        elif text == "2":
            if db.findTeacher(user_id):
                if db.verified(user_id):
                    reply_message = "請輸入廣播訊息"
                    user_states[user_id] = "Bs1"
                    line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
                    cancelTemplate(user_id)
                else:
                    reply_message = "管理員尚未驗證"
                    user_states[user_id] = "Fs"
                    line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            else:
                reply_message = "您尚未註冊，請先設定教師個人資訊"
                user_states[user_id] = "Fs"
                line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
        else:
            sendButton(event)
            note[user_id] = True
   




def select_target(event, user_id):
    # try:
    teacher = db.getTeacher(user_id)
    message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            # 把廣播訊息重複在此
            text=f"請問發送對象為......",
            actions=[
                PostbackTemplateAction(
                    label='特定班級',
                    data='action=select_class'
                ),
                PostbackTemplateAction(
                    label='群發年級',
                    data='action=select_single'
                ),
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

    # except:
    #     print("Error sendConfirm")

def cancelTemplate(user_id):
    message = TemplateSendMessage(
        alt_text='Cancel template',
        template=ButtonsTemplate(
            title=None,
            text=" ",
            actions=[
                PostbackAction(
                    label='取消',
                    data='action=cancel'
                )
            ]
        )
    )
   
    line_bot_api.push_message(user_id, message)

def sendConfirm(event, user_id):
    # try:
    teacher = db.getTeacher(user_id)
    message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            # 把廣播訊息重複在此
            text=f"你確定要發送此則訊息嗎？（請檢察將送出的訊息是否正確）",
            actions=[
                PostbackTemplateAction(
                    label='YES 我已確認',
                    data='action=confirm_yes'
                ),
                PostbackTemplateAction(
                    label='NO 訊息有誤',
                    data='action=confirm_no'
                ),
            ]
        )
    )
    confirmData = TextSendMessage(
        text=f"傳送班級:{sendClassString[user_id]} \n傳送老師:{teacher.teacher}\n傳送處室:{teacher.fromWhere}\n\n廣播訊息:\n{data[user_id]['content']}")
    line_bot_api.push_message(user_id, confirmData)
    line_bot_api.reply_message(event.reply_token, message)
    cancelTemplate(user_id)

    # except:
    #     print("Error sendConfirm")


def sort_history_message(user_id):
    global history_data
    length = len(history_data[user_id])
    for i in range(length):
        if i == length:
            break
        if history_data[user_id][i].group_send != None:
            continue    
        
        if int(history_data[user_id][i].des_grade[1:]) == 7 or int(history_data[user_id][i].des_grade[1:]) == 8 or int(history_data[user_id][i].des_grade[1:]) == 9: 
            history_data[user_id][i].des_grade = f" {swapClassFromat(history_data[user_id][i].des_grade, history_data[user_id][i].des_class)}"
        else:
            history_data[user_id][i].des_grade += f"{history_data[user_id][i].des_class}"
        for j in range(i+1,length, 1):     
            if j == length:
                break
            if history_data[user_id][i].content == history_data[user_id][j].content:
                if int(history_data[user_id][j].des_grade[1:]) == 7 or int(history_data[user_id][j].des_grade[1:]) == 8 or int(history_data[user_id][j].des_grade[1:]) == 9: 
                    history_data[user_id][i].des_grade += f" {swapClassFromat(history_data[user_id][j].des_grade, history_data[user_id][j].des_class)}"
                else:
                    history_data[user_id][i].des_grade += f" {history_data[user_id][j].des_grade + history_data[user_id][j].des_class}"
                del history_data[user_id][j]
                length = len(history_data[user_id])

def swapClassFromat(des_grade, des_class):
    result = des_grade[1:] + des_grade[0:1] + des_class
    print(result)
    return result 


if __name__ == '__main__':
    app.run()
