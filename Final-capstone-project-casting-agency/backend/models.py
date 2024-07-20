from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

def setup_db(app):
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.app = app
    db.init_app(app)
    Migrate(app, db)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.isoformat()
        }
    

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Actor {self.name}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'date of birth': self.dob.isoformat(),
            'gender': self.gender
        }
