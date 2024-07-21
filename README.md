# API Development and Documentation Project

## Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

Display Movies with attributes title and release date
Display Actors with attributes name, age and gender

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL.
- The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application require authentication by Auth0.

### LOGIN 
- accept to url http://127.0.0.1:5000/login-results
- Account: 
  - Email: castingassistant@gmail.com 
  - Pass: Abc@12345
  - Role: Casting Assistant
  
  - Email: CastingDirector@gmail.com
  - Pass: Abc@12345
  - Role: Casting Director
  
  - Email: ExecutiveProducer@gmail.com
  - Pass: Abc@12345
  - Role: Executive Producer

- Result:
```
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikc5XzVrU1lmZjJ3SW8wR1R6cFV5OSJ9.eyJpc3MiOiJodHRwczovL2Rldi12ZXJtb3JpYy5qcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjY3ZTM3NWYyODQ2MzYwMTQ1MjdlNjMwIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTcxOTcxNjkwMCwiZXhwIjoxNzE5NzI0MTAwLCJzY29wZSI6IiIsImF6cCI6ImxKU3N6YUgyNU0zTXYyUVpxYm5pTzhwWVBueGVTVk1PIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.cDpO85ONhqpNqOPeBU5y3uP1qQS8jRA9wBNDMCoKCyx2IpindFxv6jw0qDnYHAWgXp1MGUPi2DdhLqE4uYWUCMdx8W66ynpCdlxts7ImRhYOq54KcWfxP1vUiRJd-n1UTYeTx6tZ7lkeveeqWc8zDJItX8cpFBBt5ga8XLVAJfanzfj_SdadwppujnkgEaJQs9zthLZyShy-5DoYufkcV58caDcxbZSyNUdV-mMGUAkyZWdahk9lm_QJAa46bcb9xl7Tu8yDXjyVzDwxK7qpfiWsM2LgCON_MD_js7Adnn5zR2ZcEydqoPGFyv2VohQfHQcyI51lUJ8NQhXNKiMHfg",
  "expires_in": "7200",
  "token_type": "Bearer"
}
```
with token you must use for call api

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 401: Unauthorized
- 404: Resource Not Found
- 405: The method is not allowed for the requested URL
- 422: Not Processable 
- 500: Internal Server Error

### Endpoints 

### API Actors
#### GET /api/v1.0/actors
- General:
    - Fetches list actors with paging
    - Request Arguments: 
      - page: this number of page. default 1
      - pageSize: number of item in one page. default 10
    - Returns: array actor, page number, page size, total actor in database, total Pages
    - Results are paginated in groups of pageSize. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/api/v1.0/actors?page=1&pageSize=10`

```
  {
    "items": [
        {
            "age": 3,
            "gender": 1,
            "id": 1,
            "movies": [
                {
                    "id": 1,
                    "release_date": "Thu, 27 Jun 2024 18:31:00 GMT",
                    "title": "Tom And Jerry"
                }
            ],
            "name": "Tom"
        },...
    ],
    "page": 1,
    "pageSize": 10,
    "success": true,
    "totalItems": 7,
    "totalPages": 1
  }
```

#### GET /api/v1.0/actors/actor_id
- General:
    - Fetches one actor with actor id
    - Request Arguments: actor id
    - Returns: 
      - item: actor with id, name, age, gender and movies that the actor action
      - success: true or false 
- Sample: `curl http://127.0.0.1:5000/api/v1.0/actors/6`

```
  {
    "item": {
        "age": 7,
        "gender": 1,
        "id": 6,
        "movies": [
            {
                "id": 3,
                "release_date": "Sun, 26 May 2024 10:35:00 GMT",
                "title": "Doreamon"
            }
        ],
        "name": "Doreamon"
    },
    "success": true
  }
```

#### POST /api/v1.0/actors
- General:
    - Creates a new actor.
    - Returns success value.
- Sample: `curl -X POST /api/v1.0/actors`
```
-H "Content-Type: application/json" -d 
{
    "name": "Mori",
    "age": 40,
    "gender": 2,
    "movie_ids": [2]
}
```
- Result:
```
{
    "item": {
        "age": 40,
        "gender": 2,
        "id": 8,
        "movies": [
            {
                "id": 2,
                "release_date": "Sun, 28 Jul 2024 13:09:00 GMT",
                "title": "Conan"
            }
        ],
        "name": "Mori"
    },
    "success": true
}
```

#### DELETE /api/v1.0/actors/<int:actor_id>
- General:
    - Deletes the actors of the given ID if it exists. 
    - Returns success value
- Sample: `curl -X DELETE http://127.0.0.1:5000/api/v1.0/actors/8`
```
{
    "item": {
        "age": 40,
        "gender": 2,
        "id": 8,
        "movies": [
            {
                "id": 2,
                "release_date": "Sun, 28 Jul 2024 13:09:00 GMT",
                "title": "Conan"
            }
        ],
        "name": "Mori"
    },
    "success": true
}
```

#### PATCH /api/v1.0/actors/<int:actor_id>
- General:
    - Edit the actors of the given ID if it exists.
    - Returns success value.
- Sample: `curl -X PATCH http://127.0.0.1:5000/api/v1.0/actors/9`
```
-H "Content-Type: application/json" -d 
{
    "name": "Mori Na",
    "age": 41,
    "gender": 2,
    "movie_ids": [2]
}
```
- Result:
```
{
    "item": {
        "age": 41,
        "gender": 2,
        "id": 9,
        "movies": [
            {
                "id": 2,
                "release_date": "Sun, 28 Jul 2024 13:09:00 GMT",
                "title": "Conan"
            }
        ],
        "name": "Mori Na"
    },
    "success": true
}
```

### End API Actors

### API MOVIES

#### GET /api/v1.0/movies
- General:
    - Fetches list Movies with paging
    - Request Arguments: 
      - page: this number of page. default 1
      - pageSize: number of item in one page. default 10
    - Returns: array movie, page number, page size, total movie in database, total Pages
    - Results are paginated in groups of pageSize. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/api/v1.0/movies?page=1&pageSize=20`

```
  {
    "items": [
        {
            "actors": [
                {
                    "age": 3,
                    "gender": 1,
                    "id": 1,
                    "name": "Tom"
                },
                {
                    "age": 2,
                    "gender": 2,
                    "id": 2,
                    "name": "Jerry"
                }
            ],
            "id": 1,
            "release_date": "Thu, 27 Jun 2024 18:31:00 GMT",
            "title": "Tom And Jerry"
        },...
    ],
    "page": 1,
    "pageSize": 20,
    "success": true,
    "totalItems": 3,
    "totalPages": 1
}
```

#### GET /api/v1.0/movies/<movie_id>
- General:
    - Fetches one movie with movie id
    - Request Arguments: movie id
    - Returns: 
      - item: movie with id, title, release date and actor
      - success: true or false 
- Sample: `curl http://127.0.0.1:5000/api/v1.0/movies/2`

```
  {
    "item": {
        "actors": [
            {
                "age": 18,
                "gender": 1,
                "id": 3,
                "name": "Shinichi"
            },
            {
                "age": 18,
                "gender": 2,
                "id": 4,
                "name": "Ran"
            },
            {
                "age": 41,
                "gender": 2,
                "id": 9,
                "name": "Mori Na"
            }
        ],
        "id": 2,
        "release_date": "Sun, 28 Jul 2024 13:09:00 GMT",
        "title": "Conan"
    },
    "success": true
    }
```

#### POST /api/v1.0/movies
- General:
    - Creates a new movie.
    - Returns success value.
- Sample: `curl -X POST http://127.0.0.1:5000/api/v1.0/movies`
```
-H "Content-Type: application/json" -d 
{
    "title": "Inuyasha",
    "release_date": "06/27/2024 18:31:00",
    "actor_ids": [5]
}
```
- Result:
```
{
    "item": {
        "actors": [
            {
                "age": 7,
                "gender": 1,
                "id": 5,
                "name": "Nobita"
            }
        ],
        "id": 4,
        "release_date": "Thu, 27 Jun 2024 18:31:00 GMT",
        "title": "Inuyasha"
    },
    "success": true
}
```

#### DELETE /api/v1.0/movie/<movie_id>
- General:
    - Deletes the movies of the given ID if it exists. 
    - Returns success value
- Sample: `curl -X DELETE http://127.0.0.1:5000/api/v1.0/movies/4`
```
{
    "item": {
        "actors": [
            {
                "age": 7,
                "gender": 1,
                "id": 5,
                "name": "Nobita"
            }
        ],
        "id": 4,
        "release_date": "Thu, 27 Jun 2024 18:31:00 GMT",
        "title": "Inuyasha"
    },
    "success": true
}
```

#### PATCH /api/v1.0/movies/<int:actor_id>
- General:
    - Edit the movies of the given ID if it exists.
    - Returns success value.
- Sample: `curl -X PATCH http://127.0.0.1:5000/api/v1.0/movies/9`
```
-H "Content-Type: application/json" -d 
{
    "title": "Conan Movie 2",
    "release_date": "06/26/2024 18:31:00",
    "actor_ids": [1, 2, 4]
}
```
- Result:
```
{
    "item": {
        "actors": [
            {
                "age": 3,
                "gender": 1,
                "id": 1,
                "name": "Tom"
            },
            {
                "age": 2,
                "gender": 2,
                "id": 2,
                "name": "Jerry"
            },
            {
                "age": 18,
                "gender": 2,
                "id": 4,
                "name": "Ran"
            }
        ],
        "id": 5,
        "release_date": "Wed, 26 Jun 2024 18:31:00 GMT",
        "title": "Conan Movie 2"
    },
    "success": true
}
```

### End API MOVIES

