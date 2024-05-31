import os
import shutil
from datetime import datetime

from movie_recommendation.util import get_secret, remove_files_in_folder, log
from movie_recommendation.media.moviehandler import MovieHandler
from movie_recommendation.api.chatbot.chatbothandler import ChatBotHandler
from omdbapi.movie_search import GetMovie # type: ignore

class OmdbHandler:


    def __init__(self):
        self.api_key = get_secret(file_name='omdb_api.key')
        self.omdb = GetMovie(api_key=self.api_key)
        self.movieh = MovieHandler()


    def create_movie_md(self, movies):
        log_file_path = 'logs/recommended_movies.log'
        now = datetime.now()
        today = now.strftime("%y-%m-%d %H:%M:%S")
        skipped_file_amount = 0

        #remove_files_in_folder(self.movieh.recommendation_folder)


        for movie in movies:
            if skipped_file_amount != 0 and skipped_file_amount == len(movies) - 1:
                raise('skipped all files, retry')
            try:
                self.omdb.get_movie(title=movie.name)

            except omdbapi.movie_search.GetMovieException as e: # type: ignore
                print(f'Did not find movie: {movie.name}')
                continue

            file_name = f'{self.omdb.title} ({self.omdb.year}).md'
            
            # Skip the movie if it allready exists
            if file_name in os.listdir(self.movieh.movies_folder):
                msg = f'{file_name[:-3]}, skipped'
                skipped_file_amount += 1
                log(log_path=log_file_path, message=msg)
                #print(msg)
                continue

            full_file_path = f'{self.movieh.recommendation_folder}/{file_name}'

            with open(full_file_path, 'w') as file:

                file.write('---\n')
                file.write(f'title: {self.omdb.title}\n')
                file.write(f'year: {movie.data["year"]}\n')
                file.write(f'dataSource: {ChatBotHandler.get_model()}\n')
                file.write(f'plot: {self.omdb.plot}\n')
                file.write(f'onlineRating: {self.omdb.imdbrating}\n')
                file.write(f'duration: {self.omdb.runtime}\n')
                file.write(f'type: {self.omdb.type}\n')
                file.write(f'url: https://www.imdb.com/title/{self.omdb.imdbid}\n')
                file.write(f'id: {self.omdb.imdbid}\n')
                file.write(f'image: {self.omdb.poster}\n') 
                file.write(f'watched: false\n')
                file.write(f'fetched: {today}\n') 
                #file.write(f'genres: {self.omdb.genre}\n')
                file.write('genres:\n')
                for genre in self.omdb.genre.split(', '):
                    file.write(f'  - {genre}\n')

                #file.write(f'actors: {self.omdb.actors}\n')
                file.write('actors:\n')
                for actor in self.omdb.actors.split(', '):
                    file.write(f'  - {actor}\n')

                #file.write(f'writer: {self.omdb.writer}\n')
                file.write('writer:\n')
                for writer in self.omdb.writer.split(', '):
                    file.write(f'  - {writer}\n')

                #file.write(f'director: {self.omdb.director}\n')
                file.write('director:\n')
                for director in self.omdb.director.split(', '):
                    file.write(f'  - {director}\n')

                file.write('---\n')

                msg = f'{file_name}, create'
                print(f'created file {file_name}')
                log(log_path=log_file_path, message=msg)
                #print(msg)

                #shutil.copy(full_file_path, f'{self.movieh.recommendation_folder}/{file_name}')

            #for attribute, value in self.omdb.get_movie(title=movie.name).items():
                