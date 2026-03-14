import requests

def search_books(query):
    response = requests.get(
        "https://openlibrary.org/search.json",
        params={
            "q": query,
            "fields": "key,title,author_name,cover_i,number_of_pages_median,first_publish_year",
            "limit": 10
        }
    )
    response.raise_for_status()

    books = []
    for doc in response.json().get("docs", []):
        books.append({
            "title": doc.get("title", "Unknown Title"),
            "author": ", ".join(doc.get("author_name", ["Unknown Author"])),
            "pages": doc.get("number_of_pages_median", None),
            "year": doc.get("first_publish_year", None),
            "cover_image": f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-M.jpg" if doc.get("cover_i") else None,
        })
    return books