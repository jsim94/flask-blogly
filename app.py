"""Blogly application."""
import datetime
from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post, Tag
import validations as validate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ahdlkhawkedhwa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

NULL_USER = {'first_name': '', 'last_name': '', 'image_url': ''}
NULL_POST = {'title': '', 'content': ''}
NULL_TAG = {'name': ''}

############################################################################
#  HOME ROUTES
############################################################################


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('posts/list.html', posts=posts)


############################################################################
#  USER ROUTES
############################################################################

@app.route('/users')
def home_route():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/list.html', users=users)


@app.route('/users/<int:uid>')
def user(uid):
    user = User.query.get_or_404(uid)
    return render_template('users/user.html', user=user)


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        return render_template('users/form.html', user=NULL_USER, type="new")
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        image_url = request.form['image-url']

        msg = validate.user_input(first_name, last_name)
        if msg:
            flash(msg)
            return redirect('/users/new')

        User.add(first_name=first_name,
                 last_name=last_name, image_url=image_url)
        return redirect(f'/users')


@app.route('/users/<int:uid>/edit', methods=['GET', 'POST'])
def edit_user(uid):
    user = User.query.get_or_404(uid)
    if request.method == 'GET':
        return render_template('users/form.html', user=user, type="edit")
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        image_url = request.form['image-url']

        msg = validate.user_input(first_name, last_name)
        if msg:
            flash(msg)
            return redirect(f'/users/{uid}/edit')

        user.update(first_name=first_name,
                    last_name=last_name, image_url=image_url)

        return redirect(f'/users/{uid}')


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
    return render_template('posts/post.html', post=post)


@app.route('/users/<uid>/posts/new', methods=['GET', 'POST'])
def new_post(uid):
    user = User.query.get_or_404(uid)
    tags = Tag.query.all()
    if request.method == 'GET':
        return render_template('posts/form.html', user=user, post=NULL_POST, tags=tags, tag_list=[], type="new")
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tag_list = request.form.getlist('tags')

        msg = validate.post_input(title=title)
        if msg:
            flash(msg)
            return redirect(f'/users/{uid}/posts/new')

        Post.add(title=title,
                 content=content, user_id=uid, tag_list=tag_list)

        return redirect(f'/users/{uid}')


@app.route('/posts/<int:pid>/edit', methods=['GET', 'POST'])
def edit_post(pid):
    post = Post.query.get_or_404(pid)
    tags = Tag.query.all()
    if request.method == 'GET':
        return render_template('posts/form.html', user=post.user, post=post, tags=tags, tag_list=post.tags, type="edit")
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tag_list = request.form.getlist('tags')

        msg = validate.post_input(title=title)
        if msg:
            flash(msg)
            return redirect(f'/posts/{post.user_id}/edit/posts/new')

        post.update(title=title, content=content, tag_list=tag_list)

        return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:pid>/delete', methods=['POST'])
def delete_post(pid):
    post = Post.query.get_or_404(pid)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


############################################################################
#  TAG ROUTES
############################################################################

@app.route('/tags')
def show_tags_list():
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)


@app.route('/tags/<tid>')
def show_tag(tid):
    tag = Tag.query.get_or_404(tid)
    return render_template('tags/tag.html', tag=tag)


@app.route('/tags/new', methods=['GET', 'POST'])
def new_tag():
    if request.method == 'GET':
        return render_template('tags/form.html', tag=NULL_TAG, type="new")
    if request.method == 'POST':
        name = request.form['name']

        msg = validate.tag_input(name=name)
        if msg:
            flash(msg)
            return redirect(f'/tags/new')

        Tag.add(name=name)

        return redirect(f'/tags')


@app.route('/tags/<tid>/edit', methods=['GET', 'POST'])
def edit_tag(tid):
    tag = Tag.query.get_or_404(tid)
    if request.method == 'GET':
        return render_template('tags/form.html', tag=tag, type="edit")
    if request.method == 'POST':
        name = request.form['name']

        msg = validate.tag_input(name=name)
        if msg:
            flash(msg)
            return redirect(f'/tags/new')

        tag.update(name=name)

        return redirect(f'/tags/{tag.id}')


@app.route('/tags/<tid>/delete', methods=['POST'])
def delete_tag(tid):
    tag = Tag.query.get_or_404(tid)
    db.session.delete(tag)
    db.session.commit()
    return redirect(f'/tags')
