from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))
    completed = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.completed = datetime.utcnow()

    def is_valid(self):
        if self.title and self.body and self.completed:
            return True
        else:
            return False

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog_index():
    blog_id = request.args.get('id')
    blogs = Blog.query.all()

    if blog_id:
        post = Blog.query.get(blog_id)
        blog_title = post.title
        blog_body = post.body
        return render_template('entry.html', title="Blog Entry #" + blog_id, blog_title=blog_title, blog_body=blog_body)

    sort = request.args.get('sort')

    if (sort=="newest"):
        blogs = Blog.query.order_by(Blog.completed.desc()).all()
    elif (sort=="oldest"):
        blogs = Blog.query.order_by(Blog.completed.asc()).all()
    else:
        blogs = Blog.query.all()
    return render_template('blog.html', title="Build A Blog", blogs=blogs)

@app.route('/post')
def new_post():
    return render_template('post.html', title="Add New Blog Entry")


@app.route('/post', methods=['POST'])
def verify_post():
    blog_title = request.form['title']
    blog_body = request.form['body']
    title_error = ''
    body_error = ''

    date_posted='Janurary 8, 1950'

    if blog_title == "":
        title_error = "Title required."
    if blog_body == "":
        body_error = "Content required."


    if not title_error and not body_error:
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        blog = new_blog.id
        
        return redirect('/blog?id={0}'.format(blog))
    else:
        
        return render_template('post.html', title="Add New Blog Entry", blog_title = blog_title, blog_body = blog_body, title_error = title_error, body_error = body_error, date_posted = date_posted())
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)



if __name__ == '__main__':
    app.run()