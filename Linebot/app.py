import json
import re
import database_lastest as db
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


sendClassString = " "
send_class_list = []
data = {}
tea_infor = {}
user_states = {}
global pattern
pattern = r'(\d+)[, ]*'
class_list = ['701', '702', '703', '704', '705', '706', '801', '802', '803', '804', '805', '806', '901', '902', '903', '904', '905',
              '906', '101', '102', '103', '104', '105', '106', '111', '112', '113', '114', '115', '116', '121', '122', '123', '124', '125', '126']


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
                thumbnail_image_url='https://www.ahs.nccu.edu.tw/ischool/resources/WID_0_13_0ce2b9c79ca44206e2a2bf72c2010f148662e9ed/463eb099b18cfc7b518b81007c909b64.png',
                title='請選擇服務：',
                text='請務必先點選"教師個人資訊"按鈕以設定身分',
                actions=[
                    # URITemplateAction(
                    #     label='連結校網',
                    #     text='連結校網',
                    #     uri='https://ahs.nccu.edu.tw/home'
                    # ),
                    PostbackTemplateAction(
                        label='教師個人資訊',
                        data='action=教師個人資訊'
                    ),
                    PostbackTemplateAction(
                        label='發送廣播 [上限300字]',
                        data='action=文字廣播'
                    ),                   
                    PostbackTemplateAction(
                        label='其他',
                        data='action=其他'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！請洽鍾2鍾'))

#教師初次登入
@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    reply_message = "老師好, 請輸入您的名稱"
    user_states[user_id] = "設定教師個人資訊階段1"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))


@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    # backdata = event.postback.data
    backdata = dict(parse_qsl(event.postback.data))
    if backdata.get("action") == "文字廣播":
        reply_text = "請輸入廣播訊息"
        user_states[user_id] = "廣播訊息階段1"

    elif backdata.get("action") == "教師個人資訊":
        reply_text = "設定教師個人資訊\n請輸入您的姓名"
        user_states[user_id] = "設定教師個人資訊階段1"

    elif backdata.get("action") == "其他":
        reply_text = "您選擇了其他！\n不過此功能尚在開發中"
        user_states[user_id] = "其他"

    elif backdata.get('action') == 'sell':
        sendData_sell(event, backdata)
    
    elif backdata.get('action') == "confirm_yes":
            reply_text = "成功發布訊息"
            user = db.findTeacher(user_id)
            if user != False and user != "Error":
                data['teacher'] = user.teacher
                data['office'] = user.fromWhere
                db.insertData(data)
            else:
                reply_message = "插入失敗"

    elif backdata.get('action') == "confirm_no":
        reply_text = "訊息有誤 請重新輸入訊息\n請輸入您的廣播內容"
        user_states[user_id] = "廣播訊息階段1"

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_text))
    



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
    note = False

    if user_id in user_states:
        user_state = user_states[user_id]
        # 廣播訊息
        if user_state == "廣播訊息階段1":
            if len(text) > 300:
                reply_message = f"輸入字數請勿超過300字, 目前字數{len(text)}"
            else:
                data['content'] = text
                reply_message = '請問發送對象為...(請輸入中文字後的代號)\n特定班級 0 \n 群發年級 1'
                user_states[user_id] = "廣播訊息階段2"

        elif user_state == "廣播訊息階段2":
            if text == '0':
                user_states[user_id] = '廣播訊息階段2-1'
                reply_message = "輸入班級"
            elif text == '1':
                user_states[user_id] = '廣播訊息階段2-2'
                reply_message = "選擇群發年級!\n請輸入傳送班級 (請輸入中文字後的代號)\n 全校 0 \n 高一 1 \n 高二 2 \n 高三 3 \n 七年級 7 \n 八年級 8 \n 九年級 9\n 特定跳班級 班級三位數並用逗號或空格隔開"
            else:
                reply_message = '請輸入有效代碼'

        elif user_state == "廣播訊息階段2-1":
            if text.isdigit() and len(text) == 3:
                sendClassString = text
                if int(text[2]) <= 6 and int(text[2]) > 0:
                    if int(text[0:1]) == 7 or int(text[0:1]) == 8 or int(text[0:1]) == 9:
                        data['des_grade'] = "0" + text[0:1]
                        data['des_class'] = text[2]
                    else:
                        data['des_grade'] = text[0:2]
                        data['des_class'] = text[2]
                    sendConfirm(event, user_id)
                    note = True
                    user_states[user_id] = "空閒"
                else:
                    reply_message = "請輸入在範圍內的班級"
            else:
                reply_message = "請輸入班級"

        elif user_state == "廣播訊息階段2-2":
            number_groups = re.findall(pattern, text)
            for group in number_groups:
                if len(group) == 1:
                    if group == "0":
                        reply_message = "全體廣播"
                        sendClassString = "全體廣播"
                        break
                    else:
                        if int(group) <= 9 or int(group) >= 2:
                            send_class_list.append(text)
                            sendClassStirng = sendClassString + group + "年級,"
                            print(group)
                if len(group) == 3:
                    if group in class_list:
                        sendClassString += group + ","
                        send_class_list.append(text)
                        print(group)
                    else:
                        reply_message = "請輸入正確班級"
                else:
                    reply_message = "請輸入有效代碼"

            user_states[user_id] = "廣播訊息階段2-3"
        
        elif user_state == "空閒":
            if text == "!":
                sendButton(event)
                note=True

       # 設定教師個人資訊
        elif user_state == "設定教師個人資訊階段1":
            tea_infor['teacher'] = text
            reply_message = "輸入成功!\n 請輸入處室"
            user_states[user_id] = "設定教師個人資訊階段2"
        elif user_state == "設定教師個人資訊階段2":
            tea_infor['fromWhere'] = text
            reply_message = "成功"
            db.insertTeaInfor(user_id, tea_infor)
            user_states[user_id] = "空閒"
        # 其他
        elif user_state == "其他":
            reply_message = "還在開發中"

    else:  # 改上去
        if text == "!" or text == "！":
            sendButton(event)
            note = True

    if note == False:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    else:
        note = False


def sendConfirm(event, userid):
    # try:
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
        text=f"傳送班級:{sendClassString} \n\n 廣播訊息:\n{data['content']}")
    line_bot_api.push_message(userid, confirmData)
    line_bot_api.reply_message(event.reply_token, message)

    # except:
    #     print("Error sendConfirm")


def senddatetime(event):
    try:
        message = TemplateSendMessage(
            alt_text='日期與時間',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
                title='日期與時間test',
                text='請選擇',
                actions=[
                    DatetimePickerTemplateAction(
                        label='選取日期',
                        data='action=sell&mode=date',
                        mode='date',
                        initial='2023-8-21',
                        min='2023-8-21',
                        max='2023-9-25'
                    ),
                    DatetimePickerTemplateAction(
                        label='選取時間',
                        data='action=sell&mode=time',
                        mode='time',
                        initial='08:00',
                        min='00:00',
                        max='23:59'
                    ),
                    DatetimePickerTemplateAction(
                        label='選取日期and時間',
                        data='action=sell&mode=datetime',
                        mode='date',
                        initial='2023-8-21T08:00',
                        min='2023-8-21T00:00',
                        max='2023-9-25T23:59'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message( event.reply_token, TextSendMessage(text="發生錯誤(datetime)!"))


def sendData_sell(event, backdata):
    try:
        if backdata.get('mode') == 'date':
            dt = '日期為：' + event.postback.params.get('date')
        elif backdata.get('mode') == 'date':
            dt = '時間為：' + event.postback.params.get('date')
        elif backdata.get('mode') == 'date':
            dt = '日期為：' + event.postback.params.get('date')
            dt = '日期為：' + event.postback.params.get('date')
        message = TextSendMessage(text=dt)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="發生錯誤(sendData_sell)!"))


if __name__ == '__main__':
    app.run()
