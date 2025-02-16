
class Recommend:

    def __init__(self):
        pass


    def run(self):
        print('hello world')
        
        
import random
import os


base_path = '/mnt/c/users/twist/Documents/obsidian/main/media'
#C:\Users\twist\Documents\Obsidian\main\Media

movies = os.listdir(os.path.join(base_path, 'movies'))
watched_movies = []
movies_to_watch = []

def is_watched_movie(file):
    with open(file, encoding='latin-1', mode='r') as f:
        
        for line in f.readlines():
        
            if 'watched: true' in line:
                return True
            
    return False
    

for movie in movies:
    
    if os.path.isdir(os.path.join(base_path, 'movies', movie)):
        continue
    
    if is_watched_movie(os.path.join(base_path, 'movies', movie)):
        watched_movies.append(movie)
    else:
        movies_to_watch.append(movie)
                
            
print(len(movies_to_watch))