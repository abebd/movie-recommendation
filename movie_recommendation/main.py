import os
import random
import sys
import traceback

from movie_recommendation.media.moviehandler import MovieHandler
from movie_recommendation.api.chatbot.chatbothandler import ChatBotHandler
from movie_recommendation.api.omdb.omdbhandler import OmdbHandler
from movie_recommendation.user.inputhandler import InputHandler
from movie_recommendation.recommend import Recommend
from movie_recommendation.api.sheets.sheetshandler import SheetsHandler

class Main:
    def __init__(self):
        self.movieh = MovieHandler()
        self.chat = ChatBotHandler()
        self.omdbh = OmdbHandler()
        self.inputh = InputHandler(self)
        self.recommend = Recommend()
        self.sheets = SheetsHandler()
        self.retry_index = 0
        self.retry_max = 10


    def get_movie_recomentations(self) -> dict:
        print(f'current retry index={self.retry_index}')
        if self.retry_index == self.retry_max:
            return

        watched_movies = self.movieh.get_watched_movies()
        movies_string = ''

        for movie in random.sample(watched_movies, 5):
            movies_string += movie.get_datapoint('title') + ', '


        # remove trailing ', '
        movies_string = movies_string[:-2]

        if movies_string == '':
            print('movies_string is empty, can not provide any recomendations')
            return ''

        prompt = self.chat.base_movie_prompt % (movies_string)
        response = self.chat.send_prompt(prompt)

        new_movies = self.chat.handle_response(response)

        if new_movies == None:
            raise("Something went wrong when finding new movies")

        #return new_movies

        response = self.omdbh.create_movie_md(new_movies)

    def list_movies(self, type):

        if type == 'new':
            self.movieh.list_movies(self.movieh.recommendation_folder)
            return

        if type == 'old':
            self.movieh.list_movies(self.movieh.movies_folder)
            return

    def run_fetch(self):

        for self.retry_index in range(self.retry_max):
            try:
                self.get_movie_recomentations()

            except Exception as e:
                #print_excinfo()
                traceback.print_exc()
                continue

            else:
                break
        else:
            # Fully failed
            print('Something went terribly wrong :)')

    def run_userinput(self):

        while(True):

            self.inputh.get_input()
            self.inputh.handle_input()

            #movies = self.get_movie_recomentations()
            #self.omdbh.create_movie_md(movies)

    def run_list_new(self):
        self.list_movies(type='new')

    def run_list_alt(self):
        self.movieh.list_moveis_alt(folder=self.movieh.recommendation_folder)

    def run_recommend(self):
        self.recommend.run()

    def run_sheets(self):
        self.sheets.parse_file_with_movies()

