import re
import regex
from datetime import datetime, time

class_list = ['701', '702', '703', '704', '705', '801', '802', '803', '804', '805', '901', '902', '903', '904', '905','101', '102', '103', '104', '105', '106', '111', '112', '113', '114', '115', '116', '121', '122', '123', '124', '125', '126']
group_index = [-1, 4, 9, 14, 20, 26, 32]
grade_list = ['1', '2', '3', '4', '5','7', '8', '9']


help_text = '''歡迎加入政大附中無聲廣播系統
設定好個人資訊後，向管理員提出身分認證。

🔴🔴功能選單🔴🔴
若您使用電腦版Line，取得管理員認證後，傳送任意文字即可叫出功能選單。

🔴🔴發送廣播🔴🔴
1. 選擇"發送廣播"。
2. 選擇發送類型 "個別發送" 或 "群發年級"\n個別發送:限定發送一個班級(跳至2.1) 例如: 113\n群發年級:可組合不同年級與班級或是全校廣播(跳至2.2)
2.1 若您選擇 "個別發送"，輸入單個目標班級
2.2 若您選擇 "群體發送"，輸入班級組合(使用空格分開)
3. 輸入完目標班級後，系統提示"輸入廣播文字"，即可傳送廣播文字
4. 系統發送檢查通知，系統預設結束廣播時間為隔日(後天有傳出的廣播會被刪除)，若需延長廣播時間，請點"調整廣播結束日期"\n
5. 若無須修改結束廣播時間，按"YES我已確認"或"NO訊息有誤"更正即完成廣播。
🔴🔴重設&更正教師資訊🔴🔴
在選單點選"教師個人資訊"，按步驟更新資料，耐心等候管理員認證。

🔴🔴尋求幫助🔴🔴
忘記如何使用？歡迎連繫:#9611 資訊組長'''


# 建立下課字典
def make_break(BreakList):
    j = 0
    for i in range(8, 17, 1):
        if i == 12:
            BreakList['12S'] = "0"
            BreakList['12E'] = "30"
        elif i == 13:
            BreakList['13S'] = "5"
            BreakList['13E'] = "30"
        elif i == 15:
            BreakList['15S'] = "0"
            BreakList['15E'] = "15"
        else:
            BreakList[f'{i}S'] = "0"
            BreakList[f'{i}E'] = "10"
        j+=1






# 格式化班級
def format_class(input):
    numbers = re.findall(r'\d+', input)
    numbers = list(map(int, numbers))
    if not numbers:
        return input
    numbers.sort()
    print(numbers)
    result = []
    res = ""

    if "高中部" in input:
        res = "高中部"
    if  "國中部" in input:
        res += "國中部"

    start = numbers[0]
    prev_num = numbers[0]

    for current_num in numbers[1:]:
        if len(str(current_num)) == 3:
            if prev_num == current_num - 1:
                prev_num = current_num
            else:
                if start == prev_num:
                    if len(str(start)) == 3:
                        result.append(str(start))
                    else:
                        match (start):
                            case 1 | 2 | 3:
                                result.append(f"高{start}")
                                
                            case 7 | 8 | 9:
                                result.append(f"國{start}")
                else:
                    result.append(f"{start}-{prev_num}")

                start = current_num
                prev_num = current_num
        else:
            match (current_num):
                case 1 | 2 | 3:
                    result.append(f"高{current_num}")
                    
                case 7 | 8 | 9:
                    result.append(f"國{current_num}")
    # 處理最後一個數字
    if start == prev_num:
        result.append(str(start))
    else:
        result.append(f"{start}-{prev_num}")
    for item in result:
        res += " "+item

    return res


# 歷史訊息排序
def sort_history_message(history_data):
    length = len(history_data)
    i = 0
    for m in range(length):
        cList = []
        if i >= len(history_data):
            break
        # 國中格式處理
        elif int(history_data[i].des_grade[1:]) == 7 or int(history_data[i].des_grade[1:]) == 8 or int(history_data[i].des_grade[1:]) == 9:
            cList.append(history_data[i].des_grade + history_data[i].des_class)
            history_data[i].des_grade = f" {swapClassFromat(history_data[i].des_grade, history_data[i].des_class)}"
            
        # 高中加入字串
        else:
            history_data[i].des_grade += f"{history_data[i].des_class}"
            cList.append(history_data[i].des_grade)

        j = i+1 # 第i筆的下一個
        for k in range(i+1,length, 1):
            if j >= len(history_data):
                
                break
            if history_data[i].content == history_data[j].content and history_data[i].time == history_data[j].time:
                if int(history_data[j].des_grade[1:]) == 7 or int(history_data[j].des_grade[1:]) == 8 or int(history_data[j].des_grade[1:]) == 9: 
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
        history_data[i].des_grade = check_class(history_data[i].des_grade)
        i += 1
    return history_data


# 交換班級格式
def swapClassFromat(des_grade, des_class):
    result = des_grade[1:] + des_grade[0:1] + des_class
    return result 


# 縮短班級
def check_class(input):
    result = input
    for i in range(6):
        temp = class_list[group_index[i]+1:group_index[i+1]+1]
        words = result.split()
        if all(code in words for code in temp):
            match i:
                case 0:
                    result = "國一 " + ' '.join(word for word in words if word not in temp)
                case 1:
                    result = "國二 " + ' '.join(word for word in words if word not in temp)
                case 2:
                    result = "國三 " + ' '.join(word for word in words if word not in temp)
                case 3:
                    result = "高一 " + ' '.join(word for word in words if word not in temp)
                case 4:
                    result = "高二 " + ' '.join(word for word in words if word not in temp)
                case 5:
                    result = "高三 " + ' '.join(word for word in words if word not in temp)
            # print(result)
        else:
            pass
    
    words = result.split()
    if all(code in result for code in ["國一", "國二", "國三"]):
        result = "國中部 " + ' '.join(code for code in words if code not in ["國一", "國二", "國三"])
        words = result.split()
    if all(code in result for code in ["高一", "高二", "高三"]):
        result = "高中部 " + ' '.join(code for code in words if code not in ["高一", "高二", "高三"])
        words = result.split()

    if all(code in result for code in ["國中部", "高中部"]):
        result = "全校"
    # print(f"result: {result}")
    return result


# 計算字數
def calc_unicode_seg(text):
    segments = regex.findall(r'\X', text, regex.U)
    character_count = len(segments)
    return character_count


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


# 判斷是否為下課
def isBreak(BreakList):
    NowTime = datetime.now().time()
    if NowTime.hour >= 15:
        return 2
    elif NowTime.hour < 8:
        return 3
    breakTime_Start = time(NowTime.hour,int(BreakList[str(NowTime.hour)+"S"]), 0)
    breakTime_End = time(NowTime.hour, int(BreakList[str(NowTime.hour)+"E"]), 0)
    if NowTime >= breakTime_Start and NowTime <= breakTime_End:
        return 1
    else:
        return 3

