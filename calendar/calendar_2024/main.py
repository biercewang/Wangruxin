import calendar
from fpdf import FPDF

def create_calendar_grid(year):
    # 创建横向的A4 PDF
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font("Arial", size=8)

    # 定义每个月份格子的大小
    cell_width = pdf.w / 4
    cell_height = pdf.h / 3

    # 生成每个月的日历
    for i, month in enumerate(range(1, 13)):
        # 计算每个格子的位置
        x = (i % 4) * cell_width
        y = (i // 4) * cell_height

        # 设置格子位置
        pdf.set_xy(x, y)

        # 获取月份日历字符串
        month_calendar = calendar.month(year, month).split("\n")

        # 月份标题
        pdf.cell(cell_width, 6, month_calendar[0], 0, 1, 'C')

        # 星期标题
        pdf.cell(cell_width, 6, " ".join(month_calendar[1].split()), 0, 1, 'C')

        # 日期
        for day_line in month_calendar[2:]:
            pdf.cell(cell_width, 6, " ".join(day_line.split()), 0, 1, 'C')

    # 保存PDF文件
    pdf_file = f'calendar_{year}.pdf'
    pdf.output(pdf_file)
    print(f"Calendar for {year} saved as {pdf_file}")

# 示例：生成2024年的日历
create_calendar_grid(2024)
