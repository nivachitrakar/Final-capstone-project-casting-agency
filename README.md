# Final-capstone-project-casting-agency
# Documentation for Casting Agency

## Overview
This API is for casting agents. The casting assistants can view the database to find the suitable actors for their upcoming projects as well as view the list of movies. Similarly, Casting Directors are responsible for adding and removing the actors as well as view the list of actors and movies. And finally, Executive Producers are responsible for adding, updating and deleting the movies as well as viewing them

## Base URL
- Localhost: `http://127.0.0.1:5000/casting_agency/v1.0`

## Endpoints

### Movies
Lists all the movies stored in our database.
1. **Get All movies**
- **URL:** `/casting_agency/v1.0/movies`
- **Method:** GET
- **Description:** Fetches all available movies.
- **Sample Response:**
```
{
    {
        "id": 4,
        "release_date": "2015-06-09",
        "title": "Inside Out 2"
    },
    {
        "id": 6,
        "release_date": "2024-07-24",
        "title": "The Good half"
    },
    {
        "id": 1,
        "release_date": "2024-12-31",
        "title": "Devdas"
    }
}
```
2. **Create a Movie**
Allows users to add new movies into the list.
- **URL:** `/casting_agency/v1.0/movies`
- **Method:** POST
- **Description:** Creates a new movie.
- **Request Arguments:**
```
{
    "title": "Devdas",
    "release_date": "2024-07-24"
}
```
3. **Update Movies**
Updates the information about the movie for particular id with the given information
- **URL:** `casting_agency/v1.0/movies/<int:movie_id>`
- **Method:** PATCH
- **Description:** Searches for questions based on a search term.
- **Request Arguments:**
```
{
    "title": "Devdas",
    "release_date": "2023-01-01"
}
```
4. **Delete a Movie**
Allows users to delete the existing movie
- **URL:** `casting_agency/v1.0/movies/<int:movie_id>`
- **Method:** DELETE
- **Description:** Deletes a question by ID.
- **curl:** `curl --request DELETE 'http://127.0.0.1:5000casting_agency/v1.0/movies/2`
- **Sample Response:**
```
204
```

### Actors
List all the actors stored in our database

1. **Get All Actors**
- **URL:** `/casting_agency/v1.0/actors`
- **Method:** GET
- **Description:** Fetches all available movies.
- **Sample Response:**
```
{
    {
        "id": 4,
        "dob": "1978-06-09",
        "name": "Tom Hanks",
        "gender": "M"
    },
    {
        "id": 7,
        "dob": "1940-06-09",
        "name": "Marilyn Monrow",
        "gender": "F"
    }
}
```
2. **Create a Actor**
Allows users to add new actor and their information.
- **URL:** `/casting_agency/v1.0/actors`
- **Method:** POST
- **Description:** Creates a new movie.
- **Request Arguments:**
```
{
        "dob": "1978-01-22",
        "name": "Johnny Depp",
        "gender": "M"
    }
```
3. **Update Actors**
Allows users to update information about the actor
- **URL:** `casting_agency/v1.0/actors/<int:actor_id>`
- **Method:** PATCH
- **Description:** Searches for questions based on a search term.
- **Request Arguments:**
```
{
        "dob": "1978-01-22",
        "name": "Jenny Depp",
        "gender": "F"
}
```
4. **Delete a Movie**
Takes question id in an URL as an input and deletes the particular question id sent for deleted
- **URL:** `casting_agency/v1.0/actors/<int:actor_id>`
- **Method:** DELETE
- **Description:** Deletes a question by ID.
- **curl:** `curl --request DELETE 'http://127.0.0.1:5000/casting_agency/v1.0/actors/2`
- **Sample Response:**
```
204
```

### Contact
For any inquiries or issues, please contact:

- **Name:** Niva Chitrakar
- **Email:** nivachitrakar9@gmail.com