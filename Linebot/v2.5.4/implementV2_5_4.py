
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

dataTemplate = {'content':"", 'classLs': [], 'classStr': "", 'des_class': "", 'des_grade': "", 'group_send': "", 'history_data': []}
# dataTemplate['content'] = ""
# dataTemplate['classLs'] = []
# dataTemplate['classStr'] = " "
# dataTemplate['des_class'] = ""
# dataTemplate['des_grade'] = ""
# dataTemplate['group_send'] = "" 




class Teacher():
    
    def __init__(self, id, name = None, office = None, status = None, isAdm = None, data = dataTemplate):
        self.id = id
        self.name = name
        self.office = office
        self.isAdm = isAdm
        self.data = data
        self.status = status

class Bot():

    def __init__(self, api, database, users, Confirm_List = []):
        self.api = api
        self.db = database
        self.users = users 
        self.Confirm_List = Confirm_List
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
                            label='1 更改教師個人資訊',
                            data='action=@教師個人資訊'
                        ),
                        PostbackTemplateAction(
                            label='2 發送廣播',
                            data='action=@文字廣播'

                        ),
                        PostbackTemplateAction(
                            label='3 歷史訊息',
                            data='action=@歷史訊息'
                        ),
                        PostbackTemplateAction(
                            label='4 幫助',
                            data = 'action=@幫助'
                        )
                    ]
                )
            )
            self.api.reply_message(event.reply_token, message)
        except Exception as e:
            print(e)
            self.api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！請洽資訊組長'))
    

    # 回覆樣板
    def reply_cancel(self, event, text, needCancel = True):
        if needCancel == True:
            message = TemplateSendMessage(
                alt_text='Text-Cancel template',
                template=ButtonsTemplate(
                    title=None,
                    text= text,
                    actions=[
                        PostbackAction(
                            label='取消',
                            data='action=@cancel'
                        )
                    ]
                )
            )
            self.api.reply_message(event.reply_token, message)

        else:
            self.api.reply_message(event.reply_token, TextSendMessage(text=text))


    # 取消按鈕處理
    def postback_C(self, event, user_id):
        if self.users[user_id].status != "Fs":
            self.users[user_id].status = "Fs"
            reply_message = "已取消"
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))

    # 傳送訊息按鈕
    def postback_Bs(self, event, user_id):
        if self.users[user_id].status != "Bs1":
            if self.db.verified(user_id):
                self.users[user_id].status = "Bs1"
                self.select_target(event)
            else:
                reply_message = "管理員尚未驗證，請耐心等候🙏"
                self.api.reply_message(event.reply_token,TextSendMessage(text=reply_message))


    # 單獨或群發按鈕
    def select_target(self, event):
        try:
            message = TemplateSendMessage(
                alt_text='Button Template',
                template=ButtonsTemplate(
                    # 把廣播訊息重複在此
                    text=f"請問發送對象為......",
                    actions=[
                        PostbackTemplateAction(
                            label='個別發送',
                            data='action=@select_class'
                        ),
                        PostbackTemplateAction(
                            label='群發年級',
                            data='action=@select_group'
                        ),
                        PostbackTemplateAction(
                            label='取消',
                            data='action=@cancel'
                        )
                    ]
                )
            )
            self.api.reply_message(event.reply_token, message)
        except Exception as e:
            print(e)

    # 選擇特定班級按鈕 Select Class
    def postback_Sc(self, event, user_id):
        if self.users[user_id].status == "Bs1":
            reply_message = "您選擇個別發送，請輸入要發送的班級 ex: 703"
            self.users[user_id].status = "Bs2.1"
            self.reply_cancel(event, reply_message)
        


    # 選擇群發按鈕 Select group
    def postback_Sg(self, event, user_id):
        if self.users[user_id].status == "Bs1":
            self.users[user_id].status = "Bs2.2"
            self.select_group_list(event) # 傳送群發按鈕列表

    
    
    # 群發文字
    def select_group_list(self, event):
        try:
            message = TemplateSendMessage(
                alt_text='Button Template',
                template=ButtonsTemplate(
                    # 
                    text=f"選擇群發年級!\n請輸入傳送班級(請輸入中文字後的代號)\n 全校 0 \n 高一 1 \n 高二 2 \n 高三 3 \n 高中 4 \n 國中 5 \n 七年級 7 \n 八年級 8 \n 九年級 9\n 特定跳班級 班級三位數並用逗號或空格隔開",
                    actions=[
                        PostbackTemplateAction(
                            label='取消',
                            data='action=@cancel'
                        )
                    ]
                )
            )
            self.api.reply_message(event.reply_token, message)
        except Exception as e:
            print(e)


    def confirm_yes(self, event, user_id):
        if self.users[user_id].status == "Cs":
                data = {}
                
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

                    else:                            
                        for C in self.users[user_id].data["classLs"]:
                            data["des_class"] = None
                            data["des_grade"] = None
                            data["group_send"] = None
                            if len(C) == 1:
                                data['group_send'] = C
                                self.db.insertData(data)
                                
                            else:
                                if int(C[0:1]) == 7 or int(C[0:1]) == 8 or int(C[0:1]) == 9:                    
                                        data['des_grade'] = "0" + C[0:1]
                                        data['des_class'] = C[2]
                                        self.db.insertData(data)
                                else:                                    
                                        data['des_grade'] = C[0:2]
                                        data['des_class'] = C[2]
                                        self.db.insertData(data)
                    reply_message = "✅已更新置資料庫，將在下一節下課廣播"
                    self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                elif user == "Error":
                    print(f"E0002: The user {user_id} has more than one data in the database")
                    reply_message = "您有多於一筆資料在資料庫中，請洽管理員協助"
                    self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                    # Send message to Admin
                else:
                    reply_message = "插入失敗，請設置教師個人資訊或洽資訊組"
                    self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        
        # else:
        #     reply_message = "請勿重複點選"
        #     self.api.reply_message(
        # event.reply_token, TextSendMessage(text=reply_message))
        
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
            self.users[user_id].status = "Bs1"
            self.users[user_id].data['classLs'] = []
            self.users[user_id].data['classStr'] = " "
            self.users[user_id].data['des_class'] = ""
            self.users[user_id].data['des_grade'] = ""
            self.users[user_id].data['group_send'] = "" 

            self.select_target(event)
        # else:
        #     reply_message ="請勿重複點選"
        #     self.api.reply_message(
        # event.reply_token, TextSendMessage(text=reply_message))


    def sendConfirm(self,event, user_id):
        try:
            message = TemplateSendMessage(
                alt_text='Button template',
                template=ButtonsTemplate(
                    # 把廣播訊息重複在此
                    text=f"你確定要發送此則訊息嗎？\n(請檢察將送出的訊息是否正確)\n教師名稱: {self.users[user_id].name}\n處室: {self.users[user_id].office}\n傳送班級: {self.users[user_id].data['classStr']}\n廣播內容:{self.users[user_id].data['content']}",
                    actions=[
                        PostbackTemplateAction(
                            label='YES 我已確認',
                            data='action=@confirm_yes'
                        ),
                        PostbackTemplateAction(
                            label='NO 訊息有誤',
                            data='action=@confirm_no'
                        ),
                        PostbackTemplateAction(
                            label='取消',
                            data='action=@cancel'
                        )
                    ]
                )
            )
            self.api.reply_message(event.reply_token, message)
        except Exception as e:
            print(e)
            self.api.push_message(user_id, TextSendMessage(text="確認按鈕傳送錯誤，請再試一次或聯絡管理員 錯誤代碼: E0001")) # 按鈕發生錯誤
            self.users[user_id].status = "Fs"
    
    # 單獨班級廣播
    def handle_Bs2_1(self, event, user_id, text):
        if text in class_list:
            self.users[user_id].data['group_send'] = None
            self.users[user_id].data['classLs'] = []
            self.users[user_id].data['classStr'] = text
            if int(text[0:1]) == 7 or int(text[0:1]) == 8 or int(text[0:1]) == 9:
                self.users[user_id].data['des_grade'] = "0" + text[0:1]
                self.users[user_id].data['des_class'] = text[2]
            else:
                self.users[user_id].data['des_grade'] = text[0:2]
                self.users[user_id].data['des_class'] = text[2]
            self.users[user_id].status = "Bs3"
            self.reply_cancel(event, "請輸入廣播文字")
        else:
            reply_message = "請輸入在範圍內的班級!"
            self.reply_cancel(event, reply_message)

    # 群發廣播
    def handle_Bs2_2(self, event, user_id, text):
        canSend = True
        number_groups = re.findall(pattern, text) # 使用正則表達式解析(僅可判斷以空格或逗號隔開)
        if number_groups != []:
            
            number_groups = arrangeGetClass(number_groups)
            print(number_groups)
            for group in number_groups:
                if len(group) == 1:   # 判斷為年級或班級
                    print(group)
                    if group == "0":
                        self.users[user_id].data['classStr'] = "全體廣播"
                        self.users[user_id].data['des_class'] = None
                        self.users[user_id].data['des_grade'] = None
                        self.users[user_id].data['group_send'] = "0"
                        self.users[user_id].data['classLs'] = "0"
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
                                if '4' not in number_groups:
                                    self.users[user_id].data['classLs'].append(group)
                                    self.users[user_id].data['classStr'] += "高" + group + " " 
                            else:
                                if '5' not in number_groups:
                                    self.users[user_id].data['classLs'].append(group)
                                    self.users[user_id].data['classStr'] += group + "年級 "
                        else:
                            reply_message = "請輸入正確數字範圍"
                            self.reply_cancel(event, reply_message)
                            canSend = False
                            break
                elif len(group) == 3:
                    print(group)
                    if group in class_list:
                        if int(group[0:1]) < 4: 
                            if str(int(group[0:2]) - 9) not in number_groups:
                                self.users[user_id].data['classStr'] += group + " "
                                self.users[user_id].data['classLs'].append(group)
                                # print(group)
                        else:
                            if group[0:1] not in number_groups:
                                self.users[user_id].data['classStr'] += group + " "
                                self.users[user_id].data['classLs'].append(group)
                                # print(group)

                    else:
                        reply_message = "請輸入正確班級"
                        self.reply_cancel(event, reply_message)
                        canSend = False
                        break
            if canSend:
                self.users[user_id].status = "Bs3"
                reply_message = "請輸入廣播訊息"
                self.reply_cancel(event, reply_message)
        else:
            reply_message = "請輸入有效代碼"
            self.reply_cancel(event, reply_message)

    # 廣播訊息3
    def handle_Bs3(self, event, user_id, text):

        if len(text) > 200:
            reply_message = f"輸入字數請勿超過200字, 目前字數{len(text)}"
            self.reply_cancel(event, reply_message)
        elif text.count('\n') > 10:
            reply_message = "訊息請勿超過10行，目前行數" + text.count('\n')
            self.reply_cancel(event, reply_message)
        else:
            self.users[user_id].data['content'] = text
            self.users[user_id].status = "Cs"
            self.sendConfirm(event, user_id)


    # 設置教師個人資訊
    def postback_Ss(self, event, user_id):
        isRegis = self.db.findTeacher(user_id)
        self.users[user_id].status = "Ss1"
        if isRegis != "Error" and isRegis != False:
            reply_message = "重新設定教師個人資訊\n請輸入您的姓名"
            self.reply_cancel(event, reply_message)

        else:
            reply_message = "設定教師個人資訊\n請輸入您的姓名"
            self.reply_cancel(event, reply_message, False)



    # 設置個人資訊一
    def handle_Ss1(self, event, user_id, text, status):
        self.users[user_id].name = text
        reply = f"您好 {text} \n請輸入您所在的處室"

        if status == "Ss1":
            self.users[user_id].status = "Ss2"
            self.reply_cancel(event, reply)

        else:
            self.users[user_id].status = "FSs2"
            self.reply_cancel(event, reply, False)

    # 設置個人資訊二
    def handle_Ss2(self, event, user_id, text, status):
        self.users[user_id].office = text
        reply = f"您的名字為: {self.users[user_id].name}\n所在處室: {self.users[user_id].office}"
        if status == "FSs2":
            self.sendSettingConfirm(event,user_id, reply, True)
        else:
            self.sendSettingConfirm(event, user_id, reply, False)

    # 個人資訊確認按鈕
    def sendSettingConfirm(self, event,user_id, text, isFisrt):
        #try:
            if isFisrt:
                message = TemplateSendMessage(
                    alt_text='Button template',
                    template=ButtonsTemplate(
                        # 把廣播訊息重複在此
                        text=f"請問確認是否輸入錯誤\n{text}",
                        actions=[
                            PostbackTemplateAction(
                                label='YES 我已確認',
                                data='action=@CofS_Y'
                            ),
                            PostbackTemplateAction(
                                label='NO 訊息有誤',
                                data='action=@CofS_N'
                            ),
                        ]
                    )
                )
                self.api.reply_message(event.reply_token, message)

            else:
                message = TemplateSendMessage(
                    alt_text='Button template',
                    template=ButtonsTemplate(
                        # 把廣播訊息重複在此
                        text=f"請問確認是否輸入錯誤\n{text}",
                        actions=[
                            PostbackTemplateAction(
                                label='YES 我已確認',
                                data='action=@CofS_Y'
                            ),
                            PostbackTemplateAction(
                                label='NO 訊息有誤',
                                data='action=@CofS_N'
                            ),
                            PostbackTemplateAction(
                                label="取消",
                                data="action=@cancel"
                            )
                        ]
                    )
                )
                self.api.reply_message(event.reply_token, message)

        # except Exception as e:
        #     print(e)
        #     self.api.push_message(user_id, TextSendMessage(text="確認按鈕傳送錯誤，請再試一次或聯絡管理員 錯誤代碼: E0004")) # 按鈕發生錯誤
    
    
    # 個人資訊確認按鈕處理 User Setting
    def postback_US(self, event, user_id, t):
        if t == "CofS_Y":
            if self.users[user_id].status == "FSs2" or self.users[user_id].status == "Ss2":
                self.db.insertTeaInfor(user_id, {'name': self.users[user_id].name, 'office': self.users[user_id].office, "verifyStat": 0})
                # print(self.users[user_id].name)
                if user_id not in self.Confirm_List:    
                    self.Confirm_List.append(user_id)
                    reply_message = f"🔴有新教師加入‼\n以下為尚未驗證之列表，請透過數字鍵來表示要許可之用戶，其他將會被拒絕 ex 1~4 7 表示1到4號和7號都會許可\n代認證列表:"
                    for i in range(len(self.Confirm_List)):
                        print(self.Confirm_List)
                        temp = self.db.getTeacherUnVerify(self.Confirm_List[i])
                        if temp != "Error" and temp != False:
                            reply_message += f"\n▶️{i+1}) 教師: {temp.name} 處室: {temp.office}"
                AdminList = self.db.findAdmin()
                if AdminList != False:
                    for Admin in AdminList:
                        if Admin not in self.users:
                            self.users[Admin] = Teacher(Admin, isAdm=1, status="ACs")
                        else:
                            self.users[Admin].status = "ACs"
                       
                        self.api.push_message(
                            Admin, TextSendMessage(text=reply_message))
                        
                    reply = "已送交，等待管理員確認"
                    self.api.reply_message(event.reply_token, TextSendMessage(text=reply))

            else:
                reply = "伺服器錯誤，請詢問資訊組 錯誤代碼:E0003"
                self.api.reply_message(event.reply_token, TextSendMessage(text=reply))
                print("**Error: There isn't any Admin in the database!!**")
            
            self.users[user_id].status = "Ss3"

        elif t == "CofS_N":
            isRegis = self.db.findTeacher(user_id)
            if self.users[user_id].status == "Ss2":
                self.users[user_id].status = "Ss1" 
                if isRegis != "Error" and isRegis != False:
                    reply_message = "重新設定教師個人資訊\n請輸入您的姓名"
                    self.reply_cancel(event, reply_message)
                else:
                    reply_message = "設定教師個人資訊\n請輸入您的姓名"
                    self.reply_cancel(event, reply_message)

            elif self.users[user_id].status == "FSs2":
                self.users[user_id].status = "FSs1"  
                reply_message = "請輸入您的姓名"
                self.reply_cancel(event, reply_message, False)

    # 管理員許可1
    def handle_Admin1(self, event, user_id,text):
        result = re.findall(AdminConfirmPatter, text)
        note = False
        if result != None:
            for scope in result:
                if "-" in scope:
                    if int(scope[0:1]) >= 1 and int(scope[2:3]) <= len(self.Confirm_List):
                        for i in range(int(scope[0:1]), int(scope[2:3])+1, 1):
                            self.db.modifyVerifyStat(self.Confirm_List[i-1])
                            self.api.push_message(self.Confirm_List[i-1], TextSendMessage(text="管理員已認證，歡迎您加入"))
                            self.users[self.Confirm_List[i-1]].status = "Fs"
                            self.Confirm_List[i-1] = ""
                    else:
                        note = True
                        reply_message = "請輸入在範圍內的數字"
                        self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                else:
                    # print(scope)
                    if int(scope) >= 1 and int(scope) <= len(self.Confirm_List):
                        self.db.modifyVerifyStat(self.Confirm_List[int(scope)-1])
                        self.api.push_message(self.Confirm_List[int(scope)-1], TextSendMessage(text="管理員已認證，歡迎您加入"))
                        
                        self.users[self.Confirm_List[int(scope)-1]].status = "Fs"
                        self.Confirm_List[int(scope)-1] = ""
                    else:
                        note = True
                        reply_message = "請輸入在範圍內的數字"
                        self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                        
            if not note:
                for user in self.Confirm_List:
                    if user != "":
                        self.api.push_message(user, TextSendMessage(text="很抱歉，管理員已否決您的申請。"))
                        self.db.DelTeacherData(user)
                self.Confirm_List = []

                reply_message = "更新成功"
                self.api.reply_message(
                event.reply_token, TextSendMessage(text=reply_message))
                self.users[user_id].status = "Fs"
        else:
            reply_message = "輸入錯誤, 請使用 "-" 來指定範圍，或是輸入特定數字"
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

                self.reply_cancel(event, reply_message)
        elif text == "2":
            if self.db.findTeacher(user_id):
                if self.db.verified(user_id):
                    self.users[user_id].status = "Bs1"
                    self.select_target(event)
                else:
                    reply_message = "管理員尚未驗證，請耐心等候"
                    self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
            else:
                reply_message = "您尚未註冊，請輸入您的姓名"
                self.users[user_id].status = "Ss1"
                self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))
        else:
            if self.users[user_id].status != "Ss3":
                self.SendButton(event)

    # 歷史訊息按鈕
    def History_Data_Button(self,user_id):
        message = TemplateSendMessage(
            alt_text='Button template',
            template=ButtonsTemplate(
                # 把廣播訊息重複在此
                text=f"請選擇要修改的地方",
                actions=[
                    PostbackTemplateAction(
                        label='廣播對象',
                        data='action=@CST' # Change Send To
                    ),
                    PostbackTemplateAction(
                        label='廣播內容',
                        data='action=@CC' # Change Content
                    ),
                    PostbackTemplateAction(
                        label="全部修改",
                        data='action=@CA' # Change All
                    ),
                    PostbackTemplateAction(
                        label="取消",
                        data="action=@cancel"
                    )
                ]
            )
        )
        self.api.push_message(user_id, message)

    # 歷史訊息按紐處理
    def postback_Hs(self, event, user_id):
        if self.users[user_id].status != "Hs":
            history_data = []
            history_data = self.db.getHistoryData(user_id)
            if len(history_data) == 0:
                reply_message = "無歷史訊息"
                self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
            else:
                reply_message = "以下是您最近發送的歷史訊息\n"
                self.users[user_id].status = "Hs"
                history_data = self.sort_history_message(history_data)
                for i in range(1,len(history_data)+1, 1):
                    if history_data[i-1].group_send != None:
                        reply_message += f"▶️{i})  {history_data[i-1].time} To: {history_data[i-1].group_send} \n\t {history_data[i-1].content} \n"
                    else:
                        reply_message += f"▶️{i})  {history_data[i-1].time} To: {history_data[i-1].des_grade} \n\t {history_data[i-1].content} \n"
                self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                self.History_Data_Button(user_id)

    # 歷史訊息排序
    def sort_history_message(self, history_data):
        length = len(history_data)
        i = 0
        for m in range(length):
            cList = []
            if i >= len(history_data):
                break
            if history_data[i].group_send != None:
                if history_data[i].group_send == '0':
                    history_data[i].group_send = "全體廣播"
                    i = i+1
                    continue
                elif history_data[i].group_send == '4':
                    history_data[i].group_send = "高中部"
                    i = i+1
                    continue
                elif history_data[i].group_send == '5':
                    history_data[i].group_send = "國中部"
                    i = i+1
                    continue

                else:
                    cList.append(history_data[i].group_send)
                    history_data[i].group_send = f"高{history_data[i].group_send}"
                    print(cList)

            elif int(history_data[i].des_grade[1:]) == 7 or int(history_data[i].des_grade[1:]) == 8 or int(history_data[i].des_grade[1:]) == 9:
                cList.append(history_data[i].des_grade + history_data[i].des_class)
                history_data[i].des_grade = f" {swapClassFromat(history_data[i].des_grade, history_data[i].des_class)}"
                

            else:
                history_data[i].des_grade += f"{history_data[i].des_class}"
                cList.append(history_data[i].des_grade)

            j = i+1
            print(history_data[i].group_send)
            for k in range(i+1,length, 1):
                if j >= len(history_data):
                    break
                if history_data[i].content == history_data[j].content:
                    if history_data[j].group_send != None:
                        history_data[i].group_send += f"高{history_data[j].group_send}"
                        if history_data[j].group_send not in cList:
                            cList.append(history_data[j].group_send)
                       
                    elif int(history_data[j].des_grade[1:]) == 7 or int(history_data[j].des_grade[1:]) == 8 or int(history_data[j].des_grade[1:]) == 9: 
                        if history_data[j].des_grade + history_data[j].des_class not in cList:
                            cList.append(history_data[j].des_grade + history_data[j].des_class)
                            history_data[i].des_grade += f" {swapClassFromat(history_data[j].des_grade, history_data[j].des_class)}"

                    else:
                        if history_data[j].des_grade + history_data[j].des_class not in cList:
                            cList.append(history_data[j].des_grade + history_data[j].des_class)
                            history_data[i].des_grade += f" {history_data[j].des_grade + history_data[j].des_class}"
                    del history_data[j]
                else:
                    j += 1
            i += 1
        return history_data

# 交換班級格式
def swapClassFromat(des_grade, des_class):
    result = des_grade[1:] + des_grade[0:1] + des_class
    return result 


# 將讀到的傳送班級列表中，重複的刪除
def arrangeGetClass(list):
    list.sort()
    j = 0
    for i in range(len(list)):
        if j >= len(list)-1:
            return list
        if list[j] == list[j+1]:
            del list[j+1]
            print(list)
        else:
            j+=1
