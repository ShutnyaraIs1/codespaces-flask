from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import os

os.environ['FLASK_SKIP_DOTENV'] = '1'  # Отключение предупреждения о секретном ключе

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def load_news(category):
    news = []
    file_path = os.path.join('uploads', f'{category}.xlsx')
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        news.append({
            'title': row['Title'],
            'date': row['Date'].strftime('%Y-%m-%d'),
            'content': row['Content']
        })
    return news

def get_categories():
    categories = []
    for file in os.listdir('uploads'):
        if file.endswith('.xlsx'):
            categories.append(file.replace('.xlsx', ''))
    return categories

@app.route('/')
def index():
    categories = get_categories()
    return render_template('index.html', categories=categories)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload_news', methods=['POST'])
def upload_news():
    file = request.files['file']
    password = request.form['password']

    if password != '**11072007**':
        flash('Неверный пароль')
        return redirect(url_for('upload'))

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('news', category=filename.replace('.xlsx', '')))

@app.route('/news/<category>')
def news(category):
    news_list = load_news(category)
    return render_template('news.html', news=news_list, category=category)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

