"""Blogly application."""
import datetime
from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ahdlkhawkedhwa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

NULL_USER = {'first_name': '', 'last_name': '', 'image_url': ''}
NULL_POST = {'title': '', 'content': ''}


def add_edit_user(first_name, last_name, image_url, user=None):
    '''If user=none, adds new user and commits to db, otherwise updates existing user. Returns false if required fields are None'''

    if not first_name or not last_name:
        flash("First and last name required!")
        return False

    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
    else:
        user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()
    return True


def add_edit_post(title, content, user_id, post=None):
    '''If post=none, adds new post and commits to db, otherwise updates existing post. Returns false if required fields are None'''
    if not title:
        flash("Title required!")
        return False

    if post:
        post.title = title
        post.content = content
        post.last_edit_time = datetime.datetime.now()
    else:
        post = Post(title=title,
                    content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()
    return True


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


############################################################################
#  USER ROUTES
############################################################################

@app.route('/users')
def home_route():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user-list.html', users=users)


@app.route('/users/<int:uid>')
def user(uid):
    user = User.query.get_or_404(uid)
    return render_template('user.html', user=user)


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        return render_template('user-form.html', user=NULL_USER, type="new")
    if request.method == 'POST':

        if not add_edit_user(first_name=request.form['first-name'], last_name=request.form['last-name'], image_url=request.form['image-url']):
            return redirect('/users/new')

        return redirect(f'/users')


@app.route('/users/<int:uid>/edit', methods=['GET', 'POST'])
def edit_user(uid):
    user = User.query.get_or_404(uid)
    if request.method == 'GET':
        return render_template('user-form.html', user=user, type="edit")
    if request.method == 'POST':

        if not add_edit_user(first_name=request.form['first-name'], last_name=request.form['last-name'], image_url=request.form['image-url'], user=user):
            return redirect('/users/{uid}/edit')

        return redirect(f'/users')


@app.route('/users/<int:uid>/delete', methods=['POST'])
def delete_user(uid):
    user = User.query.get_or_404(uid)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

############################################################################
#  POST ROUTES
############################################################################


@app.route('/posts/<int:pid>')
def show_post(pid):
    post = Post.query.get_or_404(pid)
    return render_template('post.html', post=post)


@app.route('/users/<uid>/posts/new', methods=['GET', 'POST'])
def new_post(uid):
    user = User.query.get_or_404(uid)
    if request.method == 'GET':
        return render_template('post-form.html', user=user, post=NULL_POST, type="new")
    if request.method == 'POST':

        if not add_edit_post(title=request.form['title'], content=request.form['content'], user_id=uid):
            return redirect(f'/users/{uid}/posts/new')

        return redirect(f'/users/{uid}')


@app.route('/posts/<int:pid>/edit', methods=['GET', 'POST'])
def edit_post(pid):
    post = Post.query.get_or_404(pid)
    if request.method == 'GET':
        return render_template('post-form.html', user=post.user, post=post, type="edit")
    if request.method == 'POST':

        if not add_edit_post(title=request.form['title'], content=request.form['content'], user_id=post.user_id, post=post):
            return redirect(f'/posts/{pid}/edit')

        return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:pid>/delete', methods=['POST'])
def delete_post(pid):
    post = Post.query.get_or_404(pid)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')
