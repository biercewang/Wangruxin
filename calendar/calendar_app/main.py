import calendar
import sys
import webbrowser
import os

def generate_calendar_html(year):
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
                font-size: 18px;
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
                height: 70mm;
            }}
            .month-header {{
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 2px;
            }}
            .month-grid {{
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                grid-gap: 1px;
                text-align: center;
                font-size: 10px;
                height: 100%;
            }}
            .day-header {{
                font-weight: bold;
                background-color: #f0f0f0;
            }}
        </style>
    </head>
    <body>
        <div id="year-header">{year}年</div>
        <div id="calendar">
    """

    # 为每个月生成日历布局
    for month in range(1, 13):
        # 月份格子
        html_content += f"<div class='month'><div class='month-header'>{month}月</div><div class='month-grid'>"

        # 星期标题
        weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
        for day in weekdays:
            html_content += f"<div class='day-header'>{day}</div>"

        # 填充空白直到第一天
        first_day_of_month = calendar.weekday(year, month, 1)
        for _ in range((first_day_of_month + 1) % 7):
            html_content += "<div></div>"

        # 填充日期
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            html_content += f"<div>{day}</div>"

        html_content += "</div></div>"

    # HTML结尾
    html_content += """
        </div>
    </body>
    </html>
    """

    # 将HTML内容写入文件
    html_file_name = f"calendar_{year}.html"
    with open(html_file_name, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Calendar for {year} saved as {html_file_name}")

    webbrowser.open('file://' + os.path.realpath(html_file_name))

# 获取命令行中的年份参数
if len(sys.argv) > 1:
    try:
        year = int(sys.argv[1])
        generate_calendar_html(year)
    except ValueError:
        print("Please provide a valid year.")
else:
    print("Please provide a year as an argument.")

