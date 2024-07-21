import unittest
import json

from settings import DB_NAME_TEST, DB_USER, DB_PASSWORD

from app import create_app
from models import create_data_test

TOKEN_CASTING_ASSISTANT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikc5XzVrU1lmZjJ3SW8wR1R6cFV5OSJ9.eyJpc3MiOiJodHRwczovL2Rldi12ZXJtb3JpYy5qcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjY3ZDdhNTVkY2JjN2E5MzE4NDA4MDdkIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTcxOTY1NjczMSwiZXhwIjoxNzE5NjYzOTMxLCJzY29wZSI6IiIsImF6cCI6ImxKU3N6YUgyNU0zTXYyUVpxYm5pTzhwWVBueGVTVk1PIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.XdYuDtRVRhXcD4UWRrM5lB2A7S8aHVzGYtBiV6mA0VmrBbUHeQj3e6KLlpoq-BEL3UW666sxSxW-7tD_378QR7H2yUxmFd5fSRijHtc4TBbwNUV77mYl3VrNZEcjDvrKKJcFKPfXdOKPI1CXSGD35GvKEI3Yj7TcYf2TrFlJaDJUOf7sGzQPNgZHVrT0Fprck20MZ5fqoRLsAdxKmf-CqN3Gps0ITBkvu-WPn2DH8df6FBW0UYqDuxEwXgDFZgwHRr-ThYNFykAZOd5u6kOO4rz6jBVnJXtAKiCXrxmbMZbl7VKIyr58EmOITv07mh373S4zSBXhqDjno7frPFmbig"
TOKEN_CASTING_DIRECTOR = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikc5XzVrU1lmZjJ3SW8wR1R6cFV5OSJ9.eyJpc3MiOiJodHRwczovL2Rldi12ZXJtb3JpYy5qcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjY3ZTMwYWRkY2JjN2E5MzE4NDBjZTQ5IiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTcxOTY1NzQzNiwiZXhwIjoxNzE5NjY0NjM2LCJzY29wZSI6IiIsImF6cCI6ImxKU3N6YUgyNU0zTXYyUVpxYm5pTzhwWVBueGVTVk1PIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.Pnq7RnQD8d7hM9jsSaNeyvsUkzikgRLVwmlS873Opv7yWlynrjNeQtfjojKFMNWs6zfzsZBPns6xJlenHUwTT8Q4NLyOJMTLGtV8dg8IO4LHqn529Lui0zTOtzAsVrwBXkSnOxWPLk4ZSfaDa1zlD6jvWTgXTgGJ_h8qIURfdWltgVaquSvoQOnBjHxps5MNUWtFqB9fU23oo14M0hIdHhgmE_rC-JS9e9JX_9QaTMy-ZAOJ_ms6WWy6ZTfROgnuZZeZAGNASQYG-D_00a9y8kKHN4ZL4IpiUk0xVRaQsJxaShjd7qdn_nMJYGkFneUlrydhWW1acvO72ac9gzdD0A"
TOKEN_EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikc5XzVrU1lmZjJ3SW8wR1R6cFV5OSJ9.eyJpc3MiOiJodHRwczovL2Rldi12ZXJtb3JpYy5qcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjY3ZTM3NWYyODQ2MzYwMTQ1MjdlNjMwIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTcxOTY1NTYxNCwiZXhwIjoxNzE5NjYyODE0LCJzY29wZSI6IiIsImF6cCI6ImxKU3N6YUgyNU0zTXYyUVpxYm5pTzhwWVBueGVTVk1PIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.R7GBr8k4MyhVcP-mr_9jbr96PnQiSFrwdT3D2KiiqRjffj-2iA6RID-7j2FUeg4j6Eh-TIPrNErc7U33tNJWd7cLgRncrhRTStQCpyPCPbYj6ybMsHgNrk3Y0zaBU4PkBmvRuadxk2MVY1Ke2sz-Zb-4t7_IUIIQyveJPrD93-uZ2V5NJuGpT9eSEaVhmDa7rDr_T4LSTATO2Fz01_NGiroo2Ntf7l6qjww1ySKAjSokkTD6QsSxBRhFWc8uOlnyAgU-LuKsVp9rrACftWeeFIIm1fNBLA8K7JDGy_MIB1JF7EKwl5IIX88kXebgGQ0X4ou2MIiak8BZWfMEEeV94w'


HEADERS_ROLE_CASTING_ASSISTANT = {
    "Authorization": f"Bearer {TOKEN_CASTING_ASSISTANT}",
    "Content-Type": "application/json"
}

HEADERS_ROLE_CASTING_DIRECTOR = {
    "Authorization": f"Bearer {TOKEN_CASTING_DIRECTOR}",
    "Content-Type": "application/json"
}

HEADERS_ROLE_EXECUTIVE_PRODUCER = {
    "Authorization": f"Bearer {TOKEN_EXECUTIVE_PRODUCER}",
    "Content-Type": "application/json"
}


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = DB_NAME_TEST
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, 'localhost:5432',
                                                               self.database_name)

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
        create_data_test()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # region test actor

    def test_get_all_actors(self):
        res = self.client().get("/api/v1.0/actors", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["items"])

    def test_get_actors(self):
        res = self.client().get("/api/v1.0/actors/1", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_get_actors_404(self):
        res = self.client().get("/api/v1.0/actors/10000", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_create_actors(self):
        res = self.client().post("/api/v1.0/actors", json={
            "name": "Mori",
            "age": 40,
            "gender": 1,
            "movie_ids": [2]
        }, headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_create_actors_404(self):
        res = self.client().post("/api/v1.0/actors", json={
            "name": "Mori",
            "age": 40,
            "gender": 1,
            "movie_ids": [20000]
        }, headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_actors(self):
        res = self.client().delete("/api/v1.0/actors/1", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_delete_actors_404(self):
        res = self.client().delete("/api/v1.0/actors/100000", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_edit_actors(self):
        res = self.client().patch("/api/v1.0/actors/1", json={
            "name": "Tom 1",
            "age": 4,
            "gender": 2,
            "movie_ids": [2]
        }, headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_edit_actors_404(self):
        res = self.client().patch("/api/v1.0/actors/1000", json={
            "name": "Tom 1",
            "age": 4,
            "gender": 2,
            "movie_ids": [2]
        }, headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

    # endregion

    # region test movie

    def test_get_all_movies(self):
        res = self.client().get("/api/v1.0/movies", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["items"])

    def test_get_movies(self):
        res = self.client().get("/api/v1.0/movies/1", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_get_movies_404(self):
        res = self.client().get("/api/v1.0/movies/10000", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_create_movies(self):
        res = self.client().post("/api/v1.0/movies", json={
            "title": "Inuyasha",
            "release_date": "06/27/2025 18:31:00"
        }, headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_create_movies_404(self):
        res = self.client().post("/api/v1.0/movies", json={
            "title": "Inuyasha 11",
            "release_date": "06/26/2024 18:31:00",
            "actor_ids": [100000]
        }, headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movies(self):
        res = self.client().delete("/api/v1.0/movies/1", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_delete_movies_404(self):
        res = self.client().delete("/api/v1.0/movies/100000", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_edit_movies(self):
        res = self.client().patch("/api/v1.0/movies/1", json={
            "title": "Thám tử Home 6",
            "release_date": "06/26/2024 18:31:00",
            "actor_ids": [3]
        }, headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_edit_movies_404(self):
        res = self.client().patch("/api/v1.0/movies/1000", json={
            "name": "Tom 1",
            "age": 4,
            "gender": 2,
            "movie_ids": [2]
        }, headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

     # endregion

    # region test RBAC
    def test_get_actors_role_casting_assistant(self):
        res = self.client().get("/api/v1.0/actors/1", headers=HEADERS_ROLE_CASTING_ASSISTANT)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_create_actors_role_casting_assistant_403(self):
        res = self.client().post("/api/v1.0/actors", json={
            "name": "Mori",
            "age": 40,
            "gender": 1,
            "movie_ids": [2]
        }, headers=HEADERS_ROLE_CASTING_ASSISTANT)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])

    def test_create_actors_role_casting_director(self):
        res = self.client().post("/api/v1.0/actors", json={
            "name": "Mori",
            "age": 40,
            "gender": 1,
            "movie_ids": [2]
        }, headers=HEADERS_ROLE_CASTING_DIRECTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_delete_movie_role_casting_director_403(self):
        res = self.client().delete("/api/v1.0/movies/1", headers=HEADERS_ROLE_CASTING_DIRECTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])

    def test_delete_movie_role_executive_producer(self):
        res = self.client().delete("/api/v1.0/movies/1", headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    def test_create_movie_role_executive_producer(self):
        res = self.client().post("/api/v1.0/movies", json={
            "title": "Inuyasha",
            "release_date": "06/27/2025 18:31:00"
        }, headers=HEADERS_ROLE_EXECUTIVE_PRODUCER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["item"])

    # endregion


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
