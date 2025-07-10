
import pendulum
from sxtwl import fromSolar
from jieqi import jq  # 導入項目自有的節氣計算模塊

# 天干地支基礎數據
tiangan = list('甲乙丙丁戊己庚辛壬癸')
dizhi = list('子丑寅卯辰巳午未申酉戌亥')

# 月柱地支與節氣的對應關係
month_dizhi_map = {
    "立春": "寅", "雨水": "寅",
    "驚蟄": "卯", "春分": "卯",
    "清明": "辰", "穀雨": "辰",
    "立夏": "巳", "小滿": "巳",
    "芒種": "午", "夏至": "午",
    "小暑": "未", "大暑": "未",
    "立秋": "申", "處暑": "申",
    "白露": "酉", "秋分": "酉",
    "寒露": "戌", "霜降": "戌",
    "立冬": "亥", "小雪": "亥",
    "大雪": "子", "冬至": "子",
    "小寒": "丑", "大寒": "丑",
}
# 寅月開始的天干順序
month_tiangan_list = ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"]
month_dizhi_list = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]


# 五虎遁月：年上起月法
wuhu_dun = {
    ('甲', '己'): "丙",
    ('乙', '庚'): "戊",
    ('丙', '辛'): "庚",
    ('丁', '壬'): "壬",
    ('戊', '癸'): "甲"
}

def get_bazi(dt: pendulum.DateTime) -> dict:
    """
    根據 pendulum 日期時間對象計算四柱 (Bazi)。
    使用 jieqi.py 進行節氣判斷，確保月柱準確。
    """
    year, month, day, hour, minute = dt.year, dt.month, dt.day, dt.hour, dt.minute
    lunar_info = fromSolar(year, month, day)

    # 1. 年柱 (來自sxtwl)
    year_gz = f"{tiangan[lunar_info.getYearGZ().tg]}{dizhi[lunar_info.getYearGZ().dz]}"
    year_gan = year_gz[0]

    # 2. 月柱 (核心修正：使用 jieqi.py 和五虎遁)
    # 獲取當前節氣
    current_jieqi = jq(year, month, day, hour, minute)
    
    # 根據節氣確定月柱地支
    month_zhi = month_dizhi_map[current_jieqi]
    
    # 根據年干確定寅月的月干
    start_tiangan = None
    for k, v in wuhu_dun.items():
        if year_gan in k:
            start_tiangan = v
            break
    
    # 從寅月開始，找到對應地支的月干
    start_index = tiangan.index(start_tiangan)
    month_gan_index = (start_index + month_dizhi_list.index(month_zhi)) % 10
    month_gan = tiangan[month_gan_index]
    
    month_gz = f"{month_gan}{month_zhi}"

    # 3. 日柱 (來自sxtwl)
    day_gz = f"{tiangan[lunar_info.getDayGZ().tg]}{dizhi[lunar_info.getDayGZ().dz]}"
    
    # 4. 時柱 (來自sxtwl)
    hour_info = lunar_info.getHourGZ(hour)
    hour_gz = f"{tiangan[hour_info.tg]}{dizhi[hour_info.dz]}"

    return [year_gz, month_gz, day_gz, hour_gz]

if __name__ == "__main__":
    # 根據您的要求，使用此時間作為範例
    target_datetime = pendulum.datetime(2003, 5, 12, 22, 40, tz='Asia/Hong_Kong')
    
    bazi_result = get_bazi(target_datetime)
    print(bazi_result)
    print(bazi_result[0][0])