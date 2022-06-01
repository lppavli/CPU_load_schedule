import io
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime as dt, timedelta
from flask import Flask, render_template, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__, template_folder='template')


def getLastData():
    """Дата и время последних измерений"""
    conn = sqlite3.connect('cpu.db')
    curs = conn.cursor()
    for row in curs.execute("SELECT * FROM data ORDER BY created_date DESC LIMIT 1"):
        time = str(row[1])
        value = row[2]
    conn.close()
    return time, value


def getHistData():
    """Подготовка данных для построения графиков"""
    conn = sqlite3.connect('cpu.db')
    curs = conn.cursor()
    last_date = dt.now()
    first_date = last_date - timedelta(hours=1)
    curs.execute(f"""SELECT * FROM data WHERE (created_date <= '{last_date}' and 
                     created_date >= '{first_date}') order by created_date""")
    data = curs.fetchall()
    dates = []
    values = []
    avg_values = []
    while data:
        row = data[0]
        if dates and dt.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f") - dates[-1] > timedelta(seconds=6):
            dates.append(dates[-1] + timedelta(seconds=5))
            values.append(0)
            avg_values.append(0)
        else:
            dates.append(dt.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f"))
            values.append(row[2])
            avg_values.append(row[3])
            data.pop(0)
    conn.close()
    return dates, values, avg_values


@app.route("/")
def index():
    """Главная страница приложения"""
    time, value = getLastData()
    templateData = {'time': time, 'value': value}
    return render_template('index.html', **templateData)


@app.route('/plot1')
def plot_1():
    times, values, avg_values = getHistData()
    ys = values
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("История изменений моментальной загрузки процессора")
    axis.grid(True)
    xs = times
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


@app.route('/plot2')
def plot_2():
    times, values, avg_values = getHistData()
    ys = avg_values
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("История изменений средней загрузки процессора")
    axis.grid(True)
    xs = times
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=False)
