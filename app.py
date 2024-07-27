# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, jsonify, request, abort, redirect
from models import setup_db, History, Book, db
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

    @app.route("/api/v1.0/histories")
    @requires_auth('get:histories')
    def get_all_histories():
        selection = History.query.order_by(History.id).all()
        result = paginate_item(request, selection)
        return result

    @app.route("/api/v1.0/histories/<int:history_id>")
    @requires_auth('get:histories')
    def get_history(history_id):
        item = History.query.filter(History.id == history_id).one_or_none()
        if item is None:
            abort(404)
        else:
            return jsonify(
                {
                    "success": True,
                    "item": item.format()
                }
            )

    @app.route("/api/v1.0/histories", methods=["POST"])
    @requires_auth('post:histories')
    def create_histories():
        body = request.get_json()

        new_content = body.get("content", None)
        new_fromPage = body.get("fromPage", None)
        new_toPage = body.get("toPage", None)
        new_tag = body.get("tag", None)
        new_createDate = body.get("createDate", None)
        new_book_ids = body.get("book_ids", None)

        item = History(content= new_content, fromPage=new_fromPage, toPage=new_toPage, tag=new_tag, createDate=new_createDate)

        if not new_book_ids is None:
            for book_id in new_book_ids:
                book = Book.query.get(book_id)
                if not book is None:
                    item.books.append(book)
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

    @app.route("/api/v1.0/histories/<int:history_id>", methods=["DELETE"])
    @requires_auth('delete:histories')
    def delete_history(history_id):
        item = History.query.filter(History.id == history_id).one_or_none()
        if item is None:
            abort(404)
        item.delete()

        return jsonify(
            {
                "item": item.format(),
                "success": True,
            }
        )

    @app.route("/api/v1.0/histories/<int:history_id>", methods=["PATCH"])
    @requires_auth('patch:histories')
    def edit_history( history_id):
        body = request.get_json()

        new_content = body.get("content", None)
        new_fromPage = body.get("fromPage", None)
        new_toPage = body.get("toPage", None)
        new_tag = body.get("tag", None)
        new_createDate = body.get("createDate", None)
        new_book_ids = body.get("book_ids", None)

        try:
            item = History.query.get(history_id)
            item.content = new_content
            item.fromPage = new_fromPage
            item.toPage = new_toPage
            item.tag = new_tag
            item.createDate = new_createDate
            if not new_book_ids is None:
                item.books.clear()
                for book_id in new_book_ids:
                    book = Book.query.get(book_id)
                    item.books.append(book)
            db.session.commit()
            return jsonify(
                {
                    "item": item.format(),
                    "success": True,
                }
            )

        except:
            abort(422)

    @app.route("/api/v1.0/books")
    @requires_auth('get:books')
    def get_all_books():
        selection = Book.query.order_by(Book.id).all()
        result = paginate_item(request, selection)
        return result

    @app.route("/api/v1.0/books/<int:book_id>")
    @requires_auth('get:books')
    def get_book(book_id):
        item = Book.query.filter(Book.id == book_id).one_or_none()
        if item is None:
            abort(404)
        else:
            return jsonify(
                {
                    "success": True,
                    "item": item.format()
                }
            )

    @app.route("/api/v1.0/books", methods=["POST"])
    @requires_auth('post:books')
    def create_books():
        body = request.get_json()

        new_name = body.get("name", None)
        new_author = body.get("author", None)
        new_numberOfPages = body.get("numberOfPages", None)
        new_photo = body.get("photo", None)
        new_createDate = body.get("createDate", None)
        new_history_ids = body.get("history_ids", None)
        book = Book(name=new_name, author=new_author, numberOfPages=new_numberOfPages, photo=new_photo, createDate=new_createDate)

        if not new_history_ids is None:
            for history_id in new_history_ids:
                history = History.query.get(history_id)
                if history is None:
                    abort(404)
                else:
                    book.histories.append(history)

        db.session.add(book)
        db.session.commit()

        return jsonify(
            {
                "item": book.format(),
                "success": True,
            }
        )

    @app.route("/api/v1.0/books/<int:book_id>", methods=["DELETE"])
    @requires_auth('delete:books')
    def delete_book(book_id):
        item = Book.query.filter(Book.id == book_id).one_or_none()
        if item is None:
            abort(404)
        item.delete()

        return jsonify(
            {
                "item": item.format(),
                "success": True,
            }
        )

    @app.route("/api/v1.0/books/<int:book_id>", methods=["PATCH"])
    @requires_auth('patch:books')
    def edit_book(book_id):
        body = request.get_json()

        new_name = body.get("name", None)
        new_author = body.get("author", None)
        new_numberOfPages = body.get("numberOfPages", None)
        new_photo = body.get("photo", None)
        new_createDate = body.get("createDate", None)
        new_history_ids = body.get("history_ids", None)

        try:
            item = Book.query.get(book_id)
            item.name = new_name
            item.author = new_author
            item.numberOfPages = new_numberOfPages
            item.photo = new_photo
            item.createDate = new_createDate
            if not new_history_ids is None:
                item.histories.clear()
                for history_id in new_history_ids:
                    history = History.query.get(history_id)
                    if not history is None:
                        item.histories.append(history)
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
