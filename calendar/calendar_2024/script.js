function generateCalendar(year) {
    const yearHeader = document.getElementById('year-header');
    yearHeader.innerText = year + '年';

    const calendarContainer = document.getElementById('calendar');
    const weekdays = ['日', '一', '二', '三', '四', '五', '六'];

    for (let month = 0; month < 12; month++) {
        const monthDiv = document.createElement('div');
        monthDiv.className = 'month';
        
        const monthHeader = document.createElement('div');
        monthHeader.className = 'month-header';
        monthHeader.innerText = (month + 1) + '月';
        monthDiv.appendChild(monthHeader);

        const grid = document.createElement('div');
        grid.className = 'month-grid';

        // 添加星期标题
        weekdays.forEach(day => {
            const dayDiv = document.createElement('div');
            dayDiv.className = 'day-header';
            dayDiv.innerText = day;
            grid.appendChild(dayDiv);
        });

        // 添加日期
        const date = new Date(year, month, 1);
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // 从星期日开始填充空格
        for (let i = 0; i < date.getDay(); i++) {
            grid.appendChild(document.createElement('div'));
        }

        // 填充日期
        for (let i = 1; i <= daysInMonth; i++) {
            const dateDiv = document.createElement('div');
            dateDiv.innerText = i;
            grid.appendChild(dateDiv);
        }

        monthDiv.appendChild(grid);
        calendarContainer.appendChild(monthDiv);
    }
}

generateCalendar(2024);
