import unittest
import json
from app import app, db
from models import setup_db, Movie, Actor

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "casting_agency"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.create_all()
        
        self.new_movie = {
            "title": "New Movie",
            "release_date": "2024-07-20"
        }
        
        self.update_movie_data = {
            "title": "Updated Movie",
            "release_date": "2024-08-20"
        }

        self.new_actor = {
            "name": "John Doe",
            "dob": "1990-01-01",
            "gender": "Male"
        }
        
        self.update_actor_data = {
            "name": "Jane Doe",
            "dob": "1991-01-01",
            "gender": "Female"
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_create_movie(self):
        """Test creating a new movie"""
        res = self.client().post('/casting_agency/v1.0/movies', 
                                  headers={"Authorization": "Bearer YOUR_TOKEN_HERE"}, 
                                  json=self.new_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['title'], self.new_movie['title'])
    
    def test_update_movie(self):
        """Test updating an existing movie"""
        res = self.client().post('/casting_agency/v1.0/movies', 
                                  headers={"Authorization": "Bearer YOUR_TOKEN_HERE"}, 
                                  json=self.new_movie)
        movie_id = json.loads(res.data)['id']
        
        res = self.client().patch(f'/casting_agency/v1.0/movies/{movie_id}', 
                                  headers={"Authorization": "Bearer YOUR_TOKEN_HERE"}, 
                                  json=self.update_movie_data)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['title'], self.update_movie_data['title'])

    def test_delete_movie(self):
        """Test deleting an existing movie"""
        res = self.client().post('/casting_agency/v1.0/movies', 
                                  headers={"Authorization": "Bearer YOUR_TOKEN_HERE"}, 
                                  json=self.new_movie)
        movie_id = json.loads(res.data)['id']
        
        res = self.client().delete(f'/casting_agency/v1.0/movies/{movie_id}', 
                                   headers={"Authorization": "Bearer YOUR_TOKEN_HERE"})
        
        self.assertEqual(res.status_code, 204)

    def test_create_actor(self):
        """Test creating a new actor"""
        res = self.client().post('/casting_agency/v1.0/actors', 
                                  headers={"Authorization": "Bearer YOUR_TOKEN_HERE"}, 
                                  json=self.new_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['name'], self.new_actor['name'])
    
    def test_update_actor(self):
        """Test updating an existing actor"""
        res = self.client().post('/casting_agency/v1.0/actors', 
                                  headers={"Authorization": "Bearer YOUR_TOKEN_HERE"}, 
                                  json=self.new_actor)
        actor_id = json.loads(res.data)['id']
        
        res = self.client().patch(f'/casting_agency/v1.0/actors/{actor_id}', 
                                  headers={"Authorization": "Bearer YOUR_TOKEN_HERE"}, 
                                  json=self.update_actor_data)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor']['name'], self.update_actor_data['name'])

    def test_delete_actor(self):
        """Test deleting an existing actor"""
        res = self.client().post('/casting_agency/v1.0/actors', 
                                  headers={"Authorization": "Bearer YOUR_TOKEN_HERE"}, 
                                  json=self.new_actor)
        actor_id = json.loads(res.data)['id']
        
        res = self.client().delete(f'/casting_agency/v1.0/actors/{actor_id}', 
                                   headers={"Authorization": "Bearer YOUR_TOKEN_HERE"})
        
        self.assertEqual(res.status_code, 204)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
