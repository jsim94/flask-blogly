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

    @staticmethod
    def add(first_name, last_name, image_url):
        new_user = User(first_name=first_name,
                        last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def update(self, first_name, last_name, image_url):
        '''If user=none, adds new user and commits to db, otherwise updates existing user.'''

        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

        db.session.add(self)
        db.session.commit()
        return self


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

    def get_clean_create_date(self):
        return self.created_at.strftime('%b %d, %Y')

    def get_clean_last_edit(self):
        return self.last_edit_time.strftime('%b %d, %Y')

    clean_date = property(get_clean_create_date)
    clean_last_edit = property(get_clean_last_edit)

    def set_tags(self, tag_list):
        self.tags = Tag.query.filter(Tag.name.in_(tag_list)).all()
        return self

    @staticmethod
    def add(title, content, user_id, tag_list):
        new_post = Post(title=title, content=content, user_id=user_id)
        new_post.set_tags(tag_list=tag_list)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    def update(self, title, content, tag_list):
        self.title = title
        self.content = content
        self.last_edit_time = datetime.datetime.now()
        self.set_tags(tag_list=tag_list)

        db.session.add(self)
        db.session.commit()
        return self


class Tag(db.Model):

    __tablename__ = "tags"

    name = db.Column(db.String(50), primary_key=True, nullable=False)
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

    def add(name):
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

    def update(self, name):
        self.name = name
        db.session.add(self)
        db.session.commit()
        return self


class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"),
                        primary_key=True, )
    tag_id = db.Column(db.String(50), db.ForeignKey("tags.name"),
                       primary_key=True,)
