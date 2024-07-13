from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Post, Comment, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        # Assuming user with id=1 exists
        new_post = Post(title=title, content=content, user_id=1)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_post.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)