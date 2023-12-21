
import re
from urllib.parse import parse_qsl
from linebot.models import  ConfirmTemplate, MessageEvent, TextMessage, TextSendMessage, PostbackTemplateAction, PostbackEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from flask import request, abort



pattern = r'(\d+)[, ]*'
AdminConfirmPatter = r'(\d+-\d+|\d+)'
class_list = ['701', '702', '703', '704', '705', '706', '801', '802', '803', '804', '805', '806', '901', '902', '903', '904', '905',
              '906', '101', '102', '103', '104', '105', '106', '111', '112', '113', '114', '115', '116', '121', '122', '123', '124', '125', '126']
grade_list = ['1', '2', '3', '4', '5','7', '8', '9']

dataTemplate = {'content':"", 'classLs': [], 'classStr': "", 'des_class': "", 'des_grade': "", 'group_send': ""}
# dataTemplate['content'] = ""
# dataTemplate['classLs'] = []
# dataTemplate['classStr'] = " "
# dataTemplate['des_class'] = ""
# dataTemplate['des_grade'] = ""
# dataTemplate['group_send'] = "" 




class Teacher():
    
    def __init__(self, id, name = None, office = None, status = None, isAdm = [], data = dataTemplate):
        self.id = id
        self.name = name
        self.office = office
        self.isAdm = isAdm
        self.data = data
        self.status = status

class Bot():

    def __init__(self, api, database, users):
        self.api = api
        self.db = database
        self.users = users 

    def SendButton(self, event):
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
            self.api.reply_message(event.reply_token, message)
        except Exception as e:
            print(e)
            self.api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！請洽資訊組長'))
    



    
    def confirm_yes(self, event, user_id):
        if self.users[user_id].status == "Cs":
                data = {}
                reply_message = "成功發布訊息"
                self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
                user = self.db.getTeacher(user_id)
                if user != False and user != "Error":
                    data["name"] = user.name
                    data["office"] = user.office
                    data["des_class"] = None
                    data["des_grade"] = None
                    data["group_send"] = None
                    data['content'] = self.users[user_id].data['content']

                    if len(self.users[user_id].data['classLs']) == 0:
                        data['content'] = self.users[user_id].data['content']
                        data['des_class'] = self.users[user_id].data['des_class']
                        data['des_grade'] = self.users[user_id].data['des_grade'] 
                        ack = self.db.insertData(data)
                        print(ack)
                    else:
                        if self.users[user_id].data['group_send'] == 0:
                            data['group_send'] = 0
                            ack = self.db.insertData(data)
                            print(ack)
                        else:    
                            
                            for C in self.users[user_id].data["classLs"]:
                                if len(C) == 1:
                                    data['group_send'] = C
                                    self.db.insertData(data)
                                    
                                else:
                                    if int(C[2]) <= 6 and int(C[2]) > 0:
                                        if int(C[0:1]) == 7 or int(C[0:1]) == 8 or int(C[0:1]) == 9:                    
                                                data['des_grade'] = "0" + C[0:1]
                                                data['des_class'] = C[2]
                                                self.db.insertData(data)
                                        else:                                    
                                                data['des_grade'] = C[0:2]
                                                data['des_class'] = C[2]
                                                self.db.insertData(data)
                elif user == "Error":
                    pass
                    # Send message to Admin
                else:
                    reply_message = "插入失敗，請設置教師個人資訊或洽資訊組"
                    self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        
        else:
            reply_message = "請勿重複點選"
            self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
        
        self.users[user_id].status = "Fs"
        self.users[user_id].data['content'] = ""
        self.users[user_id].data['classLs'] = []
        self.users[user_id].data['classStr'] = " "
        self.users[user_id].data['des_class'] = ""
        self.users[user_id].data['des_grade'] = ""
        self.users[user_id].data['group_send'] = "" 
        # self.users[user_id] = ""
            


    def confirm_no(self, event, user_id):
        if self.users[user_id].status == "Cs":
            reply_message = "訊息有誤 請重新輸入訊息\n請輸入您的廣播內容"
            self.users[user_id].status = "Bs1"
            self.users[user_id].data.clear()

            self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
        else:
            reply_message ="請勿重複點選"
            self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))


    
    def sendConfirm(self,event, user_id):
        try:
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
                text=f"傳送班級:{(self.users[user_id].data['classStr'])} \n傳送老師:{self.users[user_id].name}\n傳送處室:{self.users[user_id].office}\n\n廣播訊息:\n{self.users[user_id].data['content']}")
            self.api.push_message(user_id, confirmData)
            self.api.reply_message(event.reply_token, message)
            self.cancelTemplate(user_id)
        except Exception as e:
            print(e)
            self.api.reply_message(event.reply_token, TextSendMessage(text="確認按鈕傳送錯誤，請再試一次或聯絡管理員 錯誤代碼: E001")) # 按鈕發生錯誤

    # 個人資訊確認按鈕
    def sendSettingConfirm(self, user_id):
        try:
            message = TemplateSendMessage(
                alt_text='Confirm template',
                template=ConfirmTemplate(
                    # 把廣播訊息重複在此
                    text=f"請問確認是否輸入錯誤（請檢察將送出的訊息是否正確）",
                    actions=[
                        PostbackTemplateAction(
                            label='YES 我已確認',
                            data='action=CofS_Y'
                        ),
                        PostbackTemplateAction(
                            label='NO 訊息有誤',
                            data='action=ConfS_N'
                        ),
                    ]
                )
            )
            self.api.push_message(user_id, message)
            self.cancelTemplate(user_id)
        except Exception as e:
            print(e)
            self.api.push_message(user_id, TextSendMessage(text="確認按鈕傳送錯誤，請再試一次或聯絡管理員 錯誤代碼: E001")) # 按鈕發生錯誤
    
    
    # 取消按鈕
    def cancelTemplate(self, user_id):
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
   
        self.api.push_message(user_id, message)



    # 管理員認證按鈕
    def AdminConfirm(self, event, user_id):
        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                # 把廣播訊息重複在此
                text=f"許可新加入用戶",
                actions=[
                    PostbackTemplateAction(
                        label='許可',
                        data='action=Adm_Yes'
                    ),
                    PostbackTemplateAction(
                        label='拒絕',
                        data='action=Adm_No'
                    ),
                ]
            )
        )
        self.api.reply_message(event.reply_token, message)
        self.cancelTemplate(user_id)


    
    # 單獨或群發按鈕
    def select_target(self, event):
        try:
            message = TemplateSendMessage(
                alt_text='Confirm template',
                template=ConfirmTemplate(
                    # 把廣播訊息重複在此
                    text=f"請問發送對象為......",
                    actions=[
                        PostbackTemplateAction(
                            label='個別發送',
                            data='action=select_class'
                        ),
                        PostbackTemplateAction(
                            label='群發年級',
                            data='action=select_group'
                        ),
                    ]
                )
            )
            self.api.reply_message(event.reply_token, message)
        except Exception as e:
            print(e)


    # 傳送訊息按鈕
    def postback_Bs(self, event, user_id):
        if self.db.findTeacher(user_id):
            if self.db.verified(user_id):
                reply_message = "請輸入廣播訊息"
                self.users[user_id].status = "Bs1"
                self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
                self.cancelTemplate(user_id)
            else:
                reply_message = "管理員尚未驗證"
                send_message = "請輸入您的姓名"
                self.users[user_id].status = "Ss1"
                self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
                self.api.push_message(user_id, TextSendMessage(text=send_message))
        else:
            reply_message = "您尚未註冊，請先設定教師個人資訊"
            self.users[user_id].status = "Fs"
            self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))

    # 設置教師個人資訊
    def postback_Ss(self, event, user_id):
        isRegis = self.db.findTeacher(user_id)
        self.users[user_id].status = "Ss1"
        if isRegis != "Error" and isRegis != False:
            reply_message = "重新設定教師個人資訊\n請輸入您的姓名"

        else:
            reply_message = "設定教師個人資訊\n請輸入您的姓名"

        self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    # 歷史訊息按紐處理
    def postback_Hs(self, event, user_id):
        reply_message = "以下是您最近發送的歷史訊息"
        self.users[user_id].status = "Hs"
        history_data = []
        history_data = self.db.getHistoryData(user_id)
        reply_message = "歷史訊息\n"
        self.sort_history_message(user_id)
        for i in range(1,len(history_data[user_id])+1, 1):
            if history_data[user_id][i-1].group_send != None:
                reply_message += f"▶️{i})  {history_data[user_id][i-1].time} To:{history_data[user_id][i-1].group_send} \n\t {history_data[user_id][i-1].content} \n"
            else:
                reply_message += f"▶️{i})  {history_data[user_id][i-1].time} To:{history_data[user_id][i-1].des_grade} \n\t {history_data[user_id][i-1].content} \n"
        self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
        self.cancelTemplate(user_id)

    # 選擇特定班級按鈕 Select Class
    def postback_Sc(self, event, user_id):
        if self.users[user_id].status == "Bs2":
            reply_message = "您選擇個別發送，請輸入要發送的班級 ex: 703"
            self.users[user_id].status = "Bs2.1"
            self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
            self.cancelTemplate(user_id)
        else:
            reply_message ="請勿重複點選"
            self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))

    # 選擇群發按鈕 Select group
    def postback_Sg(self, event, user_id):
        if self.users[user_id].status == "Bs2":
            reply_message = "選擇群發年級!\n請輸入傳送班級 (請輸入中文字後的代號)\n 全校 0 \n 高一 1 \n 高二 2 \n 高三 3 \n 高中 4 \n 國中 5 \n 七年級 7 \n 八年級 8 \n 九年級 9\n 特定跳班級 班級三位數並用逗號或空格隔開"
            self.users[user_id].status = "Bs2.2"
            self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
            self.cancelTemplate(user_id)
        else:
            reply_message ="請勿重複點選"
            self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))

    # 取消按鈕處理
    def postback_C(self, event, user_id):
        if self.users[user_id].status != "Fs":
            self.users[user_id].status = "Fs"
            reply_message = "已取消"
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))


    # 管理員許可按鈕處理
    def postback_Adm(self, event, user_id, t):
        if t == "Adm_Yes":
            client = self.users[user_id].isAdm[1][0]
            sendStat = self.db.modifyVerifyStat(client)
            AdminList = self.db.find_Admin()
            
            if sendStat == True:
                message = "已更新"
                for Admin in AdminList:
                    if Admin != user_id:
                        ToAdmMes = f"{self.users[user_id].name} 已許可 在{self.users[client].office} 的 {self.users[client].name}"
                        self.api.push_message(Admin, TextSendMessage(text= ToAdmMes))
                ToClientMes = "管理員已許可，歡迎使用!"
                self.api.push_message(client, TextSendMessage(text=ToClientMes))
            elif sendStat == "Uped":
                message = "此用戶已被更新"
            else:
                message = "資料庫異常，請洽工程師"
            self.api.reply_message(event.reply_token, TextSendMessage(text=message))
        else:
            client = self.users[user_id].data['confirmList'][0]
            delStat = self.db.DelTeacherData(client)
            AdminList = self.db.find_Admin()
            if delStat == True:
                message = "已刪除此用戶"
                if Admin != user_id:
                        ToAdmMes = f"{self.users[user_id].name} 已拒絕 在{self.users[client].office} 的 {self.users[client].name}"
                        self.api.push_message(Admin, TextSendMessage(text= ToAdmMes))
                    
                ToClientMes = "很抱歉，管理員沒有允許您的請求"
                self.api.push_message(client, TextSendMessage(text=ToClientMes))
            else:
                message = "資料庫異常"
            self.api.reply_message(event.reply_token, TextSendMessage(text=message))


    # 個人資訊確認按鈕處理 User Setting
    def postback_US(self, event, user_id, t):
        if t == "CofS_Y":
            self.db.insertTeaInfor(user_id, {'name': self.users[user_id].name, 'office': self.users[user_id].office, "verifyStat": 0})
            print(self.users[user_id].name)
            AdminList = self.db.findAdmin()
            if AdminList != False:
                for Admin in AdminList:
                    if Admin not in self.users:
                        self.users[Admin] = Teacher(Admin, isAdm=[1, []])
                    else:
                        self.users[Admin].status = "ACs"
                    self.users[Admin].isAdm[1].append(user_id)
                    self.api.push_message(
                        Admin, TextSendMessage(text=f"有新教師加入‼\n請許可或拒絕\n教師名稱:{self.users[user_id].name}\n處室:{self.users[user_id].office}"))
                    self.AdminConfirm(event, user_id)

                reply = "已送交，等待管理員確認"
                self.api.reply_message(event.reply_token, TextSendMessage(text=reply))
            else:
                reply = "伺服器錯誤，請詢問資訊組"
                self.api.reply_message(event.reply_token, TextSendMessage(text=reply))
                print("**Error: There isn't any Admin in the database!!**")
            self.users[user_id].status = "Fs"
        else:
            isRegis = self.db.findTeacher(user_id)
            self.users[user_id].status = "Ss1"
            if isRegis != "Error" and isRegis != False:
                reply_message = "重新設定教師個人資訊\n請輸入您的姓名"

            else:
                reply_message = "設定教師個人資訊\n請輸入您的姓名"

            self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))



    # 設置個人資訊一
    def handle_Ss1(self, event, user_id, text):
        self.users[user_id].name = text
        self.users[user_id].status = "Ss2"
        reply = f"您好 {text} \n請輸入您所在的處室"
        self.api.reply_message(event.reply_token, TextSendMessage(text=reply))
        self.cancelTemplate(user_id)


    # 設置個人資訊二
    def handle_Ss2(self, event, user_id, text):
        self.users[user_id].office = text
        reply = f"您的名字為 {self.users[user_id].name} 所在處室 {self.users[user_id].office}"
        self.api.reply_message(event.reply_token, TextSendMessage(text=reply))
        self.sendSettingConfirm(user_id)
        

    
    # 管理員許可1
    def handle_admin1(self, event, user_id):
        if self.db.isAdmin(user_id):
            getList = self.db.findUnVerify()
        if getList != False:
            headNum = 1
            confirmList  = []
            reply_message = "以下為尚未驗證之列表，請透過數字鍵來表示要許可之用戶，其他將會被拒絕 ex 1~4 7 表示1到4號和7號都會許可"
            for user in getList:
                reply_message += f"\n{headNum} {user.teacher} {user.fromWhere}"
                headNum += 1
                confirmList[headNum] = user.teacher
            self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))
            self.users[user].data['confirmList'] = []
        else:
            reply_message = "目前無須認證名單"
            self.api.reply_message(
        event.reply_token, TextSendMessage(text=reply_message))

    # 管理員許可2
    def handle_Admin2(self, event, user_id,text):
        result = re.findall(AdminConfirmPatter, text)
        if result != None:
            for scope in result:
                if "-" in scope:
                    for i in range(int(scope[0:1]), int(scope[2:3])+1):
                        self.db.modifyVerifyStat(self.users[user_id].data['confirmList'][i])
                else:
                    print(scope)
                    self.db.modifyVerifyStat(self.users[user_id].data['confirmList'][int(scope)])
            reply_message = "更新成功"
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            self.users[user_id].status = "Fs"
        else:
            reply_message = "輸入錯誤"
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))


    # 廣播訊息1
    def handle_Bs1(self, event, user_id, text):
        if len(text) > 200:
            reply_message = f"輸入字數請勿超過200字, 目前字數{len(text)}"
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            self.cancelTemplate(user_id)
        elif text.count('\n') > 10:
            reply_message = "訊息請勿超過10行，目前行數" + text.count('\n')
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            self.cancelTemplate(user_id)
        else:
            self.users[user_id].data['content'] = text
            reply_message = '請問發送對象為...(請輸入中文字後的代號)\n特定班級 0 \n 群發年級 1'
            self.users[user_id].status = "Bs2"
            self.select_target(event)
            self.cancelTemplate(user_id)


    # 廣播訊息2
    def handle_Bs2(self, event, user_id, text):
        if text == '0':
                self.users[user_id].status = 'Bs2.1'
                reply_message = "請輸入班級"
                self.api.reply_message(
                event.reply_token, TextSendMessage(text=reply_message))
                self.cancelTemplate(user_id)
        elif text == '1':
            self.users[user_id].status = 'Bs2.2'
            reply_message = "選擇群發年級!\n請輸入傳送班級 (請輸入中文字後的代號)\n 全校 0 \n 高一 1 \n 高二 2 \n 高三 3 \n 高中 4 \n 國中 5 \n 七年級 7 \n 八年級 8 \n 九年級 9\n 特定跳班級 班級三位數並用逗號或空格隔開"
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            self.cancelTemplate(user_id)
        else:
            reply_message = '請輸入有效代碼'
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            self.cancelTemplate(user_id)
    
    # 單獨班級廣播
    def handle_Bs2_1(self, event, user_id, text):
        if text.isdigit() and len(text) == 3:
            self.users[user_id].data['group_send'] = None
            if int(text[2]) <= 6 and int(text[2]) > 0:
                self.users[user_id].data['classStr'] = text
                if int(text[0:1]) == 7 or int(text[0:1]) == 8 or int(text[0:1]) == 9:
                    self.users[user_id].data['des_grade'] = "0" + text[0:1]
                    self.users[user_id].data['des_class'] = text[2]
                else:
                    self.users[user_id].data['des_grade'] = text[0:2]
                    self.users[user_id].data['des_class'] = text[2]
                self.sendConfirm(event, user_id)
                self.users[user_id].status = "Cs"
            else:
                reply_message = "請輸入在範圍內的班級"
                self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
                self.cancelTemplate(user_id)
        else:
            reply_message = "請輸入班級"
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            self.cancelTemplate(user_id)

    # 群發廣播
    def handle_Bs2_2(self, event, user_id, text):
        number_groups = re.findall(pattern, text) # 使用正則表達式解析(僅可判斷以空格或逗號隔開)
        if number_groups != []:
            for group in number_groups:
                if len(group) == 1:   # 判斷為年級或班級
                    if group == "0":
                        self.users[user_id].data['classStr'] = "全體廣播"
                        self.users[user_id].data['des_class'] = None
                        self.users[user_id].data['des_grade'] = None
                        self.users[user_id].data['group_send'] = "0"
                        self.users[user_id].data['classLs'].clear()
                        break
                    elif group == "4":
                        self.users[user_id].data['classStr']  += "高中部 "
                        self.users[user_id].data['classLs'].append(group)
                    elif group == "5":
                        self.users[user_id].data['classStr'] += "國中部 "
                        self.users[user_id].data['classLs'].append(group)
                    else:
                        if  group in grade_list:
                            if int(group) < 4:
                                if "4" not in number_groups:
                                    self.users[user_id].data['classLs'].append(group)
                                    self.users[user_id].data['classStr'] += group + "年級 "
                            else:
                                if "5" not in number_groups:
                                    self.users[user_id].data['classLs'].append(group)
                                    self.users[user_id].data['classStr'] += group + "年級 "
                        else:
                            reply_message = "請輸入正確數字範圍"
                            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
                            break
                elif len(group) == 3:
                    if group in class_list:
                        if int(group[0:1]) < 4: 
                            if "4" not in number_groups:
                                self.users[user_id].data['classStr'] += group + " "
                                self.users[user_id].data['classLs'].append(group)
                                print(group)
                        else:
                            if "5" not in number_groups:
                                self.users[user_id].data['classStr'] += group + " "
                                self.users[user_id].data['classLs'].append(group)
                                print(group)

                    else:
                        reply_message = "請輸入正確班級"
                        self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
                        break
            self.users[user_id].status = "Cs"
            self.sendConfirm(event, user_id)
        else:
            reply_message = "請輸入有效代碼"
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))

    # 空閒
    def handle_Fs(self, event, user_id, text):
        if text == "1":
                isRegis = self.db.findTeacher(user_id)
                self.users[user_id].status = "Ss1"
                if isRegis != "Error" and isRegis != False:
                    reply_message = "重新設定教師個人資訊\n請輸入您的姓名"

                else:
                    reply_message = "設定教師個人資訊\n請輸入您的姓名"

                self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        elif text == "2":
            if self.db.findTeacher(user_id):
                if self.db.verified(user_id):
                    reply_message = "請輸入廣播訊息"
                    self.users[user_id].status = "Bs1"
                    self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
                    self.cancelTemplate(user_id)
                else:
                    reply_message = "管理員尚未驗證"
                    
                    self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
                    self.api.push_message(user_id, TextSendMessage(text=send_message))
            else:
                reply_message = "您尚未註冊，請先設定教師個人資訊"
                send_message = "請輸入您的姓名"
                self.users[user_id].status = "Ss1"
                self.users[user_id].status = "Fs"
                self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
        else:
            self.SendButton(event)

    # 歷史訊息排序
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



# 交換班級格式
def swapClassFromat(des_grade, des_class):
    result = des_grade[1:] + des_grade[0:1] + des_class
    print(result)
    return result 