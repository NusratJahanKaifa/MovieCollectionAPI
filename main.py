from fastapi import FastAPI, HTTPException
from database import create_table, get_connection
from models import MovieCreate, MovieUpdate

app = FastAPI(title="Movie Collection API")
create_table()
@app.get("/")
def home():
    return {"message": "Movie Collection API is running"}
@app.get("/movies")
def get_movies():
    connection = get_connection()
    movies = connection.execute(
        "SELECT * FROM movies"
    ).fetchall()
    connection.close()
    return [dict(movie) for movie in movies]
@app.post("/create_movies", status_code=201)
def create_movie(movie: MovieCreate):
    connection = get_connection()
    existing_movie = connection.execute(
        "SELECT * FROM movies WHERE movie_id = ?",
        (movie.movie_id,)
    ).fetchone()
    if existing_movie:
        connection.close()
        raise HTTPException(
            status_code=400,
            detail="Movie with this movie_id already exists"
        )
    connection.execute(
        """
        INSERT INTO movies
        (movie_id, title, director, genre, duration, rating)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            movie.movie_id,
            movie.title,
            movie.director,
            movie.genre,
            movie.duration,
            movie.rating
        )
    )
    connection.commit()
    new_movie = connection.execute(
        "SELECT * FROM movies WHERE movie_id = ?",
        (movie.movie_id,)
    ).fetchone()
    connection.close()
    return dict(new_movie)
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    connection = get_connection()
    movie = connection.execute(
        "SELECT * FROM movies WHERE movie_id = ?",
        (movie_id,)
    ).fetchone()
    connection.close()
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    return dict(movie)
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: MovieUpdate):
    connection = get_connection()
    existing_movie = connection.execute(
        "SELECT * FROM movies WHERE movie_id = ?",
        (movie_id,)
    ).fetchone()
    if existing_movie is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    connection.execute(
        """
        UPDATE movies
        SET title = ?,
            director = ?,
            genre = ?,
            duration = ?,
            rating = ?
        WHERE movie_id = ?
        """,
        (
            movie.title,
            movie.director,
            movie.genre,
            movie.duration,
            movie.rating,
            movie_id
        )
    )
    connection.commit()
    updated_movie = connection.execute(
        "SELECT * FROM movies WHERE movie_id = ?",
        (movie_id,)
    ).fetchone()
    connection.close()
    return dict(updated_movie)
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    connection = get_connection()
    movie = connection.execute(
        "SELECT * FROM movies WHERE movie_id = ?",
        (movie_id,)
    ).fetchone()
    if movie is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    connection.execute(
        "DELETE FROM movies WHERE movie_id = ?",
        (movie_id,)
    )
    connection.commit()
    connection.close()
    return {
        "message": "Movie deleted successfully"
    }
@app.get("/movies/sort")
def sort_movies(
    sort_by: str = "rating",
    order: str = "desc"
):
    connection = get_connection()
    if sort_by not in ["duration", "rating"]:
        connection.close()
        raise HTTPException(
            status_code=400,
            detail="sort_by must be duration or rating"
        )
    if order not in ["asc", "desc"]:
        connection.close()
        raise HTTPException(
            status_code=400,
            detail="order must be asc or desc"
        )
    query = f"""
        SELECT * FROM movies
        ORDER BY {sort_by} {order}
    """
    movies = connection.execute(query).fetchall()
    connection.close()
    return [dict(movie) for movie in movies]