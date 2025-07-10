import pendulum
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random
import re
from bazi import get_bazi

# 定义天干和地支列表
tian_gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
di_zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
# 创建一个字典来表示五行属性
data = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火',
    '戊': '土', '己': '土', '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
}
# 创建一个字典来映射五行生克关系
sheng_ke_relations = {
    '水': {'生': '木', '克': '火', '比': '水'},
    '火': {'生': '土', '克': '金', '比': '火'},
    '木': {'生': '火', '克': '土', '比': '木'},
    '金': {'生': '水', '克': '木', '比': '金'},
    '土': {'生': '金', '克': '水', '比': '土'}
}

# 排四柱
def sizhu(time_zero):
    # 移除时区信息
    time_format = time_zero.replace(tzinfo=None)
    time_zero = get_bazi(time_zero)

    rizhi = time_zero[2][1]
    shigan = time_zero[3][0]
    shizhi = time_zero[3][1]
    # shizhi在di_zhi检索其位置 -> int
    shizhi_index = di_zhi.index(shizhi)

    
    bazisizhu = time_zero
    bazisizhu.append(time_format)
    ren = [rizhi, shigan, shizhi, shizhi_index]

    return bazisizhu, ren



def shengke(zhu, ke):
    element1 = data[zhu]
    element2 = data[ke]
    if sheng_ke_relations[element1]['生'] == element2:
        a = "子孙"
    elif sheng_ke_relations[element1]['克'] == element2:
        a = "妻财"
    elif sheng_ke_relations[element2]['生'] == element1:
        a = "父母"
    elif sheng_ke_relations[element2]['克'] == element1:
        a = "官鬼"
    elif sheng_ke_relations[element2]['比'] == element1:
        a = "兄弟"
    return a

# 小六壬排盘
def liuren(bazisizhu, ren, random_num):
    # 定义小六壬的基本元素
    gong = ["大安", "留连", "速喜", "赤口", "小吉", "空亡"]
    qin = []  # 存放六亲运算结果
    shen = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]
    xing = ["木星", "火星", "土星", "金星", "水星", "天空"]
    yin = ['丑', '卯', '巳', '未', '酉', '亥']
    yang = ['子', '寅', '辰', '午', '申', '戌']
    order = [1, 2, 3, 0, 5, 4]  # 绘图顺序

    # 日上起时
    # 日
    random_label = str(random_num)
    random_num %= 6  # 随机数
    ri = ren[0]
    ri_num = di_zhi.index(ri) + random_num
    ri_num %= 6
    # 时
    # 断阴阳
    yy = ren[3]
    shi = ren[2]
    if yy % 2 != 0:
        shi_index = yin.index(shi)
        new_shi = yin[shi_index:] + yin[:shi_index]
    else:
        shi_index = yang.index(shi)
        new_shi = yang[shi_index:] + yang[:shi_index]
    # 校准序数
    shi_num = di_zhi.index(shi) + 1
    shi_num = (shi_num % 6 + ri_num - 1) % 6  # 序数化
    new_shi = new_shi[-(shi_num-1):] + new_shi[:-(shi_num-1)]

    # 星
    xing_num = ri_num
    new_xing = xing[-(xing_num-1):] + xing[:-(xing_num-1)]

    # 六亲
    for i in range(0, len(new_shi)):
        zhu = ren[2]
        ke = new_shi[i]
        qin_qin = shengke(zhu, ke)  # 调用函数计算
        qin.append(qin_qin)
    # print(qin, shi_num)
    shi_x = new_shi.index(shi)
    del qin[shi_x]  # 安命度
    qin.insert((shi_x), '身命')
    # 找兄弟
    if '兄弟' in qin:
        pass
    else:
        tu = []
        for t in new_shi:
            if data[t] == '土':
                tu.append(t)
        dist1 = abs(new_shi.index(tu[0]) - (shi_num-1))
        dist2 = abs(new_shi.index(tu[1]) - (shi_num-1))
        if dist1 > dist2:
            qin[new_shi.index(tu[0])] = '兄弟'
        else:
            qin[new_shi.index(tu[1])] = '兄弟'

    # 六神
    shen_huo = data[new_shi[(ri_num-1)]]
    print(shen_huo)
    if shen_huo == '金':
        shen_index = shen.index('白虎')
        new_shen = shen[shen_index:] + shen[:shen_index]
        new_shen = new_shen[-(ri_num-1):] + new_shen[:-(ri_num-1)]
    elif shen_huo == '木':
        shen_index = shen.index('青龙')
        new_shen = shen[shen_index:] + shen[:shen_index]
        new_shen = new_shen[-(ri_num-1):] + new_shen[:-(ri_num-1)]
    elif shen_huo == '火':
        shen_index = shen.index('朱雀')
        new_shen = shen[shen_index:] + shen[:shen_index]
        new_shen = new_shen[-(ri_num-1):] + new_shen[:-(ri_num-1)]
    elif shen_huo == '水':
        shen_index = shen.index('玄武')
        new_shen = shen[shen_index:] + shen[:shen_index]
        new_shen = new_shen[-(ri_num-1):] + new_shen[:-(ri_num-1)]
    elif shen_huo == '土':
        goushe = new_shi[(ri_num-1)]
        if goushe == '丑' or goushe == '辰':
            shen_index = shen.index('勾陈')
            new_shen = shen[shen_index:] + shen[:shen_index]
            new_shen = new_shen[-(ri_num - 1):] + new_shen[:-(ri_num - 1)]
        elif goushe == '未' or goushe == '戌':
            shen_index = shen.index('螣蛇')
            new_shen = shen[shen_index:] + shen[:shen_index]
            new_shen = new_shen[-(ri_num - 1):] + new_shen[:-(ri_num - 1)]


    # 加日时
    end_shi = new_shi
    end_shi_index = end_shi.index(shi)  # 找时支
    end_shigan = ren[1]
    end_shi_qin = shengke(shi, end_shigan)
    del end_shi[end_shi_index]
    end_shi.insert((end_shi_index), '%s(%s)\n%s(时)'%(end_shigan, end_shi_qin, shi))
    end_ri = new_shi[(ri_num-1)]  # 找日支
    end_ri_index = end_shi.index(end_ri)
    del end_shi[end_ri_index]
    end_shi.insert((end_ri_index), end_ri + '(日)')

    # 初始化主窗口
    root2 = tk.Toplevel()
    root2.title("小六壬")
    # 设置窗口图标
    icon_path = 'img/cons.ico'  # 替换为你的图标文件的实际路径
    root2.iconbitmap(icon_path)

    # 定义字体  https://color.llc/
    custom_font = '黑体'

    # 创建画布
    canvas = tk.Canvas(root2, width=1200, height=400, bg="white")
    canvas.pack()

    # 宫格的宽和高
    cell_width = 270
    cell_height = 180
    # 计算水平和垂直方向的边距，使宫格居中
    margin_x = (1000 - 3 * cell_width) // 2 - 80
    margin_y = (400 - 2 * cell_height) // 2

    # 绘制表格
    for i in range(2):  # 两行
        for j in range(3):  # 三列
            # 真序数
            index = i * 3 + j
            real_index = order[index]

            x1 = margin_x + j * cell_width
            y1 = margin_y + i * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height

            # 绘制线条区分的矩形
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=4)

            # 宫位标题
            title_text = f"{gong[real_index]}"
            canvas.create_text(x1 + 10, y2 - 10, text=title_text, font=(custom_font, 20, "bold"), anchor="sw")

            # 六星信息
            star_text = f"{new_xing[real_index]}"
            canvas.create_text(x2 - 10, y1 + 10, text=star_text, font=(custom_font, 16), anchor="ne")

            # 六亲信息
            qin_text = f"{qin[real_index]}"
            canvas.create_text(x2 - 10, y2 - 10, text=qin_text, font=(custom_font, 17, "bold"), anchor="se")

            # 用神信息
            shen_text = f"{new_shen[real_index]}"
            canvas.create_text(x1 + 10, y1 + 10, text=shen_text, font=(custom_font, 18, "bold"), anchor="nw")

            # 地支信息
            zhi_text = f"{end_shi[real_index]}"
            canvas.create_text(x1 + 10, (y1 + y2) // 2, text=zhi_text, font=(custom_font, 16), anchor="w")

        # 参数
        # 自由度
        random_text = 6 if random_num == 0 else random_num
        zhi_text = '起数%s  ' % (random_label) + '变数' + f"{random_text}"
        canvas.create_text(margin_x + 900, margin_y // 2 + 70, text=zhi_text, font=('custom_font', 18), anchor="w")

        # 八字
        bazi_str = '年月日时\n'
        bazi_str += bazisizhu[0][0] + bazisizhu[1][0] + bazisizhu[2][0] + bazisizhu[3][0] + '\n'
        bazi_str += bazisizhu[0][1] + bazisizhu[1][1] + bazisizhu[2][1] + bazisizhu[3][1]
        bazi_str = ''.join([char + ' ' for char in bazi_str])[:-1]
        bazi_str = ' ' + bazi_str
        bazi_str = '\n\n' + str(bazisizhu[4]) + '\n\n' + bazi_str
        zhi_text = f"{bazi_str}"
        canvas.create_text(margin_x + 900, margin_y // 2 + 200, text=zhi_text, font=('楷体', 20), anchor="w")


    # 进入主循环
    root2.mainloop()


# main
# 定义一个函数来检查给定的年份是否为闰年
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# 定义一个函数来生成指定月份的有效日期列表
def get_days_in_month(year, month):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return list(range(1, 32))
    elif month in [4, 6, 9, 11]:
        return list(range(1, 31))
    elif month == 2:
        return list(range(1, 29 + is_leap_year(year)))

# 更新
def update_days(event=None):
    selected_year = var_year.get()
    selected_month = var_month.get()

    # 检查是否选择了有效的年份和月份
    if selected_year.isdigit() and selected_month.isdigit():
        selected_year = int(selected_year)
        selected_month = int(selected_month)
        days = get_days_in_month(selected_year, selected_month)
        var_day.set('请选择日期')  # 重置当前选定的日期
        day_menu['values'] = [str(d) for d in days]
    else:
        day_menu['values'] = []  # 如果没有选择有效的年份或月份，清空日期下拉菜单


def create_input_window():
    global var_year, var_month, var_day, day_menu, var_hour, var_minute # 声明全局变量以便在函数外部也能访问

    root = tk.Tk()
    root.title("小六壬")
    # 设置窗口图标
    icon_path = 'img/cons.ico'  # 替换为你的图标文件的实际路径
    root.iconbitmap(icon_path)

    frame = tk.Frame(root)
    frame.pack(pady=20)

    # 初始化变量
    var_year = tk.StringVar(value='年份')
    var_month = tk.StringVar(value='月份')
    var_day = tk.StringVar(value='日期')
    var_hour = tk.StringVar(value='时')
    var_minute = tk.StringVar(value='分')
    var_random = tk.StringVar(value='变数(整数)')

    # 随机数输入框
    tk.Label(frame, text="数").grid(row=5, column=0)
    random_list = [random.randint(0, 1000) for _ in range(20)]
    random_menu = ttk.Combobox(frame, textvariable=var_random, values=random_list)
    random_menu.grid(row=5, column=1)

    # 年份下拉菜单
    tk.Label(frame, text="年").grid(row=0, column=0)
    year_menu = ttk.Combobox(frame, textvariable=var_year, values=[str(y) for y in range(2018, 2035)], state='readonly')
    year_menu.grid(row=0, column=1)
    year_menu.bind('<<ComboboxSelected>>', update_days)  # 当年份改变时也更新日期

    # 月份下拉菜单
    tk.Label(frame, text="月").grid(row=1, column=0)
    month_menu = ttk.Combobox(frame, textvariable=var_month, values=[str(m) for m in range(1, 13)], state='readonly')
    month_menu.grid(row=1, column=1)
    month_menu.bind('<<ComboboxSelected>>', update_days)  # 绑定事件，当月份改变时更新日期

    # 日下属菜单
    tk.Label(frame, text="日").grid(row=2, column=0)
    day_menu = ttk.Combobox(frame, textvariable=var_day, state='readonly')  # 正确定义day_menu
    day_menu.grid(row=2, column=1)

    # 小时下拉菜单
    tk.Label(frame, text="时").grid(row=3, column=0)
    hour_menu = ttk.Combobox(frame, textvariable=var_hour, values=[str(h) for h in range(24)], state='readonly')
    hour_menu.grid(row=3, column=1)

    # 分钟下拉菜单
    tk.Label(frame, text="分").grid(row=4, column=0)
    minute_menu = ttk.Combobox(frame, textvariable=var_minute, values=[str(m) for m in range(60)], state='readonly')
    minute_menu.grid(row=4, column=1)


    # 提交
    button = tk.Button(frame, text="起课", command=lambda: on_button_click(var_year, var_month, var_day, var_hour, var_minute, var_random))
    button.grid(row=6, column=1, pady=0)

    # 一键生成
    now = datetime.now()
    now_year = now.year
    now_month = now.month
    now_day = now.day
    now_hour = now.hour
    now_minute = now.minute
    button = tk.Button(frame, text="当前时辰", command=lambda: auto_click(now_year, now_month, now_day, now_hour, now_minute, var_random))
    button.grid(row=6, column=2, pady=0)

    root.mainloop()

# 一键生成
def auto_click(year, month, day, hour, minute, random_num_var):
    print(f"Selected Year: {year}, Month: {month}, Day: {day}, Hour: {hour}, Minute: {minute}")
    random_num = random_num_var.get()
    actual_random_num = 1 if not re.match(r'^-?\d+$', random_num) else int(random_num)  # 随机数int处理
    
    time_zero = pendulum.datetime(year, month, day, hour, minute)
    bazisizhu_auto, ren_auto = sizhu(time_zero)
    liuren(bazisizhu_auto, ren_auto, actual_random_num)

# 点击起课
def on_button_click(year_var, month_var, day_var, hour_var, minute_var, random_num_var):
    year = int(year_var.get())
    month = int(month_var.get())
    day = int(day_var.get())
    hour = int(hour_var.get())
    minute = int(minute_var.get())

    random_num = random_num_var.get()
    random_num = 1 if not re.match(r'^-?\d+$', random_num) else int(random_num)  # 随机数int处理

    time_zero = pendulum.datetime(year, month, day, hour, minute)
    
    print(f"Selected Year: {year}, Month: {month}, Day: {day}, Hour: {hour}, Minute: {minute}")
    bazisizhu, ren = sizhu(time_zero)
    liuren(bazisizhu, ren, random_num)

# 调用函数创建窗口
create_input_window()