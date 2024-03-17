from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def load_news():
    news = []
    df = pd.read_excel('news.xlsx')
    for index, row in df.iterrows():
        news.append({
            'title': row['Title'],
            'date': row['Date'].strftime('%d-%m-%Y'),
            'content': row['Content']
        })
    return news

@app.route('/')
def index():
    news_list = load_news()
    return render_template('index.html', news=news_list)

if __name__ == '__main__':
    app.run(debug=True)

