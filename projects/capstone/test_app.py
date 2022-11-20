
from email import header
import os
from unicodedata import name
import unittest
import json
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db,Movie,Actor,Cast

load_dotenv()
database_path = os.environ.get('DATABASE_URL')
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)
producer_jwt = os.environ.get('producer_jwt')
director_jwt = os.environ.get('director_jwt')
assistant_jwt = os.environ.get('assistant_jwt')
print(producer_jwt)

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    ###_________ ACTOR TEST _____________

    def test_create_actor(self):
        movie = Movie.query.first()
        actor = {
            "name":"Test",
            "gender":"Male",
            "age":100,
            "movie":movie.id
        }
        res = self.client().post("/actor",json=actor,headers={
              'Authorization': producer_jwt,
           })
        res1 = self.client().post("/actor",json=actor,headers={
              'Authorization': producer_jwt,
           })
        res2 = self.client().post("/actor",json=actor,headers={
              'Authorization': producer_jwt,
           })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["actor"])

    def test_create_actor_fail(self):
        actor = {
            "name":"",
            "gender":"Male",
            "age":100,
            "movie":""
        }
        res = self.client().post("/actor",json=actor,headers={
              'Authorization': producer_jwt,
           })
        self.assertEqual(res.status_code, 400)
    
    def test_edit_actor(self):
        update_actor = {
            "name":"Test",
            "gender":"Male",
            "age":100,
            "movie":""
        }
        actor = Actor.query.first()
        res = self.client().patch(f'/actor/{actor.id}/',json=update_actor,headers={
              'Authorization': producer_jwt,
           })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["actor"])

        
        
    
    def test_edit_actor_fail(self):
        actor = {
            "name":"Test",
            "gender":"Male",
            "age":100,
            "movie":""
        }
        res = self.client().patch("/actor/10000/",json=actor,headers={
              'Authorization': producer_jwt,
           })
        self.assertEqual(res.status_code, 404)
    
    def test_delete_actor(self):
        actor = Actor.query.first()
        res = self.client().delete(f'/actor/{actor.id}/',headers={
              'Authorization': producer_jwt,
           })
        self.assertEqual(res.status_code, 200)
    
    def test_delete_actor_fail(self):
        res = self.client().delete("/actor/22345/",headers={
              'Authorization': producer_jwt,
           })
        self.assertEqual(res.status_code, 404)


    ###_________ MOVIE TEST _____________

    def test_create_movie(self):
        movie = {
            "title":"Hot Test",
            "release_date":"3/21/2022",
            "actors":[]
        }
        res = self.client().post("/movie",json=movie,headers={
              'Authorization': producer_jwt,
           })
        res2 = self.client().post("/movie",json=movie,headers={
              'Authorization': producer_jwt,
           })
        res3 = self.client().post("/movie",json=movie,headers={
              'Authorization': producer_jwt,
           })
        res4 = self.client().post("/movie",json=movie,headers={
              'Authorization': producer_jwt,
           })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["movie"])

    def test_create_movie_fail(self):
        movie = {
            "title":"",
            "release_date":"3/21/2022",
            "actors":[]
        }
        res = self.client().post("/movie",json=movie,headers={
              'Authorization': producer_jwt,
           })
        self.assertEqual(res.status_code, 400)

    def test_edit_movie(self):
        update_movie = {
            "title":"Hot Test",
            "release_date":"3/21/2022",
            "add_actors":[],
            "remove_actors":[]
        }
        movie = Movie.query.first()
        res = self.client().patch(f'/movie/{movie.id}/',json=update_movie,headers={
              'Authorization': producer_jwt,
           })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["movie"])
    
    def test_edit_movie_fail(self):
        movie = {
            "title":"Hot Test",
            "release_date":"3/21/2022",
            "actors":[]
        }
        res = self.client().patch("/movie/1000/",json=movie,headers={
              'Authorization': producer_jwt,
           })
        self.assertEqual(res.status_code, 404)
    
    def test_delete_movie(self):
        movie = Movie.query.first()
        res = self.client().delete(f'/movie/{movie.id}/',headers={
              'Authorization': producer_jwt,
           })
        self.assertEqual(res.status_code, 200)
    
    def test_delete_movie_fail(self):
        res = self.client().delete("/movie/22345/",headers={
              'Authorization': producer_jwt,
           })
        self.assertEqual(res.status_code, 404)
    
    def test_get_data(self):
        res = self.client().get("http://localhost:5000/",headers={
                'Authorization': producer_jwt,
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["result"])
    
    ###_________ JWT TEST _____________

    def test_delete_movie_director(self):
        movie = Movie.query.first()
        res = self.client().delete(f'/movie/{movie.id}/',headers={
              'Authorization': director_jwt,
           })
        self.assertEqual(res.status_code, 403)
    
    def test_delete_actor_assistant(self):
        actor = Actor.query.first()
        res = self.client().delete(f'/movie/{actor.id}/',headers={
              'Authorization': director_jwt,
           })
        self.assertEqual(res.status_code, 403)
    
    
    

    
    
    
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()