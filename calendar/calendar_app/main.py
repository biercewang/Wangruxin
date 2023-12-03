import calendar
import sys
import webbrowser
import os
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
from datetime import datetime

class FestivalGenerator:
    def __init__(self, year):
        self.year = year

        self.festivals = {

            (1, 1): "元旦",  
            (2, 14): "情人节",
            (3, 8): "妇女节",
            (3, 12): "植树节",
            (4, 1): "愚人节",
            (5, 1): "劳动节",
            (5, 4): "青年节",
            (6, 1): "儿童节",
            (7, 1): "党的生日",
            (8, 1): "建军节",
            (9, 10): "教师节",
            (10, 1): "国庆节",
            (12, 25): "圣诞节",
        }
       
        self.birthdays = {
            (1, 20): "贝贝生日",
            (2, 21): "妈妈生日",
            (11, 5): "如心生日",
            (12, 24): "爸爸生日",
            (12, 7): "爷爷生日",
            (6, 2): "奶奶生日",             
            # ... [在这里添加其他生日]
        }

        self.floating_festivals = {
            (11, 4, 4): "感恩节",  
            (5, 2, 7): "母亲节",
            (6, 3, 7): "父亲节",
            # ... [在这里添加其他浮动节日] (月份, 月份中的第几个星期,星期几的索引,其中星期一为1，星期日为7)
        }

        self.add_lunar_festivals()

        self.add_floating_festivals()

    def calculate_floating_festival(self, month, occurrence, weekday_index):
        """计算浮动节日的日期，星期一为1，星期日为7"""
        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        month_cal = c.monthdatescalendar(self.year, month)
        # 调整weekday_index以符合Python calendar模块的要求
        adjusted_weekday_index = (weekday_index - 1) % 7
        festival_day = [day for week in month_cal for day in week if day.weekday() == adjusted_weekday_index and day.month == month][occurrence-1]
        return festival_day

    def add_floating_festivals(self):
        """根据floating_festivals字典添加浮动日期的节日"""
        for (month, occurrence, weekday_index), name in self.floating_festivals.items():
            festival_day = self.calculate_floating_festival(month, occurrence, weekday_index)
            self.festivals[(festival_day.month, festival_day.day)] = name

    def add_lunar_festivals(self):
        """添加农历节日"""
        lunar_festivals = {
            (1, 1): "春节",
            (5, 5): "端午节",
            (8, 15): "中秋节",
            (1, 15): "元宵节",
            (5, 5): "端午节",
            (7, 7): "七夕节",
            (9, 9): "重阳节",
            (12, 8): "腊八节",
            # ... [在这里添加其他农历节日]
        }

        for (lunar_month, lunar_day), festival_name in lunar_festivals.items():
            try:
                solar_date = Converter.Lunar2Solar(Lunar(self.year, lunar_month, lunar_day))
                self.festivals[(solar_date.month, solar_date.day)] = festival_name
            except DateNotExist:
                pass  # 在某些年份，特定的农历日期可能不存在（比如闰月）

    def get_festivals(self):
            """返回节日字典"""
            return self.festivals
    
    def get_birthdays(self):
            """返回生日字典"""
            return self.birthdays

    


def generate_calendar_html(year,festivals,birthdays):
    # 创建一个calendar对象
    cal = calendar.Calendar(firstweekday=6)  # 将周日设为每周的第一天

    # HTML头部和样式
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{year} Calendar</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 0;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}
            #year-header {{
                font-size: 25px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            #calendar {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                grid-gap: 5px;
                width: 100%;
                max-width: 297mm;
            }}
            .month {{
                border: 1px solid black;
                padding: 3px;
                display: grid;
                grid-template-rows: auto 1fr; /* 分为标题和日历网格 */
                height: 70mm;
            }}
            .month-header {{
                font-size: 20px;
                font-weight: bold;
            }}
            .month-grid {{
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                grid-gap: 1px;
                text-align: center;
                font-size: 10px;
                overflow: hidden; /* 确保内容不会溢出 */
            }}
            .day-header, .month-grid div {{
                border: 1px solid darkgray;
                box-sizing: border-box;
                height: 90%; /* 使得每个小格子高度一致 */
            }}
            .day-header {{
                font-weight: bold;
                background-color: #f0f0f0;
                height: 10px; /* 统一星期标题的高度 */
                line-height: 20px; /* 垂直居中文本 */
                font-size: 18px; /* 增大星期标题字体大小 */
            }}
        </style>
    </head>
    <body>
        <div id='year-header'>{year}年</div>
        <div id='calendar'>
    """

    # 为每个月生成日历布局
    for month in range(1, 13):
        # 月份格子
        html_content += f"<div class='month'><div class='month-header'>{month}月</div><div class='month-grid'>"

        # 星期标题
        weekdays = ['日', '一', '二', '三', '四', '五', '六']
        for day in weekdays:
            html_content += f"<div class='day-header'>{day}</div>"

        # 计算每个月的日期布局
        month_days = cal.monthdayscalendar(year, month)
        if len(month_days) == 6:
            # 将最后一行的日期合并到倒数第二行
            for i, day in enumerate(month_days[-1]):
                if day != 0:
                    month_days[-2][i] = f"{month_days[-2][i]}/{day}"
            month_days.pop()  # 移除最后一行

        # 填充日期
        for week in month_days:
            for day in week:
                day_str = f"{day}" if day != 0 else ""
                festival_str = festivals.get((month, day), "")
                birthday_str = birthdays.get((month, day), "")
                if not festival_str and not birthday_str:
                    festival_str = "&nbsp;"
                if not birthday_str:
                    birthday_str = "&nbsp;"               
                # 将日期和节日放在不同的行
                html_content += f"<div><span>{day_str}</span><br><span class='festival'>{festival_str}</span><br><span class='birthday'>{birthday_str}</span></div>"



        html_content += "</div></div>"

    # HTML结尾
    html_content += """
        </div>
        <style>
            .festival {
                font-size: 6px; /* 调整节日文字大小 */
                color: #999; /* 节日文字颜色 */
            }
            .birthday {
                font-size: 6px; /* 调整生日文字大小 */
                color: #ff6666; /* 生日文字颜色 */
            }
            /* 其他样式 */
        </style>
    </body>
    </html>
    """

    # 将HTML内容写入文件
    html_file_name = f"calendar_{year}.html"
    with open(html_file_name, "w", encoding="utf-8") as file:
        file.write(html_content)

    # 打开文件在默认浏览器
    webbrowser.open('file://' + os.path.realpath(html_file_name))

def main(year):
    """生成并显示指定年份的日历HTML文件。"""
    festival_generator = FestivalGenerator(year)
    festivals = festival_generator.get_festivals()
    birthdays = festival_generator.get_birthdays() 
    generate_calendar_html(year, festivals, birthdays)


if __name__ == "__main__":
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
            main(year)
        except ValueError:
            print("Please provide a valid year.")
    else:
        print("Please provide a year as an argument.")
