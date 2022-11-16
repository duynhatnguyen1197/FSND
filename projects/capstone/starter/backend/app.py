import os
import json
from sqlalchemy import exc
from flask import Flask ,request,jsonify,abort
from flask_cors import CORS
from models import setup_db,Movie,Actor,Cast
from auth.auth import AuthError, requires_auth
def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    @requires_auth('get:data')
    def home(jwt):
        movies = Movie.query.all()
        result = []
        print("Hello")
        for movie in movies:
            actors_in_movie = []
            for cast in movie.casts:
                actor = Actor.query.get(cast.actor_id)
                if actor is None:
                    continue
                else:
                    actors_in_movie.append(actor.name)
            movie_result_view = {
                'id':movie.id,
                'title':movie.title,
                'release':movie.release_date,
                'actors':actors_in_movie
            }
            result.append(movie_result_view)
        
        return  jsonify({
                'success':True,
                'result':result
            })

   

    @app.route('/movie/<int:id>/',methods=['DELETE'])
    @requires_auth('modify:movie')
    def delete_movie(jwt,id):
        try:
            movie = Movie.query.get(id)
            casts = Cast.query.filter_by(movie_id=id)
            if movie is None:
                abort(400)
            if casts is not None:
                casts.delete()
            movie_name = movie.name
            movie.delete()
            return jsonify({
                "success": True,
                "delete": id,
                "movie":movie_name
            })
        except exc.SQLAlchemyError as e:
            return jsonify({
                "message": str(e),
                "error": True
            })
    
    @app.route('/actor/<int:id>/',methods=['DELETE'])
    @requires_auth('modify:actor')
    def delete_actor(jwt,id):
        try:
            actor = Actor.query.get(id)
            casts = Cast.query.filter_by(actor_id=id)
            if actor is None:
                abort(400)
            if casts is not None:
                casts.delete()
            actor_name = actor.name
            actor.delete()
            return jsonify({
                "success": True,
                "delete":id,
                "actor":actor_name
            })
        except exc.SQLAlchemyError as e:
            return jsonify({
                "message": str(e),
                "error": True
            })
    
    @app.route('/actor',methods=['POST'])
    @requires_auth('modify:actor')
    def create_actor(jwt):
        try:
            receive_data = json.loads(request.data.decode('utf-8'))
            movie_title = receive_data['movie']
            actor = Actor(
                name=receive_data['name'], 
                age=receive_data['age'],
                gender=receive_data['gender']
            )
            actor.insert()
            if movie_title :
                movie = Movie.query.filter_by(title = movie_title).first()
                if movie is not None:
                    cast = Cast(
                        movie_id = movie.id,
                        actor_id = actor.id
                    )
                    cast.insert()
            return jsonify({
                "success": True,
                "actor": actor.format()
            })
        except exc.SQLAlchemyError as e:
            return jsonify({
                "message": str(e),
                "error": True
            })
    
    @app.route('/movie',methods=['POST'])
    @requires_auth('modify:movie')
    def create_movie(jwt):
        try:
            receive_data = json.loads(request.data.decode('utf-8'))
            actors = receive_data['actors']
            movie = Movie(
                title=receive_data['title'], 
                release_date=receive_data['release_date']
            )
            movie.insert()
            if actors :
                 assign_actor_to_movie(actors,movie)

            return jsonify({
                "success": True,
                "movie": movie.format()
            })
        except exc.SQLAlchemyError as e:
            return jsonify({
                "message": str(e),
                "error": True
            })
    
    def assign_actor_to_movie(actors,movie):
        for a in actors:
            actor = Actor.query.filter_by(name=a).first()
            if actor is not None :
               cast = Cast.query.filter_by(movie_id= movie.id).filter_by(actor_id=actor.id).first()
               if cast is None:
                   cast = Cast(
                       movie_id = movie.id,
                       actor_id = actor.id
                   )
                   cast.insert()


    def remove_actor_from_movie(actors,movie):
        for a in actors:
            actor = Actor.query.filter_by(name=a).first()
            if actor is not None :
                cast = Cast.query.filter_by(movie_id= movie.id).filter_by(actor_id=actor.id).first()
                if cast is  not None:
                    cast.delete()
        

    @app.route('/actor/<int:actor_id>/',methods=['PATCH'])
    @requires_auth('patch:data')
    def edit_actor(jwt,actor_id):
        try:
            actor = Actor.query.get(actor_id)
            if actor is None:
                abort(400)
            else:
                receive_data = json.loads(request.data.decode('utf-8'))
                update_actor = Actor(
                name=receive_data['name'], 
                age=receive_data['age'],
                gender=receive_data['gender']
                )
                if update_actor.name:
                    actor.name = update_actor.name
                if update_actor.age:
                    actor.age = update_actor.age
                if update_actor.gender:
                    actor.gender = update_actor.gender
                
                actor.update()
                
            return jsonify({
                "success": True,
                "actor": actor.format()
            })
        except exc.SQLAlchemyError as e:
            return jsonify({
                "message": str(e),
                "error": True
            })
            
    @app.route('/movie/<int:movie_id>/',methods=['PATCH'])
    @requires_auth('patch:data')
    def edit_movie(jwt,movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if movie is None:
                abort(400)
            else:
                receive_data = json.loads(request.data.decode('utf-8'))
                add_actors = receive_data['add_actors']
                remove_actors = receive_data['remove_actors']
                update_movie = Movie(
                title=receive_data['title'], 
                release_date=receive_data['release_date']
                )
                if update_movie.title:
                    movie.title = update_movie.title
                if update_movie.release_date:
                    movie.release_date = update_movie.release_date
                movie.update()
                if add_actors:
                    assign_actor_to_movie(add_actors,movie)
                if remove_actors:
                   remove_actor_from_movie(remove_actors,movie)

                
            return jsonify({
                "success": True,
                "actor": movie.format()
            })
        except exc.SQLAlchemyError as e:
            print(e)
            return jsonify({
                "message": str(e),
                "error": True
            })

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
