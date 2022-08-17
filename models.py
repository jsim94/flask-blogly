"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    full_name = property(get_full_name)


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    last_edit_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='posts')

    # How to pass an argument to a callback function to combine these two functions into one?
    def get_string_date(self):
        return self.created_at.strftime('%b %d, %Y')

    def get_string_last_edit(self):
        return self.last_edit_time.strftime('%b %d, %Y')

    str_date = property(get_string_date)
    str_last_edit = property(get_string_last_edit)
