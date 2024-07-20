from authlib.integrations.flask_client import OAuth
from flask import Flask, request, jsonify, abort, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor, db
from auth import init_app, requires_auth, requires_role
from flask_cors import CORS
from config import Config
import logging


# Configure logging
logging.basicConfig(level=logging.DEBUG)

oauth = OAuth()

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
CORS(app)

# Ensure the database is setup correctly
setup_db(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

# Endpoints for the movies
@app.route('/')
def index():
    return "Casting Agency App"

@app.route('/casting_agency/v1.0/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.format() for movie in movies]), 200

@app.route('/casting_agency/v1.0/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    return jsonify(movie.format()), 200

@app.route('/casting_agency/v1.0/movies', methods=['POST'])
@requires_auth('create:movies')
@requires_role('Executive Producer')
def create_movie():
    data = request.get_json()
    title = data.get('title')
    release_date = data.get('release_date')

    if not title or not release_date:
        abort(400, description='Title and release date are required.')

    movie = Movie(title=title, release_date=release_date)
    movie.insert()
    return jsonify(movie.format()), 201

@app.route('/casting_agency/v1.0/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('update:movie')
@requires_role('Executive Producer')
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie is None:
        abort(404, description="Resource not Found")
    try:
        body = request.get_json()
        if 'title' in body:
            movie.title = body['title']
        if 'release_date' in body:
            movie.release_date = body['release_date']
        movie.update()
        return jsonify({'success': True, 'movie': movie.format()})
    except Exception as e:
        db.session.rollback()
        db.session.rollback()
        abort(422, description='Unable to process the request')
    finally:
        db.session.close()

@app.route('/casting_agency/v1.0/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
@requires_role('Executive Producer')
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    movie.delete()
    return '', 204


#Endpoints for the actors

@app.route('/casting_agency/v1.0/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors():
    actors = Actor.query.all()
    return jsonify([actor.format() for actor in actors]), 200

@app.route('/casting_agency/v1.0/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor_by_id(actor_id):
    actor = Actor.query.get(actor_id)
    return jsonify(actor.format()), 200

@app.route('/casting_agency/v1.0/actors', methods=['POST'])
@requires_auth('create:actors')
@requires_role('Casting Director')
def create_actor():
    data = request.get_json()
    name = data.get('name')
    dob = data.get('dob')
    gender = data.get('gender')

    if not name or not dob or not gender:
        abort(400, description='Actor name, dob and gender is required')

    actor = Actor(name=name, dob=dob, gender=gender)
    actor.insert()
    return jsonify(actor.format()), 201

@app.route('/casting_agency/v1.0/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('update:actors')
@requires_role('Casting Director')
def update_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
        abort(404, description="Resource not Found")
    try:
        body = request.get_json()
        if 'name' in body:
            actor.name = body['name']
        if 'dob' in body:
            actor.dob = body['dob']
        if 'gender' in body:
            actor.gender = body['gender']
        
        actor.update()
        return jsonify({'success': True, 'actor': actor.format()})
    
    except Exception as e:
        db.session.rollback()
        db.session.rollback()
        abort(422, description='Unable to process the request')

    finally:
        db.session.close()

@app.route('/casting_agency/v1.0/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
@requires_role('Casting Director')
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    actor.delete()
    return 'Successfully deleted', 204

# Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": error.description
    }), 422

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
