from datetime import date, timedelta
import calendar
import datetime
from flask import Flask, render_template

app = Flask(__name__)


SWEEPING_DAY = 0 #monday

def get_next_sweeping_date():
    today = date.today()
    year = today.year
    month = today.month
    day = 1
    while True:
        try:
            d = date(year, month, day)
        except ValueError:
            month += 1
            if month > 12:
                month = 1
                year += 1
            day = 1
            continue

        if d.weekday() == SWEEPING_DAY and d >= today:
            break
        day += 1

    return d


# ngl i suck ass at coding and even more so at frontend 
@app.route('/')
def index():
    next_sweeping_date = get_next_sweeping_date()
    week_number = (next_sweeping_date.day - 1) // 7 + 1
    if week_number % 2 == 1:
        side = 'odd'
    else:
        side = 'even'
        car_class = 'even'
    if next_sweeping_date.weekday() == SWEEPING_DAY:
        message = f'The next street sweeping date is {calendar.month_name[next_sweeping_date.month]} {next_sweeping_date.day}.<br>The <span class="{side}">{side}</span> side of the street will be swept.'
    else:
        next_sweeping_date += timedelta(weeks=1)
        side = 'odd' if side == 'even' else 'even'
        message = f'The next street sweeping date is {calendar.month_name[next_sweeping_date.month]} {next_sweeping_date.day}.<br>The <span class="{side}">{side}</span> side of the street will be swept.'
    
    return render_template('index.html', message=message, side=side)

if __name__ == '__main__':
    app.run()