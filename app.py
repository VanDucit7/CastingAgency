# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, jsonify, request, abort, redirect
from models import setup_db, Actor, Movie, db
from flask_cors import CORS
from auth import requires_auth, AuthError, URL_LOGIN
from urllib.parse import urlparse, parse_qs

PAGE_SIZE_DEFAULT = 10


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    # ----------------------------------------------------------------------------#
    # Controllers.
    # ----------------------------------------------------------------------------#

    CORS(app)

    def paginate_item(request, selection):
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("pageSize", PAGE_SIZE_DEFAULT, type=int)

        total_items = len(selection)
        total_pages = (total_items + page_size - 1) // page_size

        start = (page - 1) * page_size
        end = start + page_size
        items = [item.format() for item in selection]
        current_items = items[start:end]

        return jsonify(
            {
                "page": page,
                "pageSize": page_size,
                "totalPages": total_pages,
                "totalItems": total_items,
                "items": current_items,
                "success": True,
            }
        )

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/')
    def index():
        return redirect(URL_LOGIN, code=302)

    @app.route('/login-results')
    def login_results():
        # Lấy URL đầy đủ
        full_url = request.url

        # Lấy các thông số từ query string
        access_token = request.args.get('access_token')
        expires_in = request.args.get('expires_in')
        token_type = request.args.get('token_type')
        if access_token is None:
            return '''
                <script>
                    if (window.location.hash) {
                        var fragment = window.location.hash.substring(1);
                        window.location.href = '/login-results?' + fragment;
                    } else {
                        document.body.innerHTML = "No fragment found in URL.";
                    }
                </script>
                '''

        return jsonify({
            "access_token": access_token,
            "expires_in": expires_in,
            "token_type": token_type
        })

    @app.route("/api/v1.0/actors")
    @requires_auth('get:actors')
    def get_all_actors(jwt):
        selection = Actor.query.order_by(Actor.id).all()
        result = paginate_item(request, selection)
        return result

    @app.route("/api/v1.0/actors/<int:actor_id>")
    @requires_auth('get:actors')
    def get_actor(jwt, actor_id):
        item = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if item is None:
            abort(404)
        else:
            return jsonify(
                {
                    "success": True,
                    "item": item.format()
                }
            )

    @app.route("/api/v1.0/actors", methods=["POST"])
    @requires_auth('post:actors')
    def create_actors(jwt):
        body = request.get_json()

        new_name = body.get("name", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)
        movie_ids = body.get("movie_ids", None)

        item = Actor(name=new_name, age=new_age, gender=new_gender)

        if not movie_ids is None:
            for movie_id in movie_ids:
                movie = Movie.query.get(movie_id)
                if not movie is None:
                    item.movies.append(movie)
                else:
                    abort(404)

        db.session.add(item)
        db.session.commit()
        return jsonify(
            {
                "item": item.format(),
                "success": True,
            }
        )

    @app.route("/api/v1.0/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        item = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if item is None:
            abort(404)
        item.delete()

        return jsonify(
            {
                "item": item.format(),
                "success": True,
            }
        )

    @app.route("/api/v1.0/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth('patch:actors')
    def edit_actor(jwt, actor_id):
        body = request.get_json()

        new_name = body.get("name", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)
        movie_ids = body.get("movie_ids", None)

        try:
            item = Actor.query.get(actor_id)
            item.name = new_name
            item.age = new_age
            item.gender = new_gender
            if not movie_ids is None:
                item.movies.clear()
                for movie_id in movie_ids:
                    movie = Movie.query.get(movie_id)
                    item.movies.append(movie)
            db.session.commit()
            return jsonify(
                {
                    "item": item.format(),
                    "success": True,
                }
            )

        except:
            abort(422)

    @app.route("/api/v1.0/movies")
    @requires_auth('get:movies')
    def get_all_movies(jwt):
        selection = Movie.query.order_by(Movie.id).all()
        result = paginate_item(request, selection)
        return result

    @app.route("/api/v1.0/movies/<int:movie_id>")
    @requires_auth('get:movies')
    def get_movie(jwt, movie_id):
        item = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if item is None:
            abort(404)
        else:
            return jsonify(
                {
                    "success": True,
                    "item": item.format()
                }
            )

    @app.route("/api/v1.0/movies", methods=["POST"])
    @requires_auth('post:movies')
    def create_movies(jwt):
        body = request.get_json()

        new_title = body.get("title", None)
        new_release_date = body.get("release_date", None)
        actor_ids = body.get("actor_ids", None)
        movie = Movie(title=new_title, release_date=new_release_date)

        if not actor_ids is None:
            for actor_id in actor_ids:
                actor = Actor.query.get(actor_id)
                if actor is None:
                    abort(404)
                else:
                    movie.actors.append(actor)

        db.session.add(movie)
        db.session.commit()

        return jsonify(
            {
                "item": movie.format(),
                "success": True,
            }
        )

    @app.route("/api/v1.0/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        item = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if item is None:
            abort(404)
        item.delete()

        return jsonify(
            {
                "item": item.format(),
                "success": True,
            }
        )

    @app.route("/api/v1.0/movies/<int:movie_id>", methods=["PATCH"])
    @requires_auth('patch:movies')
    def edit_movie(jwt, movie_id):
        body = request.get_json()

        new_title = body.get("title", None)
        new_release_date = body.get("release_date", None)
        actor_ids = body.get("actor_ids", None)
        try:
            item = Movie.query.get(movie_id)
            item.title = new_title
            item.release_date = new_release_date
            if not actor_ids is None:
                item.actors.clear()
                for actor_id in actor_ids:
                    actor = Actor.query.get(actor_id)
                    if not actor is None:
                        item.actors.append(actor)
            item.update()
            return jsonify(
                {
                    "item": item.format(),
                    "success": True,
                }
            )

        except:
            abort(422)

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }
            ),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 500,
                    "message": "Internal Server Error"
                }
            ),
            500,
        )

    @app.errorhandler(405)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 405,
                    "message": "The method is not allowed for the requested URL"
                }
            ),
            405,
        )

    return app


app = create_app()
# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
