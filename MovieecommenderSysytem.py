import requests
import json
import time
import pandas as pd

def get_movies_from_tastedive(string, limit=5):
    url = "https://tastedive.com/api/similar"
    parameters = {"q": string, "type": type, "limit": limit, "k": "352565-RelatedM-DC4NSDNT"}
    TasteDiveData = requests.get(url, params=parameters)
    TasteDiveResponse = json.loads(TasteDiveData.text)
    return TasteDiveResponse

def extract_title(dict):
    related_movies = list()
    for ele in dict["Similar"]["Results"]:
        related_movies.append(ele["Name"])
    return related_movies

def realated_title(lst):
    type = "movies"
    relatedTitle = list()
    _list = list()
    for movie in lst:
        _list.append(extract_title(get_movies_from_tastedive(movie, type)))
    _lst = [ele for lst in _list for ele in lst]

    for movie in _lst:
        if movie not in relatedTitle:
            relatedTitle.append(movie)
    return relatedTitle

def movie_data(string):
    api_key = "a6c4b3a0"
    url = "http://www.omdbapi.com/"
    parameter = {"apikey" : api_key, "t" : string}
    OMBdData = requests.get(url, params= parameter)
    OMBdResponse = json.loads(OMBdData.text)
    return OMBdResponse

def get_movie_rating(dict):
    Rating = dict["imdbRating"]
    return Rating

def summary(dict):
    Plot = dict["Plot"]
    Casting = dict["Actors"]
    Direction = dict["Director"]
    return [Plot, Casting, Direction]

def sorted_data(listMovies):
    listMovies = sorted(listMovies, key= lambda x : (get_movie_rating(movie_data(x)), x), reverse= True)
    return listMovies


name = input("Enetr your name : ")
print(f"""
Welcome {name.title()} to the Related Movie Suggester System
we are here to help you decide which movie to watch next
""")
while True:
    print("""
    Choose one of the following:
    1. Ask for recommendation
    2. Quit
    """)
    choice = input("Make a choice : ")
    if choice == "1":
        movie = input("Enter the last movie you watched : ")
        while True:
            n = int(input("Enetr the number of movie you want to be recommended : "))
            if n < 1  or n > 20:
                print("Please select the limit between 2 and 18")
                continue
            else:
                break
        print("Wait while we find the best results....")
        time.sleep(1)
        relatedMovies = get_movies_from_tastedive(movie, n)
        # print(relatedMovies)
        relatedTitles = extract_title(relatedMovies)
        # print(relatedTitles)
        relatedTitlesData = [movie_data(movie) for movie in relatedTitles]
        # print(relatedTitlesData)
        Rating = [get_movie_rating(movie) for movie in relatedTitlesData]
        final = sorted_data(relatedTitles)
        pd.options.display.max_colwidth = 100
        _RelatedMovie = pd.DataFrame(Rating, columns= ["IMDB Rating"],
                                     index= final)
        _RelatedMovie = _RelatedMovie.sort_values("IMDB Rating", ascending= False)
        print(_RelatedMovie)
    elif choice == "2":
        break
    else:
        print("Make a valid Input")
        continue



