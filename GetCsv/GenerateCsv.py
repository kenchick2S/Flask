import csv
import random
import time


# 生成隨機的日期
def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y%m%d', prop)

# 客戶資料
C_NAME_ID_DICT = {
    "X1760":"賴凰鳴",
    "W2337":"涂玉芸",
    "U2636":"江可微",
    "H2664":"林丹雨",
    "A2401":"顏平言",
    "J2985":"胡正爾",
    "X1422":"吳光理",
    "O2672":"孫捷玟",
    "C2834":"王亞鬆",
    "D1287":"田杉遠",
    "G1787":"詹剛勝",
    "C2526":"王喧海",
    "U1092":"王伯潮",
    "Y1718":"鄒祺興",
    "Z2432":"鄭慧飛",
    "I1055":"張實豪",
    "B2099":"洪安文",
    "A1849":"王斯運",
    "O1949":"周塵文",
    "E2600":"林銀霞"
}

# 員工資料
E_NAME_ID_DICT = {
    "L2699":"黃容旭",
    "B1436":"吳光磊",
    "W1150":"洪林歆",
    "K2546":"賴芯菡",
    "F2871":"黎奕舒",
    "X2889":"魏于嬋",
    "Y2145":"魏宛禹",
    "U2206":"林昀琉",
    "A1405":"曾添瑩",
    "V1046":"陳濮舒"
}

# 商品名稱
Product_Name = ["富邦吉祥貨幣市場基金", "富邦精準基金", "富邦長紅基金", "富邦高成長基金", "富邦科技基金" \
              "富邦台灣心基金", "富邦全球不動產基金", "富邦大中華成長基金", "富邦精銳中小基金", "富邦全球投資等級債券"]

# 建立 客戶和員工 ID 列表
E_ID_List = list(E_NAME_ID_DICT.keys())
C_ID_List = list(C_NAME_ID_DICT.keys())

# 建立日期列表
Date_List = []
for ID in range(1,1001):
  Date_List.append(random_date("20220101", "20240101", random.random()))
Date_List.sort()

# 開啟一個 CSV
with open('Customer_Performance.csv', mode='w') as file:
  file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

  # 寫入欄位名稱
  file_writer.writerow(['Transaction_ID', 'Employee_ID', 'Employee_Name', 'Transaction_Date', 'Product_Name', 'Transaction_Amount', 'Customer_ID', 'Customer_Name'])

  # 生成隨機的資料
  for ID in range(1,1001):
    E_ID = random.choice(E_ID_List)
    E_Name = E_NAME_ID_DICT[E_ID]
    C_ID = random.choice(C_ID_List)
    C_Name = C_NAME_ID_DICT[C_ID]
    Product = random.choice(Product_Name)
    Date = Date_List[ID-1]
    Amount = random.randint(1000, 100000)

    file_writer.writerow([str(ID).zfill(5), E_ID, E_Name, Date, Product, Amount, C_ID, C_Name])
