import re
from linebot.models import  TextSendMessage, PostbackTemplateAction, TemplateSendMessage, ButtonsTemplate, PostbackAction, DatetimePickerTemplateAction,MessageAction
from datetime import date, timedelta
import imple_toolV2_8 as t

pattern = r'(\d+)[, ]*'
AdminConfirmPatter = r'(\d+-\d+|\d+)'
class_list = ['701', '702', '703', '704', '705', '801', '802', '803', '804', '805', '901', '902', '903', '904', '905','101', '102', '103', '104', '105', '106', '111', '112', '113', '114', '115', '116', '121', '122', '123', '124', '125', '126']
group_index = [-1, 4, 9, 14, 20, 26, 32]
grade_list = ['1', '2', '3', '4', '5','7', '8', '9']
dataTemplate = {'content':"", 'classLs': [], 'classStr': "", 'des_class': "", 'des_grade': "", 'finish_date':"", 'sound':''}
BreakList = {}


t.make_break(BreakList)

class Teacher():
    
    def __init__(self, id, name = None, office = None, status = None, isAdm = None, data = None, preStatus = None):
        self.id = id
        self.name = name
        self.office = office
        self.isAdm = isAdm
        self.data = data if data is not None else dataTemplate.copy()  # 使用copy()创建新的字典
        self.status = status
        self.preStatus = preStatus

class Bot():

    def __init__(self, api, database, users, Confirm_List = []):
        self.api = api
        self.db = database
        self.users = users 
        self.Confirm_List = Confirm_List

    # 傳送功能選單
    def SendButton(self, event, user_id):
        try:
            message = TemplateSendMessage(
                alt_text='按鈕樣板',
                template=ButtonsTemplate(
                    title='請選擇服務：',
                    thumbnail_image_url = "https://raw.githubusercontent.com/jason355/SWBS/main/img1.png",
                    text='請務必先點選"教師個人資訊"按鈕以設定身分',
                    actions=[
                        PostbackTemplateAction(
                            label='發送廣播',
                            data='action=@文字廣播'
                        ),
                        PostbackTemplateAction(
                            label='更改教師個人資訊',
                            data='action=@教師個人資訊'
                        ),
                        PostbackTemplateAction(
                            label='歷史訊息',
                            data='action=@歷史訊息'
                        ),
                        PostbackTemplateAction(
                            label='幫助',
                            data = 'action=@幫助'
                        )
                    ]
                )
            )
            self.api.reply_message(event.reply_token, message)
        except Exception as e:
            print(e)
            self.api.push_message(user_id, TextSendMessage(text="選擇傳送按鈕傳送錯誤，若樣板有傳出請忽略此訊息，若無請再試一次或是聯絡資訊組"))

    # 管理員樣板
    def SendButton_Adm(self, event):
        try:
            message = TemplateSendMessage(
                alt_text='按鈕樣板',
                template=ButtonsTemplate(
                    title='請選擇服務：',
                    thumbnail_image_url = "https://raw.githubusercontent.com/jason355/SWBS/main/img1.png",
                    text='請務必先點選"教師個人資訊"按鈕以設定身分',
                    actions=[
                        PostbackTemplateAction(
                            label='發送廣播',
                            data='action=@文字廣播'
                        ),
                        PostbackTemplateAction(
                            label='更改教師個人資訊',
                            data='action=@教師個人資訊'
                        ),
                        PostbackTemplateAction(
                            label='歷史訊息',
                            data='action=@歷史訊息'
                        ),
                        PostbackTemplateAction(
                            label='管理員功能',
                            data = 'action=@Adm_func'
                        )
                    ]
                )
            )
            self.api.reply_message(event.reply_token, message)
        except Exception as e:
            print(e)
            self.api.reply_message(
                event.reply_token, TextSendMessage(text='⚠️發生錯誤！請在試一次或是使用@resetBot來重啟'))

    #管理員樣板
    def cmd_button(self, event):
        try:
            message = TemplateSendMessage(
                alt_text='按鈕樣板',
                template=ButtonsTemplate(
                    title='請選擇服務：',
                    thumbnail_image_url = "https://raw.githubusercontent.com/jason355/SWBS/main/img1.png",
                    text='請務必先點選"教師個人資訊"按鈕以設定身分',
                    actions=[
                        MessageAction(
                            label='重啟linebot',
                            text="@resetBot"
                        ),
                        MessageAction(
                            label='教師列表',
                            text='@userList'
                        ),
                        MessageAction(
                            label='刪除資料庫資料',
                            text='@delData'
                        ),
                    ]
                )
            )
            self.api.reply_message(event.reply_token, message)
        except Exception as e:
            print(e)
            self.api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤!請再試一次或是使用@resetBot來重啟'))


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


    # 幫助
    def postback_Help(self, event):
        reply_message = t.help_text
        self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))


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
                self.select_target(event, user_id)
            else:
                reply_message = "管理員尚未驗證，請耐心等候🙏"
                self.api.reply_message(event.reply_token,TextSendMessage(text=reply_message))




    # 單獨或群發按鈕
    def select_target(self, event, user_id):
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
            self.api.push_message(user_id, TextSendMessage(text="選擇傳送按鈕傳送錯誤，若樣板有傳出請忽略此訊息，若無請再試一次或是聯絡資訊組"))

    # 特定班級樣板
    def select_single(self, event,user_id):
        try:
            message = TemplateSendMessage(
                alt_text='Button Template',
                template=ButtonsTemplate(
                    text="您選擇個別發送，請輸入要發送的班級 ex: 703",
                    actions=[
                        PostbackTemplateAction(
                            label='更改成 群發年級',
                            data='action=@Cselect_group' # Change select group
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
            self.api.push_message(user_id, TextSendMessage(text="選擇傳送按鈕傳送錯誤，若樣板有傳出請忽略此訊息，若無請再試一次或是聯絡資訊組"))


    # 選擇特定班級按鈕 Select Class
    def postback_Sc(self, event, user_id, Edit=False):
        if self.users[user_id].status == "Bs1":
            if not Edit:
                self.users[user_id].status = "Bs2.1"
                self.select_single(event, user_id)

            else:
                self.users[user_id].status = "Bs2.1c"
                self.select_single(event, user_id)
    # 選擇群發按鈕 Select group
    def postback_Sg(self, event, user_id, Edit = False):
        if self.users[user_id].status == "Bs1":
            if not Edit:
                self.users[user_id].status = "Bs2.2"
                self.select_group_list(event, user_id) # 傳送群發按鈕列表
            else:
                self.users[user_id].status = "Bs2.2c"
                self.select_group_list(event, user_id)    
    
    # 群發文字
    def select_group_list(self, event, user_id):
        try:
            message = TemplateSendMessage(
                alt_text='Button Template',
                template=ButtonsTemplate(
                    # 
                    text=f"選擇群發年級!\n請輸入傳送班級(請輸入中文字後的代號)\n 全校 0 \n 高一 1 \n 高二 2 \n 高三 3 \n 高中 4 \n 國中 5 \n 七年級 7 \n 八年級 8 \n 九年級 9\n 特定跳班級 班級三位數並用逗號或空格隔開",
                    actions=[
                        PostbackTemplateAction(
                            label='更改成 個別發送',
                            data='action=@Cselect_class' # Change select class
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
            self.api.push_message(user_id, TextSendMessage(text="選擇傳送按鈕傳送錯誤，若樣板有傳出請忽略此訊息，若無請再試一次或是聯絡資訊組"))






    def confirm_yes(self, event, user_id):
        if self.users[user_id].status == "Cs":
                data = {}
                user = self.db.getTeacher(user_id)
                if user != False and user != "Error":
                    data["name"] = user.name
                    data["office"] = user.office
                    data["des_class"] = None
                    data["des_grade"] = None
                    data['content'] = self.users[user_id].data['content']
                    data['finish_date'] = self.users[user_id].data['finish_date']
                    data['sound'] = self.users[user_id].data['sound']

                    if len(self.users[user_id].data['classLs']) == 0:
                        data['des_class'] = self.users[user_id].data['des_class']
                        data['des_grade'] = self.users[user_id].data['des_grade'] 
                        ack = self.db.insertData(data)

                        if not ack:
                            self.api.push_message(user_id, TextSendMessage(text="🙇‍♂️插入資料時發生錯誤，請重新傳送，或是聯絡資訊組"))
                    else:                            
                        for C in self.users[user_id].data["classLs"]:
                            data["des_class"] = None
                            data["des_grade"] = None
                            if len(C) == 1:
                                match (C):
                                    case "0":
                                        for i in range(7, 10, 1):
                                            for j in range(1,6, 1):
                                                data['des_class'] = j
                                                data['des_grade'] = "0" + str(i)
                                                ack = self.db.insertData(data)
                                                if not ack:
                                                    self.api.push_message(user_id, TextSendMessage(text="🙇‍♂️插入資料時發生錯誤，請重新傳送，或是聯絡資訊組"))
                                                    break
                                        for i in range(0, 3):
                                            for j in range(1, 7, 1):
                                                data['des_class'] = j 
                                                data['des_grade'] = "1"+ str(i)
                                                ack = self.db.insertData(data)
                                                if not ack:
                                                    self.api.push_message(user_id, TextSendMessage(text="🙇‍♂️插入資料時發生錯誤，請重新傳送，或是聯絡資訊組"))
                                                    break                                               
                                    case "1" | "2" | "3":
                                        for i in range(1, 7, 1):
                                            data['des_class'] = i
                                            data['des_grade'] = "1" + str(int(C) - 1)
                                            ack = self.db.insertData(data)
                                            if not ack:
                                                self.api.push_message(user_id, TextSendMessage(text="🙇‍♂️插入資料時發生錯誤，請重新傳送，或是聯絡資訊組"))
                                                break     
                                        
                                    case "4":
                                        for i in range(0, 3):
                                            for j in range(1, 7, 1):
                                                data['des_class'] = j 
                                                data['des_grade'] = "1"+ str(i)
                                                ack = self.db.insertData(data)
                                                if not ack:
                                                    self.api.push_message(user_id, TextSendMessage(text="🙇‍♂️插入資料時發生錯誤，請重新傳送，或是聯絡資訊組"))
                                                    break     
                                    case "5":
                                        for i in range(7, 10, 1):
                                            for j in range(1,6, 1):
                                                data['des_class'] = j
                                                data['des_grade'] = "0" + str(i)
                                                ack = self.db.insertData(data)
                                                if not ack:
                                                    self.api.push_message(user_id, TextSendMessage(text="🙇‍♂️插入資料時發生錯誤，請重新傳送，或是聯絡資訊組"))
                                                    break     
                                    
                                    case "7" | "8" | "9":
                                        for i in range(1, 6, 1):
                                            data['des_class'] = i
                                            data['des_grade'] = "0" + C
                                            ack = self.db.insertData(data)
                                            if not ack:
                                                self.api.push_message(user_id, TextSendMessage(text="🙇‍♂️插入資料時發生錯誤，請重新傳送，或是聯絡資訊組"))
                                                break     
                            else:       
                                if int(C[0:1]) == 7 or int(C[0:1]) == 8 or int(C[0:1]) == 9:                    
                                        data['des_grade'] = "0" + C[0:1]
                                        data['des_class'] = C[2]
                                        ack = self.db.insertData(data)
                                        if not ack:
                                            self.api.push_message(user_id, TextSendMessage(text="🙇‍♂️插入資料時發生錯誤，請重新傳送，或是聯絡資訊組"))
                                            break     
                                else:
                                        data['des_grade'] = C[0:2]
                                        data['des_class'] = C[2]
                                        ack = self.db.insertData(data)
                                        if not ack:
                                            self.api.push_message(user_id, TextSendMessage(text="🙇‍♂️插入資料時發生錯誤，請重新傳送，或是聯絡資訊組"))
                                            break     
                    if ack == True:
                        T = t.isBreak(BreakList)
                        if T == 1:
                            reply_message = "✅已更新置資料庫，將在現在廣播"
                            self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                        elif T == 2:
                            reply_message = "✅已更新置資料庫，將在明天廣播"
                            self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                        elif T == 3:
                            reply_message = "✅已更新置資料庫，將在下一節下課廣播"
                            self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                elif user == "Error":
                    print(f"E0002: The user {user_id} has more than one data in the database")
                    reply_message = "您有大於一筆個人資料在伺服器中，請洽管理員協助"
                    self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                    # Send message to Admin
                else:
                    reply_message = "插入失敗，請設置教師個人資訊或洽資訊組"
                    self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        
        self.users[user_id].status = "Fs"
        self.users[user_id].data['content'] = ""
        self.users[user_id].data['finish_date'] = ""
        self.users[user_id].data['classLs'] = []
        self.users[user_id].data['classStr'] = " "
        self.users[user_id].data['des_class'] = ""
        self.users[user_id].data['des_grade'] = ""
        self.users[user_id].data['sound'] = ""

        # self.users[user_id] = ""
            


        
    # 修改訊息樣板
    def confirm_no(self, event, user_id):
        if self.users[user_id].status == "Cs":
            message = TemplateSendMessage(
                alt_text='Button Template',
                template=ButtonsTemplate(
                    # 
                    text="請選擇要修改的內容",
                    actions=[
                        PostbackTemplateAction(
                            label='修改發送班級',
                            data='action=@EC' # Edit Class
                        ),
                        PostbackTemplateAction(
                            label='修改廣播內容',
                            data='action=@ET' # Edit Text
                        ),
                        PostbackTemplateAction(
                            label='音效修改',
                            data='action=@ES' # Edit Sound
                        ),
                        PostbackTemplateAction(
                            label='全部修改',
                            data='action=@EA' # Edit All
                        )
                    ]
                )
            )
            self.api.reply_message(event.reply_token, message)

    # 修改班級
    def edit_class(self, event, user_id):
        try:
            self.users[user_id].status = "Bs1" # Edit Class stat
            self.users[user_id].data['classLs'] = []
            self.users[user_id].data['classStr'] = " "
            self.users[user_id].data['des_class'] = ""
            self.users[user_id].data['des_grade'] = ""            
            message = TemplateSendMessage(
                alt_text='Button Template',
                template=ButtonsTemplate(
                    # 把廣播訊息重複在此
                    text=f"請問發送對象為......",
                    actions=[
                        PostbackTemplateAction(
                            label='個別發送',
                            data='action=@Eselect_class'
                        ),
                        PostbackTemplateAction(
                            label='群發年級',
                            data='action=@Eselect_group'
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
            self.api.push_message(user_id, TextSendMessage(text="選擇傳送按鈕傳送錯誤，若樣板有傳出請忽略此訊息，若無請再試一次或是聯絡資訊組"))


    # 全部修改
    def edit_all(self, event, user_id):
        self.users[user_id].data['classLs'] = []
        self.users[user_id].data['classStr'] = " "
        self.users[user_id].data['des_class'] = ""
        self.users[user_id].data['des_grade'] = "" 
        self.users[user_id].status = "Bs1"
        self.select_target(event, user_id)



    # 傳送確認樣板
    def sendConfirm(self,event, user_id):
        try:
            if self.users[user_id].data['sound'] == "1":
                sound = "有"
            elif self.users[user_id].data['sound'] == "0":
                sound = "無"
            reply_message = f"你確定要發送此則訊息嗎？\n教師名稱: {self.users[user_id].name}\n處室: {self.users[user_id].office}\n傳送班級: \n廣播內容:\n \n結束廣播時間: {self.users[user_id].data['finish_date']}\n廣播音效: {sound}"
            reply_len = t.calc_unicode_seg(reply_message)
            class_len = t.calc_unicode_seg(self.users[user_id].data['classStr'])
            content_Max = 160 - reply_len - class_len
            print(f"reply_len:{reply_len} class_len:{class_len} content_Max:{content_Max}")
            content_len = t.calc_unicode_seg(self.users[user_id].data['content'])
            print(f"content_len :{content_len}")
            if content_len > content_Max:
                content = self.users[user_id].data['content'][0:content_Max-4] + "...略"
            else:
                content = self.users[user_id].data['content']
            print(f"content:{content} len:{t.calc_unicode_seg(content)}")

            reply_message = f"你確定要發送此則訊息嗎？\n教師名稱: {self.users[user_id].name}\n處室: {self.users[user_id].office}\n傳送班級: {self.users[user_id].data['classStr']}\n廣播內容:\n {content}\n結束廣播時間: {self.users[user_id].data['finish_date']}\n廣播音效: {sound}"
            print(t.calc_unicode_seg(reply_message), t.calc_unicode_seg(self.users[user_id].data['classStr']))
            message = TemplateSendMessage(
                alt_text='Button template',
                template=ButtonsTemplate(
                    # 把廣播訊息重複在此
                    text=reply_message,
                    actions=[
                        PostbackTemplateAction(
                            label='YES 我已確認',
                            data='action=@confirm_yes'
                        ),
                        PostbackTemplateAction(
                            label='NO 訊息有誤',
                            data='action=@confirm_no'
                        ),
                        DatetimePickerTemplateAction(
                        label='調整廣播結束日期',
                        data='action=@FD',  
                        mode='date'
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
            # self.api.push_message(user_id, TextSendMessage(text="確認按鈕傳送錯誤，請再試一次或聯絡管理員 錯誤代碼: E0001")) # 按鈕發生錯誤
            self.users[user_id].status = "Fs"
            self.users[user_id].data['classLs'] = []
            self.users[user_id].data['classStr'] = " "
            self.users[user_id].data['des_class'] = ""
            self.users[user_id].data['des_grade'] = ""     
    # 單獨班級廣播
    def handle_Bs2_1(self, event, user_id, text):
        if text in class_list:
            self.users[user_id].data['classLs'] = []
            self.users[user_id].data['classStr'] = text
            if int(text[0:1]) == 7 or int(text[0:1]) == 8 or int(text[0:1]) == 9:
                self.users[user_id].data['des_grade'] = "0" + text[0:1]
                self.users[user_id].data['des_class'] = text[2]
            else:
                self.users[user_id].data['des_grade'] = text[0:2]
                self.users[user_id].data['des_class'] = text[2]
            if self.users[user_id].status == "Bs2.1":
                self.users[user_id].status = "Bs3"
                self.reply_cancel(event, "請輸入廣播文字")
            else:
                self.users[user_id].status = "Cs"
                self.sendConfirm(event, user_id)
        else:
            reply_message = "請輸入在範圍內的班級!"
            self.reply_cancel(event, reply_message)

    # 群發廣播
    def handle_Bs2_2(self, event, user_id, text):
        canSend = True
        number_groups = re.findall(pattern, text) # 使用正則表達式解析(僅可判斷以空格或逗號隔開)
        if number_groups != []:
            number_groups = t.arrangeGetClass(number_groups)
            print(number_groups)
            for group in number_groups:
                if len(group) == 1:   # 判斷為年級或班級
                    print(group)
                    if group == "0":
                        self.users[user_id].data['classStr'] = "全體廣播"
                        self.users[user_id].data['des_class'] = None
                        self.users[user_id].data['des_grade'] = None
                        self.users[user_id].data['classLs'] = ["0"]
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
                self.users[user_id].data['classStr'] = t.format_class(self.users[user_id].data['classStr'])

                if self.users[user_id].status == "Bs2.2":
                    self.users[user_id].status = "Bs3"
                    self.reply_cancel(event, "請輸入廣播文字")
                else:
                    self.users[user_id].status = "Cs"
                    self.sendConfirm(event, user_id)
        else:
            reply_message = "請輸入有效代碼"
            self.reply_cancel(event, reply_message)


    def date_picker_template(self, event):
        date_picker = TemplateSendMessage(
            alt_text='日期選擇',
            template=ButtonsTemplate(
                title='日期選擇',
                text="請選擇結束廣播日期",
                actions=[
                    DatetimePickerTemplateAction(
                        label='選擇日期',
                        data='action=@FD',  
                        mode='date'
                    )
                ]    
            )   
        )
        self.api.reply_message(event.reply_token, date_picker)
    
    
    # 廣播訊息3
    def handle_Bs3(self, event, user_id, text):
        textLen = len(text)
        if textLen > 90:
            reply_message = f"輸入字數請勿超過90字, 目前字數{len(text)}"
            self.reply_cancel(event, reply_message)
        elif text.count('\n') > 4:
            reply_message = "訊息請勿超過5行，目前行數" + str(text.count('\n')+1)
            self.reply_cancel(event, reply_message)
        else:

            self.users[user_id].data['content'] = text

            self.users[user_id].data['finish_date'] = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            if self.users[user_id].status == "Bs3":
                self.users[user_id].status = "Bs4"
                self.sound_select(event, user_id)
            else:
                self.users[user_id].status = "Cs"
                self.sendConfirm(event, user_id)

    # 聲音選擇樣板
    def sound_select(self, event, user_id):
        try:
            message = TemplateSendMessage(
                alt_text='Button template',
                template=ButtonsTemplate(
                    text=f"是否需要廣播提醒音效?",
                    actions=[
                        PostbackTemplateAction(
                            label='是',
                            data='action=@sound_yes'
                        ),
                        PostbackTemplateAction(
                            label='否',
                            data='action=@sound_no'
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


  

    # 廣播訊息5 接收結束廣播時間
    def postback_Bs5(self, event, user_id):
        selected_date = event.postback.params['date']
        selected_date = date(int(selected_date[0:4]), int(selected_date[5:7]), int(selected_date[8:]))
        todayDate = date.today()
        # print((nowTime > com), (selected_date - todayDate))
        if (selected_date - todayDate).days == 0:
            selected_date = selected_date + timedelta(days=1)
            self.users[user_id].data['finish_date'] = selected_date.strftime("%Y-%m-%d")
            self.users[user_id].status = "Cs"
            self.sendConfirm(event, user_id)
        elif (selected_date - todayDate).days >= 0:
            self.users[user_id].data['finish_date'] = selected_date.strftime("%Y-%m-%d")
            self.users[user_id].status = "Cs"
            self.sendConfirm(event, user_id)
        else:
            todayDate = todayDate.strftime("%Y/%m/%d")
            self.api.reply_message(event.reply_token, TextSendMessage(text=f"⚠️請輸入{todayDate}以後的日期"))

    # 設置教師個人資訊
    def postback_Ss(self, event, user_id):
        teacher = self.db.getTeacher(user_id)
        self.users[user_id].status = "Ss1"
        if teacher != "Error" and teacher != False:
            reply_message = f"您好 {teacher.name}\n您所在的處室:{teacher.office}\n重新設定教師個人資訊\n請輸入您的姓名"
            self.reply_cancel(event, reply_message)
        else:
            reply_message = "設定教師個人資訊\n請輸入您的姓名"
            self.reply_cancel(event, reply_message, False)



    # 設置個人資訊一
    def handle_Ss1(self, event, user_id, text, status):
        if len(text) < 10:
            self.users[user_id].name = text
            reply = f"您好 {text} \n請輸入您所在的處室"
            if status == "Ss1":
                self.users[user_id].status = "Ss2"
                self.reply_cancel(event, reply)
            else:
                self.users[user_id].status = "FSs2"
                self.reply_cancel(event, reply, False)
        else:
            reply = f"名稱請勿超過20字，目前字數 {len(text)}"
            self.api.reply_message(event.reply_token, TextSendMessage(text=reply))

        

    # 設置個人資訊二
    def handle_Ss2(self, event, user_id, text, status):
        self.users[user_id].office = text
        if len(text) <= 5:
            reply = f"您的名字為: {self.users[user_id].name}\n所在處室: {self.users[user_id].office}"
            if status == "FSs2":
                self.sendSettingConfirm(event, reply, True)
            else:
                self.sendSettingConfirm(event, reply, False)
        else:
            reply = f"處室請勿超過5字，目前字數{len(text)}"
            self.api.reply_message(event.reply_token, TextSendMessage(text=reply))

    # 個人資訊確認按鈕
    def sendSettingConfirm(self, event, text, isFisrt):
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
            if self.db.isAdmin(user_id):
                reply_message = "已更新"
                self.users[user_id].status = "Fs"
                self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
            elif self.users[user_id].status == "FSs2" or self.users[user_id].status == "Ss2":
                self.db.insertTeaInfor(user_id, {'name': self.users[user_id].name, 'office': self.users[user_id].office, "verifyStat": 0})
                # print(self.users[user_id].name)
                if user_id not in self.Confirm_List:    
                    self.Confirm_List.append(user_id)
                    reply_message = f"🔴有新教師加入‼\n以下為尚未驗證之列表，請透過數字鍵來表示要許可之用戶，其他將會被拒絕 ex 1~4 7 表示1到4號和7號都會許可\n代認證列表:"
                    for i in range(len(self.Confirm_List)):
                        print(self.Confirm_List)
                        temp = self.db.getTeacher(self.Confirm_List[i])
                        if temp != "Error" and temp != False:
                            reply_message += f"\n▶️{i+1}) 教師: {temp.name} 處室: {temp.office}"
                AdminList = self.db.findAdmin()
                if AdminList != False:
                    for Admin in AdminList:
                        if Admin not in self.users:
                            self.users[Admin] = Teacher(Admin, isAdm=1, status="ACs")
                        else:
                            self.users[Admin].preStatus = self.users[Admin].status
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
                AdminList = self.db.findAdmin()
                self.users[user_id].name =  self.db.getTeacher(user_id).name
                reply_message = f"{self.users[user_id].name} 已認證，您可繼續使用廣播功能"
                for Admin in AdminList:
                    if Admin not in self.users:
                        self.users[Admin] = Teacher(Admin, isAdm=1, status="Fs")
                        self.api.push_message(
                        Admin, TextSendMessage(text=reply_message))
                
                    
                    else:
                        self.users[Admin].status = self.users[Admin].preStatus
                        print(f"Admin:{Admin} status:{self.users[Admin].status}")
                        if Admin != user_id:
                            self.api.push_message(
                            Admin, TextSendMessage(text=reply_message))

                        if self.users[Admin].status == "Bs1":
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
                            self.api.push_message(Admin, message)
                        elif self.users[Admin].status == "Ss1":
                            reply_message = "重新設定教師個人資訊\n請輸入您的姓名"
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
                            self.api.push_message(Admin, message)
                            
                        # 個人資訊設定2
                        elif self.users[Admin].status == "Ss2":
                            reply = f"您好 {self.users[Admin].name} \n請輸入您所在的處室"
                            message = TemplateSendMessage(
                                alt_text='Text-Cancel template',
                                template=ButtonsTemplate(
                                    title=None,
                                    text= reply,
                                    actions=[
                                        PostbackAction(
                                            label='取消',
                                            data='action=@cancel'
                                        )
                                    ]
                                )
                            )
                            self.api.push_message(Admin, message)
                        elif self.users[Admin].status == "Ss3":
                            message = TemplateSendMessage(
                                alt_text='Button template',
                                template=ButtonsTemplate(
                                    # 把廣播訊息重複在此
                                    text=f"請問確認是否輸入錯誤\n名稱: {self.users[Admin].name}\n處室:{self.users[Admin].office}",
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
                        # 廣播訊息 2.1
                        elif self.users[Admin].status == "Bs2.1":
                            reply_message = "您選擇個別發送，請輸入要發送的班級 ex: 703"
                            message = TemplateSendMessage(
                                alt_text='Text-Cancel template',
                                template=ButtonsTemplate(
                                    title=None,
                                    text= reply_message,
                                    actions=[
                                        PostbackAction(
                                            label='取消',
                                            data='action=@cancel'
                                        )
                                    ]
                                )
                            )
                            self.api.push_message(Admin, message)
                        
                        # 廣播訊息 2.2
                        elif self.users[Admin].status == "Bs2.2":
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
                            self.api.push_message(Admin, message)
                            
                        # 廣播訊息 3
                        elif self.users[Admin].status == "Bs3":
                            reply_message = "請輸入廣播訊息"
                            message = TemplateSendMessage(
                                alt_text='Text-Cancel template',
                                template=ButtonsTemplate(
                                    title=None,
                                    text= reply_message,
                                    actions=[
                                        PostbackAction(
                                            label='取消',
                                            data='action=@cancel'
                                        )
                                    ]
                                )
                            )
                            self.api.push_message(Admin, message)
                        elif self.users[Admin].status == "Cs":
                            Textlen = self.count_chinese_characters(self.users[Admin].data['content']) * 3
                            Textlen += (len(self.users[Admin].data['content']) - self.count_chinese_characters(self.users[Admin].data['content']))
                            if  Textlen > 160:
                                content = self.users[Admin].data['content'][0:20] + "\n"+"...以下省略"
                            else:
                                content = self.users[Admin].data['content']

                            message = TemplateSendMessage(
                                alt_text='Button template',
                                template=ButtonsTemplate(
                                    # 把廣播訊息重複在此
                                    text=f"你確定要發送此則訊息嗎？\n(請檢察將送出的訊息是否正確)\n教師名稱: {self.users[Admin].name}\n處室: {self.users[Admin].office}\n傳送班級: {self.users[Admin].data['classStr']}\n廣播內容:\n  {content}\n結束廣播時間:{self.users[Admin].data['finish_date']}",
                                    actions=[
                                        PostbackTemplateAction(
                                            label='YES 我已確認',
                                            data='action=@confirm_yes'
                                        ),
                                        PostbackTemplateAction(
                                            label='NO 訊息有誤',
                                            data='action=@confirm_no'
                                        ),
                                        DatetimePickerTemplateAction(
                                        label='調整廣播結束日期',
                                        data='action=@FD',  
                                        mode='date'
                                        ),
                                        PostbackTemplateAction(
                                            label='取消',
                                            data='action=@cancel'
                                        )
                                    ]
                                )
                            )
                            self.api.push_message(Admin, message)
        else:
            reply_message = "輸入錯誤, 請使用 "-" 來指定範圍，或是輸入特定數字"
            self.api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message))


    # 空閒
    def handle_Fs(self, event, user_id, text):
            if self.users[user_id].status != "Ss3":
                if text == "發送廣播":
                    self.postback_Bs(event, user_id)
                elif text == "重新設定個人資訊":
                    self.postback_Ss(event, user_id)
                elif text == "歷史訊息":
                    self.postback_Hs(event, user_id)
                elif text == "幫助":
                    self.postback_Help(event)
                elif not self.db.isAdmin(user_id):
                    self.SendButton(event, user_id)
                elif text == "@resetBot":
                    self.users[user_id].status = "Rs" # Reset status
                    message = TemplateSendMessage(
                        alt_text='Button template',
                        template=ButtonsTemplate(
                            # 重啟確認
                            text="⚠️⚠️你確認要重啟程式?正在執行的流程可能會遺失資料?",
                            actions=[
                                PostbackTemplateAction(
                                    label='是',
                                    data='action=@reset_yes'
                                ),
                                PostbackTemplateAction(
                                    label='否',
                                    data='action=@reset_no'
                                ),
                            ]
                        )
                    )
                    self.api.reply_message(event.reply_token, message)

                elif text == "@userList":
                    AllTeacher = self.db.GetAllTeacherID()
                    if AllTeacher:
                        reply_message = f"🔴以下是教師列表 共{len(AllTeacher)}位:"
                        for user in AllTeacher:
                            get = self.db.getTeacher(user)
                            if user != user_id:
                                reply_message += "\n▶️ "+ get.name+" "+get.office
                            else:
                                reply_message += "\n▶️ "+get.name+" (您)"+" "+get.office
                        self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                elif text == "@delData":
                    self.users[user_id].status = "Ds" # Reset status

                    message = TemplateSendMessage(
                        alt_text='Button template',
                        template=ButtonsTemplate(
                            # 重啟確認
                            text="⚠️⚠️你確認要刪除所有資料庫中資料?",
                            actions=[
                                PostbackTemplateAction(
                                    label='是',
                                    data='action=@del_yes'
                                ),
                                PostbackTemplateAction(
                                    label='否',
                                    data='action=@del_no'
                                ),
                            ]
                        )
                    )
                    self.api.reply_message(event.reply_token, message)
                else:
                    self.SendButton_Adm(event)    
    

    
    # 歷史訊息按紐處理
    def postback_Hs(self, event, user_id):
        history_data = []
        history_data = self.db.getHistoryData(user_id)
        if len(history_data) == 0:
            reply_message = "無歷史訊息"
            self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        else:
            reply_message = "以下是您最近發送的歷史訊息\n"
            history_data = t.sort_history_message(history_data)
            for i in range(1,len(history_data)+1, 1):
                reply_message += f"▶️{i})  {history_data[i-1].time} To: {history_data[i-1].des_grade} \n\t {history_data[i-1].content} \n"
            self.api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

