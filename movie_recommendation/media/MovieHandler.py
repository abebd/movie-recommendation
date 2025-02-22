import os
import random
import chardet

from tabulate import tabulate # type: ignore
from movie_recommendation.media import StoredMovieCategory
from movie_recommendation.media.Movie import Movie
from movie_recommendation.Util import get_time_delta, create_hyperlink, shorten_string, validate_path

class MovieHandler:

    def __init__(self):
        
        # win
        #self.movies_folder = validate_path('C:/Users/twist/Documents/Obsidian/main/Media/Movies')
        #self.recommendation_folder = validate_path('C:/Users/twist/Documents/Obsidian/main/Media/Movies/Recommendations')

        # wsl
        self.movies_folder = validate_path('/mnt/c/Users/twist/Documents/Obsidian/main/Media/Movies')
        self.recommendation_folder = validate_path('/mnt/c/Users/twist/Documents/Obsidian/main/Media/Movies/Recommendations')

        self.movies = self.load_movies(self.movies_folder)


    def get_watched_movies(self):
        
        watched_movies = []
        base_rating = 0.0

        for movie in self.movies:

            rating = movie.get_datapoint('personalRating')
            
            if rating == '.nan':
                rating = base_rating
            
            if movie.get_datapoint('watched') == 'true' and float(rating) >= 3.0:
                watched_movies.append(movie)

        return watched_movies


    def load_movies(self, folder):
        movies = []

        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            
            if os.path.isfile(file_path) == False:
                continue

            # detect charset
            content = ''
            with open(file_path, 'rb') as f:
                content = f.read()

            encoding = chardet.detect(content)['encoding']

            with open(file_path, 'r', encoding=encoding) as file:

                movie_data = {}
                last_key = ''

                for line in file.readlines():
                    
                    line = line.replace('\r\n', '\n')
                    line = line.replace('\n', '')

                    # end of file
                    if '```' in line:
                        break

                    if ':' in line:
                    
                        splitted_line = line.split(':', 1)

                        key = splitted_line[0]
                        last_key = key

                        value = splitted_line[1][:].lstrip().rstrip().replace('"', '')

                        #movie_data[splitted_line[0]] = splitted_line[1][:].lstrip().rstrip()
                        movie_data[key] = value

                    elif '  - ' in line:
                        
                        if movie_data[last_key] == '':

                            movie_data[last_key] = line[4:]
                        else:

                            movie_data[last_key] = movie_data[last_key] + '|' + line[4:]


            movie = Movie(file_name[:-3], data=movie_data)
            
            movies.append(movie)

        return movies
    
    def fetch_attributes_from_movie(self, file_path):
        
        attributes = {}
        
        # detect encoding
        content = ''
        with open(file_path, 'rb') as f:
            content = f.read()

        encoding = chardet.detect(content)['encoding']

        with open(file_path, 'r', encoding=encoding) as file:
            
            for line in file.readlines():
                splitted_line = line.split(':', 1)

                if len(splitted_line) != 2:
                    continue

                attribute, value = splitted_line
                
                value = value.replace('"', '')
                
                if attribute == 'fetched':
                    #calculate how old the datapost is
                    attributes[attribute] = get_time_delta(value.replace('\r', '').rstrip().lstrip())
                else:
                    # for the generic ones
                    attributes[attribute] = shorten_string(value)

        return attributes
    
    def list_movies_random(self, folder=''):
        # make this main list_movies method
        # BUG: list of attributes is not ordered in the same way everytime
        
        files = os.listdir(folder)
        
        # create new list of only the 5 randomly chosen files
        random_files = []
        li = random.sample(range(1, len(files)), 6)
           
        for i in li:
            random_files.append(files[i])
            
        files = random_files
        
        attributes_wanted = ['title', 'year', 'plot', 'onlineRating', 'url']
        movies = []
        movie_index = 0
        
        if len(files) == 0:
            print('No files to list')
            return
        
        for file_name in files:
            movie_index+=1

            if movie_index > 5:
                continue

            file_path = os.path.join(folder, file_name)

            if os.path.isdir(file_path):
                continue

            movie_attributes = self.fetch_attributes_from_movie(file_path)
            filtered_attributes = {
                key: value 
                #simple sort for now, should make it sortable by @attributes
                for key, value in sorted(
                    movie_attributes.items()
                ) 
                if key in attributes_wanted
            }
            movies.append(filtered_attributes.values())
        
        print(tabulate(movies, attributes_wanted))
        
    def list_movies(self, folder=''):

        files = os.listdir(folder)
        attributes_wanted = ['title', 'year', 'plot', 'onlineRating', 'url']
        attributes_order = []
        movies = []
        movie_index = 0
        max_movies = 20

        if len(files) == 0:
            print('No new files exists')
            return

        for file_name in files:

            if movie_index > 20:
               # TODO: this is probably very shitty
               continue 

            movie_index+=1

            file_path = os.path.join(folder, file_name)

            if os.path.isdir(file_path):
                continue

            movie = []
            url = ''

            content = ''
            with open(file_path, 'rb') as f:
                content = f.read()

            encoding = chardet.detect(content)['encoding']


            with open(file_path, 'r', encoding=encoding) as file:
                lines = file.readlines()
                
                for line in lines:
                    splitted_line = line.split(':', 1)

                    if len(splitted_line) != 2:
                        continue

                    attribute, value = splitted_line
                    
                    if attribute == 'fetched':
                        #calculate how old the datapost is
                        delta = get_time_delta(value.replace('\r', '').rstrip().lstrip())
                        movie.append(delta)
                        attributes_order.append(attribute)

                    # for the generic ones
                    if attribute in attributes_wanted:
                        movie.append(shorten_string(value))
                        attributes_order.append(attribute)


            movies.append(movie)


        print(tabulate(movies, attributes_order))

    
    def list_moveis_alt(self, folder=''):
            
        files = os.listdir(folder)
        attributes_wanted = ['year', 'plot', 'onlineRating']
        attributes_order = []
        movies = []
        movie_index = 0
        max_movies = 20

        if len(files) == 0:
            print('No new files exists')
            return

        for file_name in files:
            movie_index+=1

            if movie_index > max_movies:
               # TODO: this is probably very shitty
               continue

            file_path = os.path.join(folder, file_name)
            if os.path.isdir(file_path):
                continue

            movie = []
            url = ''
            last_attribute = ''
            actors = ''
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
                for line in lines:

                    if last_attribute == 'actors':
                        value = line.replace('\n', '')
                        actors += value[4:] + ', '

                    splitted_line = line.split(':', 1)

                    if len(splitted_line) != 2:
                        continue

                    attribute, value = splitted_line
                    last_attribute = attribute

                    if attribute == 'url':
                        url = value


                for line in lines:
                    splitted_line = line.split(':', 1)

                    if len(splitted_line) != 2:
                        continue

                    attribute, value = splitted_line
                    
                    if attribute == 'fetched':
                        #calculate how old the datapost is
                        #delta = get_time_delta(value.replace('\r\n', '').rstrip().lstrip())
                        #movie.append(delta)
                        movie.append(value.replace('\r\n'.rstrip().lstrip(), ''))
                        attributes_order.append(attribute)                        

                    if attribute == 'title':
                        value = create_hyperlink(label=value.lstrip().rstrip(), url=url)
                        movie.append(value)
                        attributes_order.append(attribute)

                    if attribute == 'actors':
                        value = actors[:-7]
                        movie.append(value)
                        attributes_order.append(attribute)

                    # for the generic ones
                    if attribute in attributes_wanted:
                        movie.append(value.replace('\r', ''))
                        attributes_order.append(attribute)

            movies.append(movie)
            
            #for i in range(len(movie)):
            #    print(f'{attributes_order[i]}: {movie[i].replace('\n', '')}')

        #sorted_list = movies.sort(key=lambda x: x[0])
        movies = sorted(movies, key=lambda x: x[4], reverse=False)
        
        i = 0
        for movie in movies:
            print('\n')

            for i in range(len(movie)):

                if attributes_order[i] == 'fetched':
                    print(f'{attributes_order[i]}: {get_time_delta(movie[i].lstrip().rstrip())}')
                    continue

                cleaned_movie = movie[i].replace('\n', '')
                print(f'{attributes_order[i]}: {cleaned_movie}')



