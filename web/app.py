import os
import json
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    # Зчитуємо звіт про якість даних
    quality_data = {}
    quality_path = '/app/reports/quality_report.json'
    if os.path.exists(quality_path):
        with open(quality_path, 'r', encoding='utf-8') as f:
            quality_data = json.load(f)

    # Передаємо ці дані у HTML-шаблон
    return render_template('index.html', quality=quality_data)

# Спеціальний маршрут для роздачі картинок (графіків)
@app.route('/plots/<filename>')
def get_plot(filename):
    return send_from_directory('/app/plots', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)