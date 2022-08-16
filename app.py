"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def home():
    return redirect('/users')


@app.route('/users')
def home_route():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user-list.html', users=users)


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        null_user = {'first_name': '', 'last_name': '', 'image_url': ''}
        return render_template('user-form.html', user=null_user, type="new")
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        image_url = request.form['image-url']
        new_user = User(first_name=first_name,
                        last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect(f'/users')


@app.route('/users/<int:uid>')
def user(uid):
    user = User.query.get_or_404(uid)
    return render_template('user.html', user=user)


@app.route('/users/<int:uid>/edit', methods=['GET', 'POST'])
def edit_user(uid):
    user = User.query.get_or_404(uid)
    if request.method == 'GET':
        return render_template('user-form.html', user=user, type="edit")
    if request.method == 'POST':
        user.first_name = request.form['first-name']
        user.last_name = request.form['last-name']
        user.image_url = request.form['image-url']
        db.session.add(user)
        db.session.commit()
        return redirect(f'/users')


@app.route('/users/<int:uid>/delete', methods=['POST'])
def delete_user(uid):
    user = User.query.get_or_404(uid)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')
