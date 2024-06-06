from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from transformers import pipeline

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the News model
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summarized_content = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<News {self.title}>'

# Initialize the database
with app.app_context():
    db.create_all()

# Load the summarization pipeline
pipe = pipeline("summarization", model="Azma-AI/bart-large-text-summarizer")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_news', methods=['POST'])
def add_news():
    title = request.form['title']
    content = request.form['content']
    
    summary = pipe(content, max_length=150, min_length=30, do_sample=False)
    summarized_content = summary[0]['summary_text']
    
    new_article = News(title=title, content=content, summarized_content=summarized_content)
    
    db.session.add(new_article)
    db.session.commit()
    
    return jsonify({'title': title, 'summary': summarized_content})

@app.route('/get_news', methods=['GET'])
def get_news():
    articles = News.query.with_entities(News.title, News.summarized_content).all()
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
