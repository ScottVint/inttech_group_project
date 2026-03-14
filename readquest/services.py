import requests

API_KEY = "2a5b14e214msh8ee3c1b2ab357f8p1519c3jsn8d295323620b"


def search_books(query):
    url = "https://project-gutenberg-free-books-api1.p.rapidapi.com/subjects"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "project-gutenberg-free-books-api1.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.get(
        "https://project-gutenberg-free-books-api1.p.rapidapi.com/books",
        headers=headers,
        params={"title": query}
    )


    return response.json()["results"]