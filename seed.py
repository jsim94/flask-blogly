from models import db, User, Post

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add pets
users = [
    User(first_name='Aang',
         last_name='Avatar', image_url='https://miro.medium.com/max/1400/0*3xTjr7rYOjGYjKqi.jpg'),
    User(first_name='Michael',
         last_name='Jackson', image_url='https://zipmex.com/static/d1af016df3c4adadee8d863e54e82331/1bbe7/Twitter-NFT-profile.jpg'),
    User(first_name='Peter',
         last_name='Parker', image_url='https://artprojectsforkids.org/wp-content/uploads/2021/05/How-to-Draw-Spiderman.jpg.webp')
]
posts = []

# Add new objects to session, so they'll persist
db.session.add_all(users)
# db.session.add_all(posts)

# Commit--otherwise, this never gets saved!
db.session.commit()
