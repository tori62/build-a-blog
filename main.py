from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://build-a-blog:assign3@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'secretpassword'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(1000))

    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['POST','GET'])
def new_blog_entry():
    if request.method == 'POST':
        new_title = request.form['blog-title']
        new_post = request.form['body']

        if new_title == "" or new_post == "":
            error = "Please enter additional information."
            return render_template('newpost.html',blog_title=new_title,body=new_post,error=error)

        else:
            new_entry = Blog(new_title,new_post)
            db.session.add(new_entry)
            db.session.commit()
#        return render_template('single.html',blog_title=new_title,body=new_post)
        return redirect('/blog?id=' + str(new_entry.id))

    else:
        return render_template('newpost.html')

@app.route('/blog')
def blog_post():
    blog_id = request.args.get('id')
    if not blog_id:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)
    else:
        blogs = Blog.query.get(blog_id)
        title = blogs.title
        post = blogs.body
        return render_template('single.html',blog_title=title,body=post)


if __name__ == '__main__':
    app.run()   