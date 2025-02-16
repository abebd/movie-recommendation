import json

from gemini import OpenRouter # type: ignore
from movie_recommendation.Util import get_secret
from movie_recommendation.media.Movie import Movie

class ChatBotHandler:

    def __init__(self):
        self.api_key = get_secret(file_name="chat_api.key")
        #self.client = OpenRouter(api_key=self.api_key, model="google/gemma-7b-it:free")
        self.model = self.get_model()
        self.client = OpenRouter(api_key=self.api_key, model=self.model)
        #self.base_movie_prompt = "Hey I recently watched the movies: %s and thought they were good. Could you give me recommendation of a few movies which I might enjoy? Please supply this information in a list form and and in this matter the less information = the better. I just wan't the names of the movies and the year it was released, structured like this 'Movie1 (year)'. Each movie should reside on it's own line. There is no need to number each line, and a handful of movies would suffice. There is no need to introduce the list"
        self.base_movie_prompt = "Hey I recently watched the movies: %s and thought they were good. Could you give me recommendation of a few movies which I might enjoy? Please supply this information in a list form and and in this matter the less information = the better. I just wan't the names of the movies and the year it was released, structured like this 'Movie1 (year)'. Present this as a json format"
     

    @staticmethod
    def get_model():
        return 'mistralai/mistral-7b-instruct:free'


    def send_prompt(self, prompt):

        #print("prompt=%s" % (prompt))
        response = self.client.create_chat_completion(prompt)
        
        return response
    
    def handle_response(self, response):
        # This function parses the response into an object which then gets sent to Moviehandler
        new_movies = []
    
        # bot is wierd, sometimes you get 5 different objects, and sometimes you get an array of 5 items

        # retry 5 times (hardcoded)
        try:

            for movie in json.loads(response):
                for _, value in movie.items():
                    
                    name = value[:-7]
                    year = value[len(value) - 5:-1]

                    print(1)

                    movie = Movie(name=name, data={'year': year})

                    new_movies.append(movie)

            return new_movies

        except AttributeError as e:
            # When bot gives an array

            for value in json.loads(response):
                name = value[:-7]
                year = value[len(value) - 5:-1]


                movie = Movie(name=name, data={'year': year})

                new_movies.append(movie)

            return new_movies
    
        except Exception as e:
            return 
            