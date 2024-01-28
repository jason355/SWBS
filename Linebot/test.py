from datetime import datetime, time

BreakList = {}
Timekey = 0
class_list = ['701', '702', '703', '704', '705', '801', '802', '803', '804', '805', '901', '902', '903', '904', '905','101', '102', '103', '104', '105', '106', '111', '112', '113', '114', '115', '116', '121', '122', '123', '124', '125', '126']
group_index = [-1, 4, 9, 14, 20, 26, 32]


def isBreak():
    NowTime = datetime.now().time()
    breakTime_Start = time(NowTime.hour,int(BreakList[str(NowTime.hour)+"S"]), 0)
    breakTime_End = time(NowTime.hour, int(BreakList[str(NowTime.hour)+"E"]), 0)
    if NowTime >= breakTime_Start and NowTime <= breakTime_End:
        return 1
    elif NowTime.hour >= 15:
        return 2
    else:
        return 3


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
    
    return result


check_class("103 104 105 106 111 112 116 121 122 123 124 125 126 701 702 703  803 804 805 901 902 903 904 905")